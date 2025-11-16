"""
Code to Image Bot - macOS Window Style
Creates beautiful code images with macOS window styling like Carbon/Ray.so
"""

import importlib
import io
import os
import sys
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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
try:  # python-telegram-bot < 21 (builder uses Updater internally)
    from telegram.ext import Updater as _PTBUpdater  # type: ignore
except ImportError:  # pragma: no cover
    _PTBUpdater = None
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Work around python-telegram-bot bug where Updater.__slots__ misses
# __polling_cleanup_cb (older patch levels on Python 3.13) by swapping in a
# subclass that defines the missing slot and re-exporting it wherever PTB
# expects the original Updater.
if _PTBUpdater is not None:
    _UPDATER_SLOT = "_Updater__polling_cleanup_cb"
    slots = getattr(_PTBUpdater, "__slots__", ())
    if isinstance(slots, str):
        slots = (slots,)
    elif slots is None:
        slots = ()
    else:
        slots = tuple(slots)

    if _UPDATER_SLOT not in slots:
        class _PatchedUpdater(_PTBUpdater):  # type: ignore[misc]
            __slots__ = slots + (_UPDATER_SLOT,)

        for module_name in (
            "telegram.ext",
            "telegram.ext._updater",
            "telegram.ext._applicationbuilder",
        ):
            module = sys.modules.get(module_name)
            if module is None:
                try:
                    module = importlib.import_module(module_name)
                except ModuleNotFoundError:
                    continue
            setattr(module, "Updater", _PatchedUpdater)

        _PTBUpdater = _PatchedUpdater

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Themes with background gradients
THEMES = {
    "monokai": {
        "name": "🌙 Monokai",
        "style": "monokai",
        "bg_gradient": ("#7b2cbf", "#5a189a"),
    },
    "dracula": {
        "name": "🧛 Dracula",
        "style": "dracula",
        "bg_gradient": ("#6c5ce7", "#a29bfe"),
    },
    "nord": {
        "name": "❄️ Nord",
        "style": "nord",
        "bg_gradient": ("#5e60ce", "#7209b7"),
    },
    "github-dark": {
        "name": "🌃 GitHub Dark",
        "style": "github-dark",
        "bg_gradient": ("#4895ef", "#4361ee"),
    },
    "one-dark": {
        "name": "🌑 One Dark",
        "style": "one-dark",
        "bg_gradient": ("#f72585", "#b5179e"),
    },
    "solarized-dark": {
        "name": "☀️ Solarized Dark",
        "style": "solarized-dark",
        "bg_gradient": ("#fb5607", "#ff006e"),
    },
    "material": {
        "name": "🎨 Material",
        "style": "material",
        "bg_gradient": ("#06ffa5", "#00d9ff"),
    },
    "gruvbox": {
        "name": "🟤 Gruvbox",
        "style": "gruvbox-dark",
        "bg_gradient": ("#fb8500", "#ffb703"),
    },
}

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
    "auto": "🤖 Auto",
}

# Available fonts
FONTS = {
    "fira": {
        "name": "✨ Fira Code",
        "path": "/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf",
        "fallback": "DejaVu Sans Mono",
    },
    "jetbrains": {
        "name": "🚀 JetBrains Mono",
        "path": "/usr/share/fonts/truetype/jetbrains/JetBrainsMono-Regular.ttf",
        "fallback": "DejaVu Sans Mono",
    },
    "cascadia": {
        "name": "💻 Cascadia Code",
        "path": "/usr/share/fonts/truetype/cascadia/CascadiaCode.ttf",
        "fallback": "DejaVu Sans Mono",
    },
    "dejavu": {
        "name": "📝 DejaVu Sans Mono",
        "path": "DejaVu Sans Mono",
        "fallback": "DejaVu Sans Mono",
    },
    "ubuntu": {
        "name": "🟠 Ubuntu Mono",
        "path": "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "fallback": "DejaVu Sans Mono",
    },
    "hack": {
        "name": "🔧 Hack",
        "path": "/usr/share/fonts/truetype/hack/Hack-Regular.ttf",
        "fallback": "DejaVu Sans Mono",
    },
}

