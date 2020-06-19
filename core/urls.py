from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'urls', views.LinkViewSet)                # GET(short_url lists), POST(origin_url)
router.register(r'urls/redirect/*', views.RedirectViewSet)
urlpatterns = router.urls


obtain_auth_token