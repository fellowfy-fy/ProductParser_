from wagtail.log_actions import log
from wagtail.snippets.views.snippets import CreateView


class CreateViewAuthorSave(CreateView):
    """Set author field to current user"""

    def save_instance(self):
        instance = self.form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        log(instance=instance, action="wagtail.create", content_changed=True)
        return instance
