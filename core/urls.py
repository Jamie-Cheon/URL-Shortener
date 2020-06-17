from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'urls', views.LinkViewSet)                # GET(short_url lists), POST(origin_url)
urlpatterns = router.urls

