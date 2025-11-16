"""
Code to Image Bot - Telegram Bot for Converting Code Snippets to Styled Images
"""

import os
import io
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Available themes
THEMES = {
    "monokai": "🌙 Monokai (Dark)",
    "github-dark": "🌃 GitHub Dark",
    "dracula": "🧛 Dracula",
    "nord": "❄️ Nord",
    "one-dark": "🌑 One Dark",
    "solarized-dark": "☀️ Solarized Dark",
    "solarized-light": "☀️ Solarized Light",
    "github-light": "☁️ GitHub Light",
    "default": "📝 Default",
}

# Available programming languages
LANGUAGES = {
    "python": "🐍 Python",
    "javascript": "📜 JavaScript",
    "typescript": "📘 TypeScript",
    "java": "☕ Java",
    "cpp": "⚙️ C++",
    "csharp": "🔷 C#",
    "go": "🐹 Go",
    "rust": "🦀 Rust",
    "php": "🐘 PHP",
    "ruby": "💎 Ruby",
    "swift": "🍎 Swift",
    "kotlin": "🟣 Kotlin",
    "html": "🌐 HTML",
    "css": "🎨 CSS",
    "sql": "🗄️ SQL",
    "bash": "💻 Bash",
    "auto": "🤖 Auto-detect",
}

# User settings storage
user_settings = {}


def get_user_settings(user_id: int) -> dict:
    """Get user settings with defaults"""
    if user_id not in user_settings:
        user_settings[user_id] = {
            "theme": "monokai",
            "language": "auto",
            "font_size": 16,
        }
    return user_settings[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_text = """
🎨 *ברוכים הבאים לבוט המרת קוד לתמונה!*

פשוט שלחו לי קטע קוד ואני אהפוך אותו לתמונה מעוצבת יפהפייה!

*פקודות זמינות:*
/start - הצג הודעת פתיחה
/theme - בחר ערכת נושא
/language - בחר שפת תכנות
/settings - הגדרות נוכחיות
/help - עזרה

*איך להשתמש:*
1. שלח לי קטע קוד (או השתמש ב-/language לבחירת שפה)
2. אבחר את הנושא המתאים (או השתמש ב-/theme)
3. קבל תמונה מעוצבת מושלמת!

תתחילו לשלוח קוד? 🚀
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """
📚 *מדריך שימוש*

*שליחת קוד:*
פשוט שלח את קטע הקוד שלך כהודעה רגילה או בתוך ``` (code block)

*ערכות נושא זמינות:*
🌙 Monokai, 🌃 GitHub Dark, 🧛 Dracula, ❄️ Nord
🌑 One Dark, ☀️ Solarized (Dark/Light)

*שפות תכנות נתמכות:*
Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, HTML, CSS, SQL, Bash ועוד...

*טיפים:*
• הבוט מזהה אוטומטית את שפת התכנות
• אפשר לבחור ידנית דרך /language
• שנה נושא דרך /theme
• כל ההגדרות נשמרות אוטומטית

נתקלתם בבעיה? צרו קשר עם המפתח.
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def theme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Theme selection command"""
    keyboard = []
    themes_list = list(THEMES.items())
    
    # Create 2-column layout
    for i in range(0, len(themes_list), 2):
        row = []
        for j in range(2):
            if i + j < len(themes_list):
                theme_key, theme_name = themes_list[i + j]
                row.append(
                    InlineKeyboardButton(
                        theme_name, callback_data=f"theme_{theme_key}"
                    )
                )
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎨 *בחר ערכת נושא:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Language selection command"""
    keyboard = []
    languages_list = list(LANGUAGES.items())
    
    # Create 2-column layout
    for i in range(0, len(languages_list), 2):
        row = []
        for j in range(2):
            if i + j < len(languages_list):
                lang_key, lang_name = languages_list[i + j]
                row.append(
                    InlineKeyboardButton(
                        lang_name, callback_data=f"lang_{lang_key}"
                    )
                )
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💻 *בחר שפת תכנות:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display current settings"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    settings_text = f"""
⚙️ *ההגדרות הנוכחיות שלך:*

🎨 ערכת נושא: {THEMES.get(settings['theme'], 'Unknown')}
💻 שפת תכנות: {LANGUAGES.get(settings['language'], 'Unknown')}
📏 גודל פונט: {settings['font_size']}

שנה הגדרות באמצעות:
/theme - שינוי ערכת נושא
/language - שינוי שפת תכנות
"""
    await update.message.reply_text(settings_text, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    data = query.data
    
    if data.startswith("theme_"):
        theme = data.replace("theme_", "")
        settings["theme"] = theme
        await query.edit_message_text(
            f"✅ ערכת הנושא שונתה ל-{THEMES[theme]}!\n\n"
            "עכשיו שלח לי קוד לעיצוב 🎨"
        )
    
    elif data.startswith("lang_"):
        language = data.replace("lang_", "")
        settings["language"] = language
        await query.edit_message_text(
            f"✅ שפת התכנות שונתה ל-{LANGUAGES[language]}!\n\n"
            "עכשיו שלח לי קוד לעיצוב 💻"
        )


def create_code_image(code: str, language: str = "python", style: str = "monokai") -> io.BytesIO:
    """
    Create a styled code image using Pygments
    
    Args:
        code: The code snippet to render
        language: Programming language for syntax highlighting
        style: Color scheme/theme to use
        
    Returns:
        BytesIO object containing the PNG image
    """
    try:
        # Get the lexer
        if language == "auto":
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language, stripall=True)
        
        # Create the formatter with custom settings
        formatter = ImageFormatter(
            style=style,
            font_name="DejaVu Sans Mono",
            font_size=16,
            line_numbers=True,
            line_number_separator=True,
            line_number_bg="#1e1e1e",
            line_number_fg="#858585",
            hl_color="#3e4451",
        )
        
        # Generate the image
        result = highlight(code, lexer, formatter)
        
        # Convert to BytesIO
        image_bytes = io.BytesIO(result)
        image_bytes.seek(0)
        
        return image_bytes
    
    except Exception as e:
        print(f"Error creating image: {e}")
        # Create a simple error image
        img = Image.new('RGB', (800, 200), color='#1e1e1e')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 90), f"Error: {str(e)}", fill='white', font=font)
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes


async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming code messages"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    # Get the code from the message
    code = update.message.text
    
    # Remove code block markers if present
    if code.startswith("```") and code.endswith("```"):
        lines = code.split("\n")
        # Remove first and last line
        code = "\n".join(lines[1:-1])
        # Check if first line specifies language
        if lines[0].startswith("```") and len(lines[0]) > 3:
            lang_hint = lines[0][3:].strip()
            if lang_hint in LANGUAGES:
                settings["language"] = lang_hint
    
    # Send "processing" message
    status_msg = await update.message.reply_text("⏳ מעבד את הקוד...")
    
    try:
        # Create the image
        image_bytes = create_code_image(
            code,
            language=settings["language"],
            style=settings["theme"]
        )
        
        # Send the image
        await update.message.reply_photo(
            photo=image_bytes,
            caption=f"🎨 נושא: {THEMES[settings['theme']]}\n"
                   f"💻 שפה: {LANGUAGES[settings['language']]}",
        )
        
        # Delete status message
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(
            f"❌ שגיאה ביצירת התמונה:\n{str(e)}\n\n"
            "נסה שוב או שנה הגדרות עם /settings"
        )


def main():
    """Main function to run the bot"""
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("theme", theme_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code)
    )
    
    # Start the bot
    print("🚀 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
