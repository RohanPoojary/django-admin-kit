from django.conf.urls import url, include
from django.contrib import admin
import admin_kit
import nested_admin

urlpatterns = [
    url('admin/', admin.site.urls, name="admin"),
    url('nested_admin/', include('nested_admin.urls'), name="nested_admin"),
    url('admin_kit/', admin_kit.site.urls, name="admin_kit")
]