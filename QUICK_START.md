# 🚀 מדריך התקנה מהיר - Code to Image Bot

## התקנה בפחות מ-5 דקות!

### שלב 1: קבלת טוכן לבוט

1. פתח את Telegram ושלח הודעה ל-[@BotFather](https://t.me/BotFather)
2. שלח את הפקודה: `/newbot`
3. בחר שם לבוט (לדוגמה: "Code Image Bot")
4. בחר username לבוט (חייב להסתיים ב-bot, לדוגמה: `my_code_image_bot`)
5. העתק את הטוכן שקיבלת (נראה כך: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### שלב 2: התקנת Python והכנה

```bash
# בדוק שיש לך Python מותקן (גרסה 3.8+)
python --version

# אם אין Python, התקן מ:
# Windows: https://www.python.org/downloads/
# Mac: brew install python3
# Linux: sudo apt install python3 python3-pip
```

### שלב 3: הורדת הפרויקט

הורד את כל הקבצים שקיבלת לתיקייה חדשה:

```bash
mkdir code-image-bot
cd code-image-bot
# העתק את כל הקבצים לכאן
```

### שלב 4: התקנת תלויות

```bash
# צור סביבה וירטואלית (מומלץ)
python -m venv venv

# הפעל את הסביבה:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# התקן תלויות:
pip install -r requirements.txt
```

### שלב 5: הגדרת הטוכן

בחר אחת משתי האפשרויות:

**אפשרות 1: דרך קובץ .env (מומלץ)**
```bash
# צור קובץ .env
cp .env.example .env

# ערוך את הקובץ והכנס את הטוכן:
# Windows: notepad .env
# Mac/Linux: nano .env

# שנה את השורה:
TELEGRAM_BOT_TOKEN=your_bot_token_here
# ל:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**אפשרות 2: ישירות בקוד**
```bash
# ערוך את code_image_bot.py
# Windows: notepad code_image_bot.py
# Mac/Linux: nano code_image_bot.py

# מצא את השורה:
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# שנה ל:
TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### שלב 6: הפעלת הבוט

```bash
python code_image_bot.py
```

אם הכל עובד, תראה:
```
🚀 Bot is starting...
```

### שלב 7: בדיקה בטלגרם

1. חפש את הבוט שלך בטלגרם (לפי ה-username שבחרת)
2. שלח `/start`
3. שלח קטע קוד לבדיקה:

```python
def hello():
    print("Hello World!")
```

4. תקבל תמונה מעוצבת! 🎉

## פתרון בעיות מהיר

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Invalid token"
ודא שהטוכן נכון ללא רווחים מיותרים

### "Font not found"
התקן גופנים:
```bash
# Ubuntu/Debian:
sudo apt-get install fonts-dejavu

# Mac:
brew install --cask font-dejavu
```

### הבוט לא מגיב
- בדוק חיבור לאינטרנט
- ודא שהטוכן נכון
- נסה להפעיל מחדש את הבוט

## שימוש בסיסי

1. **שינוי ערכת נושא**: שלח `/theme` ובחר מהרשימה
2. **בחירת שפה**: שלח `/language` ובחר שפה
3. **הגדרות**: שלח `/settings` לראות הגדרות נוכחיות
4. **עזרה**: שלח `/help` למדריך מפורט

## טיפים מהירים

✅ שלח קוד ישירות - הבוט יזהה את השפה אוטומטית  
✅ השתמש ב-``` להדגשת בלוקי קוד  
✅ כל ההגדרות נשמרות אוטומטית לכל משתמש  
✅ תמיכה במגוון רחב של שפות תכנות  

## שאלות נפוצות

**ש: האם הבוט בחינם?**  
ת: כן! הקוד פתוח לחלוטין.

**ש: כמה קוד אפשר לשלוח?**  
ת: עד 5000 תווים לכל בקשה.

**ש: אפשר להוסיף ערכות נושא?**  
ת: כן! ערוך את `config.py` והוסף נושאים משלך.

**ש: הבוט שומר את הקוד שלי?**  
ת: לא! הבוט מעבד ומוחק מיד.

## צריך עזרה?

📖 קרא את [README.md](README.md) למדריך מלא  
💡 בדוק את [examples.py](examples.py) לדוגמאות  
⚙️ ראה [config.py](config.py) להתאמות מתקדמות  

---

**בהצלחה! 🚀**
