from rest_framework import routers
from django.urls import path
from .views import SpinGlassFieldViewSet
from . import views

#qa_solverをrouterとし, その先はViewSetに委託
router = routers.DefaultRouter()
router.register(r'^QASimulator', SpinGlassFieldViewSet)

urlpatterns = [
  path('manual/', views.manual, name='manual'),
 ]
