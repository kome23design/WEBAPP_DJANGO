from django.urls import path
from regisapp import views
from django.contrib.auth.views import LoginView, LogoutView

app_name='regisapp'
urlpatterns=[
    

    path("", LoginView.as_view(template_name='regisapp/login.html'),name="login_page"),

    path("signup/",views.Register,name="regis_page"),
    path("logout/",views.logout_view,name="logout_page")


]