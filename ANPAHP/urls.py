"""
Add your URLs here in the following form:
path('URL_you_want', 'corresponding_view', name = 'name used in redirection and links')
"""

from django.urls import path
from . import old_views
from . import views


urlpatterns = [
    # Setup basic pages found in the header:
    path('', views.basics.home, name = "home"),
    path('howtoANPAHP', views.basics.how_to_anp_ahp_view, name = 'howto_ANP_AHP'),
    path('about', views.basics.about_view, name = 'about'),
    # Pushed into the about page.
    # path('privacy', views.basics.privacy_view, name = 'privacy'),

    # Setup basic pages for user management:
    path('register', views.user_management.user_register_view, name = 'register'),
    path('login', views.user_management.user_login_view, name = 'login'),
    path('logout', views.user_management.user_logout_view, name = 'logout'),

    # Setup pages for the management of a user's ANP-AHP evaluations:
    path('myANPAHP', views.anpahp_management.my_anp_ahp, name = 'myANPAHP'),
    path('myANPAHPCreate', views.anpahp_management.my_anp_ahp_create, name = 'myANPAHPCreate'),
    path('myANPAHPDelete/<int:pk>', views.anpahp_management.my_anp_ahp_delete, name= 'myANPAHPDelete'),
    path('myANPAHP/<int:pk>/Home', views.my_anpahp.my_anpahp_home_view, name = 'myANPAHPHome'),
    
    # New content creation pages:
    path('myANPAHP/<int:pk>/createobjective', views.content_management.create_objective_view, name = 'create_objective'),
    path('myANPAHP/<int:pk>/deleteobjective', views.content_management.delete_objective_view, name = 'delete_objective'),
    path('myANPAHP/<int:pk>/createKPI', views.content_management.create_kpi_view, name = 'create_kpi'),
    path('myANPAHP/<int:pk>/deleteKPI', views.content_management.delete_kpi_view, name = 'delete_kpi'),

    # path('newcriterion', old_views.NewObjectives, name='newcriterion'),


    
    # Objective selection:
    path('myANPAHP/<int:pk>/Step1', views.steps.step1.step1_view, name = "myANPAHPStep1"),

    # Perspectives BSC
    path('myANPAHP/<int:pk>/Step2', views.steps.step2.step2_view, name='myANPAHPStep2'),
    
    # KPI selection:
    path('myANPAHP/<int:pk>/Step3', views.steps.step3.step3_view, name='myANPAHPStep3'),
    
    
    # #Objectives
    # path('myANPAHPStep1/<int:pk>', old_views.MyANPAHPStep1, name='myANPAHPStep1'),
    # #KPIs
    # path('myANPAHPStep2/<int:pk>', old_views.MyANPAHPStep2, name='myANPAHPStep2'),
    # path('myANPAHPStep3/<int:pk>', old_views.MyANPAHPStep3, name='myANPAHPStep3'),
    # path('myANPAHPStep4/<int:pk>', old_views.MyANPAHPStep4, name='myANPAHPStep4'),
    # path('myANPAHPStep5/<int:pk>', old_views.MyANPAHPStep5, name='myANPAHPStep5'),
    # path('newKPI/<int:pk>', old_views.NewKPI, name='newKPI'),
    # #objectives
    # path('myANPAHPStep6/<int:pk>', old_views.MyANPAHPStep6, name='myANPAHPStep6'),
    # path('newObjectives/<int:pk>', old_views.NewObjectives, name='newObjectives'),
    # #criteria
    # path('myANPAHPStep7/<int:pk>', old_views.MyANPAHPStep7, name='myANPAHPStep7'),
    # path('myANPAHPStep8/<int:pk>', old_views.MyANPAHPStep8, name='myANPAHPStep8'),
    # path('newCriterion/<int:pk>', old_views.NewCriterion, name='newCriterion'),
    
    # #Interanalysis
    # path('myANPAHPStep9/<int:pk>', old_views.MyANPAHPStep9, name='myANPAHPStep9'),
    # path('myANPAHPStep10/<int:pk>', old_views.MyANPAHPStep10, name='myANPAHPStep10'),
    # #Results
    # path('myANPAHPResults/<int:pk>', old_views.myANPAHPResult, name='myANPAHPResults'),

    #path('myANPAHPPdf/<int:pk>',old_views.myANPAHPPdf, name= 'myANPAHPPdf'),

]