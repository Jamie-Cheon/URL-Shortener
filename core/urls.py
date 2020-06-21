from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'urls', views.LinkViewSet)
router.register(r'urls/redirect/*', views.RedirectViewSet)
urlpatterns = router.urls


