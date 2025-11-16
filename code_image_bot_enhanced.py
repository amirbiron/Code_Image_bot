"""
Code to Image Bot - Enhanced Version
With additional features: watermarks, custom backgrounds, gradients, etc.
"""

import os
import io
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
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Enhanced themes with gradients
THEMES = {
    "monokai": {"name": "🌙 Monokai", "style": "monokai"},
    "github-dark": {"name": "🌃 GitHub Dark", "style": "github-dark"},
    "dracula": {"name": "🧛 Dracula", "style": "dracula"},
    "nord": {"name": "❄️ Nord", "style": "nord"},
    "one-dark": {"name": "🌑 One Dark", "style": "one-dark"},
    "solarized-dark": {"name": "☀️ Solarized Dark", "style": "solarized-dark"},
    "solarized-light": {"name": "☀️ Solarized Light", "style": "solarized-light"},
    "gruvbox": {"name": "🟤 Gruvbox", "style": "gruvbox-dark"},
    "material": {"name": "🎨 Material", "style": "material"},
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

# Background styles
BACKGROUND_STYLES = {
    "solid": "⬛ Solid",
    "gradient": "🌈 Gradient",
    "rounded": "⭕ Rounded",
    "shadow": "💫 Shadow",
}

# User settings with enhanced options
user_settings = {}


def get_user_settings(user_id: int) -> dict:
    """Get user settings with defaults"""
    if user_id not in user_settings:
        user_settings[user_id] = {
            "theme": "monokai",
            "language": "auto",
            "font_size": 16,
            "background_style": "gradient",
            "add_watermark": False,
            "line_numbers": True,
        }
    return user_settings[user_id]


def add_gradient_background(img: Image.Image, colors: Tuple[str, str]) -> Image.Image:
    """Add gradient background to image"""
    width, height = img.size
    gradient = Image.new('RGB', (width, height), colors[0])
    draw = ImageDraw.Draw(gradient)
    
    # Create gradient
    for y in range(height):
        # Calculate color interpolation
        ratio = y / height
        r1, g1, b1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Composite images
    gradient.paste(img, (0, 0), img if img.mode == 'RGBA' else None)
    return gradient


def add_rounded_corners(img: Image.Image, radius: int = 20) -> Image.Image:
    """Add rounded corners to image"""
    # Create mask
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    
    # Apply mask
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    return output


def add_shadow(img: Image.Image, offset: Tuple[int, int] = (10, 10)) -> Image.Image:
    """Add shadow effect to image"""
    # Create shadow layer
    shadow = Image.new('RGBA', 
                      (img.width + offset[0] * 2, img.height + offset[1] * 2),
                      (0, 0, 0, 0))
    
    # Create shadow
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 128))
    shadow.paste(shadow_img, offset)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    
    # Composite
    final = Image.new('RGBA', shadow.size, (255, 255, 255, 0))
    final.paste(shadow, (0, 0))
    final.paste(img, offset, img if img.mode == 'RGBA' else None)
    
    return final


def add_watermark(img: Image.Image, text: str = "CodeBot") -> Image.Image:
    """Add watermark to image"""
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    # Calculate position (bottom right)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = (img.width - text_width - 15, img.height - text_height - 10)
    
    # Draw semi-transparent background
    draw.rectangle(
        [position[0] - 5, position[1] - 2,
         position[0] + text_width + 5, position[1] + text_height + 2],
        fill=(0, 0, 0, 100)
    )
    
    # Draw text
    draw.text(position, text, fill=(255, 255, 255, 150), font=font)
    
    return img


