from django.urls import path
from . import views as core_views

app_name = 'core'

urlpatterns = [
    path("", core_views.HomePageView.as_view(), name="home"),
    path("result", core_views.SearchResultsView.as_view(), name="corp-search"),
    path("ranking", core_views.RankingView.as_view(), name="ranking"),
    path("ranking/revenue_growth", core_views.ajax_revenue_growth, name="ajax-revenue-growth"),
    path("ranking/net_income_growth", core_views.ajax_income_growth, name="ajax-net-income-growth"),
]