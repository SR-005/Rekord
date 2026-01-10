from django.urls import path
from . import views

urlpatterns=[path("homepage/",views.homepage,name="homepage"),
             path("create/",views.create,name="create"),
            path("claim/<str:code>/", views.claim, name="claim")]