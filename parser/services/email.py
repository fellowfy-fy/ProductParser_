import logging
from parser.models import ParseTask
from parser.tasks import task_send_email

from django.conf import settings
from django.template import Context, Template
from dynamic_preferences.registries import global_preferences_registry

from accounts.models import CustomUser

global_preferences = global_preferences_registry.manager()


def get_task_link(task: ParseTask):
    return f"{settings.PUBLIC_URL}/user/tasks/{task.pk}"


def process_variables(task: ParseTask, text: str, extra: dict = dict()) -> str:
    """Process variables in template"""
    t = Template(text)
    c = Context(
        {
            "task": task,
            "status": task.get_status_display(),
            "author": task.author.get_username(),
            **extra,
        }
    )

    task_link = get_task_link(task)
    task_link_text = f'<br>\n<a href="{task_link}">Ссылка на задачу</a>'
    res = t.render(c)

    if task_link not in res:
        res += task_link_text

    return res


def email_task_status(task: ParseTask, old_status: str):
    if not task.author.email:
        logging.warning("Task author hasn't email set")
        return

    task_send_email(
        email=task.author.email,
        title=global_preferences["emails__status_title"],
        template=process_variables(
            task, global_preferences["emails__status_content"], extra={"old_status": old_status}
        ),
    )


def email_task_prices(task: ParseTask, old_price: float, new_price: float):
    if not task.author.email:
        logging.warning("Task author hasn't email set")
        return

    task_send_email(
        email=task.author.email,
        title=global_preferences["emails__prices_title"],
        template=process_variables(
            task,
            global_preferences["emails__prices_content"],
            extra={"old_price": old_price, "new_price": new_price, "price": new_price},
        ),
    )


def email_task_approve(task: ParseTask):
    manager: CustomUser | None = task.author.manager

    if not manager or not manager.email:
        logging.warning("Task author manager hasn't email set")
        return

    task_send_email(
        email=manager.email,
        title=global_preferences["emails__approval_title"],
        template=process_variables(task, global_preferences["emails__approval_content"]),
    )
