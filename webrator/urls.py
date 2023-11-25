from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import HelloWorldView, AnalyticsView, PersonaView

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('analytics', AnalyticsView.as_view(), name='analytics'),
    path('personas', PersonaView.as_view(), name='personas'),
    path('', include(router.urls)),
]
