from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reconhecimento.api.views import PrevisaoViewSet
router = DefaultRouter()
router.register(r'previsoes', PrevisaoViewSet, basename='previsao')
urlpatterns = [
    path('', include(router.urls)),
]
