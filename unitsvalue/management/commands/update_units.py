# crawler/management/commands/update_units.py
from django.core.management.base import BaseCommand
from unitsvalue.models import Fund, LivePercentUnit
from unitsvalue.utils import process_funds  # Import the process function

class Command(BaseCommand):
    help = 'Scrapes unit_values from funds and saves them to the database.'

    def handle(self, *args, **kwargs):
        funds = Fund.objects.all()

        if not funds:
            self.stdout.write(self.style.WARNING('No funds found to scrape.'))
            return

        for fund in funds:
            self.stdout.write(f'Scraping: {fund.url}')
            self._process_fund(fund)

    def _process_fund(self, fund):
        """Processes the fund and saves the unit_value."""
        try:
            percent_unit = process_funds(fund)
            if percent_unit is not None:
                self._save_unit_value(fund, percent_unit)
                self.stdout.write(self.style.SUCCESS(f'Successfully scraped and saved unit_values for {fund.url}.'))
            else:
                self.stdout.write(self.style.WARNING(f'Could not find required elements on {fund.url}.'))
        except ValueError as ve:
            self.stdout.write(self.style.ERROR(str(ve)))

    def _save_unit_value(self, fund, percent_unit):
        """Updates the existing unit_value or creates a new one if it doesn't exist."""
        # Attempt to update the existing unit_value
        unit_value, created = LivePercentUnit.objects.update_or_create(
            funds_id=fund.id,
            defaults={'text': percent_unit}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created a new unit_value for {fund.url}.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated the unit_value for {fund.url}.'))