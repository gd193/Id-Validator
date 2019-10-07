from django.urls import include, path
from rest_framework import routers
from . import views


#router = routers.DefaultRouter()
#router.register( r'id', views.id_view ,basename='id')

urlpatterns = [
    path( 'id/',views.id_view.as_view()),
    path( 'api-auth/', include('rest_framework.urls') )
]
