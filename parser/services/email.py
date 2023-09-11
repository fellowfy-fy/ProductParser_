from parser.models import ParseTask

from django.template import Context, Template


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
    return t.render(c)
