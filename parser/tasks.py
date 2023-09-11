import logging
from datetime import datetime
from parser.models import ParseTask, TaskPeriodChoices, TaskStatusChoices
from parser.services.parse import process_task

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.html import strip_tags
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task
from huey_monitor.tasks import TaskModel
from huey_monitor.tqdm import ProcessInfo

log = logging.getLogger(__name__)


def run_periodic_now(period_choice: TaskPeriodChoices, task: TaskModel):
    """Run periodic tasks now"""

    run_states = [
        TaskStatusChoices.PAUSED,
        TaskStatusChoices.RUN,
        TaskStatusChoices.ERROR,  # Task will retry
    ]
    parse_tasks = ParseTask.objects.filter(period=period_choice).filter(status__in=run_states)

    if period_choice == TaskPeriodChoices.ONETIME:
        parse_tasks = parse_tasks.filter(period_date1=datetime.today())
    elif period_choice == TaskPeriodChoices.TWO_MONTHLY:
        parse_tasks = parse_tasks.filter(Q(period_date1=datetime.today()) | Q(period_date2=datetime.today()))

    log.info(f"Running periodic tasks {period_choice}...")
    for parse_task in parse_tasks.all():
        log.info(f"Running periodic task: {parse_task}")
        run_now(parse_task=parse_task, parent_task_id=task.id)


@db_periodic_task(crontab(minute="0", hour="0"), context=True)
def run_daily(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.DAILY, task)
    run_periodic_now(TaskPeriodChoices.TWO_MONTHLY, task)
    run_periodic_now(TaskPeriodChoices.ONETIME, task)


@db_periodic_task(crontab(minute="0", hour="0", day="1"), context=True)
def run_monthly(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.MONTHLY, task)


@db_periodic_task(crontab(minute="0", hour="0", day="1", month="*/3"), context=True)
def run_quarterly(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.QUARTER, task)


@db_task(context=True)
def run_now(task: TaskModel, parse_task: ParseTask, parent_task_id: int | None = None, test: bool = False):
    process_info = ProcessInfo(task, desc="task-" + str(parse_task.pk), total=1, parent_task_id=parent_task_id)

    def callback(curr: int, total: int):
        if not process_info.total:
            process_info.total = total

        process_info.update()

    res = process_task(parse_task, callback=callback, test=test)

    return {
        "logs": parse_task.log.logs,
        "data": res,
    }


@db_task()
def task_send_email(email: str, title: str, template: str):
    send_mail(
        title,
        strip_tags(template),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=template,
    )
