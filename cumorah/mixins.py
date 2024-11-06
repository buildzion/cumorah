from django.http import Http404

from cumorah.contributor.models import Contributor


class CumorahMixin:
    admin_required = False
    admin_get_permitted_groups = None
    admin_post_permitted_groups = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()

        self.passport = request.passport
        self.is_admin = self._admin_authorized(request, self.passport)

        if self.admin_required and not self.is_admin:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def _admin_authorized(self, request, passport):
        if not passport:
            return False

        if passport.is_admin:
            return True

        if request.method == 'GET':
            return passport.is_any_permitted(self.admin_get_permitted_groups)
        else:
            return passport.is_any_permitted(self.admin_post_permitted_groups)


class PassportMiddleware:
    def __init__(self, get_response):
        self.next_function = get_response

    def __call__(self, request):

        request.passport = Passport(request.user)

        return self.next_function(request)


class Passport:
    def __init__(self, user=None):
        self.user = user
        self.contributor = Contributor.objects.filter(user=user).first()
        self.is_admin = False
        if user.is_superuser:
            self.is_admin = True

    def is_any_permitted(self, group_list):
        if not group_list:
            return False
        return self.user.groups.filter(name__in=group_list).exists()
