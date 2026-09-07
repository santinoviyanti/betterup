from django.db import models
from django.contrib.auth.models import User

# DETEKSI DINI
class MentalHealthTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    predicted_disorder = models.CharField(max_length=100)
    
    # 4 Kelompok Usia di Database
    AGE_CHOICES = [
        (0, 'Anak-anak (0 - 11 tahun)'),
        (1, 'Remaja (12 - 18 tahun)'),
        (2, 'Dewasa Muda (19 - 25 tahun)'),
        (3, 'Dewasa (> 25 tahun)'),
    ]
    age_group = models.IntegerField(choices=AGE_CHOICES)

    # 26 Pertanyaan Gejala ( Nilai 0 atau 1 )
    feeling_nervous = models.IntegerField(default=0)
    panic = models.IntegerField(default=0)
    breathing_rapidly = models.IntegerField(default=0)
    sweating = models.IntegerField(default=0)
    trouble_in_concentration = models.IntegerField(default=0)
    having_trouble_in_sleeping = models.IntegerField(default=0)
    having_trouble_with_work = models.IntegerField(default=0)
    hopelessness = models.IntegerField(default=0)
    anger = models.IntegerField(default=0)
    over_react = models.IntegerField(default=0)
    change_in_eating = models.IntegerField(default=0)
    suicidal_thought = models.IntegerField(default=0)
    feeling_tired = models.IntegerField(default=0)
    close_friend = models.IntegerField(default=0)
    social_media_addiction = models.IntegerField(default=0)
    weight_gain = models.IntegerField(default=0)
    introvert = models.IntegerField(default=0)
    popping_up_stressful_memory = models.IntegerField(default=0)
    having_nightmares = models.IntegerField(default=0)
    avoids_people_or_activities = models.IntegerField(default=0)
    feeling_negative = models.IntegerField(default=0)
    trouble_concentrating = models.IntegerField(default=0)
    blamming_yourself = models.IntegerField(default=0)
    hallucinations = models.IntegerField(default=0)
    repetitive_behaviour = models.IntegerField(default=0)
    increased_energy = models.IntegerField(default=0)

    # Property penolong untuk mengambil teks label berdasarkan angka age_group
    @property
    def age_group_label(self):
        age_dict = dict(self.AGE_CHOICES)
        return age_dict.get(self.age_group, '-')

    def __str__(self):
        user_str = self.user.username if self.user else "Guest"
        return f"Diagnosa {user_str} - {self.predicted_disorder}"

# ARTIKEL
class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    kategori = models.CharField(max_length=50, default="Kesehatan Mental") #
    ringkasan = models.TextField(help_text="Deskripsi singkat yang tampil di kartu artikel")
    konten = models.TextField(help_text="Isi lengkap artikel")
    gambar = models.ImageField(upload_to='artikel/', blank=True, null=True) 
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul