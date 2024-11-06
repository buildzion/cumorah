from django.urls import path, re_path, include, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from . import views


contributor_urls = [
    path('', views.ContributorListView.as_view(), name='list'),
    path('requests', views.RequestedContributorActivationListView.as_view(), name='activation_requests'),
    re_path(r'(?P<slug>cc-[\w]{20})/update$', views.ContributorAdminUpdateView.as_view(), name='update'),

]


@hooks.register('register_admin_urls')
def register_contributor_url():
    return [
        path('contributor/', include((contributor_urls, 'contributor_admin')))
    ]

@hooks.register('register_admin_menu_item')
def register_contributor_menu_item():
    return MenuItem('Contributors', reverse('contributor_admin:list'), icon_name='group')