# User settings
user_settings = {}


def get_user_settings(user_id: int) -> dict:
    """Get user settings with defaults"""
    if user_id not in user_settings:
        user_settings[user_id] = {
            "theme": "monokai",
            "language": "auto",
            "show_line_numbers": True,
            "font": "fira",  # Default to Fira Code
        }
    return user_settings[user_id]


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_gradient_background(width: int, height: int, color1: str, color2: str) -> Image.Image:
    """Create a gradient background"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            # Diagonal gradient
            mask_data.append(int(255 * (x + y) / (width + height)))
    mask.putdata(mask_data)
    
    base.paste(top, (0, 0), mask)
    return base


def create_macos_window(code_img: Image.Image, gradient_colors: Tuple[str, str]) -> Image.Image:
    """
    Create macOS-style window with title bar and gradient background
    """
    # Window dimensions
    titlebar_height = 60
    padding = 80
    border_radius = 20
    
    # Calculate final size
    window_width = code_img.width + (padding * 2)
    window_height = code_img.height + titlebar_height + (padding * 2)
    
    # Create gradient background
    final_img = create_gradient_background(
        window_width + 100,
        window_height + 100,
        gradient_colors[0],
        gradient_colors[1]
    )
    
    # Create window with rounded corners
    window = Image.new('RGBA', (window_width, window_height), (0, 0, 0, 0))
    
    # Draw rounded rectangle for window
    window_draw = ImageDraw.Draw(window)
    window_draw.rounded_rectangle(
        [(0, 0), (window_width, window_height)],
        radius=border_radius,
        fill='#2d2d2d'
    )
    
    # Draw titlebar
    titlebar = Image.new('RGBA', (window_width, titlebar_height), (0, 0, 0, 0))
    titlebar_draw = ImageDraw.Draw(titlebar)
    
    # Draw titlebar background (slightly lighter)
    titlebar_draw.rounded_rectangle(
        [(0, 0), (window_width, titlebar_height + border_radius)],
        radius=border_radius,
        fill='#323232'
    )
    
    # Draw the bottom part to make it not rounded
    titlebar_draw.rectangle(
        [(0, titlebar_height - border_radius), (window_width, titlebar_height)],
        fill='#323232'
    )
    
    # Draw macOS buttons (red, yellow, green)
    button_y = titlebar_height // 2
    button_spacing = 20
    button_start_x = 25
    
    buttons = [
        ('#ff5f56', button_start_x),  # Red
        ('#ffbd2e', button_start_x + button_spacing),  # Yellow
        ('#27c93f', button_start_x + button_spacing * 2),  # Green
    ]
    
    for color, x in buttons:
        titlebar_draw.ellipse(
            [(x, button_y - 6), (x + 12, button_y + 6)],
            fill=color
        )
    
    # Paste titlebar onto window
    window.paste(titlebar, (0, 0), titlebar)
    
    # Add shadow to code image
    shadow = Image.new('RGBA', (code_img.width + 20, code_img.height + 20), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [(10, 10), (code_img.width + 10, code_img.height + 10)],
        fill=(0, 0, 0, 50)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    
    # Paste shadow and code onto window
    code_x = padding
    code_y = titlebar_height + padding
    
    window.paste(shadow, (code_x - 10, code_y - 10), shadow)
    window.paste(code_img, (code_x, code_y))
    
    # Add subtle shadow to entire window
    window_shadow = Image.new('RGBA', 
                               (window_width + 60, window_height + 60),
                               (0, 0, 0, 0))
    window_shadow_draw = ImageDraw.Draw(window_shadow)
    window_shadow_draw.rounded_rectangle(
        [(30, 30), (window_width + 30, window_height + 30)],
        radius=border_radius,
        fill=(0, 0, 0, 80)
    )
    window_shadow = window_shadow.filter(ImageFilter.GaussianBlur(20))
    
    # Composite everything
    final_canvas = Image.new('RGBA', (window_width + 100, window_height + 100), (0, 0, 0, 0))
    final_canvas.paste(final_img, (0, 0))
    final_canvas.paste(window_shadow, (20, 20), window_shadow)
    final_canvas.paste(window, (50, 50), window)
    
    return final_canvas


def create_code_image(
    code: str,
    language: str = "python",
    theme: str = "monokai",
    show_line_numbers: bool = True,
    font: str = "fira"
) -> io.BytesIO:
    """
    Create a beautiful code image in macOS window style
    """
    try:
        # Get lexer
        if language == "auto":
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language, stripall=True)
        
        # Get theme details
        theme_details = THEMES.get(theme, THEMES["monokai"])
        
        # Get font details
        font_details = FONTS.get(font, FONTS["fira"])
        font_name = font_details.get("fallback", "DejaVu Sans Mono")
        
        # Try to use the specified font, fallback to DejaVu if not available
        try:
            if "path" in font_details and font_details["path"] != font_details["fallback"]:
                # Test if font file exists
                import os
                if os.path.exists(font_details["path"]):
                    font_name = font_details["path"]
        except:
            pass
        
        # Create formatter
        formatter = ImageFormatter(
            style=theme_details["style"],
            font_name=font_name,
            font_size=16,
            line_numbers=show_line_numbers,
            line_number_separator=True,
            line_number_bg="#1e1e1e",
            line_number_fg="#858585",
        )
        
        # Generate base code image
        result = highlight(code, lexer, formatter)
        code_img = Image.open(io.BytesIO(result))
        
        # Convert to RGBA
        if code_img.mode != 'RGBA':
            code_img = code_img.convert('RGBA')
        
        # Create macOS window with gradient background
        final_img = create_macos_window(code_img, theme_details["bg_gradient"])
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        final_img.save(img_bytes, format='PNG', quality=95)
        img_bytes.seek(0)
        
        return img_bytes
    
    except Exception as e:
        logger.error(f"Error creating image: {e}")
        # Create error image
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    welcome_text = """
🎨 *ברוכים הבאים לבוט המרת קוד לתמונה!*

