from django.urls import path
from .views import TeamsViews,TeamsDetailView
urlpatterns = [
    path("teams/", TeamsViews.as_view()),
    path("teams/<int:team_id>/", TeamsDetailView.as_view()),
]
