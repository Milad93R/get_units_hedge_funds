# unitsvalue/views.py
from django.shortcuts import render
import pandas as pd
from .models import LivePercentUnit,PercentUnit, Fund

def liveValues(request):
    live_percent_units = LivePercentUnit.objects.all()  # Fetch live_percent_units from the database
    live_percent_units_list = list(live_percent_units)  # Convert to a list
    print(live_percent_units_list)
    return render(request, "live_values.html", {"live_percent_units": live_percent_units})

def historyValues(request):
    # Fetch all data records
    percent_unit = PercentUnit.objects.all()

    # Create a DataFrame
    df = pd.DataFrame(list(percent_unit.values('datetime', 'funds_id', 'percent_unit')))

    # Pivot the DataFrame
    df_pivot = df.pivot_table(index='datetime', columns='funds_id', values='percent_unit')

    # Fetch funds names for proper column naming
    fundss = Fund.objects.all()
    funds_mapping = {funds.id: funds.name for funds in fundss}

    # Rename columns using the funds names
    df_pivot.rename(columns=funds_mapping, inplace=True)
    df_pivot.fillna('-', inplace=True) 
    # Convert the pivoted DataFrame to a dictionary
    records_dict = df_pivot.to_dict(orient='index')
    # Extract headers and data rows
    headers = list(next(iter(records_dict.values())).keys())
    rows = []

    for date, records in records_dict.items():
        row = [date] + [records.get(header, 'N/A') for header in headers]
        rows.append(row)
    # Prepare context for the template
    context = {
        'headers': ['تاریخ'] + headers,
        'rows': rows,
    }
    return render(request, 'history_values.html', context)