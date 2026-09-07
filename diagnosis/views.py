import os
import joblib
import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import MentalHealthTest

from django.core.paginator import Paginator
from django.db.models import Q
from .models import Artikel

# -------------------------------------------------------------------
# LOAD MODEL DECISION TREE & METADATA PERTANYAAN (DATASET EXCEL)
# -------------------------------------------------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, 'model_disorder_dt.pkl')

if os.path.exists(MODEL_PATH):
    model_dt = joblib.load(MODEL_PATH)
else:
    model_dt = None

# 27 Pertanyaan Terstruktur Sesuai Kolom Dataset Excel
QUESTIONS = [
    {'code': 'ag+1:629e', 
    'text': 'Berapa rentang usia Anda saat ini?', 
    'type': 'select', 
    'options': [
        ('0', 'Anak-anak (0 - 11 tahun)'),
        ('1', 'Remaja (12 - 18 tahun)'),
        ('2', 'Dewasa Muda (19 - 25 tahun)'),
        ('3', 'Dewasa (> 25 tahun)')]},
    {'code': 'feeling.nervous', 'text': 'Apakah Anda sering merasa cemas atau gugup?'},
    {'code': 'panic', 'text': 'Apakah Anda sering mengalami rasa panik secara mendadak?'},
    {'code': 'breathing.rapidly', 'text': 'Apakah Anda sering mengalami napas cepat / tersengal-sengal?'},
    {'code': 'sweating', 'text': 'Apakah Anda sering berkeringat dingin secara berlebihan?'},
    {'code': 'trouble.in.concentration', 'text': 'Apakah Anda mengalami kesulitan untuk fokus atau berkonsentrasi?'},
    {'code': 'having.trouble.in.sleeping', 'text': 'Apakah Anda mengalami gangguan / kesulitan tidur (insomnia)?'},
    {'code': 'having.trouble.with.work', 'text': 'Apakah masalah emosional mengganggu pekerjaan atau aktivitas Anda?'},
    {'code': 'hopelessness', 'text': 'Apakah Anda sering merasa putus asa tentang masa depan?'},
    {'code': 'anger', 'text': 'Apakah Anda mudah merasa marah atau emosional?'},
    {'code': 'over.react', 'text': 'Apakah Anda sering bereaksi secara berlebihan terhadap masalah kecil?'},
    {'code': 'change.in.eating', 'text': 'Apakah terjadi perubahan pola makan yang drastis?'},
    {'code': 'suicidal.thought', 'text': 'Apakah pernah muncul pikiran untuk mengakhiri hidup?'},
    {'code': 'feeling.tired', 'text': 'Apakah Anda sering merasa sangat lelah tanpa alasan yang jelas?'},
    {'code': 'close.friend', 'text': 'Apakah Anda merasa tidak memiliki teman dekat untuk berbagi cerita?'},
    {'code': 'social.media.addiction', 'text': 'Apakah Anda merasa kecanduan media sosial?'},
    {'code': 'weight.gain', 'text': 'Apakah Anda mengalami kenaikan berat badan secara signifikan?'},
    {'code': 'introvert', 'text': 'Apakah Anda cenderung menyendiri atau seorang introvert?'},
    {'code': 'popping.up.stressful.memory', 'text': 'Apakah sering teringat kenangan masa lalu yang traumatik?'},
    {'code': 'having.nightmares', 'text': 'Apakah Anda sering mengalami mimpi buruk?'},
    {'code': 'avoids.people.or.activities', 'text': 'Apakah Anda sering menghindari orang lain atau aktivitas sosial?'},
    {'code': 'feeling.negative', 'text': 'Apakah Anda sering berpikiran negatif terhadap diri sendiri?'},
    {'code': 'trouble.concentrating', 'text': 'Apakah Anda sangat mudah terdistraksi saat melakukan sesuatu?'},
    {'code': 'blamming.yourself', 'text': 'Apakah Anda sering menyalahkan diri sendiri secara berlebihan?'},
    {'code': 'hallucinations', 'text': 'Apakah Anda pernah mendengar atau melihat sesuatu yang tidak nyata?'},
    {'code': 'repetitive.behaviour', 'text': 'Apakah Anda sering melakukan perilaku yang berulang-ulang?'},
    {'code': 'increased.energy', 'text': 'Apakah Anda pernah merasa energi sangat meluap-luap secara tiba-tiba?'}
]


# Home view (beranda)
def home(request):
    articles = Artikel.objects.all().order_by('-tanggal_dibuat')
    return render(request, 'home.html', {'articles': articles})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Selamat datang kembali, {user.username}!")
            
            # 1. JIKA AKUN ADALAH SUPERUSER / ADMIN
            # Selalu arahkan ke Dashboard Admin Django, abaikan 'next_url'
            if user.is_superuser:
                return redirect('/admin/')
            
            # 2. JIKA USER BIASA & ADA PARAMETER 'next'
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # 3. USER BIASA TANPA PARAMETER 'next'
            return redirect('home')
        else:
            messages.error(request, 'Username/Email atau password salah!')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Register view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Cek ketersediaan email
            if email and get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'Email sudah digunakan!')
                return render(request, 'register.html', {'form': form})

            # Simpan user ke database
            user = form.save()
            
            # Otomatis login dengan backend khusus
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, "Akun berhasil dibuat!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# Diagnosa view
def deteksi_view(request):
    return render(request, 'deteksi.html', {'questions': QUESTIONS})


