# FaceVision Tracker

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Haar%20Cascade-green)
![Status](https://img.shields.io/badge/Status-Public%20Project-brightgreen)
![License](https://img.shields.io/badge/License-GPLv3-orange)

**FaceVision Tracker**, Python ve OpenCV kullanılarak geliştirilmiş gerçek zamanlı yüz ve göz algılama uygulamasıdır. Proje; webcam veya video dosyası üzerinden görüntü alır, yüzleri ve gözleri Haar Cascade modeliyle tespit eder, ekranda işaretler ve kullanıcıya FPS, tespit sayısı, ekran görüntüsü alma gibi gelişmiş özellikler sunar.

## Özellikler

- Gerçek zamanlı yüz algılama
- Yüz bölgesi içinde göz algılama
- FPS göstergesi
- Algılanan yüz ve göz sayısı göstergesi
- Ekran görüntüsü kaydetme
- Göz algılamayı çalışma sırasında açma/kapatma
- Ayna modunu çalışma sırasında açma/kapatma
- Komut satırı parametreleriyle kamera, çözünürlük ve algılama ayarlarını değiştirme
- Webcam veya video dosyası üzerinden çalışma
- Hata kontrolü ve düzenli proje yapısı

## Proje Yapısı

```text
facevision-tracker/
├── cascades/
│   ├── haarcascade_eye.xml
│   └── haarcascade_frontalface_default.xml
├── output/
│   └── .gitkeep
├── main.py
├── requirements.txt
├── CHANGELOG.md
├── README.md
├── LICENSE
└── .gitignore
```

## Kurulum

Projeyi GitHub üzerinden klonladıktan sonra terminali proje klasöründe açın.

```bash
git clone https://github.com/kullanici-adin/facevision-tracker.git
cd facevision-tracker
```

Sanal ortam oluşturun:

```bash
python -m venv .venv
```

Windows için sanal ortamı aktif edin:

```bash
.venv\\Scripts\\activate
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Kullanım

Varsayılan kamera ile çalıştırmak için:

```bash
python main.py
```

Farklı kamera seçmek için:

```bash
python main.py --camera 1
```

Çözünürlük belirlemek için:

```bash
python main.py --width 1280 --height 720
```

Video dosyası üzerinden çalıştırmak için:

```bash
python main.py --source video.mp4
```

Göz algılamayı kapalı başlatmak için:

```bash
python main.py --no-eyes
```

Ayna modunu kapalı başlatmak için:

```bash
python main.py --no-mirror
```

## Klavye Kısayolları

| Tuş | İşlem |
| --- | --- |
| `q` veya `ESC` | Programdan çıkış |
| `s` | Ekran görüntüsü kaydetme |
| `e` | Göz algılamayı aç/kapat |
| `m` | Ayna modunu aç/kapat |

## Teknik Açıklama

Uygulama, OpenCV'nin `CascadeClassifier` sınıfını kullanır. Görüntü önce gri tona çevrilir ve histogram eşitleme uygulanır. Daha sonra yüz algılama yapılır. Yüz tespit edilen alanlarda ayrıca göz algılama çalıştırılır. Bu yaklaşım düşük donanımlarda bile hızlı sonuç verdiği için temel görüntü işleme projelerinde yaygın olarak kullanılır.

## Gereksinimler

- Python 3.10 veya üzeri
- OpenCV
- NumPy
- Webcam veya video dosyası

## Ekran Görüntüleri

Program çalışırken `s` tuşuna basıldığında ekran görüntüleri otomatik olarak `output/` klasörüne kaydedilir.

## Notlar

- Webcam açılmıyorsa kamera izinlerini kontrol edin.
- Laptoplarda genellikle varsayılan kamera `--camera 0` olur.
- Harici kamera kullanıyorsanız `--camera 1` veya `--camera 2` deneyebilirsiniz.
- Kaydedilen ekran görüntüleri `output/` klasöründe tutulur.

## Lisans

Bu proje GPLv3 lisansı ile açık kaynak olarak paylaşılmıştır. Haar Cascade XML dosyaları OpenCV/Intel lisans açıklamalarını kendi içlerinde barındırır.
