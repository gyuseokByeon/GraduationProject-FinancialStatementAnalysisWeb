from django.urls import path
from . import views
app_name = 'corps'

urlpatterns = [
    path("<str:corp_code>/", views.CorpDetailView.as_view(), name="corp-detail"),

    path("ajax/finance/<str:corp_code>/", views.ajax_finance, name="ajax-finance"),
    path("ajax/income/<str:corp_code>/", views.ajax_income, name="ajax-income"),
    path("ajax/finance/analysis/<str:corp_code>/", views.ajax_finance_analysis, name="ajax-finance-analysis"),
    path("ajax/income/analysis/<str:corp_code>/", views.ajax_income_analysis, name="ajax-income-analysis"),

    path("ajax/asset_graph/<str:corp_code>/", views.asset_graph, name="asset-graph"),
    path("ajax/liability_graph/<str:corp_code>/", views.liability_graph, name="liability-graph"),
    path("ajax/capital_graph/<str:corp_code>/", views.capital_graph, name="capital-graph"),

    path("ajax/revenue_graph/<str:corp_code>/", views.revenue_graph, name="revenue-graph"),
    path("ajax/cost_graph/<str:corp_code>/", views.cost_graph, name="cost-graph"),
    path("ajax/gross_profit_graph/<str:corp_code>/", views.gross_porfit_graph, name="gross_profit-graph"),
    path("ajax/operating_expense_graph/<str:corp_code>/", views.operating_expense_graph, name="operating_expense-graph"),
    path("ajax/operating_profit_graph/<str:corp_code>/", views.operating_profit_graph, name="operating_profit-graph"),
    path("ajax/financial_income_graph/<str:corp_code>/", views.financial_income_graph, name="financial_income-graph"),
    path("ajax/net_income_graph/<str:corp_code>/", views.net_income_graph, name="net_income-graph"),
]