Kuş Arama ve Değerlendirme Sistemi

Bu Python kodu, Excel veri setlerinden kuş türleri ve onların gözlem verileriyle ilgili bilgileri alıp, kullanıcının belirttiği habitat, diyet, tarih ve konum gibi kriterlere dayalı olarak kuş türlerini değerlendiren bir sistem sunar. Kod, çeşitli skorlar hesaplayarak öncelikli kuş türlerini listeler.


Kullanılan Kütüphaneler

pandas: Veri işlemleri ve analizleri.

numpy: Matematiksel hesaplamalar.

datetime: Tarih işlemleri.

geopy.distance: Konumlar arası mesafe hesaplama.


Kodun Amacı

Bu kod, kuş gözlemcileri, araştırmacılar veya kuş türlerine ilgi duyan bireylerin belirli kriterlere göre türleri değerlendirmelerine yardımcı olmayı amaçlar. Kullanıcı, belirli bir bölgedeki gözlemlerine uygun kuş türlerini, habitat ve diyet tercihlerinden tarih ve konum bilgisine kadar geniş bir yelpazede kriterlerle filtreleyebilir.

Kod, verilen Excel dosyalarından elde edilen verilerle kullanıcı girişlerini eşleştirir ve bu verileri analiz ederek her tür için skorlar oluşturur. Bu skorlar, türlerin kullanıcı ihtiyaçlarına uygunluğunu yansıtır. Skorlar, farklı faktörlerin birleştirilmesiyle hesaplanır ve türler, toplam uygunluk puanlarına göre sıralanır.

Sonuçta kullanıcı, gözlemleyip tanımlayamadığı türleri kolayca belirleyebilir ve zamandan tasarruf edebilir. Bu sistem, özellikle doğa meraklıları ve doğa bilimciler için pratik bir çözüm sunar.


Kriterler ve Skor Hesaplama

Habitat ve Diyet Skorları: Kullanıcı seçimlerine göre, türlerin özelliklerine uygunluk oranıyla normalize edilmiş skorlar hesaplanır.

Ağırlık Skoru: Belirtilen ağırlık kategorisine uygun türler tam puan alır; daha az uygun türler düşük puan alır.

Tarih Skoru: Kullanıcının gözlem tarihi ile türlerin veritabanındaki tarihler eşleşirse tam puan alır.

Konum Skoru: Kullanıcının verdiği enlem-boylam konumuna uzaklığa göre:

3 km içinde: 1 puan

5 km içinde: 0.5 puan

10 km içinde: 0.3 puan

10 km dışında: 0 puan

Skor Hesaplaması

Combined Score 1: Habitat, diyet ve ağırlık skorları birleştirilir.

(1/3 * Weight_score) + (1/4 * Habitat_score) + (2/12 * Diet_score)

Combined Score 2: Tarih ve konum skorları birleştirilir.

(2/12 * Date_score) + (1/12 * Location_score)

Nihai Skor: Combined Score 1 ve Combined Score 2 toplamıdır. Türler, bu skora göre sıralanır.

Girdiler ve Çıktılar

Girdiler: Habitat, diyet, ağırlık kategorisi, tarih ve konum bilgileri.

Çıktılar: Nihai skora göre sıralanmış en uygun kuş türleri listesi.

Dosya Yapısı

kus_turleri_5.xlsx: Habitat ve diyet verilerini içerir.

ankaraall5.xlsx: Türlerin gözlem tarihi ve konum bilgilerini içerir.




