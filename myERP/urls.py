# -*- coding: utf-8 -*-
### import_part
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from myERP import views


### path_part
app_name='myERP'
urlpatterns = [
	path('register/',views.MyRegisterView.as_view(),name='register'),
	path('login/',views.MyLoginView.as_view(),name='login'),
	path('logout/',views.MyLoginView.as_view(),name='logout'),
	path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
	path('password_change/',auth_views.PasswordChangeView.as_view(),name='change-password'),
	path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
	path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
	path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
	path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
	path('register_validation/',views.RegisterValidationView.as_view(),name='register_validation'),
	
	path('add/<str:m_name>/',views.GlobalAddView.as_view(),name='global_add'),
	path('delete/<str:m_name>/<int:pk>/',views.GlobalDeleteView.as_view(),name='global_delete'),
	path('detail/<str:m_name>/<int:pk>/',views.GlobalDetailView.as_view(),name='global_detail'),
	path('list/<str:m_name>/',views.GlobalListView.as_view(),name='global_list'),
	path('update/<str:m_name>/<int:pk>/',views.GlobalUpdateView.as_view(),name='global_update'),
	
	path('',views.Index.as_view(),name='index'),
	path('home/',views.Home.as_view(),name='home'),
	path('admin/',admin.site.urls),
	path('authentication/',include('authentication.urls')),
	path('calendarr/',include('calendarr.urls')),
	path('constant/',include('constant.urls')),
	path('financial/',include('financial.urls')),
	path('main/',include('main.urls')),
	path('note/',include('note.urls')),
	path('people/',include('people.urls')),
	path('series/',include('series.urls')),
	#path('temptry',temptry,name='temptry'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def handler404(request,exeption):
    return render(request,"error_page.html")
def handler403(request,exception):
    return render(request,"error_page.html")
def handler400(request,exception):
    return render(request,"error_page.html")
def handler500(request):
    return render(request,"error_page.html")