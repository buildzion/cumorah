from django.urls import path, re_path, include

from cumorah.contributor import views


contributor_patterns = [
    path('', views.ContributorRedirectView.as_view(), name='redirect'),
    re_path(r'(?P<slug>cc-[\w]{20})/$', views.ContributorDetailView.as_view(), name='detail'),
    re_path(r'(?P<slug>cc-[\w]{20})/update$', views.ContributorUpdateView.as_view(), name='update'),
    re_path(r'(?P<slug>cc-[\w]{20})/activate$', views.ContributorRequestActivationView.as_view(), name='request_activation'),
]

urlpatterns = [
    path('', include((contributor_patterns, 'contributor'))),
]
