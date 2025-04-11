from django.urls import path
from . import old_views
from . import views

# Add your URLs here in the following form:
# path('URL_you_want', 'corresponding_view', name = 'name used in redirection and links')

urlpatterns = [
    path('', views.basics.home, name = "home"),
    path('register', views.basics.user_register_view, name = 'register'),
    path('login', views.basics.user_login_view, name = 'login'),
    path('logout', views.basics.user_logout_view, name = 'logout'),
    path('howtoANPAHP', views.basics.how_to_anp_ahp_view, name = 'howto_ANP_AHP'),
    path('about', views.basics.about_view, name = 'about'),
    
    # TODO: This one is never referenced anywhere, should probably be put somewhere:
    path('privacy', views.basics.privacy_view, name = 'privacy'),

    # path('myANPAHP',old_views.MyANPAHP,name='myANPAHP'),
    # path('myANPAHPCreate',old_views.MyANPAHPCreate,name='myANPAHPCreate'),
    # path('myANPAHPDelete/<int:pk>',old_views.MyANPAHPDelete,name='myANPAHPDelete'),
    # path('myANPAHPHome/<pk>',old_views.MyANPAHPHome,name='myANPAHPHome'),
    # path('myANPAHPPdf/<int:pk>',old_views.myANPAHPPdf, name='myANPAHPPdf'),



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


]