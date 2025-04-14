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
    path('myANPAHPHome/<int:pk>', views.my_anpahp.my_anpahp_home_view, name = 'myANPAHPHome'),
    
    # Objective selection:
    path('myANPAHPStep1/<int:pk>', views.steps.step1.step1_view, name = "myANPAHPStep1"),
    
    # #Objectives
    # path('myANPAHPStep1/<int:pk>', old_views.MyANPAHPStep1, name='myANPAHPStep1'),
    # # Perspectives BSC
    # path('myANPAHPStep1_2/<int:pk>', old_views.MyANPAHPStep1_2, name='myANPAHPStep1_2'),
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