from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from .models import Observation, DocumentPage
from ..mixins import CumorahMixin


class DocumentObservationListView(ListView):
    model = Observation
    template_name = 'repository/observation_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(document__pk=self.kwargs.get('document_pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['document_pk'] = self.kwargs.get('document_pk')
        return super().get_context_data(object_list=object_list, **kwargs)


class DocumentObservationCreateView(CreateView):
    model = Observation
    template_name = 'repository/observation_create.html'
    fields = [
        'title',
        'reference',
        'description',
    ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        document = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        observation = self.model(
            document=document,
            slug=self.model.get_random_slug(),
            contributor=self.request.passport.contributor,
        )
        kwargs['instance'] = observation
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('repository:document:observation_list', args=(self.kwargs.get('document_pk'),))


class DocumentObservationUpdateView(UpdateView):
    model = Observation
    template_name = 'repository/observation_update.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # FIXME: Limit access by qs filter
        return qs.filter(document__pk=self.kwargs.get('document_pk'))


class ObservationDetailView(CumorahMixin, DetailView):
    model = Observation
    template_name = 'repository/observation_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.passport.is_admin or self.request.passport.contributor.can_admin:
            return qs
        else:
            return qs.filter(visible=True)
