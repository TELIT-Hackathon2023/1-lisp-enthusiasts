from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import HelloWorldView

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('', include(router.urls)),
]