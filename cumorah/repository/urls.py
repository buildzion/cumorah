
from django.urls import include, path, re_path

from . import views

doc_patterns = [
    path('', views.DocumentObservationListView.as_view(), name='observation_list'),
    path('add', views.DocumentObservationCreateView.as_view(), name='observation_create'),
    re_path(r'(?P<slug>ob-[\w]{12})/update$', views.DocumentObservationListView.as_view(), name='observation_update'),

]

observe_patterns = [
    path('', views.ObservationDetailView.as_view(), name='detail'),
]

repo_patterns = [
    path('<int:document_pk>/', include((doc_patterns, 'document'))),
    re_path(r'(?P<slug>ob-[\w]{12})/', include((observe_patterns, 'observation'))),
]

urlpatterns = [
    path('', include((repo_patterns, 'repository'))),
]
