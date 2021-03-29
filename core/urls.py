from django.urls import path
from . import views as core_views

app_name = 'core'

urlpatterns = [
    path("", core_views.HomePageView.as_view(), name="home"),
    path("result", core_views.SearchResultsView.as_view(), name="corp-search"),
]