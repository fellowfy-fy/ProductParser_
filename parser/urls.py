from parser.views import ParseTaskViewset, SiteParseSettingsViewset

from rest_framework import routers

router = routers.DefaultRouter()
router.register("parse_task", ParseTaskViewset)
router.register("parse_settings", SiteParseSettingsViewset)