✨ *עיצוב מסוג macOS Window עם רקעים צבעוניים!*

*פקודות זמינות:*
  `/start` - התחלה
  `/theme` - בחר ערכת נושא
  `/language` - בחר שפת תכנות
  `/font` - בחר גופן (Fira Code, JetBrains Mono ועוד)
  `/toggle_numbers` - הפעל/כבה מספור שורות
  `/settings` - הגדרות נוכחיות
  `/help` - עזרה

פשוט שלח קוד ותקבל תמונה מעוצבת! 🚀
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
📚 *מדריך שימוש*

*שליחת קוד:*
שלח את קטע הקוד שלך כהודעה רגילה

*דוגמה:*
```python
def hello():
    print("Hello World!")
```

*ערכות נושא:*
🌙 Monokai (סגול), 🧛 Dracula (סגול-כחול)
❄️ Nord (כחול), 🌃 GitHub Dark (כחול)
🎨 Material (ירוק-תכלת), 🟤 Gruvbox (כתום)

*טיפים:*
• הבוט מזהה אוטומטית את שפת התכנות
• כל תמונה נוצרת עם חלון macOS מעוצב
• רקע צבעוני גרדיאנט ייחודי לכל נושא
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def theme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Theme selection"""
    keyboard = []
    themes_list = list(THEMES.items())
    
    for i in range(0, len(themes_list), 2):
        row = []
        for j in range(2):
            if i + j < len(themes_list):
                theme_key, theme_data = themes_list[i + j]
                row.append(
                    InlineKeyboardButton(
                        theme_data["name"],
                        callback_data=f"theme_{theme_key}"
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
    """Language selection"""
    keyboard = []
    languages_list = list(LANGUAGES.items())
    
    for i in range(0, len(languages_list), 2):
        row = []
        for j in range(2):
            if i + j < len(languages_list):
                lang_key, lang_name = languages_list[i + j]
                row.append(
                    InlineKeyboardButton(
                        lang_name,
                        callback_data=f"lang_{lang_key}"
                    )
                )
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💻 *בחר שפת תכנות:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def font_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Font selection"""
    keyboard = []
    fonts_list = list(FONTS.items())
    
    for i in range(0, len(fonts_list), 2):
        row = []
        for j in range(2):
            if i + j < len(fonts_list):
                font_key, font_data = fonts_list[i + j]
                row.append(
                    InlineKeyboardButton(
                        font_data["name"],
                        callback_data=f"font_{font_key}"
                    )
                )
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔤 *בחר גופן:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def toggle_numbers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle line numbers"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    settings["show_line_numbers"] = not settings["show_line_numbers"]
    
    status = "מופעל ✅" if settings["show_line_numbers"] else "כבוי ❌"
    await update.message.reply_text(f"מספור שורות: {status}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display settings"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    settings_text = f"""
⚙️ *ההגדרות שלך:*

🎨 ערכת נושא: {THEMES[settings['theme']]['name']}
💻 שפת תכנות: {LANGUAGES[settings['language']]}
🔤 גופן: {FONTS[settings['font']]['name']}
🔢 מספור שורות: {'✅' if settings['show_line_numbers'] else '❌'}

שנה הגדרות עם:
  `/theme` - שינוי ערכת נושא
  `/language` - שינוי שפת תכנות
  `/font` - שינוי גופן
  `/toggle_numbers` - הפעל/כבה מספור שורות
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
            f"✅ ערכת הנושא שונתה ל-{THEMES[theme]['name']}!\n\n"
            "עכשיו שלח לי קוד לעיצוב 🎨"
        )
    
    elif data.startswith("lang_"):
        language = data.replace("lang_", "")
        settings["language"] = language
        await query.edit_message_text(
            f"✅ שפת התכנות שונתה ל-{LANGUAGES[language]}!\n\n"
            "עכשיו שלח לי קוד לעיצוב 💻"
        )
    
    elif data.startswith("font_"):
        font = data.replace("font_", "")
        settings["font"] = font
        await query.edit_message_text(
            f"✅ הגופן שונה ל-{FONTS[font]['name']}!\n\n"
            "עכשיו שלח לי קוד לעיצוב 🔤"
        )


async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle code messages"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    code = update.message.text
    
    # Clean code blocks
    if code.startswith("```") and code.endswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1])
        # Check for language hint
        if lines[0].startswith("```") and len(lines[0]) > 3:
            lang_hint = lines[0][3:].strip()
            if lang_hint in LANGUAGES:
                settings["language"] = lang_hint
    
    status_msg = await update.message.reply_text("⏳ יוצר תמונה מעוצבת...")
    
    try:
        image_bytes = create_code_image(
            code,
            language=settings["language"],
            theme=settings["theme"],
            show_line_numbers=settings["show_line_numbers"],
            font=settings["font"]
        )
        
        caption = (
            f"🎨 {THEMES[settings['theme']]['name']}\n"
            f"💻 {LANGUAGES[settings['language']]}\n"
            f"🔤 {FONTS[settings['font']]['name']}"
        )
        
        await update.message.reply_photo(photo=image_bytes, caption=caption)
        await status_msg.delete()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ שגיאה: {str(e)}")


def main():
    """Main function"""
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("theme", theme_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("font", font_command))
    application.add_handler(CommandHandler("toggle_numbers", toggle_numbers_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code)
    )
    
    logger.info("🚀 Bot starting with macOS window style...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
