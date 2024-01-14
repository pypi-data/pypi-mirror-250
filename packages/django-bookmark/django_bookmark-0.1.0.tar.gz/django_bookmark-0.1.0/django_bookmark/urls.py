from django.urls import path

from . import views

urlpatterns = [
    path(
        "togglebookmark/<int:content_type_id>/<int:object_id>",
        views.ToggleBookmark.as_view(),
        name="togglebookmark",
    ),
    path("bookmarks/", views.Bookmarks.as_view(), name="bookmarks"),
]
