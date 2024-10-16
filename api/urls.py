from django.urls import path

from api.views import index, add_data, get_all_data, read_file

urlpatterns = [
    path("", index, name="index"),
    path("add/", add_data, name="add_data"),
    path("read_file/", read_file, name="read_file"),
    path("get/", get_all_data, name="get_all_data"),
]
