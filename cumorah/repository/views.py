import json

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from django.db.models.query import Q

from .forms import CommentUpdateForm, NoteForm
from .models import DocumentNote, DocumentPage, NoteComment
from ..mixins import CumorahMixin


class DocumentNoteListView(CumorahMixin, ListView):
    model = DocumentNote
    template_name = 'repository/note_list.html'
    login_required = False

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(document__pk=self.kwargs.get('document_pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['document_pk'] = self.kwargs.get('document_pk')
        return super().get_context_data(object_list=object_list, **kwargs)


class DocumentNoteCreateView(CumorahMixin, CreateView):
    model = DocumentNote
    template_name = 'repository/note_create.html'
    form_class = NoteForm
    login_required = True

    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     event_info = {
    #         "initialize_tinymce":
    #             {
    #                 # "selector": f"form#comment{self.object.pk} textarea"
    #                 "selector": "textarea#id_description"
    #             }
    #     }
    #     response.headers["HX-Trigger-After-Settle"] = json.dumps(event_info)
    #     return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_page'] = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        document = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        note = self.model(
            document=document,
            slug=self.model.get_random_slug(),
            contributor=self.passport.contributor,
        )
        kwargs['instance'] = note
        return kwargs

    def get_success_url(self):
        document = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        return document.url


class DocumentNoteUpdateView(CumorahMixin, UpdateView):
    model = DocumentNote
    template_name = 'repository/note_update.html'
    form_class = NoteForm
    login_required = True

    def get_queryset(self):
        qs = super().get_queryset()

        filter_args = Q(document__pk=self.kwargs.get('document_pk'))
        if not self.passport.is_admin:
            filter_args &= Q(contributor=self.passport.contributor)

        return qs.filter(filter_args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_page'] = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        return context

    def get_success_url(self):
        document = DocumentPage.objects.get(pk=self.kwargs.get('document_pk'))
        return document.url


class NoteDetailView(CumorahMixin, DetailView):
    model = DocumentNote
    template_name = 'repository/note_detail.html'
    login_required = False

    def get_queryset(self):
        qs = super().get_queryset()
        if self.passport.is_admin or self.passport.contributor and self.passport.contributor.can_admin:
            return qs
        else:
            return qs.filter(visible=True)


class CommentListView(CumorahMixin, ListView):
    model = NoteComment
    template_name = 'repository/comment_create.html'
    login_required = False

    def get_queryset(self):
        qs = super().get_queryset().filter(note__slug=self.kwargs.get('slug'))
        if self.passport.is_admin or self.passport.contributor and self.passport.contributor.can_admin:
            return qs
        else:
            return qs.filter(visible=True)


class CommentCreateView(CumorahMixin, CreateView):
    model = NoteComment
    template_name = 'repository/comment_create.html'
    login_required = True
    fields = (
        'comment',
    )

    def dispatch(self, request, *args, **kwargs):
        self.note = get_object_or_404(DocumentNote, slug=self.kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(
            slug=self.model.get_random_slug(),
            note=self.note,
            contributor=self.passport.contributor,
        )
        return kwargs

    def get_context_data(self, **kwargs):
        qs = self.note.notecomment_set.all()
        if self.passport.is_admin or self.passport.contributor and self.passport.contributor.can_admin:
            kwargs['object_list'] = qs
        else:
            kwargs['object_list'] = qs.filter(visible=True)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return self.request.path


class CommentUpdateView(CumorahMixin, UpdateView):
    model = NoteComment
    template_name = 'repository/comment_update.html'
    login_required = True
    form_class = CommentUpdateForm

    def get_queryset(self):
        qs = super().get_queryset()
        if self.passport.is_admin:
            return qs

        return qs.filter(contributor=self.passport.contributor)


    def get_success_url(self):
        return reverse('repository:comment:detail', args=[self.object.slug])


class CommentDeleteView(CumorahMixin, DeleteView):
    model = NoteComment
    login_required = True

    def get_queryset(self):
        qs = super().get_queryset()
        if self.passport.is_admin:
            return qs

        return qs.filter(contributor=self.passport.contributor)

    def get_success_url(self):
        return reverse('repository:note:comment', args=[self.object.note.slug])


class CommentDetailView(CumorahMixin, DetailView):
    model = NoteComment
    template_name = 'repository/_comment_detail.html'
