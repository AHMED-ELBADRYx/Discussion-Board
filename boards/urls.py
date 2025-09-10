from django.urls import path
from . import views

urlpatterns = [
    # path("", views.board_list, name="board_list"), # FBV
    path("", views.BoardListView.as_view(), name="board_list"),
    path("<int:board_id>/", views.board_detail, name="board_detail"),
    path("<int:board_id>/new_topic/", views.new_topic, name="new_topic"),
    path("<int:board_id>/topics/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
]