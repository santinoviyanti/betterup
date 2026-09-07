import os
import django

# Set environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistempakar.settings')
django.setup()

# Import models
from diagnosis.models import Penyakit, Gejala, Bobot

# Menambahkan Penyakit dan Gejala

# Penyakit Insecure
insecure = Penyakit.objects.create(nama="Insecure")

gejala1 = Gejala.objects.create(penyakit=insecure, nama="Menyalahkan diri sendiri", nilai_cf=0.30)
gejala2 = Gejala.objects.create(penyakit=insecure, nama="Sulit mempercayai orang lain", nilai_cf=0.20)
gejala3 = Gejala.objects.create(penyakit=insecure, nama="Ragu untuk melakukan sesuatu", nilai_cf=0.45)
gejala4 = Gejala.objects.create(penyakit=insecure, nama="Sering membandingkan diri sendiri dengan orang lain", nilai_cf=0.50)
gejala5 = Gejala.objects.create(penyakit=insecure, nama="Negative thinking", nilai_cf=0.20)

# Penyakit Fobia Sosial
fobia_sosial = Penyakit.objects.create(nama="Fobia Sosial (Anti Sosial)")

gejala6 = Gejala.objects.create(penyakit=fobia_sosial, nama="Gangguan berinteraksi dengan orang lain", nilai_cf=0.40)
gejala7 = Gejala.objects.create(penyakit=fobia_sosial, nama="Bicara dengan suara pelan", nilai_cf=0.30)
gejala8 = Gejala.objects.create(penyakit=fobia_sosial, nama="Keringat berlebih", nilai_cf=0.20)
gejala9 = Gejala.objects.create(penyakit=fobia_sosial, nama="Tidak suka keramaian", nilai_cf=0.65)

# Penyakit Skizofernia
skizofernia = Penyakit.objects.create(nama="Skizofernia")

gejala10 = Gejala.objects.create(penyakit=skizofernia, nama="Punya khayalan/halusinasi yang tidak biasa", nilai_cf=0.20)
gejala11 = Gejala.objects.create(penyakit=skizofernia, nama="Bebicara melantur dan tidak sesuai topik", nilai_cf=0.40)
gejala12 = Gejala.objects.create(penyakit=skizofernia, nama="Delusi (Keyakinan atau kenyataan semu yang diyakini terus menerus meskipun bukti atau kesepakatan berlawanan)", nilai_cf=0.40)
gejala13 = Gejala.objects.create(penyakit=skizofernia, nama="Gelisah", nilai_cf=0.20)

# Penyakit Bipolar
bipolar = Penyakit.objects.create(nama="Bipolar")

gejala14 = Gejala.objects.create(penyakit=bipolar, nama="Detak jantung tidak normal", nilai_cf=0.20)
gejala15 = Gejala.objects.create(penyakit=bipolar, nama="Mudah teralihkan", nilai_cf=0.30)
gejala16 = Gejala.objects.create(penyakit=bipolar, nama="Mudah tersinggung", nilai_cf=0.40)
gejala17 = Gejala.objects.create(penyakit=bipolar, nama="Punya khayalan/halusinasi yang tidak biasa", nilai_cf=0.50)

# Penyakit PTSD
ptsd = Penyakit.objects.create(nama="Gangguan Stres Pasca-trauma (PTSD)")

gejala18 = Gejala.objects.create(penyakit=ptsd, nama="Negative thinking", nilai_cf=0.30)
gejala19 = Gejala.objects.create(penyakit=ptsd, nama="Suka mengelak", nilai_cf=0.30)
gejala20 = Gejala.objects.create(penyakit=ptsd, nama="Timbul ingatan pada peristiwa traumatis", nilai_cf=0.50)

# Penyakit Gangguan Psikosis
psikosis = Penyakit.objects.create(nama="Gangguan Psikosis")

gejala21 = Gejala.objects.create(penyakit=psikosis, nama="Gangguan tidur", nilai_cf=0.20)
gejala22 = Gejala.objects.create(penyakit=psikosis, nama="Berbicara melantur dan tidak sesuai topik", nilai_cf=0.50)
gejala23 = Gejala.objects.create(penyakit=psikosis, nama="Gangguan berinteraksi dengan orang lain", nilai_cf=0.30)
gejala24 = Gejala.objects.create(penyakit=psikosis, nama="Sulit berkonsentrasi", nilai_cf=0.40)

# Menambahkan Bobot untuk Penyakit dan Gejala
Bobot.objects.create(penyakit=insecure, gejala=gejala1, bobot=0.30)
Bobot.objects.create(penyakit=insecure, gejala=gejala2, bobot=0.20)
Bobot.objects.create(penyakit=insecure, gejala=gejala3, bobot=0.45)
Bobot.objects.create(penyakit=insecure, gejala=gejala4, bobot=0.50)
Bobot.objects.create(penyakit=insecure, gejala=gejala5, bobot=0.20)

Bobot.objects.create(penyakit=fobia_sosial, gejala=gejala6, bobot=0.40)
Bobot.objects.create(penyakit=fobia_sosial, gejala=gejala7, bobot=0.30)
Bobot.objects.create(penyakit=fobia_sosial, gejala=gejala8, bobot=0.20)
Bobot.objects.create(penyakit=fobia_sosial, gejala=gejala9, bobot=0.65)

Bobot.objects.create(penyakit=skizofernia, gejala=gejala10, bobot=0.20)
Bobot.objects.create(penyakit=skizofernia, gejala=gejala11, bobot=0.40)
Bobot.objects.create(penyakit=skizofernia, gejala=gejala12, bobot=0.40)
Bobot.objects.create(penyakit=skizofernia, gejala=gejala13, bobot=0.20)

Bobot.objects.create(penyakit=bipolar, gejala=gejala14, bobot=0.20)
Bobot.objects.create(penyakit=bipolar, gejala=gejala15, bobot=0.30)
Bobot.objects.create(penyakit=bipolar, gejala=gejala16, bobot=0.40)
Bobot.objects.create(penyakit=bipolar, gejala=gejala17, bobot=0.50)

Bobot.objects.create(penyakit=ptsd, gejala=gejala18, bobot=0.30)
Bobot.objects.create(penyakit=ptsd, gejala=gejala19, bobot=0.30)
Bobot.objects.create(penyakit=ptsd, gejala=gejala20, bobot=0.50)

Bobot.objects.create(penyakit=psikosis, gejala=gejala21, bobot=0.20)
Bobot.objects.create(penyakit=psikosis, gejala=gejala22, bobot=0.50)
Bobot.objects.create(penyakit=psikosis, gejala=gejala23, bobot=0.30)
Bobot.objects.create(penyakit=psikosis, gejala=gejala24, bobot=0.40)

print("Data successfully added!")
