from django.urls import path
from .views import adminhome, addbooking, editbooking, deletebooking, review,feedback_view
from .import views
urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('event/', views.event, name='event'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('logout/', views.logout, name='logout'),
    path('addbooking/', views.addbooking, name='addbooking'),
    path('editbooking/<int:booking_id>/', views.editbooking, name='editbooking'),
    path('deletebooking/<int:booking_id>/', views.deletebooking, name='deletebooking'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('booking/<int:booking_id>/review/', review, name='review'),
    
    path('feedback/', views.feedback_view, name='feedback'),

    
    path('thankyou/', views.thankyoupage, name='thankyoupage'),
]


  


  
