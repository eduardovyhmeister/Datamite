from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), # this add the urls specificioant fro events urls
    path('register',views.UserRegisterView,name='register'),
    path('login',views.UserLoginView,name='login'),
    path('logout',views.UserLogout,name='logout'),
    path('howToANPAHP',views.HowToANPAHP,name='howToANPAHP'),
    path('about',views.About,name='about'),
    #path('privacy',views.Privacy,name='privacy'),

    path('myANPAHP',views.MyANPAHP,name='myANPAHP'),
    path('myANPAHPCreate',views.MyANPAHPCreate,name='myANPAHPCreate'),
    path('myANPAHPDelete/<int:pk>',views.MyANPAHPDelete,name='myANPAHPDelete'),
    path('myANPAHPHome/<pk>',views.MyANPAHPHome,name='myANPAHPHome'),
    path('myANPAHPPdf/<int:pk>',views.myANPAHPPdf, name='myANPAHPPdf'),



    #Objectives
    path('myANPAHPStep1/<int:pk>', views.MyANPAHPStep1, name='myANPAHPStep1'),
    # Perspectives BSC
    path('myANPAHPStep1_2/<int:pk>', views.MyANPAHPStep1_2, name='myANPAHPStep1_2'),
    #KPIs
    path('myANPAHPStep2/<int:pk>', views.MyANPAHPStep2, name='myANPAHPStep2'),
    path('myANPAHPStep3/<int:pk>', views.MyANPAHPStep3, name='myANPAHPStep3'),
    path('myANPAHPStep4/<int:pk>', views.MyANPAHPStep4, name='myANPAHPStep4'),
    path('myANPAHPStep5/<int:pk>', views.MyANPAHPStep5, name='myANPAHPStep5'),
    path('newKPI/<int:pk>', views.NewKPI, name='newKPI'),
    #objectives
    path('myANPAHPStep6/<int:pk>', views.MyANPAHPStep6, name='myANPAHPStep6'),
    path('newObjectives/<int:pk>', views.NewObjectives, name='newObjectives'),
    #criterias
    path('myANPAHPStep7/<int:pk>', views.MyANPAHPStep7, name='myANPAHPStep7'),
    path('myANPAHPStep8/<int:pk>', views.MyANPAHPStep8, name='myANPAHPStep8'),
    path('newCriteria/<int:pk>', views.NewCriteria, name='newCriteria'),
    
    #Interanalysis
    path('myANPAHPStep9/<int:pk>', views.MyANPAHPStep9, name='myANPAHPStep9'),
    path('myANPAHPStep10/<int:pk>', views.MyANPAHPStep10, name='myANPAHPStep10'),
    #Results
    path('myANPAHPResults/<int:pk>', views.myANPAHPResult, name='myANPAHPResults'),


]