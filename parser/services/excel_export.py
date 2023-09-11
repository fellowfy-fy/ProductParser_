from dataclasses import dataclass
from datetime import date
from parser.models import ParseTask

from accounts.models import CustomUser


@dataclass
class ReportParams:
    user: CustomUser
    task: ParseTask
    date_from: date | None = None
    date_to: date | None = None


def report_dynamics(params: ReportParams):
    pass


def report_differences(params: ReportParams):
    pass


def report_current(params: ReportParams):
    pass
