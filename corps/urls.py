from django.urls import path
from . import views
app_name = 'corps'

urlpatterns = [
    path("<str:corp_code>/", views.CorpDetailView.as_view(), name="corp-detail"),
]