# Submit kuis view (WAJIB LOGIN)
@login_required(login_url='login')
def submit_quiz(request):
    if request.method == 'POST':
        user_answers = {}
        
        for q in QUESTIONS:
            code = q['code']
            val = request.POST.get(code)
            
            if val is None or val == '':
                return render(request, 'deteksi.html', {
                    'questions': QUESTIONS,
                    'error': 'Harap isi semua pertanyaan!'
                })
            
            user_answers[code] = int(val)
        
        # -------------------------------------------------------------------
        # LOGIKA FILTER SEMENTARA (TANPA RETRAIN MODEL)
        # -------------------------------------------------------------------
        # Hitung jumlah gejala yang bernilai > 0 (mengabaikan kolom umur 'ag+1:629e')
        symptom_values = [v for k, v in user_answers.items() if k != 'ag+1:629e']
        total_symptoms = sum(symptom_values)

        # Ambang batas minimal gejala (misal: jika mengisi kurang dari 3 gejala)
        if total_symptoms < 3:
            prediction = "Tidak Ada Gangguan"
        else:
            input_data = pd.DataFrame([user_answers])
            if model_dt is not None:
                prediction = model_dt.predict(input_data)[0]
            else:
                prediction = "Model belum siap / tidak ditemukan"
        # -------------------------------------------------------------------
        
        db_fields = {
            'user': request.user,
            'predicted_disorder': str(prediction),
            'age_group': user_answers.get('ag+1:629e', 1),
            'feeling_nervous': user_answers.get('feeling.nervous', 0),
            'panic': user_answers.get('panic', 0),
            'breathing_rapidly': user_answers.get('breathing.rapidly', 0),
            'sweating': user_answers.get('sweating', 0),
            'trouble_in_concentration': user_answers.get('trouble.in.concentration', 0),
            'having_trouble_in_sleeping': user_answers.get('having.trouble.in.sleeping', 0),
            'having_trouble_with_work': user_answers.get('having.trouble.with.work', 0),
            'hopelessness': user_answers.get('hopelessness', 0),
            'anger': user_answers.get('anger', 0),
            'over_react': user_answers.get('over.react', 0),
            'change_in_eating': user_answers.get('change.in.eating', 0),
            'suicidal_thought': user_answers.get('suicidal.thought', 0),
            'feeling_tired': user_answers.get('feeling.tired', 0),
            'close_friend': user_answers.get('close.friend', 0),
            'social_media_addiction': user_answers.get('social.media.addiction', 0),
            'weight_gain': user_answers.get('weight.gain', 0),
            'introvert': user_answers.get('introvert', 0),
            'popping_up_stressful_memory': user_answers.get('popping.up.stressful.memory', 0),
            'having_nightmares': user_answers.get('having.nightmares', 0),
            'avoids_people_or_activities': user_answers.get('avoids.people.or.activities', 0),
            'feeling_negative': user_answers.get('feeling.negative', 0),
            'trouble_concentrating': user_answers.get('trouble.concentrating', 0),
            'blamming_yourself': user_answers.get('blamming.yourself', 0),
            'hallucinations': user_answers.get('hallucinations', 0),
            'repetitive_behaviour': user_answers.get('repetitive.behaviour', 0),
            'increased_energy': user_answers.get('increased.energy', 0),
        }

        # Simpan hasil tes ke Database
        MentalHealthTest.objects.create(**db_fields)
        
        messages.success(request, "Tes berhasil diselesaikan!")
        
        # Dialihkan ke route riwayat (sesuai nama 'name' pada urls.py)
        return redirect('riwayat')

    return redirect('deteksi')


# Riwayat view
@login_required(login_url='login')
def riwayat_view(request):
    user_history = MentalHealthTest.objects.filter(user=request.user).order_by('-created_at')
    
    latest_test = user_history.first() if user_history.exists() else None
    previous_tests = list(user_history[1:]) if user_history.count() > 1 else []

    return render(request, 'riwayat.html', {
        'latest_test': latest_test,
        'previous_tests': previous_tests,
        'total_tests': user_history.count(),
    })


# View untuk Menampilkan Daftar Semua Artikel
def artikel(request):
    semua_artikel = Artikel.objects.all().order_by('-tanggal_dibuat') 
    
    context = {
        'artikel_list': semua_artikel
    }
    return render(request, 'artikel.html', context)

def detail_artikel(request, id):
    detail = get_object_or_404(Artikel, id=id)
    return render(request, 'artikel_detail.html', {'artikel': detail})


# ARTIKEL
def artikel(request):
    query = request.GET.get('q', '')
    kategori_selected = request.GET.get('kategori', '')

    # Ambil semua data artikel
    artikel_list = Artikel.objects.all().order_by('-tanggal_dibuat')

    # Filter berdasarkan pencarian kata kunci
    if query:
        artikel_list = artikel_list.filter(
            Q(judul__icontains=query) | Q(ringkasan__icontains=query)
        )

    # Filter berdasarkan kategori
    if kategori_selected:
        artikel_list = artikel_list.filter(kategori__iexact=kategori_selected)

    # Ambil daftar kategori unik untuk dropdown filter
    kategori_list = Artikel.objects.values_list('kategori', flat=True).distinct()

    # Pagination: Limit 6 item per halaman (Grid 3x2)
    paginator = Paginator(artikel_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'kategori_list': kategori_list,
        'query': query,
        'kategori_selected': kategori_selected,
    }
    return render(request, 'artikel.html', context)


# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah keluar.")
    return redirect('home')