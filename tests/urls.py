from django.conf.urls import url
from django.contrib import admin
import admin_kit

urlpatterns = [
    url('admin/', admin.site.urls, name="admin"),
    url('admin_kit/', admin_kit.site.urls, name="admin_kit")
]