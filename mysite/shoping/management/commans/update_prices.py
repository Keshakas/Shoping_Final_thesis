import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run web scraping scripts to update CSV files'

    def handle(self, *args, **kwargs):
        try:
            subprocess.run(['python', 'shoping/scraping/barbora_scraper_all.py'], check=True)
            subprocess.run(['python', 'shoping/scraping/iki_scraper_all.py'], check=True)
            subprocess.run(['python', 'shoping/scraping/rimi_scraper_all.py'], check=True)
            self.stdout.write(self.style.SUCCESS('Prices updated successfully!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))