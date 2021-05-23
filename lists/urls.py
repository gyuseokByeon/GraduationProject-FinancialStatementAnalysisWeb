from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path("myCorp/<str:corp_code>/", views.fav_corp, name="fav"),
    path("myCorp/", views.SeeFavsView.as_view(), name="myCorp"),
]