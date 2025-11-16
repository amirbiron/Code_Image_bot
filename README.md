# 🎨 Code to Image Bot - בוט המרת קוד לתמונה

בוט Telegram מתקדם להמרת קטעי קוד לתמונות מעוצבות ומקצועיות עם Syntax Highlighting.

## ✨ תכונות עיקריות

- 🎨 **ערכות נושא מגוונות** - Monokai, GitHub Dark, Dracula, Nord, One Dark, Solarized ועוד
- 💻 **תמיכה בשפות רבות** - Python, JavaScript, TypeScript, Java, C++, Go, Rust, PHP ועוד
- 🤖 **זיהוי אוטומטי** - הבוט מזהה אוטומטית את שפת התכנות
- 🎯 **ממשק אינטואיטיבי** - כפתורים אינטראקטיביים לבחירת אפשרויות
- 💾 **שמירת העדפות** - ההגדרות נשמרות לכל משתמש
- 🔢 **מספור שורות** - תמיכה במספור שורות מובנה
- 🌐 **תמיכה בעברית** - כל הממשק בעברית

## 📋 דרישות מערכת

- Python 3.8 ומעלה
- pip (מנהל החבילות של Python)
- טוקן בוט מ-@BotFather בטלגרם

## 🚀 התקנה

### 1. שכפול הפרויקט

```bash
git clone <repository-url>
cd code-image-bot
```

### 2. יצירת סביבה וירטואלית (מומלץ)

```bash
python -m venv venv

# הפעלה ב-Windows
venv\Scripts\activate

# הפעלה ב-Linux/Mac
source venv/bin/activate
```

### 3. התקנת תלויות

```bash
pip install -r requirements.txt
```

### 4. הגדרת הבוט

צור קובץ `.env` והוסף את טוקן הבוט שלך:

```bash
cp .env.example .env
# ערוך את הקובץ והכנס את הטוקן שלך
```

או לחלופין, ערוך את `code_image_bot.py` והחלף את `YOUR_BOT_TOKEN_HERE` בטוקן שלך.

### 5. הרצת הבוט

```bash
python code_image_bot.py
```

## 📖 שימוש

### פקודות בסיסיות

- `/start` - התחלת שימוש בבוט
- `/help` - מדריך מפורט
- `/theme` - בחירת ערכת נושא
- `/language` - בחירת שפת תכנות
- `/settings` - הצגת הגדרות נוכחיות

### דוגמאות שימוש

#### 1. שליחת קוד פשוט

פשוט שלח את הקוד כהודעה רגילה:

```
def hello_world():
    print("Hello, World!")
```

#### 2. שליחת קוד עם Code Block

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

#### 3. שינוי ערכת נושא

1. שלח `/theme`
2. בחר נושא מהרשימה
3. שלח קוד חדש

#### 4. שינוי שפת תכנות

1. שלח `/language`
2. בחר שפה מהרשימה
3. שלח קוד חדש

## 🎨 ערכות נושא זמינות

- 🌙 **Monokai** - נושא כהה פופולרי
- 🌃 **GitHub Dark** - נושא GitHub הכהה
- 🧛 **Dracula** - נושא כהה אלגנטי
- ❄️ **Nord** - נושא כחלחל וקריר
- 🌑 **One Dark** - נושא כהה מינימליסטי
- ☀️ **Solarized Dark** - נושא כהה מאוזן
- ☀️ **Solarized Light** - נושא בהיר מאוזן
- ☁️ **GitHub Light** - נושא GitHub הבהיר
- 📝 **Default** - נושא ברירת מחדל

## 💻 שפות תכנות נתמכות

Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, HTML, CSS, SQL, Bash ועוד עשרות שפות נוספות!

## 🏗️ מבנה הפרויקט

```
code-image-bot/
├── code_image_bot.py    # קובץ הבוט הראשי
├── requirements.txt     # תלויות Python
├── .env.example        # דוגמה לקובץ הגדרות
├── README.md           # מדריך זה
└── .gitignore         # קבצים להתעלם (אופציונלי)
```

