from django.core.management.base import BaseCommand
import asyncio
from apps.main.telegram_bot import create_bot_app

class Command(BaseCommand):
    help = 'Запускает Telegram-бота'

    def handle(self, *args, **options):
        self.stdout.write("Запуск Telegram-бота...")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        app = create_bot_app()
        try:
            loop.run_until_complete(app.run_polling())
        except KeyboardInterrupt:
            self.stdout.write("Остановка бота вручную.")
