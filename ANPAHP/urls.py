"""
Add your URLs here in the following form:
path('URL_you_want', 'corresponding_view', name = 'name used in redirection and links')
"""

from django.urls import path
from . import views


urlpatterns = [
    # Setup basic pages found in the header:
    path('', views.basics.home, name = "home"),
    path('howtoANPAHP', views.basics.how_to_anp_ahp_view, name = 'howto_ANP_AHP'),
    path('about', views.basics.about_view, name = 'about'),
    path('documentation', views.basics.documentation_view, name = 'documentation'),
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
    path('myANPAHP/<int:pk>/createcriterion', views.content_management.create_criterion_view, name = 'create_criterion'),
    path('myANPAHP/<int:pk>/deletecriterion', views.content_management.delete_criterion_view, name = 'delete_criterion'),

    # Objective selection:
    path('myANPAHP/<int:pk>/Step1', views.steps.step1_view, name = "myANPAHPStep1"),
    # Perspectives/BSC preferences:
    path('myANPAHP/<int:pk>/Step2', views.steps.step2_view, name = 'myANPAHPStep2'),
    # KPI selection:
    path('myANPAHP/<int:pk>/Step3', views.steps.step3_view, name = 'myANPAHPStep3'),
    # KPI preferences:
    path('myANPAHP/<int:pk>/Step4', views.steps.step4_view, name = 'myANPAHPStep4'),
    # # Criteria selection:
    # path('myANPAHP/<int:pk>/Step5', views.steps.step5_view, name = 'myANPAHPStep5'),
    # # Criteria preferences:
    # path('myANPAHP/<int:pk>/Step6', views.steps.step6_view, name = 'myANPAHPStep6'),
    # Intermetric relationships:
    # path('myANPAHP/<int:pk>/Step7', views.steps.step7_view, name = 'myANPAHPStep7'),
    # # Intermetric preferences:
    # path('myANPAHP/<int:pk>/Step8', views.steps.step8_view, name = 'myANPAHPStep8'),
    # Intermetric relationships:
    path('myANPAHP/<int:pk>/Step5', views.steps.step7_view, name = 'myANPAHPStep7'),
    # Intermetric preferences:
    path('myANPAHP/<int:pk>/Step6', views.steps.step8_view, name = 'myANPAHPStep8'),
    
    # Once everything has been completed:
    path('myANPAHP/<int:pk>/Results', views.steps.results_view, name = "myANPAHPResults"),
    path('myANPAHP/<int:pk>/DownloadPDF', views.steps.download_pdf_report, name = "download_pdf")
    #path('myANPAHPPdf/<int:pk>',old_views.myANPAHPPdf, name= 'myANPAHPPdf'),

]

# Chat endpoint
urlpatterns += [
    path('chat', views.chat.chat_page, name='chat_page'),
    path('api/chat/ask', views.chat.chat_ask_view, name='chat_ask')
]