
from django.urls import include, path, re_path

from . import views

doc_patterns = [
    path('', views.DocumentNoteListView.as_view(), name='note_list'),
    path('add', views.DocumentNoteCreateView.as_view(), name='note_create'),
    re_path(r'(?P<slug>n-[\w]{12})/update$', views.DocumentNoteUpdateView.as_view(), name='note_update'),

]

note_patterns = [
    path('', views.NoteDetailView.as_view(), name='detail'),
    path('comments', views.CommentListView.as_view(), name='comments'),
    path('comment', views.CommentCreateView.as_view(), name='comment'),
]

comment_patterns = [
    path('', views.CommentDetailView.as_view(), name='detail'),
    path('update', views.CommentUpdateView.as_view(), name='update'),
    path('delete', views.CommentDeleteView.as_view(), name='delete'),
]

repo_patterns = [
    path('<int:document_pk>/', include((doc_patterns, 'document'))),
    re_path(r'(?P<slug>n-[\w]{12})/', include((note_patterns, 'note'))),
    re_path(r'(?P<slug>nc-[\w]{18})/', include((comment_patterns, 'comment'))),
]

urlpatterns = [
    path('', include((repo_patterns, 'repository'))),
]
