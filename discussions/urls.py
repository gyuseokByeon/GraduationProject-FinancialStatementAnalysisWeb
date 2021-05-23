from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path("go/<int:dis_pk>/", views.go_discussion, name="go"),
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
    path("create/<str:corp_code>/", views.CreateDiscussionView.as_view(), name="create"),
    path("participate/<int:pk>/", views.participate, name="participate"),
]