def create_enhanced_code_image(
    code: str,
    language: str = "python",
    style: str = "monokai",
    background_style: str = "gradient",
    add_watermark_flag: bool = False,
    line_numbers: bool = True
) -> io.BytesIO:
    """
    Create an enhanced styled code image
    """
    try:
        # Get lexer
        if language == "auto":
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language, stripall=True)
        
        # Create formatter
        formatter = ImageFormatter(
            style=style,
            font_name="DejaVu Sans Mono",
            font_size=16,
            line_numbers=line_numbers,
            line_number_separator=line_numbers,
            line_number_bg="#1e1e1e" if line_numbers else None,
            line_number_fg="#858585" if line_numbers else None,
        )
        
        # Generate base image
        result = highlight(code, lexer, formatter)
        img = Image.open(io.BytesIO(result))
        
        # Convert to RGBA for transparency support
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Apply background style
        if background_style == "gradient":
            img = add_gradient_background(img, ("#1a1a2e", "#16213e"))
        elif background_style == "rounded":
            img = add_rounded_corners(img)
        elif background_style == "shadow":
            img = add_shadow(img)
        
        # Add watermark if requested
        if add_watermark_flag:
            img = add_watermark(img)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG', quality=95)
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
🎨 *ברוכים הבאים לבוט המרת קוד מתקדם!*

*תכונות חדשות:*
✨ רקעים מעוצבים עם גרדיאנט
💫 אפקטים של צל ופינות מעוגלות
🏷️ אופציה להוספת watermark
🎯 התאמה אישית מלאה

*פקודות:*
/start - התחלה
/theme - ערכות נושא
/language - שפות תכנות
/background - סגנון רקע
/watermark - הוספת/הסרת watermark
/settings - הגדרות
/help - עזרה

שלח קוד כדי להתחיל! 🚀
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def background_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Background style selection"""
    keyboard = [
        [InlineKeyboardButton(BACKGROUND_STYLES[style], callback_data=f"bg_{style}")]
        for style in BACKGROUND_STYLES
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎨 *בחר סגנון רקע:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def watermark_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle watermark"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    settings["add_watermark"] = not settings["add_watermark"]
    
    status = "מופעל ✅" if settings["add_watermark"] else "כבוי ❌"
    await update.message.reply_text(f"Watermark: {status}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display settings"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    
    settings_text = f"""
⚙️ *ההגדרות שלך:*

🎨 נושא: {THEMES[settings['theme']]['name']}
💻 שפה: {LANGUAGES[settings['language']]}
📐 רקע: {BACKGROUND_STYLES[settings['background_style']]}
🏷️ Watermark: {'✅' if settings['add_watermark'] else '❌'}
🔢 מספור שורות: {'✅' if settings['line_numbers'] else '❌'}
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
            f"✅ נושא שונה ל-{THEMES[theme]['name']}!"
        )
    
    elif data.startswith("lang_"):
        language = data.replace("lang_", "")
        settings["language"] = language
        await query.edit_message_text(
            f"✅ שפה שונתה ל-{LANGUAGES[language]}!"
        )
    
    elif data.startswith("bg_"):
        bg_style = data.replace("bg_", "")
        settings["background_style"] = bg_style
        await query.edit_message_text(
            f"✅ סגנון רקע שונה ל-{BACKGROUND_STYLES[bg_style]}!"
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
    
    status_msg = await update.message.reply_text("⏳ יוצר תמונה מעוצבת...")
    
    try:
        image_bytes = create_enhanced_code_image(
            code,
            language=settings["language"],
            style=settings["theme"],
            background_style=settings["background_style"],
            add_watermark_flag=settings["add_watermark"],
            line_numbers=settings["line_numbers"]
        )
        
        caption = (
            f"🎨 {THEMES[settings['theme']]['name']}\n"
            f"💻 {LANGUAGES[settings['language']]}\n"
            f"📐 {BACKGROUND_STYLES[settings['background_style']]}"
        )
        
        await update.message.reply_photo(photo=image_bytes, caption=caption)
        await status_msg.delete()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ שגיאה: {str(e)}")


# Additional command handlers would go here for theme and language selection
# (similar to the basic version)


def main():
    """Main function"""
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("background", background_command))
    application.add_handler(CommandHandler("watermark", watermark_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code)
    )
    
    logger.info("🚀 Enhanced bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
