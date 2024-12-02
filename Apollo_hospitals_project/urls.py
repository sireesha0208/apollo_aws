"""
URL configuration for Apollo_hospitals_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from location_app.views  import create_location, location_details, update_location,list_locations,\
    locations_state,locations,delete_location,create_speciality,list_speciality, update_speciality,\
    delete_speciality,create_doctor,update_doctor,delete_doctor,get_doctors


urlpatterns = [
    path('location/', create_location, name='create-location'),  #-------------
    path('location_detail/<int:location_id>/', location_details, name='location-detail'),  #single location list
    path('location/<int:location_id>/', update_location, name='update-location'),#----------
    path('delete_location/<int:location_id>/', delete_location, name='delete_location'),
    path('location_list/',list_locations, name='list-locations'), # all location details -------------------
    path('location_state/',locations, name='locations'), # only locations list ###--------
    path('locations_lists/',locations_state, name='all_locations'),# only states--------------------
    path('locations/<str:state_name>/',locations_state, name='locations_by_state'),# selected state with locations 
    path('speciality/create/', create_speciality, name='create_speciality'),
    path('speciality/', list_speciality, name='list_specialities'),
    path('speciality/<int:speciality_id>/update/', update_speciality, name='update_speciality'),
    path('speciality/<int:speciality_id>/delete/', delete_speciality, name='delete_speciality'),
    path('doctor/create/', create_doctor, name='create_doctor'),
    path('doctors/', get_doctors, name='get_doctors'),
    path('doctor/update/<int:doctor_id>/', update_doctor, name='update_doctor'),
    path('doctor/delete/<int:doctor_id>/', delete_doctor, name='delete_doctor'),



]

