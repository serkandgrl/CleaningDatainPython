#Cleaning Data in Python

#Import libraries
import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

#Görev 1: Verileri Yükleme ve İnceleme
#Yapacağımız ilk şey ham işitsel verileri yüklemek.

df = pd.read_csv("audible_uncleaned.csv")

def check_df(dataframe, head = 5):
    print("-----------------------Shape-----------------------")
    print(dataframe.shape)
    print("-----------------------Dtypes-----------------------")
    print(dataframe.dtypes)
    print("-----------------------Head-----------------------")
    print(dataframe.head(head))
    print("-----------------------Tail-----------------------")
    print(dataframe.tail(head))
    print("-----------------------NA-----------------------")
    print(dataframe.isnull().sum())
    print("-----------------------Quantiles-----------------------")
    print(dataframe.describe())

check_df(df)

#'ad' - Sesli kitabın adı.
#'yazar' - Sesli kitabın yazarı.
#'anlatıcı' - Sesli kitabın anlatıcısı.
#'time' - Saat ve dakika cinsinden sesli kitabın süresi.
#'releasedate' - Sesli kitabın yayınlandığı tarih.
#'dil' - Sesli kitabın dili.
#'yıldız' - Ortalama yıldız sayısı (5 üzerinden) ve derecelendirme sayısı (varsa).
#-'fiyat' - Sesli kitabın INR (Hint Rupisi) cinsinden fiyatı.

#Görev 2: Yazar ve Anlatıcı sütunlarındaki metin verilerini temizleme
#Yazar ve anlatıcı gibi bazı metin sütunlarını temizlemeye başlayacağız. Bu sütunlardaki metnin Yazan: ve Anlatan: bölümlerini kaldırabiliriz.
#Yazar sütunundan 'Writtenby:' öğesini kaldırın
#Anlatıcı sütunundan 'Narratedby:' ifadesini kaldırın
#sonuçları kontrol et

df["author"] = df["author"].str.replace("Writtenby:", "")
df["narrator"] = df["narrator"].str.replace("Narratedby:", "")

df[["author", "narrator"]]

#Görev 3: Yıldızların sayısını ve derecelendirmeleri Yıldızlar sütunundan çıkarın.
#Yıldızlar sütunu, yıldız sayısını ve puan sayısını birleştirir. Bunu sayılara çevirelim ve iki sütuna ayıralım: rating_stars ve n_ratings.

df["stars"].sample(n = 10)

df[df["stars"] != "Not rated yet"]["stars"].sample(n = 10)

#'Not rated yet' ifadesini NaN ile değiştirin
df["stars"].replace("Not rated yet", np.nan, inplace = True)

#Yıldız sayısını rating_stars'a çıkarın ve float'a dönüştürün
df["rating_stars"] = df["stars"].str.extract("^([\d.]+)").astype(float)

#Virgülü değiştirin, derecelendirme sayısını n_ratings'e çıkarın ve float'a çevirin
df["n_ratings"] = df["stars"].str.replace(",", "").str.extract("(\d+) rating").astype(float)

df[["rating_stars", "n_ratings"]]

df.drop(columns = ["stars"], axis = 1, inplace = True)

#Görev 4: Veri türlerini değiştirin
#Bir diğer önemli adım ise verilerimizin doğru veri tiplerinde olması.
#Fiyatı float ayarla
#Rating_stars'ı kategoriye çevir
#Yayın tarihini tarih saatine dönüştür

df["price"] = df["price"].str.replace(",", "")

df["price"] = df["price"].str.replace("Free", "0")

df["price"] = df["price"].astype(float)

df["rating_stars"].unique()

df["rating_stars"] = df["rating_stars"].astype("category")

df["releasedate"] = pd.to_datetime(df["releasedate"]);

df.info()

