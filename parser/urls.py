from rest_framework import routers

from parser.views import ParseTaskViewset

router = routers.DefaultRouter()
router.register("parse_task", ParseTaskViewset)
