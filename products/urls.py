from rest_framework import routers

from products.views import CategoryViewset, ProductPriceHistoryViewset, ProductViewset, StatusProductViewset

router = routers.DefaultRouter()
router.register("product", ProductViewset)
router.register("category", CategoryViewset)
router.register("product_price", ProductPriceHistoryViewset)
router.register("statusproduct", StatusProductViewset)
