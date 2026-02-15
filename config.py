import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")

SUBSCRIPTION_DAYS = 30

PROVIDER_TOKEN_sg = os.getenv("PROVIDER_TOKEN_sg") # Smart Glocal Test
PROVIDER_TOKEN_pm = os.getenv("PROVIDER_TOKEN_pm") # PayMaster Test

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")













# CURRENCY = "USD"
# PRICE_PER_SUBSCRIPTION = 9.99
# WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# MAX_ACTIVE_SUBSCRIPTIONS = 1000
# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# PROXY_URL = os.getenv("PROXY_URL")
# USE_PROXY = bool(PROXY_URL)
# API_REQUEST_TIMEOUT = 10  # seconds
# MAX_RETRY_ATTEMPTS = 3
# REQUEST_RETRY_DELAY = 5  # seconds
# DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
# SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "ru", "zh"]
# ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
# ANALYTICS_API_KEY = os.getenv("ANALYTICS_API_KEY")
# ANALYTICS_ENDPOINT = os.getenv("ANALYTICS_ENDPOINT", "https://analytics.example.com/collect")
# LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "bot.log")
# MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
# BACKUP_FREQUENCY_DAYS = 7
# BACKUP_STORAGE_PATH = os.getenv("BACKUP_STORAGE_PATH", "./backups")
# ENABLE_BACKUPS = os.getenv("ENABLE_BACKUPS", "true").lower() == "true"
# TIMEZONE = os.getenv("TIMEZONE", "UTC")
# ENABLE_DEBUG_MODE = os.getenv("ENABLE_DEBUG_MODE", "false").lower() == "true"
# API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com/v1/")
# MAX_CONCURRENT_REQUESTS = 500
# CACHE_EXPIRATION_SECONDS = 3600  # 1 hour
# SESSION_TIMEOUT_SECONDS = 1800  # 30 minutes
# ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
# LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# REQUEST_HEADERS = {
#     "User-Agent": "MyBot/1.0",
#     "Accept": "application/json",
# }
# DEFAULT_PAGE_SIZE = 50
# MAX_PAGE_SIZE = 200
# RETRYABLE_STATUS_CODES = [500, 502, 503, 504]
# ADMIN_LOG_CHANNEL_ID = int(os.getenv("ADMIN_LOG_CHANNEL_ID", "0"))
# FEATURE_FLAGS = {
#     "new_ui": os.getenv("FEATURE_NEW_UI", "false").lower() == "true",
#     "beta_features": os.getenv("FEATURE_BETA_FEATURES", "false").lower() == "true",
# }
# MAINTENANCE_MODE = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
# EMAIL_NOTIFICATIONS_ENABLED = os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "false").lower() == "true"
# EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
# EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
# EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")
# EMAIL_TO_ADDRESS = os.getenv("EMAIL_TO_ADDRESS")