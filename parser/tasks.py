from datetime import datetime
import logging
from huey.contrib.djhuey import db_periodic_task, db_task
from huey import crontab
from huey_monitor.tasks import TaskModel
from huey_monitor.tqdm import ProcessInfo
from django.db.models import Q

from parser.models import ParseTask, TaskPeriodChoices
from parser.services.parse import process_task

log = logging.getLogger(__name__)


def run_periodic_now(period_choice: TaskPeriodChoices, task: TaskModel):
    """Run periodic tasks now"""
    parse_tasks = ParseTask.objects.filter(period=period_choice)

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
def run_now(task: TaskModel, parse_task: ParseTask, parent_task_id: int | None = None):
    process_info = ProcessInfo(task, desc="Обработка задачи", total=1, parent_task_id=parent_task_id)

    def callback(curr: int, total: int):
        if not process_info.total:
            process_info.total = total

        process_info.update()

    process_task(parse_task, callback=callback)
