"""
Notification system for training briefs.

Phase 1: Console/log output (current)
Phase 2: Telegram bot
Phase 3: Google Calendar integration
"""
import os
import logging
from datetime import date
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class Notifier:
    """Base notifier class."""

    def send(self, message: str, title: str = None) -> bool:
        """
        Send a notification.

        Args:
            message: The message content
            title: Optional title/subject

        Returns:
            True if sent successfully, False otherwise
        """
        raise NotImplementedError


class ConsoleNotifier(Notifier):
    """Simple console output notifier."""

    def send(self, message: str, title: str = None) -> bool:
        if title:
            print(f"\n{'=' * 50}")
            print(f"  {title}")
            print(f"{'=' * 50}")
        print(message)
        return True


class LogNotifier(Notifier):
    """Log file notifier."""

    def __init__(self, log_file: str = "morning_briefs.log"):
        self.log_file = log_file

    def send(self, message: str, title: str = None) -> bool:
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"\n{'=' * 50}\n")
                if title:
                    f.write(f"{title}\n")
                f.write(f"Date: {date.today().isoformat()}\n")
                f.write(f"{'=' * 50}\n")
                f.write(message)
                f.write("\n")
            return True
        except Exception as e:
            logger.error(f"Failed to write to log: {e}")
            return False


class TelegramNotifier(Notifier):
    """
    Telegram bot notifier.

    Requires:
    - TELEGRAM_BOT_TOKEN: Your bot token from @BotFather
    - TELEGRAM_CHAT_ID: Your chat ID (get from @userinfobot)
    """

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def send(self, message: str, title: str = None) -> bool:
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
            return False

        try:
            import requests
        except ImportError:
            logger.error("requests package not installed. Run: pip install requests")
            return False

        full_message = message
        if title:
            full_message = f"*{title}*\n\n{message}"

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': full_message,
            'parse_mode': 'Markdown',
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram message sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False


def get_notifier(notifier_type: str = None) -> Notifier:
    """
    Get the appropriate notifier based on configuration.

    Args:
        notifier_type: Override type ('console', 'log', 'telegram')
                      If None, auto-detects based on environment

    Returns:
        Configured Notifier instance
    """
    if notifier_type:
        notifier_type = notifier_type.lower()
    else:
        # Auto-detect based on environment
        if os.getenv('TELEGRAM_BOT_TOKEN'):
            notifier_type = 'telegram'
        else:
            notifier_type = 'console'

    if notifier_type == 'telegram':
        return TelegramNotifier()
    elif notifier_type == 'log':
        return LogNotifier()
    else:
        return ConsoleNotifier()


def send_morning_brief(brief: str) -> bool:
    """
    Send the morning brief via configured notifier.

    Args:
        brief: The morning brief content

    Returns:
        True if sent successfully
    """
    today = date.today()
    title = f"Training Brief - {today.strftime('%A, %B %d')}"

    notifier = get_notifier()
    return notifier.send(brief, title)


# For testing
if __name__ == "__main__":
    test_brief = """## Morning Brief - Monday, 2026-01-05

**Recovery:** RHR=42 | BB=75 | Readiness=68 (MODERATE)

**Yesterday:** Completed planned long run

**Pillars:** All compliant

**Today:** Strength Training
  Duration: 45 mins

**Next Event:** Cape Town Half Marathon in 69 days
"""

    send_morning_brief(test_brief)
