from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donor/signup/', views.donor_signup, name='donor_signup'),
    path('receiver/signup/', views.receiver_signup, name='receiver_signup'),
    path("donor/login/", views.donor_login_view, name="donorLogin"),
    path("logout/", views.logout_view, name="logout"),
    path("receiver/login/", views.receiver_login_view, name="RecieverLogin"),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donation/edit/<int:id>/', views.edit_donation, name='edit_donation'),
    path('donation/delete/<int:id>/', views.delete_donation, name='delete_donation'),
    path('receiver/dashboard/', views.receiver_dashboard, name='receiver_dashboard'),
    path('donation/<int:id>/request/', views.request_food, name='request_food'),
    path("request-food/<int:id>/", views.request_food, name="request_food"),
]
