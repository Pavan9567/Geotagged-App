from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('upload/', views.upload_image, name='upload_image'),
    path('list/', views.image_list, name="image_list"),
    path('geotagged-data/', views.geotagged_data_view, name="geotagged-data"),
    path('api/geotagged-data/', views.geotagged_data_api, name='geotagged_data_api'),
    path('map/', views.map_visualization, name='map_visualization'),
]
