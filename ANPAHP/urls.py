from django.urls import path
from . import old_views

urlpatterns = [
    path('', old_views.home, name="home"), # this add the urls specificioant fro events urls
    path('register',old_views.UserRegisterView,name='register'),
    path('login',old_views.UserLoginView,name='login'),
    path('logout',old_views.UserLogout,name='logout'),
    path('howToANPAHP',old_views.HowToANPAHP,name='howToANPAHP'),
    path('about',old_views.About,name='about'),
    #path('privacy',views.Privacy,name='privacy'),

    path('myANPAHP',old_views.MyANPAHP,name='myANPAHP'),
    path('myANPAHPCreate',old_views.MyANPAHPCreate,name='myANPAHPCreate'),
    path('myANPAHPDelete/<int:pk>',old_views.MyANPAHPDelete,name='myANPAHPDelete'),
    path('myANPAHPHome/<pk>',old_views.MyANPAHPHome,name='myANPAHPHome'),
    path('myANPAHPPdf/<int:pk>',old_views.myANPAHPPdf, name='myANPAHPPdf'),



    #Objectives
    path('myANPAHPStep1/<int:pk>', old_views.MyANPAHPStep1, name='myANPAHPStep1'),
    # Perspectives BSC
    path('myANPAHPStep1_2/<int:pk>', old_views.MyANPAHPStep1_2, name='myANPAHPStep1_2'),
    #KPIs
    path('myANPAHPStep2/<int:pk>', old_views.MyANPAHPStep2, name='myANPAHPStep2'),
    path('myANPAHPStep3/<int:pk>', old_views.MyANPAHPStep3, name='myANPAHPStep3'),
    path('myANPAHPStep4/<int:pk>', old_views.MyANPAHPStep4, name='myANPAHPStep4'),
    path('myANPAHPStep5/<int:pk>', old_views.MyANPAHPStep5, name='myANPAHPStep5'),
    path('newKPI/<int:pk>', old_views.NewKPI, name='newKPI'),
    #objectives
    path('myANPAHPStep6/<int:pk>', old_views.MyANPAHPStep6, name='myANPAHPStep6'),
    path('newObjectives/<int:pk>', old_views.NewObjectives, name='newObjectives'),
    #criteria
    path('myANPAHPStep7/<int:pk>', old_views.MyANPAHPStep7, name='myANPAHPStep7'),
    path('myANPAHPStep8/<int:pk>', old_views.MyANPAHPStep8, name='myANPAHPStep8'),
    path('newCriterion/<int:pk>', old_views.NewCriterion, name='newCriterion'),
    
    #Interanalysis
    path('myANPAHPStep9/<int:pk>', old_views.MyANPAHPStep9, name='myANPAHPStep9'),
    path('myANPAHPStep10/<int:pk>', old_views.MyANPAHPStep10, name='myANPAHPStep10'),
    #Results
    path('myANPAHPResults/<int:pk>', old_views.myANPAHPResult, name='myANPAHPResults'),


]