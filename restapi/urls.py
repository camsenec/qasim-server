from rest_framework import routers
from .views import SpinGlassFieldViewSet

#qa_solverをrouterとし, その先はViewSetに委託
router = routers.DefaultRouter()
router.register(r'^QASimulator', SpinGlassFieldViewSet)
