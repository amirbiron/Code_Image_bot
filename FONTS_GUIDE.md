# 🔤 מדריך התקנת פונטים

## פונטים זמינים בבוט

הבוט תומך ב-8 פונטים מקצועיים:

- ✨ **Fira Code** - פופולרי במיוחד, עם ligatures (ברירת מחדל)
- 🚀 **JetBrains Mono** - נוצר על ידי JetBrains, אידיאלי לקוד
- ⚡ **Victor Mono** - פונט אלגנטי עם ligatures cursive
- 💻 **Cascadia Code** - מבית Microsoft
- 📝 **DejaVu Sans Mono** - מובנה ברוב המערכות
- 🟠 **Ubuntu Mono** - נקי ופשוט
- 🔧 **Hack** - אופטימלי לקריאות
- 📖 **EB Garamond** - פונט serif קלאסי (יורד אוטומטית בזמן ריצה)

## התקנה מקומית (למחשב שלך)

### Windows

1. הורד את הפונטים:
   - [Fira Code](https://github.com/tonsky/FiraCode/releases)
   - [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
   - [Victor Mono](https://github.com/rubjo/victor-mono/releases)
   - [Cascadia Code](https://github.com/microsoft/cascadia-code/releases)
   - [Hack](https://sourcefoundry.org/hack/)

2. התקן:
   - פתח את קובץ ה-TTF או OTF
   - לחץ על "Install"

### macOS

```bash
# Fira Code
brew tap homebrew/cask-fonts
brew install --cask font-fira-code

# JetBrains Mono
brew install --cask font-jetbrains-mono

# Victor Mono
brew install --cask font-victor-mono

# Cascadia Code
brew install --cask font-cascadia-code

# Hack
brew install --cask font-hack
```

### Linux (Ubuntu/Debian)

```bash
# עדכן מאגרי חבילות
sudo apt update

# Fira Code
sudo apt install fonts-firacode

# JetBrains Mono (דורש הורדה ידנית או)
wget https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip JetBrainsMono-2.304.zip -d ~/.fonts/
fc-cache -f -v

# Victor Mono
wget -O VictorMono.zip https://rubjo.github.io/victor-mono/VictorMonoAll.zip
unzip VictorMono.zip -d ~/.fonts/
fc-cache -f -v

# Cascadia Code
wget https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip
unzip CascadiaCode-2111.01.zip -d ~/.fonts/
fc-cache -f -v

# Hack
sudo apt install fonts-hack

# Ubuntu Mono (בגרסאות חדשות של Debian/Ubuntu ייתכן שהחבילה חסרה)
wget -O ubuntu-fonts.zip https://assets.ubuntu.com/v1/fad7939b-ubuntu-font-family-0.83.zip
unzip ubuntu-fonts.zip -d ubuntu-fonts
mkdir -p ~/.local/share/fonts/ubuntu
find ubuntu-fonts -name "*.ttf" -exec cp {} ~/.local/share/fonts/ubuntu/ \;
rm -rf ubuntu-fonts ubuntu-fonts.zip
fc-cache -f -v

# DejaVu (בדרך כלל מותקן כברירת מחדל)
sudo apt install fonts-dejavu
```
> אם הפקודה `sudo apt install fonts-ubuntu` עדיין זמינה אצלך (לדוגמה ב-Ubuntu 22.04), אפשר להשתמש בה במקום ההתקנה הידנית.

## התקנה בשרת (Render/Heroku/VPS)

### אופציה 1: שימוש ב-Dockerfile

צור קובץ `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install fonts
RUN apt-get update && apt-get install -y \
    fonts-firacode \
    fonts-hack \
    fonts-dejavu \
    fontconfig \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install JetBrains Mono, Victor Mono, Cascadia Code, and Ubuntu fonts manually
RUN set -eux; \
    mkdir -p /usr/share/fonts/truetype/jetbrains /usr/share/fonts/truetype/victor-mono /usr/share/fonts/truetype/cascadia /usr/share/fonts/truetype/ubuntu; \
    cd /tmp; \
    wget -O JetBrainsMono.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip; \
    unzip JetBrainsMono.zip -d JetBrainsMono; \
    find JetBrainsMono -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/jetbrains/ \;; \
    rm -rf JetBrainsMono JetBrainsMono.zip; \
    wget -O VictorMono.zip https://rubjo.github.io/victor-mono/VictorMonoAll.zip; \
    unzip VictorMono.zip -d VictorMono; \
    find VictorMono -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/victor-mono/ \;; \
    rm -rf VictorMono VictorMono.zip; \
    wget -O CascadiaCode.zip https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip; \
    unzip CascadiaCode.zip -d CascadiaCode; \
    find CascadiaCode -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/cascadia/ \;; \
    rm -rf CascadiaCode CascadiaCode.zip; \
    wget -O UbuntuFonts.zip https://assets.ubuntu.com/v1/fad7939b-ubuntu-font-family-0.83.zip; \
    unzip UbuntuFonts.zip -d UbuntuFonts; \
    find UbuntuFonts -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/ubuntu/ \;; \
    rm -rf UbuntuFonts UbuntuFonts.zip; \
    fc-cache -f -v

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "code_image_bot_macos.py"]
```

### אופציה 2: שימוש ב-Build Script

צור קובץ `install_fonts.sh`:

```bash
#!/bin/bash

# Install basic fonts
apt-get update
apt-get install -y fonts-firacode fonts-hack fonts-dejavu fontconfig wget unzip ca-certificates

# Install JetBrains Mono
mkdir -p /usr/share/fonts/truetype/jetbrains
cd /tmp
wget https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
unzip JetBrainsMono-2.304.zip -d /usr/share/fonts/truetype/jetbrains/
fc-cache -f -v
rm JetBrainsMono-2.304.zip

# Install Victor Mono
mkdir -p /usr/share/fonts/truetype/victor-mono
wget -O VictorMono.zip https://rubjo.github.io/victor-mono/VictorMonoAll.zip
unzip VictorMono.zip -d /usr/share/fonts/truetype/victor-mono/
fc-cache -f -v
rm VictorMono.zip

# Install Cascadia Code
mkdir -p /usr/share/fonts/truetype/cascadia
wget https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip
unzip CascadiaCode-2111.01.zip -d /usr/share/fonts/truetype/cascadia/
fc-cache -f -v
rm CascadiaCode-2111.01.zip

# Install Ubuntu fonts manually (fonts-ubuntu no longer in Debian testing)
mkdir -p /usr/share/fonts/truetype/ubuntu
wget -O UbuntuFonts.zip https://assets.ubuntu.com/v1/fad7939b-ubuntu-font-family-0.83.zip
unzip UbuntuFonts.zip -d UbuntuFonts
find UbuntuFonts -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/ubuntu/ \;
rm -rf UbuntuFonts UbuntuFonts.zip
fc-cache -f -v

echo "✅ All fonts installed successfully!"
```

הפעל:
```bash
chmod +x install_fonts.sh
sudo ./install_fonts.sh
```

### אופציה 3: Render Build Command

ב-Render, בשדה **Build Command**:

```bash
apt-get update && apt-get install -y fonts-firacode fonts-hack fonts-dejavu && pip install -r requirements.txt
```

## בדיקת פונטים מותקנים

### Linux/macOS

```bash
# בדוק אילו פונטים monospace מותקנים
fc-list :mono

# חפש פונט ספציפי
fc-list | grep -i "fira"
fc-list | grep -i "jetbrains"
```

### בתוך הבוט

הבוט מתמודד אוטומטית עם פונטים חסרים - אם פונט לא מותקן, הוא יעבור ל-DejaVu Sans Mono (שמותקן בכל מקום).

## פתרון בעיות

### הפונט לא נראה טוב

1. ודא שהפונט מותקן:
   ```bash
   fc-list | grep -i "fira"
   ```

2. רענן את cache הפונטים:
   ```bash
   fc-cache -f -v
   ```

3. אם זה לא עוזר, שנה לפונט אחר דרך `/font` בבוט

### שגיאה "Font not found"

הבוט עובר אוטומטית ל-DejaVu Sans Mono אם יש בעיה.
אבל אם אתה רוצה לתקן:

1. התקן את הפונט החסר
2. הפעל מחדש את הבוט

### פונטים לא עובדים ב-Docker/Render

ודא ש:
1. הפונטים מותקנים ב-Dockerfile או ב-build script
2. `fc-cache -f -v` מופעל אחרי התקנת פונטים
3. הבוט מופעל מחדש אחרי התקנת פונטים

## המלצות

### לפיתוח מקומי
- **Fira Code** - הכי פופולרי, עם ligatures יפים
- **JetBrains Mono** - קל לקריאה, מעוצב מצוין
- **Victor Mono** - מעולה ל-cursive ligatures ועיצוב אלגנטי

### לפרודקשן (שרת)
- **DejaVu Sans Mono** - תמיד זמין, לא דורש התקנה
- **Hack** - קל להתקנה, איכות טובה
- **Victor Mono** - אלגנטי, אם יש זמן להתקנה ידנית

### לעברית
כל הפונטים תומכים בעברית מצוין, אבל:
- **Ubuntu Mono** - עברית נקייה במיוחד
- **DejaVu Sans Mono** - תמיכה מלאה בעברית
> **הערה:** `EB Garamond` לא כולל Glyphs בעברית. אם יש עברית בתוך הקוד (למשל בהערות), הבוט יעשה fallback אוטומטי ל־DejaVu Sans Mono כדי שהעברית תוצג נכון.

## שינוי ברירת מחדל

ערוך את `code_image_bot_macos.py`:

```python
def get_user_settings(user_id: int) -> dict:
    if user_id not in user_settings:
        user_settings[user_id] = {
            "theme": "monokai",
            "language": "auto",
            "show_line_numbers": True,
            "font": "dejavu",  # ← שנה כאן!
        }
    return user_settings[user_id]
```

## טיפים

1. **Ligatures** - Fira Code, JetBrains Mono, ו-Victor Mono תומכים ב-ligatures (== -> ≡, >= -> ≥)
2. **גודל** - כל הפונטים מוצגים בגודל 16, אפשר לשנות ב-`create_code_image`
3. **ביצועים** - DejaVu הכי מהיר, Victor Mono הכי ייחודי
4. **תאימות** - DejaVu תמיד עובד, אפילו בלי התקנה

---

**סיכום מהיר:**
- מקומי: התקן את הפונט שאתה אוהב
- שרת: השתמש ב-DejaVu (תמיד עובד) או Fira Code (קל להתקנה)
- Render: הוסף `fonts-firacode fonts-dejavu` ל-build command
