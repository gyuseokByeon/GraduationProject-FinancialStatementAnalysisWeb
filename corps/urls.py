from django.urls import path
from . import views
app_name = 'corps'

urlpatterns = [
    path("<str:corp_code>/", views.CorpDetailView.as_view(), name="corp-detail"),
    path("ajax/finance/<str:corp_code>/", views.ajax_finance, name="ajax-finance"),
    path("ajax/income/<str:corp_code>/", views.ajax_income, name="ajax-income")
]