from django.core.management.base import BaseCommand
from bot import main

class Command(BaseCommand):
    help = "Telegram botni ishga tushiradi"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🤖 Bot ishga tushdi!"))
        main()