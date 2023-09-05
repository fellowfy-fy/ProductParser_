from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

class Settings(models.Model):
    key = models.CharField(_("Ключ"), max_length=255, db_index=True )
    value = models.CharField(_("Значение"), max_length=255, db_index=True )

    class Meta:
        verbose_name = _("Настройки")
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.key

    @classmethod
    def get_now(cls, key: str, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    @classmethod
    def get(cls, key: str, default=None):
        if cached := cache.get(key):
            return cached
        else:
            value = cls.get_now(key, default)
            cache.set(key, value, 60)
            return value
