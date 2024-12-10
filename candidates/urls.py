from django.urls import path
from .views import CandidateDetailView, CandidateListCreateView, CandidateSearchView

urlpatterns = [
    path("", CandidateListCreateView.as_view(), name="candidate-list"),
    path("search/", CandidateSearchView.as_view(), name="candidate-search"),
    path("<int:pk>/", CandidateDetailView.as_view(), name="candidate-detail"),
]
