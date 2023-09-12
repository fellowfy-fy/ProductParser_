import logging
from parser.models import ParseTask, TaskStatusChoices
from parser.services.email import email_task_approve, email_task_prices, email_task_status

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from products.models import ProductPriceHistory


@receiver(pre_save, sender=ParseTask, dispatch_uid="task_email_pre_save")
def task_email_pre_save(sender, instance: ParseTask, **kwargs):
    try:
        old_instance = ParseTask.objects.get(id=instance.id)
    except ParseTask.DoesNotExist:  # to handle initial object creation
        return None  # just exiting from signal

    old_status = old_instance.status
    new_status = instance.status
    should_notify = False

    ##
    if new_status == TaskStatusChoices.ERROR:
        should_notify = True
    if old_status in [TaskStatusChoices.SETTINGS, TaskStatusChoices.CREATED]:
        should_notify = True
    ##
    logging.info(f"Task status updated: {old_status} => {new_status} (notify={should_notify})")

    if old_status != new_status and should_notify:
        email_task_status(instance, old_status=old_instance.get_status_display())


@receiver(post_save, sender=ParseTask, dispatch_uid="task_email_post_save")
def task_email_post_save(sender, instance: ParseTask, created: bool = False, **kwargs):
    if created:
        logging.info(f"Task created: {instance}")
        email_task_approve(instance)


@receiver(post_save, sender=ProductPriceHistory, dispatch_uid="price_email_post_save")
def price_post_save(sender, instance: ProductPriceHistory, created: bool = False, **kwargs):
    task: ParseTask = instance.task
    if created and task and task.notifications_enable:
        try:
            last_instance = ProductPriceHistory.objects.order_by("-created_at").get(
                # Match same parameters
                task=instance.task,
                parse_settings=instance.parse_settings,
                product=instance.product,
                created_at__lt=instance.created_at,  # Older than current update
            )
        except ProductPriceHistory.DoesNotExist:
            return
        old_price = last_instance.price
        new_price = instance.price
        logging.info(f"Price history saved: {old_price} => {new_price} ({task})")

        if new_price != old_price:
            if (new_price > old_price and "incr" in task.notifications_target) or (
                new_price < old_price and "decr" in task.notifications_target
            ):
                email_task_prices(instance.task, old_price, new_price)
