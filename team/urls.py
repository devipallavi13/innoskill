from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login.html', views.login_page, name='login_page'),
    path('register.html', views.register_page, name='register_page'),
    path('register/', views.register, name='register'),
    path('submit/', views.submit, name='submit'),
    path('user/', views.user, name='user'),
    path('submit/register.html', views.register_page, name='redirect_to_register'),
    path('post/', views.post, name='post'),
    path('logout/', views.logout, name='logout'),
    path('my_problems/', views.my_problems, name='my_problems'),
    path('edit_problem/<int:problem_id>/', views.edit_problem, name='edit_problem'),
    path('delete_problem/<int:problem_id>/', views.delete_problem, name='delete_problem'),
    path('organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('submit_solution/', views.submit_solution, name='submit_solution'),
    path("ask/", views.contact_us, name="contact_us"),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
