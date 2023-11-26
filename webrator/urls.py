from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import HelloWorldView, AnalyticsView, PersonaView, CleanHTMLAPIView, ContrastAPIView, TipstAPIView

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('analytics', AnalyticsView.as_view(), name='analytics'),
    path('personas', PersonaView.as_view(), name='personas'),
    path('html', CleanHTMLAPIView.as_view(), name='html'),
    path('contrast', ContrastAPIView.as_view(), name='contrast'),
    path('tips', TipstAPIView.as_view(), name='tips'),
    path('', include(router.urls)),
]
