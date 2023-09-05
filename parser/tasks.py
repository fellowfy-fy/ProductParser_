from datetime import datetime
import logging
from huey.contrib.djhuey import db_periodic_task, db_task
from huey import crontab
from huey_monitor.tasks import TaskModel

from parser.models import ParseTask, TaskPeriodChoices

log = logging.getLogger(__name__)

def run_periodic_now(period_choice: TaskPeriodChoices, task: TaskModel):
    """Run periodic tasks now"""
    parse_tasks = ParseTask.objects.filter(
        period=period_choice
    )

    if period_choice == TaskPeriodChoices.ONETIME:
        parse_tasks = parse_tasks.filter(period_date1=datetime.today())

    log.info(f"Running periodic tasks {period_choice}...")
    for parse_task in parse_tasks.all():
        log.info(f"Running periodic task: {parse_task}")
        run_now(parse_task=parse_task, parent_task_id=task.id)




@db_periodic_task(crontab(minute="0", hour="0"), context=True)
def run_daily(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.DAILY, task)
    run_periodic_now(TaskPeriodChoices.ONETIME, task)

@db_periodic_task(crontab(minute="0", hour="0", day="1"), context=True)
def run_monthly(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.MONTHLY, task)

@db_periodic_task(crontab(minute="0", hour="0", day="1", month="*/3"), context=True)
def run_quarterly(task: TaskModel):
    run_periodic_now(TaskPeriodChoices.QUARTER, task)


@db_task
def run_now(task: TaskModel, parse_task: ParseTask, parent_task_id:int|None=None):
    if parent_task_id is not None:
        TaskModel.objects.set_parent_task(
            main_task_id=parent_task_id,
            sub_task_id=task.id,
        )

    # TODO: Run parsing

