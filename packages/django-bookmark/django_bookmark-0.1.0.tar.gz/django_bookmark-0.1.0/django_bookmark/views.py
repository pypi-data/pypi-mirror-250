from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from django_bookmark.models import Bookmark


class ToggleBookmark(LoginRequiredMixin, TemplateView):
    template_name = "django_bookmark/toggle_bookmark.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["exists"] = self.created
        context["content_type_id"] = kwargs["content_type_id"]
        context["object_id"] = kwargs["object_id"]
        return context

    def get(self, *args, **kwargs):
        content_type = ContentType.objects.get(pk=kwargs["content_type_id"])
        bookmark, self.created = Bookmark.objects.get_or_create(
            content_type=content_type,
            object_id=kwargs["object_id"],
            user=self.request.user,
        )
        if not self.created:
            bookmark.delete()
        if redirect_to := self.request.GET.get("to", False):
            return redirect(redirect_to)
        return super().get(*args, **kwargs)


class Bookmarks(LoginRequiredMixin, ListView):
    model = Bookmark

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)
