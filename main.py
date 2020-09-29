import csv
import numpy as np
from pprint import pprint
import pandas as pd
import math

def calculate_col(df: pd.DataFrame):
    """
    Diese Funktion filtert aus einem DataFrame folgende DataFrames, die zuerst nach dem Herkunftsort und
    dann nach dem Wohnort Gruppiert werden.
    Also: Bitburg-Bitburg
          Bitburg-Köln
          usw
    :param df: der zu filternde Frame
    :return: FilterFrame Iterator
    """

    # Alle einzigartigen Herkunftsorte
    herkunfte = list(df['Aus welchem Gebiet stammen Sie (in etwa)?'].unique())
    for herkunft in herkunfte:

        # Zuerst den Frame der Herkunftsorte kriegen
        current_unsorted_row: pd.DataFrame = dataframe.loc[dataframe['Aus welchem Gebiet stammen Sie (in etwa)?'] == herkunft]
        for herkunft in herkunfte:

            # Anschließend nach Wohnort sortieren
            sorted_row: pd.DataFrame = \
                current_unsorted_row.loc[current_unsorted_row['In welchem Gebiet leben Sie aktuell (in etwa)?'] == herkunft]
            if not sorted_row.empty:
                yield sorted_row

def calculate_unique(df: pd.DataFrame):

    # Diese hier interessieren uns
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

    # Für Print und Namenszwecke
    herkunft = df['Aus welchem Gebiet stammen Sie (in etwa)?'].iloc[0]
    wohnort = df['In welchem Gebiet leben Sie aktuell (in etwa)?'].iloc[0]

    # Neue Tabelle mit Indizes = Wörter und Spaltennamen = Zahlen von 1 - 34
    tabelle = pd.DataFrame(index=interesting_columns, columns=[str(int(i)) for i in range(34)])

    for col in interesting_columns:
        # Vorkommnisse von Schlüsseln
        occs: pd.Series = df[col].value_counts()
        for key, val in occs.iteritems():
            # Manche Schlüssel sind im Format 8, 9
            for entry in key.split(','):
                # Shadowing val to not lose it when changing in later on old entry
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

        # Sort by these columns first
        sorted = dataframe.sort_values(['Aus welchem Gebiet stammen Sie (in etwa)?',
                                        'In welchem Gebiet leben Sie aktuell (in etwa)?'])

        for sorted_row in calculate_col(sorted):
            table = calculate_unique(sorted_row)
            table.to_csv('./tables/'+table.name + '.csv')


