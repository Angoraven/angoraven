import pandas as pd
import os
import numpy as np
from datetime import datetime
from geopy.distance import geodesic


# Çalışma dizinindeki dosya adlarını belirt
filename = "kus_turleri_5.xlsx"
file_path = "ankaraall5.xlsx"

# Mevcut çalışma dizinine göre tam yolları oluştur
current_dir = os.getcwd()  # Kodun çalıştırıldığı klasör
full_filename_path = os.path.join(current_dir, filename)
full_file_path = os.path.join(current_dir, file_path)

# Excel dosyalarını oku
df = pd.read_excel(full_filename_path)
data = pd.read_excel(full_file_path)


# Habitat ve diyet sütunlarını belirleyin
habitat_cols = df.columns[4:18]  # Habitat sütunları
diyet_cols = df.columns[21:]  # Diyet sütunları
habitat_options = {str(i + 1): habitat for i, habitat in enumerate(habitat_cols)}
diyet_options = {str(i + 1): diyet for i, diyet in enumerate(diyet_cols)}

# Kullanıcıya seçenekleri gösteren yardımcı fonksiyonlar
def show_options(options_dict):
    for key, value in options_dict.items():
        print(f"{key}: {value}")

def get_selections(options_dict, option_type):
    print(f"\n{option_type} seçeneklerinden istediğiniz numaraları virgülle ayırarak seçin:")
    show_options(options_dict)
    selections = input("Seçimlerinizi girin (örnek: 1,3): ").split(',')
    return [options_dict[sel.strip()] for sel in selections if sel.strip() in options_dict]

# Ağırlık skorunu hesaplayan fonksiyon
def calculate_weight_score(weight, selected_agi, weight_limits):
    if selected_agi:
        selected_min, selected_max = weight_limits[selected_agi]

        # Tam eşleşen türler için 1 puan
        if selected_min <= weight <= selected_max:
            return 1.0

        # Bir alt ve bir üst kategorideki türler için 0.5 puan
        if selected_agi > 1 and weight < selected_min:
            lower_min, lower_max = weight_limits[selected_agi - 1]
            if lower_min <= weight <= lower_max:
                return 0.5
        if selected_agi < 7 and weight > selected_max:
            upper_min, upper_max = weight_limits[selected_agi + 1]
            if upper_min <= weight <= upper_max:
                return 0.5

        # İki alt ve iki üst kategorideki türler için -1 puan
        if selected_agi > 2 and weight < weight_limits[selected_agi - 2][0]:
            return -1
        if selected_agi < 6 and weight > weight_limits[selected_agi + 2][1]:
            return -1

        # Daha uzak kategoriler için -2 puan
        return -1
    return 0.0

def kus_arama():
    # Kullanıcıdan habitat ve diyet seçimleri al
    selected_habitats = get_selections(habitat_options, "Habitat")
    selected_diets = get_selections(diyet_options, "Diyet")

    # Kullanıcıdan ağırlık seçimi al
    agi_dict = {
        "1": "Serçe Boyutunda Veya Daha Küçük",
        "2": "Serçe ile Karatavuk Arasında",
        "3": "Karatavuk Boyutlarında",
        "4": "Karatavuk ile Karga Arasında",
        "5": "Karga Boyutunda",
        "6": "Karga ile Kaz Arasında",
        "7": "Kaz Boyutunda Veya Daha Büyük"
    }
    print("\nKuş ne büyüklükte? Seçenekler:")
    show_options(agi_dict)
    selected_agi = input("Seçiminizi girin (örnek: 1, 2) veya boş bırakın: ")
    selected_agi = int(selected_agi) if selected_agi.isdigit() else None

    # Ağırlık limitleri
    weight_limits = {
        1: (0, 30), 2: (31, 70), 3: (71, 108),
        4: (109, 455), 5: (456, 636), 6: (637, 3000), 7: (3001, float('inf'))
    }

    # Ağırlık skorunu hesapla
    df['Weight_score'] = df['Weight'].apply(lambda w: calculate_weight_score(w, selected_agi, weight_limits))

    # Habitat ve diyet skorlarını hesapla
    df['habitat_normalized'] = df[selected_habitats].sum(axis=1) / len(selected_habitats) if selected_habitats else 0
    df['diyet_normalized'] = df[selected_diets].sum(axis=1) / len(selected_diets) if selected_diets else 0

    # Kombine skoru hesapla
    df['combined_score_1'] = (
        (1 / 3) * df['Weight_score'] +
        (1 / 4) * df['habitat_normalized'] +
        (2 / 12) * df['diyet_normalized']
    )

    # Sonuçları sırala ve ilk 50 türü seç
    results = df.sort_values(by='combined_score_1', ascending=False).head(50)

    return results[['Species', 'combined_score_1']]