#Görev 5: Zaman sütunundan saatleri ve dakikaları çıkarın
#Zaman sütunu, saat ve dakika sayısını tek bir sütunda birleştirir. Bilgileri yeni bir time_ minutes sütununa dönüştürmek ve birleştirmek istiyoruz.

df["time"].sample(n = 10)

df["time"][df["time"].str.contains("minute")].sample(n = 10)

df["time"] = df["time"].str.replace("hrs", "hr")
df["time"] = df["time"].str.replace("mins", "min")
df["time"] = df["time"].str.replace("Less than 1 minute", "1 min")

df["time"]

hours = df["time"].str.extract("(\d+) hr").fillna(0).astype(int)
mins = df["time"].str.extract("(\d+) min").fillna(0).astype(int)

df["time_mins"] = hours * 60 + mins

df[["time_mins"]]

df.drop(columns = ["time"], axis = 1, inplace = True)
df.head()
df.info()

#Görev 6: Veri aralıklarını kontrol edin
#Bir diğer önemli adım ise sütunlarımızdaki değerlerin beklenen aralıklarda olduğunu ve aralık dışı değerlere sahip olmadığımızı doğrulamaktır.
#Ht aralıklarını ve dağılımın şeklini görsel olarak incelemek için sayısal sütunların bir histogramını oluşturalım:

df.hist(figsize = (10, 10), bins = 100)

df.describe().T
df.describe(exclude = [np.number]).T

#Bu alıştırma için fiyatları USD'ye çevireceğiz. 1 USD = 0,012 INR döviz kurunu kullanabiliriz
df["price"] = df["price"] * 0.012

df["price"].describe()

df["language"].unique()

#Dil sütunundaki değerler farklı büyük harf kullanımına sahiptir. Bunu düzeltelim.
df["language"] = df["language"].str.capitalize()

df["language"].unique()

#Görev 7: Kopyaları kontrol etme
#Kaç kopyamız var?

df.duplicated().sum()

#Yalnızca mantıklı olan sütunların bir alt kümesini kullanarak kopyaları aramak yararlıdır. Aşağıdaki sütun alt kümesini kullanacağız:
#name, author, narrator, time_mins, price

subset_cols = ["name", "author", "narrator", "time_mins", "price"]

df.duplicated(subset = subset_cols).sum()

#Şimdi bu değerlere bakalım (keep=false kullanın) ve neler olup bittiğini görelim:
df[df.duplicated(subset = subset_cols, keep = False)].sort_values(by = "name")

#Kopyaların farklı sürüm tarihlerine sahip dosyalar için olduğunu görebiliriz. Son çıkış tarihi ile kaydı tutmaya karar verebiliriz.
df.drop_duplicates(subset = subset_cols, keep = "last", inplace = True)

df.duplicated(subset = subset_cols).sum()

#Görev 8: Eksik verilerle ilgilenme
#Bitirmeden önce sütunlarımızdaki eksik verilere bir göz atalım

df.isna().sum()

#NaN değerlerini 0 veya başka bir sayısal değere çevirebilir veya tutabiliriz. Kullanım durumumuza bağlıdır.
#Derecelendirme dağılımını çizmek istiyorsak, derecelendirmesi olmayan sesli kitapları bırakmak mantıklı olabilir. Ancak analizimiz için fiyat dağılımını kullanmamız gerekirse, derecelendirmesiz sesli kitapların kaldırılması sonuçlarımıza yanlılık katacaktır (çünkü derecelendirilmemiş sesli kitaplar muhtemelen daha niştir ve derecelendirilmiş sesli kitaplardan farklı bir fiyatlandırma yapısına sahip olabilir).
#Derecelendirilmemiş sesli kitapları şimdilik elimizde tutacağız.

#Görev 9: Temizlenen veri setini kaydedin
#Temiz dosyayı kaydetmek için .to_csv yöntemini kullanabiliriz. Geçerli dizini hedef dosyamıza da kopyalamamak için index=False öğesini ekleriz.

df.to_csv("audible_cleaned.csv", index = False)
