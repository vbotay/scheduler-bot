import os


TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Maximal amount of members for event
MEMBERS_MAX = os.environ.get('MEMBERS_MAX', 4)

# Duration of event
DEFAULT_DURATION = os.environ.get('DEFAULT_DURATION', 30)
