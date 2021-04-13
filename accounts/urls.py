from rest_framework.routers import DefaultRouter

from .views import AccountsViewsets

router = DefaultRouter()
router.register(r'accounts', AccountsViewsets)

urlpatterns = router.urls
