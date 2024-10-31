from django.urls import path

from .views import liveValues
from .views import historyValues

urlpatterns = [
    path("live_values/", liveValues, name="liveValues"),
    path('history_values/', historyValues, name='historyValues'),
]
