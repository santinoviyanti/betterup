from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Kuis & Diagnosa
    path('deteksi/', views.deteksi_view, name='deteksi'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('riwayat/', views.riwayat_view, name='riwayat'),

    # Artikel
    path('artikel/', views.artikel, name='artikel'),
    path('artikel/<int:id>/', views.detail_artikel, name='detail_artikel'),
]