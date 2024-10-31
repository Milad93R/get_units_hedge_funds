# crawler/management/commands/save_percent_unit.py
from django.core.management.base import BaseCommand
import jdatetime  # Use jdatetime for Jalali dates
from unitsvalue.models import Fund, PercentUnit
from unitsvalue.utils import process_funds  # Import the process function

class Command(BaseCommand):
    help = 'Calculates percent values using existing logic and saves them to DataRecord.'

    def handle(self, *args, **kwargs):
        funds = Fund.objects.all()

        if not funds:
            self.stdout.write(self.style.WARNING('No funds found to process.'))
            return

        for fund in funds:
            self.stdout.write(f'Processing: {fund.url}')
            self._process_fund(fund)

    def _process_fund(self, fund):
        """Calculates the percent value and saves it to DataRecord."""
        try:
            percent_unit = process_funds(fund)  # Use the utility function
            if percent_unit is not None:
                self._save_data_record(fund, percent_unit)
                self.stdout.write(self.style.SUCCESS(f'Successfully processed data for {fund.url}.'))
            else:
                self.stdout.write(self.style.WARNING(f'Could not find required elements on {fund.url}.'))
        except ValueError as ve:
            self.stdout.write(self.style.ERROR(str(ve)))

    def _save_data_record(self, fund, percent_unit):
        """Saves a new record if it doesn't already exist for today's date."""
        # Get the current date in Jalali format (Ymd)
        current_jalali_date = jdatetime.datetime.now().strftime('%Y/%m/%d')

        # Check if a record with the current date already exists
        if not PercentUnit.objects.filter(funds=fund, datetime=current_jalali_date).exists():
            # Create a new DataRecord
            PercentUnit.objects.create(
                funds_id=fund.id,
                percent_unit=percent_unit,
                datetime=current_jalali_date
            )
            self.stdout.write(self.style.SUCCESS(f'Added new record for {fund.url} on {current_jalali_date}.'))
        else:
            self.stdout.write(self.style.WARNING(f'Record for {fund.url} on {current_jalali_date} already exists.'))