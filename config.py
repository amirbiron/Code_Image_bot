"""
Advanced Configuration for Code to Image Bot
"""

# ============================================
# Bot Settings
# ============================================

# Bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin user IDs (for statistics and management)
ADMIN_IDS = []

# Maximum code length (characters)
MAX_CODE_LENGTH = 5000

# ============================================
# Image Generation Settings
# ============================================

# Default settings
DEFAULT_SETTINGS = {
    "theme": "monokai",
    "language": "auto",
    "font_size": 16,
    "line_numbers": True,
    "font_name": "DejaVu Sans Mono",
}

# Image format settings
IMAGE_SETTINGS = {
    "format": "PNG",
    "quality": 95,
    "dpi": (72, 72),
}

# ============================================
# Theme Customization
# ============================================

CUSTOM_THEMES = {
    "monokai": {
        "name": "🌙 Monokai",
        "description": "נושא כהה פופולרי למפתחים",
        "background": "#272822",
        "line_number_bg": "#1e1e1e",
        "line_number_fg": "#858585",
    },
    "dracula": {
        "name": "🧛 Dracula",
        "description": "נושא כהה אלגנטי",
        "background": "#282a36",
        "line_number_bg": "#191a21",
        "line_number_fg": "#6272a4",
    },
    "nord": {
        "name": "❄️ Nord",
        "description": "נושא קריר וקורדי",
        "background": "#2e3440",
        "line_number_bg": "#242933",
        "line_number_fg": "#4c566a",
    },
}

# ============================================
# Language Detection Settings
# ============================================

# Language aliases
LANGUAGE_ALIASES = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "cpp": "cpp",
    "c++": "cpp",
    "cs": "csharp",
    "c#": "csharp",
    "rb": "ruby",
    "sh": "bash",
    "shell": "bash",
}

# File extension to language mapping
EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
    ".sh": "bash",
}

# ============================================
# Feature Flags
# ============================================

FEATURES = {
    "enable_line_numbers": True,
    "enable_auto_detect": True,
    "enable_custom_fonts": False,
    "enable_watermark": False,
    "enable_statistics": False,
    "enable_rate_limiting": True,
}

# ============================================
# Rate Limiting
# ============================================

RATE_LIMITS = {
    "max_requests_per_minute": 10,
    "max_requests_per_hour": 100,
    "cooldown_seconds": 2,
}

# ============================================
# Logging Configuration
# ============================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": "bot.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

# ============================================
# Message Templates
# ============================================

MESSAGES = {
    "welcome": """
🎨 *ברוכים הבאים לבוט המרת קוד לתמונה!*

פשוט שלחו לי קטע קוד ואני אהפוך אותו לתמונה מעוצבת יפהפייה!

*פקודות זמינות:*
/start - הצג הודעת פתיחה
/theme - בחר ערכת נושא
/language - בחר שפת תכנות
/settings - הגדרות נוכחיות
/help - עזרה

תתחילו לשלוח קוד? 🚀
""",
    "help": """
📚 *מדריך שימוש*

*שליחת קוד:*
פשוט שלח את קטע הקוד שלך כהודעה רגילה

*ערכות נושא זמינות:*
🌙 Monokai, 🌃 GitHub Dark, 🧛 Dracula, ❄️ Nord

*שפות תכנות נתמכות:*
Python, JavaScript, TypeScript, Java, C++ ועוד...

*טיפים:*
• הבוט מזהה אוטומטית את שפת התכנות
• שנה נושא דרך /theme
• כל ההגדרות נשמרות אוטומטית
""",
    "processing": "⏳ מעבד את הקוד...",
    "error": "❌ שגיאה ביצירת התמונה. נסה שוב.",
    "rate_limit": "⏰ יותר מדי בקשות. נסה שוב בעוד {seconds} שניות.",
    "code_too_long": "❌ הקוד ארוך מדי. מקסימום {max} תווים.",
}

# ============================================
# Statistics
# ============================================

STATS_CONFIG = {
    "track_usage": True,
    "track_popular_languages": True,
    "track_popular_themes": True,
    "reset_daily": True,
}
