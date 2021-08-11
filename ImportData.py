# Import the libraries
import pandas as pd
import glob
import os


def import_data(variable):
    """
    :param variable: Type of data (offensive/distribution/defensive).
    :return df: Dataframe with data from the available match/es.
    """

    path = './data/data_racing'

    all_files = glob.glob(os.path.join(path, '*.xlsx'))

    li = []
    for filename in all_files:
        df = pd.read_excel(filename, sheet_name=variable, engine='openpyxl')
        string = str(filename)
        ind_start = string.index('Jo')
        ind_end = string.index('.x')
        string_name = string[ind_start:ind_end]
        game = string_name.split('-')[1].strip()
        weekday = string_name.split('-')[0].strip()
        df['weekday'] = weekday.split()[1].strip()
        df['weekday'] = df['weekday'].apply(pd.to_numeric)
        df['home_team'] = game.split('VS')[0].strip()
        df['away_team'] = game.split('VS')[1].strip()

        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)

    return df


def import_event_data(file_path):
    """
    :param file_path: Path of the event data.
    :return df: Dataframe with event data from the available match/es.
    """

    all_files = glob.glob(os.path.join(file_path, '*.csv'))

    li = []
    for filename in all_files:
        df = pd.read_csv(filename)
        string = str(filename)
        ind_start = string.index('Jo')
        ind_end = string.index('.c')
        string_name = string[ind_start:ind_end]
        game = string_name.split('-')[1].strip()
        weekday = string_name.split('-')[0].strip()
        df['weekday'] = weekday.split()[1].strip()
        df['weekday'] = df['weekday'].apply(pd.to_numeric)
        df['home_team'] = game.split('VS')[0].strip()
        df['away_team'] = game.split('VS')[1].strip()

        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)

    return df


def update_data(new_df, df_total_name):
    """
    :param new_df: Dataframe with the weekday data.
    :param df_total_name: Dataframe with the data from the past weekdays.
    :return df_data_updated: Dataframe with the new weekday added.
    """

    df_past_weekdays = pd.read_csv(f'./data/data_total/{df_total_name}.csv')
    df_data_updated = pd.concat([df_past_weekdays, new_df], ignore_index=True)

    df_data_updated.to_csv(
        f'./data/data_total/{df_total_name}.csv', index=False)

    return df_data_updated
