from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entity_name>",views.get_content, name="content"),
    path("search/",views.search, name="search"),
    path("new/",views.new, name="new_page"),
    path("edit/",views.edit, name="edit"),
    path("save/",views.save, name="save_edit"),
    path("random/",views.random, name="random"),
]
