from django.contrib import admin
from .models import MentalHealthTest
from .models import Artikel


@admin.register(MentalHealthTest)
class MentalHealthTestAdmin(admin.ModelAdmin):
    # Kolom yang akan ditampilkan pada daftar di dashboard Django Admin
    list_display = ('id', 'get_username', 'predicted_disorder', 'age_group', 'created_at')
    
    # Fitur filter di sebelah kanan
    list_filter = ('predicted_disorder', 'age_group', 'created_at')
    
    # Fitur pencarian berdasarkan username atau hasil diagnosa
    search_fields = ('user__username', 'predicted_disorder')
    
    # Urutan tampilan (dari yang terbaru)
    ordering = ('-created_at',)

    # Helper method untuk menampilkan username (atau Guest jika tidak login)
    def get_username(self, obj):
        return obj.user.username if obj.user else "Guest (Tanpa Akun)"
    get_username.short_description = 'Pengguna'


# ARTIKEL
admin.site.register(Artikel)