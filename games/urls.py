from rest_framework.routers import DefaultRouter

from .views import GameViewSets

router = DefaultRouter()
router.register(r'games', GameViewSets)

urlpatterns = router.urls
