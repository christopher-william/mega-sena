from rest_framework.routers import DefaultRouter

from .views import AccountsViewSets

router = DefaultRouter()
router.register(r'accounts', AccountsViewSets)

urlpatterns = router.urls
