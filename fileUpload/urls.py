from django.urls import path
from fileUpload import views

urlpatterns = [
    # path("", views.home, name="home"),
    path('', views.index, name='index'),
    path('printExcel', views.printExcel, name='printExcel'),
]