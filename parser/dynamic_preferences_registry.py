from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import IntegerPreference, LongStringPreference, StringPreference

general = Section("general")
emails = Section("emails")


class HTMLEditorMixin:
    def get_api_additional_data(self):
        return {
            "is_editor": True,
        }


@global_preferences_registry.register
class CatalogDepth(IntegerPreference):
    section = general
    name = "catalog_depth"
    verbose_name = "Глубина запросов каталоги"
    default = 1
    required = False


@global_preferences_registry.register
class EmailApprovalTitle(StringPreference):
    section = emails
    name = "approval_title"
    verbose_name = "Письмо утверждение задания (заголовок)"
    default = "Утверждение заявки на мониторинг"
    required = False


@global_preferences_registry.register
class EmailApprovalContent(HTMLEditorMixin, LongStringPreference):
    section = emails
    name = "approval_content"
    verbose_name = "Письмо утверждение задания (содержание)"
    default = "Утверждение заявки на мониторинг"
    required = False


@global_preferences_registry.register
class EmailStatusTitle(StringPreference):
    section = emails
    name = "status_title"
    verbose_name = "Письмо статус задания (заголовок)"
    default = "Изменен статус Вашего задания на мониторинг"
    required = False


@global_preferences_registry.register
class EmailStatusContent(HTMLEditorMixin, LongStringPreference):
    section = emails
    name = "status_content"
    verbose_name = "Письмо статус задания (содержание)"
    default = "Статус вашего задания изменен. Текущий статус: {{status}}"
    required = False


@global_preferences_registry.register
class EmailPricesTitle(StringPreference):
    section = emails
    name = "prices_title"
    verbose_name = "Письмо изменились цены (заголовок)"
    default = "У конкурента изменились цены"
    required = False


@global_preferences_registry.register
class EmailPricesContent(HTMLEditorMixin, LongStringPreference):
    section = emails
    name = "prices_content"
    verbose_name = "Письмо изменились цены (содержание)"
    default = "У конкурента по товару {{product.name}} изменились цены"
    required = False