## ⚙️ הגדרות מתקדמות

### התאמה אישית של ערכות נושא

ערוך את המילון `THEMES` בקובץ `code_image_bot.py`:

```python
THEMES = {
    "custom-theme": "🎨 הנושא שלי",
    # הוסף נושאים נוספים...
}
```

### הוספת שפות תכנות

ערוך את המילון `LANGUAGES`:

```python
LANGUAGES = {
    "mylang": "🔷 השפה שלי",
    # הוסף שפות נוספות...
}
```

### שינוי גודל פונט

ערוך את הפרמטר `font_size` בפונקציה `create_code_image`:

```python
formatter = ImageFormatter(
    font_size=18,  # שנה את הגודל כאן
    # ...
)
```

## 🐛 פתרון בעיות

### הבוט לא עובד

1. ודא שהטוכן נכון
2. בדוק את החיבור לאינטרנט
3. ודא שכל התלויות מותקנות

### שגיאות בטעינת גופנים

התקן את גופן DejaVu:

```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# MacOS
brew install --cask font-dejavu
```

### שגיאות בזיהוי שפה

אם הזיהוי האוטומטי לא עובד טוב, השתמש ב-`/language` לבחירה ידנית.

## 🔧 פיתוח והרחבה

### הוספת תכונות חדשות

הבוט בנוי באופן מודולרי ומאפשר הוספת תכונות בקלות:

1. **הוספת גבולות/מסגרות** - ערוך את `create_code_image`
2. **הוספת לוגו** - הוסף watermark באמצעות Pillow
3. **אפקטים מיוחדים** - הוסף עיבוד תמונה נוסף
4. **שיתוף ישיר** - הוסף כפתור שיתוף לרשתות חברתיות

### מבנה הקוד

```python
# פונקציות ראשיות:
- start() - פקודת התחלה
- theme_command() - בחירת נושא
- language_command() - בחירת שפה
- handle_code() - עיבוד קוד
- create_code_image() - יצירת התמונה
```

## 📦 deployment

### הרצה על שרת

```bash
# התקן כ-systemd service (Linux)
sudo nano /etc/systemd/system/code-image-bot.service

# הוסף:
[Unit]
Description=Code to Image Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/bot
ExecStart=/path/to/venv/bin/python code_image_bot.py
Restart=always

[Install]
WantedBy=multi-user.target

# הפעל:
sudo systemctl enable code-image-bot
sudo systemctl start code-image-bot
```

### Docker

בקובץ `Dockerfile` שכבר נמצא בפרויקט מוגדרת סביבה מלאה עבור `code_image_bot_macos.py`, כולל התקנת כל הפונטים (Fira Code, JetBrains Mono, Cascadia Code ועוד).  
כך תפעילו אותה:

```bash
# בניית האימג'
docker build -t code-image-bot .

# הרצת הבוט עם הטוקן שלכם
docker run -e TELEGRAM_BOT_TOKEN=your_token code-image-bot
```

> אם אתם משתמשים ב-Render / Railway, העבירו את ה-build command ל-`docker build` (או השתמשו ב-Dockerfile buildpack) כדי להימנע משגיאת `apt-get` בסביבה עם read-only filesystem.

## 🤝 תרומה לפרויקט

נשמח לתרומות! אפשר:
- לדווח על באגים
- להציע תכונות חדשות
- לשפר את התיעוד
- להוסיף ערכות נושא

## 📄 רישיון

MIT License - ראה קובץ LICENSE לפרטים

## 👨‍💻 מפתח

נוצר עם ❤️ על ידי אמיר

## 🔗 קישורים שימושיים

- [תיעוד python-telegram-bot](https://docs.python-telegram-bot.org/)
- [תיעוד Pygments](https://pygments.org/docs/)
- [תיעוד Pillow](https://pillow.readthedocs.io/)

## 📞 תמיכה

יש שאלות? פנה אלי דרך:
- Telegram: @yourusername
- GitHub Issues: [repository-url]/issues

---

**הערה:** זכור לשמור על הטוקן של הבוט בסוד ולא לשתף אותו!
