import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# 1. Baca File Excel
df = pd.read_excel('betterup_dataset.xlsx')

# 2. Encode kolom teks (misal usia 'ag+1:629e') menjadi angka jika digunakan
le_age = LabelEncoder()
df['ag+1:629e'] = le_age.fit_transform(df['ag+1:629e'])

# 3. Memisahkan Fitur (X) dan Target/Disorder (Y)
X = df.drop(columns=['Disorder'])
Y = df['Disorder']

# 4. Melatih Model Decision Tree
clf = DecisionTreeClassifier(criterion='entropy', max_depth=10, random_state=42)
clf.fit(X, Y)

# 5. Simpan Model & Encoder ke File
joblib.dump(clf, 'model_disorder_dt.pkl')
joblib.dump(le_age, 'label_encoder_age.pkl')
print("Model Decision Tree berhasil dilatih dan disimpan dari Dataset Excel!")