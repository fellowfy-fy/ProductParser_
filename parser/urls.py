from rest_framework import routers

from parser.views import ParseTaskViewset, SiteParseSettingsViewset

router = routers.DefaultRouter()
router.register("parse_task", ParseTaskViewset)
router.register("parse_settings", SiteParseSettingsViewset)
