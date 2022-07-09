from django.urls import path
from .views import MarusiaRouter


urlpatterns = [
    path('', MarusiaRouter.as_view())
]