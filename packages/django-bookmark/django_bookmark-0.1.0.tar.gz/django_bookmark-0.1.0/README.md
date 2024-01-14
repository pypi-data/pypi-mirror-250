# Django Bookmark

A Django app that lets users create bookmarks to Django model instances

# Installation

Install `django-bookmark` using your favourite package manager.

Add `django_bookmark` to your Django projects `INSTALLED_APPS`:
```
...
'django_bookmark',
...
```

Include `django_bookmark.urls` in your URL dispatcher:
```
...
path("", include("django_bookmark.urls")),
...
```

Django Bookmarks adds two routes below where you include the app:
* `/bookmarks/` is a view that lists all bookmarks of the user accessing it
* `/togglebookmark/<content_type_id>/<object_id>` is a view to add or remove a bookmark, that points to the model instance specified by the `content_type_id` and the `object_id`. The bookmark will be saved with the user id of the user accessing the view.

Django Bookmarks ships the `django_bookmark` templatetags library, which currently consists of the templatetag `toggle_bookmark`.
The `toggle_bookmark` templatetag takes the model instance as argument and adds a `bookmark` link that to your template. This bookmark link displayes
a bookmark symbol that is either white, if the model instance *is not* bookmarked or yellow, if the model instance *is* bookmarked. Clicking the link
toggles the bookmarking state of the model instance for the logged in user.
If you have [htmx](htmx.org/) included in your web application, the bookmarking link uses htmx to update the bookmark symbol, otherwise the link
redirects to the page where you came from.

Django Bookmarks uses the [Bookmark Add](https://fonts.google.com/icons?selected=Material%20Symbols%20Outlined%3Abookmark_add%3AFILL%400%3Bwght%40400%3BGRAD%400%3Bopsz%4024) svg from the Material Symbols collection and the [Bookmark](https://fonts.google.com/icons?selected=Material%20Icons%20Outlined%3Abookmark%3A) svg from the Material Icons collection. Both are licensed under the [SIL Open Font License](https://openfontlicense.org/).
