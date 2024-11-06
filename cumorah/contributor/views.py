from django.views.generic import UpdateView, RedirectView, ListView, DetailView
from django.shortcuts import reverse

from cumorah.contributor.models import Contributor
from cumorah.contributor.forms import RequestActivationForm, ContributorUpdateForm
from cumorah.mixins import CumorahMixin


class ContributorRedirectView(CumorahMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        try:
            contributor = Contributor.objects.get(user=self.request.user)
        except Contributor.DoesNotExist:
            contributor = Contributor.objects.create(
                user=self.request.user,
                display_name=self.request.user.username,
                slug=Contributor.get_random_slug(),
            )

        return reverse('contributor:detail', kwargs={'slug': contributor.slug})


class ContributorDetailView(CumorahMixin, DetailView):
    slug_field = 'slug'
    model = Contributor
    template_name = 'contributor/contributor_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_admin:
            return qs

        return qs.filter(user=self.request.user)


class ContributorUpdateView(CumorahMixin, UpdateView):
    slug_field = 'slug'
    model = Contributor
    fields = (
        'display_name',
        'bio',
    )
    template_name = 'contributor/contributor_update.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.is_admin:
            return qs

        return qs.filter(user=self.request.user)

    def get_success_url(self, *args, **kwargs):
        return reverse('contributor:detail', kwargs={'slug': self.kwargs['slug']})


class ContributorRequestActivationView(CumorahMixin, UpdateView):
    """
    ContributorRequestActivationView is the contributor side of the
    activation flow. A contributor will verify their display name and bio
    then provide any additional activation request notes. The admin view
    is then used to accept the application, activate the contributor,
    and set a contribution level.
    """
    slug_field = 'slug'
    model = Contributor
    form_class = RequestActivationForm
    template_name = 'contributor/contributor_request_activation.html'


    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user, active=False)



    def get_success_url(self, *args, **kwargs):
        return reverse('contributor:detail', kwargs={'slug': self.kwargs['slug']})


class ContributorListView(ListView):
    admin_required = True
    model = Contributor
    template_name = 'contributor/contributor_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['link_to_activation_requests'] = True
        return super().get_context_data(object_list=object_list, **kwargs)


class RequestedContributorActivationListView(CumorahMixin, ListView):
    admin_required = True
    model = Contributor
    template_name = 'contributor/contributor_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(active=False, activation_request_notes__isnull=False)


class ContributorAdminUpdateView(CumorahMixin, UpdateView):
    admin_required = True
    slug_field = 'slug'
    model = Contributor
    form_class = ContributorUpdateForm
    template_name = 'contributor/contributor_admin_update.html'

    def form_valid(self, form):
        if form.cleaned_data['active'] and form.instance.approved_by is None:
            form.instance.approved_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contributor_admin:list')

