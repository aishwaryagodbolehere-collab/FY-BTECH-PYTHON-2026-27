from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from profiles import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- UI Page Routes ---
    path('', views.home_page, name='welcome'),
    path('home/', views.home_page, name='home'),
    path('select-role/', views.role_selection_page, name='role_selection'),

 # Student Routes
    path('login/', never_cache(TemplateView.as_view(template_name='login.html')), name='login'),
    path('onboarding/', never_cache(TemplateView.as_view(template_name='onboarding.html')), name='student_onboarding_page'),
    path('student-success/', never_cache(TemplateView.as_view(template_name='student_success.html')), name='student_success'),
    path('profile/', views.student_profile, name='student_profile_page'),

    # Recruiter Routes
    path('login/recruiter/', never_cache(TemplateView.as_view(template_name='login_recruiter.html')), name='login_recruiter'),
    path('recruiter-onboarding/', never_cache(TemplateView.as_view(template_name='recruiter_onboarding.html')), name='recruiter_onboarding_page'),
    path('recruiter/', views.recruiter_dashboard_view, name='recruiter_dashboard'),

    # --- Authentication & Profile APIs ---
    path('api/auth/verify/', views.verify_google_login, name='api_verify_google'),
    path('api/student/signup/', views.student_signup, name='api_student_signup'),
    path('api/student/login/', views.student_login, name='api_student_login'),
    path('api/student/verify-pin/', views.verify_student_pin, name='api_verify_student_pin'),
    path('api/onboarding/', views.student_onboarding, name='api_onboarding'),
    path('api/recruiter-onboarding/', views.recruiter_onboarding, name='api_recruiter_onboarding'),
    path('api/recruiter-login/', views.recruiter_login, name='api_recruiter_login'),
    path('api/recruiter/verify-pin/', views.verify_recruiter_pin, name='api_verify_recruiter_pin'),
    path('api/recruiter/profile/', views.recruiter_profile_api, name='api_recruiter_profile'),
    path('api/students/', views.get_all_students, name='api_get_all_students'),
    path('api/student/<str:prn>/', views.get_student_profile, name='api_get_student_profile'),
    path('api/student/<str:prn>/update/', views.update_student_profile, name='api_update_student_profile'),

    # --- Gemini AI Candidate Search API ---
    path('api/ai-search/', views.ai_candidate_search, name='api_ai_candidate_search'),

    # --- E2EE Chat, Voice Notes, Edit/Delete & Silent Block APIs ---
    path('api/chat/send/', views.send_chat_message, name='api_send_chat_message'),
    path('api/chat/respond/', views.respond_chat_request, name='api_respond_chat_request'),
    path('api/chat/student/<str:prn>/', views.get_student_chats, name='api_get_student_chats'),
    path('api/chat/recruiter/', views.get_recruiter_chats, name='api_get_recruiter_chats'),
    path('api/chat/messages/<int:connection_id>/', views.get_connection_messages, name='api_get_connection_messages'),
    path('api/chat/message/<int:msg_id>/edit/', views.edit_chat_message, name='api_edit_chat_message'),
    path('api/chat/message/<int:msg_id>/delete/', views.delete_chat_message, name='api_delete_chat_message'),
    path('api/chat/connection/<int:connection_id>/delete/', views.delete_chat_connection, name='api_delete_chat_connection'),
    path('api/chat/connection/<int:connection_id>/block/', views.toggle_block_connection, name='api_toggle_block_connection'),

    path('api/account/delete/', views.delete_user_account, name='api_delete_user_account'),

    path('settings/', views.settings_page, name='settings_page'),
    path('api/auth/send-otp/', views.send_verification_code, name='send_verification_code'),
    path('api/auth/reset-credential/', views.verify_and_reset_credential, name='verify_and_reset_credential'),
    path('api/feedback/submit/', views.submit_feedback, name='submit_feedback'),
]