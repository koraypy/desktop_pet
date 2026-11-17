# 🐈‍⬛ Desktop Pet

Ekranınızın altında dolaşan küçük, neon çizgili siyah bir kedi.
Yürür, durur, uyur; her zaman üstte kalır ve **tıklamalarınızı engellemez**.

## Kurulum

Python 3.9+ gerekir.

```bash
git clone https://github.com/koraypy/desktop-pet.git
cd desktop-pet
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım

```bash
python -m desktop_pet --scale 1.5 --speed 3
```

| Seçenek   | Varsayılan | Açıklama                     |
|-----------|------------|------------------------------|
| `--scale` | `1.0`      | Boyut çarpanı                |
| `--speed` | `2.0`      | Yürüme hızı                  |
| `--fps`   | `30`       | Saniyedeki kare sayısı       |

Kedi fare girdisini yok sayar. Duraklatmak veya kapatmak için **sistem
tepsisi (tray) simgesini** kullanın ya da terminalde `Ctrl+C` yapın.

## Lisans

[MIT](LICENSE)
