import csv
import numpy as np
from pprint import pprint
import pandas as pd
import math

def calculate_col(df: pd.DataFrame):
    # Zuerst filtern nach Herkunft
    # Dann filtern nach Wohnort
    # Alle einzigartigen Einträge in Herkunft
    herkunfte = list(df['Aus welchem Gebiet stammen Sie (in etwa)?'].unique())
    for herkunft in herkunfte:
        current_unsorted_row: pd.DataFrame = dataframe.loc[dataframe['Aus welchem Gebiet stammen Sie (in etwa)?'] == herkunft]
        for herkunft in herkunfte:
            sorted_row: pd.DataFrame = \
                current_unsorted_row.loc[current_unsorted_row['In welchem Gebiet leben Sie aktuell (in etwa)?'] == herkunft]
            if not sorted_row.empty:
                yield sorted_row

def calculate_unique(df: pd.DataFrame):
    interesting_columns = [
     'acheln',
     'Aschpes',
     'baldowern',
     'beganneft',
     'Boker',
     'dibbern / diwwern',
     'Goi',
     'kapores',
     'lau',
     'malochen',
     'Reibach / Rebbes',
     'schaskeln',
     'Schawwes',
     'schicker / beschickert',
     'Schmu',
     'Schores',
     'Stuss',
     'Toches / Dokes',
     'tof',
     'Zores',
    ]

    herkunft = df['Aus welchem Gebiet stammen Sie (in etwa)?'].iloc[0]
    wohnort = df['In welchem Gebiet leben Sie aktuell (in etwa)?'].iloc[0]

    tabelle = pd.DataFrame(index=interesting_columns, columns=[str(int(i)) for i in range(34)])

    for col in interesting_columns:
        occs: pd.Series = df[col].value_counts()
        for key, val in occs.iteritems():
            for entry in key.split(','):
                shadow_val = val
                entry: str = entry.strip()
                if entry == '':
                    continue
                old_entry = tabelle.loc[col, entry]
                if not math.isnan(old_entry):
                    shadow_val = int(entry) + int(old_entry)
                tabelle.loc[col, entry] = shadow_val
        print(f'Wort {col} hat für Herkunft {herkunft} und Wohnort {wohnort} folgende Schlüssel: ')
        pprint(occs)
    result = tabelle.where(pd.notnull(tabelle), '')
    result.name = herkunft + wohnort
    return result
if __name__ == '__main__':
    with open('table.csv', 'r') as file:
        dataframe = pd.read_csv(file, sep=';', dtype=str)
        names = list(dataframe.columns)

        sorted = dataframe.sort_values(['Aus welchem Gebiet stammen Sie (in etwa)?',
                                        'In welchem Gebiet leben Sie aktuell (in etwa)?'])

        for sorted_row in calculate_col(sorted):
            table = calculate_unique(sorted_row)
            table.to_csv('./tables/'+table.name + '.csv')