# Çıktıyı veri seti (DataFrame) olarak almak için çalıştırma
pd.set_option('display.max_columns', None)


# Tarih verisini kontrol et ve dönüştür
if data["date"].dtype != "datetime64[ns]":
    try:
        data["date"] = pd.to_datetime(data["date"], origin='1900-01-01', unit='D')
    except Exception as e:
        print(f"Tarih formatında hata: {e}")


# Kullanıcıdan giriş al
user_date = input("Gözlem tarihi girin (YYYY-MM-DD): ")

user_input = input("Enlem ve Boylam girin (ör. 38.2735210, 32.5035560): ")

# Girdiyi virgüle göre parçala
try:
    user_lat, user_lon = map(float, user_input.split(","))
except ValueError:
    print("Geçersiz giriş! Enlem ve boylamı doğru formatta girin (ör. 38.2735210, 32.5035560).")
    exit()
user_location = (user_lat, user_lon)


# Haversine fonksiyonu (iki koordinat arasındaki mesafeyi hesaplar)
def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # Dünya yarıçapı (km)
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return r * c


# Konum skorunu hesaplayan fonksiyon
def calculate_location_score(lat, lon, user_lat, user_lon):
    # Mesafeyi hesapla
    distance = haversine(lat, lon, user_lat, user_lon)

    # Mesafeye göre skor ata
    if distance <= 3:
        return 1.0  # 3 km içinde tam puan
    elif 1 < distance <= 5:
        return 0.5  # 3-5 km arasında 0.5 puan
    elif 5 < distance <= 10:
        return 0.3  # 5-10 km arasında 0.3 puan
    else:
        return 0.0  # 10 km dışında sıfır puan


# Tarih verisi işlemleri
user_date = pd.to_datetime(user_date)

# Skorları hesapla
date_scores = []
location_scores = []
for _, row in data.iterrows():
    # Tarih skoru hesapla
    date_score = 1.0 if row["date"].month == user_date.month else 0.0
    date_scores.append(date_score)

    # Konum skoru hesapla
    location_score = calculate_location_score(row["lat"], row["lon"], user_lat, user_lon)
    location_scores.append(location_score)

# Skorları veri çerçevesine ekle
data["date_score"] = date_scores
data["location_score"] = location_scores

# Kullanıcının belirttiği ay
user_month = user_date.month

# Belirtilen ayda her türün gözlem sayısını hesapla
data["month"] = data["date"].dt.month  # Ay sütununu ekle
species_observation_counts = (
    data[data["month"] == user_month]  # Sadece kullanıcı ayındaki gözlemleri al
    .groupby("Species")  # Türlere göre gruplandır
    .size()  # Her tür için gözlem sayısını hesapla
    .reset_index(name="observation_count")  # Yeni bir sütun olarak ekle
)

# Orijinal veri çerçevesine gözlem sayılarını ekle
data = pd.merge(data, species_observation_counts, on="Species", how="left")
data["observation_count"] = data["observation_count"].fillna(0)  # NaN olanları 0 yap

# Tarih ve konum skorlarını topla
data["combined_score_2"] = data["date_score"]*2/12 + data["location_score"]*1/12

# Türleri sıralama: önce toplam skora, sonra gözlem sayısına göre
top_species = data.sort_values(
    by=["combined_score_2", "observation_count"],  # Toplam skor ve gözlem sayısını kullanıyoruz
    ascending=[False, False]  # Büyükten küçüğe sıralama
)

# Benzersiz türleri al, sadece ilk görünen türü alacak şekilde
top_species_unique = top_species.drop_duplicates(subset="Species", keep="first")


# Sonuçları DataFrame olarak almak için
output_df_2 = top_species_unique[["Species", "combined_score_2"]].head(50)
output_df_1 = kus_arama()

# Her iki DataFrame'deki tüm türleri birleştir (outer join)
merged_df = pd.merge(output_df_1, output_df_2, on="Species", how="outer")

# Eksik değerleri 0 ile doldur
merged_df['combined_score_1'] = merged_df['combined_score_1'].fillna(0)
merged_df['combined_score_2'] = merged_df['combined_score_2'].fillna(0)

merged_df['combined_score'] = merged_df['combined_score_1'] + merged_df['combined_score_2']

merged_df = merged_df.sort_values(by='combined_score', ascending=False)

final_df = merged_df[['Species', 'combined_score']].head(10)

print(final_df)