# crawler/management/commands/convert_xlsx_to_df.py
import os

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from unitsvalue.models import PercentUnit, Fund


class Command(BaseCommand):
    help = 'Converts XLSX files to a pandas DataFrame and saves records to the database.'

    def handle(self, *args, **kwargs):
        for i in range(10):
            file_path = self._get_file_path(i)

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f'File does not exist: {file_path}'))
                continue

            try:
                df = self._read_excel(file_path)
                self.stdout.write(self.style.SUCCESS('Successfully read the Excel file.'))

                df_processed = self._process_dataframe(df)
                fund = self._get_fund(i)

                # Clear existing records for the current fund
                self._clear_existing_records(fund)

                # Save new records to the database
                self._save_records(df_processed, fund)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing file {file_path}: {e}'))

    def _get_file_path(self, index):
        """Constructs the file path for the given index."""
        return os.path.join(settings.BASE_DIR, 'unitsvalue', 'static', 'xlsxs', f'DownloadNavChartList-{index}.xlsx')

    def _read_excel(self, file_path):
        """Reads an Excel file into a DataFrame."""
        return pd.read_excel(file_path)

    def _process_dataframe(self, df:pd.DataFrame):
        """Processes the DataFrame for the required columns and calculations."""
        df_processed = df.iloc[:, -7:-2]
        df_processed.columns = ['base_unit', 'Column2', 'super_unit', 'Column4', 'datetime']
        df_processed['base_unit'] = pd.to_numeric(df_processed['base_unit'], errors='coerce')
        df_processed['super_unit'] = pd.to_numeric(df_processed['super_unit'], errors='coerce')

        # Calculating percent_unit while avoiding division by zero
        df_processed['percent_unit'] = df_processed['base_unit'] / df_processed['super_unit'].replace(0, pd.NA) * 100
        df_processed['percent_unit'] = df_processed['percent_unit'].round(1)
        df_processed = df_processed[['percent_unit', 'datetime']].iloc[3:]

        return df_processed

    def _get_fund(self, index):
        """Fetches the corresponding fund instance."""
        try:
            return Fund.objects.get(id=index)
        except Fund.DoesNotExist:
            raise ValueError(f'fund with ID {index} does not exist.')

    def _clear_existing_records(self, fund):
        """Deletes existing DataRecord instances for the given fund."""
        PercentUnit.objects.filter(funds=fund).delete()

    def _save_records(self, df_processed:pd.DataFrame, fund):
        """Converts the DataFrame to DataRecord instances and saves them in bulk."""
        records = df_processed.to_dict('records')
        data_records = [
            PercentUnit(funds=fund, percent_unit=record['percent_unit'], datetime=record['datetime'])
            for record in records
        ]
        PercentUnit.objects.bulk_create(data_records)
        self.stdout.write(self.style.SUCCESS('Successfully saved records to the database.'))