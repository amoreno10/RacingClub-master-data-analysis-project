# Import the functions from ImportData.py
from ImportData import *

# Loop to import all the data from the three variables.
sheets = ['offensive', 'distribution', 'defensive']
dfs = [import_data(sheet) for sheet in sheets]
offensive_data = dfs[0]
distribution_data = dfs[1]
defensive_data = dfs[2]

# Merge the three dataframes.
df_total = offensive_data.merge(distribution_data, on=['Num.', 'Name', 'Pos.', 'Rating', 'Minutes Played',
                                                       'weekday', 'home_team', 'away_team'])
df_total = df_total.merge(defensive_data, on=['Num.', 'Name', 'Pos.', 'Rating', 'Minutes Played',
                                              'weekday', 'home_team', 'away_team'])

# Reorder the columns.
columns = ['Num.', 'Name', 'Pos.', 'Rating', 'Minutes Played', 'weekday', 'home_team',
           'away_team', 'Goals', 'Assists', 'Shots', 'Shots On Target', 'Blocked Shots',
           'Shots Off Target', 'Shots Inside PA', 'Shots Outside PA',
           'Offsides', 'Freekicks', 'Corners', 'Throw-Ins',
           'Take-Ons Success', 'Take-Ons Total', 'Passes Success',
           'Passes Total', 'Pass Accuracy(%)',
           'Key Passes', 'Passes In Final Third Success',
           'PassesInFinalThird Total', 'Passes In Middle Third Success',
           'PassesInMiddleThird Total', 'Passes In Defensive Third Success',
           'PassesInDefensiveThird Total', 'Long Passes Success',
           'LongPasses Total', 'Medium Range Passes Success',
           'MediumRangePasses Total', 'Short Passes Success',
           'ShortPasses Total', 'Passes Forward Success',
           'PassesForward Total', 'Passes Sideways Success',
           'PassesSideways Total', 'Passes Backward Success',
           'PassesBackward Total', 'Crosses Success', 'Crosses Total',
           'Control Under Pressure', 'Tackles Success', 'Tackles Total',
           'Aerial Duels Success', 'AerialDuels Total',
           'Ground Duels Success', 'GroundDuels Total', 'Interceptions',
           'Clearances', 'Interventions', 'Recoveries', 'Blocks', 'Mistakes',
           'Fouls', 'Fouls Won', 'Yellow Cards', 'Red Cards']

df_total = df_total[columns]
df_total = df_total.sort_values(by=['weekday'], ascending=True)
df_total.drop(columns=['Num.', 'Rating'], inplace=True)
df_total = df_total[df_total['Pos.'] != 'GK']

df_total = update_data(df_total, 'data_racing_per_match')

# Export the Racing data per match.
df_total.to_csv('./data/data_total/data_racing_per_match.csv', index=False)

# Group data by Name to get the summary from all the games.
data_grouped = df_total.groupby('Name').sum().reset_index()
data_grouped.drop(columns=['weekday'], inplace=True)
data_grouped['Pass Accuracy(%)'] = round(
    data_grouped['Passes Success']/data_grouped['Passes Total'], 2)

# Export Racing data total.
data_grouped.to_csv('./data/data_total/data_racing_total.csv', index=False)

# Import event data
event_data = import_event_data('./data/event_data')

# Processing of event data
event_data = event_data.rename(
    columns={'relative_x': 'end_x', 'relative_y': 'end_y'})


def join_players_name(df, column_name, column_last_name):
    """
    :param df: Event data dataframe.
    :param column_name: Column with the first name.
    :param column_last_name: Column with the last name.
    :return df: Event data dataframe with those columns merged in one.
    """

    df[column_name] = df[column_name] + ' ' + df[column_last_name]
    df.drop(column_last_name, axis=1, inplace=True)

    return df


# Join both columns
event_data = join_players_name(event_data, 'player_name', 'player_last_name')
event_data = join_players_name(
    event_data, 'relative_player_name', 'relative_player_last_name')

# Filter unnecessary data
event_data.drop(event_data[event_data['filtered_event_types']
                           == 'passReceived'].index, inplace=True)
event_data.dropna(subset=['player_id'], inplace=True)

# Reorder the columns
columns_event_data = ['weekday', 'home_team', 'away_team', 'id', 'match_id',
                      'match_full_time', 'extra_full_time',
                      'player_id', 'back_number', 'player_name', 'team_id', 'team_name',
                      'event_time', 'event_period', 'is_side_changed', 'event_types',
                      'filtered_event_types', 'x', 'y', 'relative_player_id',
                      'relative_player_name', 'end_x', 'end_y']

event_data = event_data[columns_event_data]
event_data['filtered_event_types'] = event_data['filtered_event_types'].apply(
    lambda x: str(x).split()[0])
event_data[['x', 'y', 'end_x', 'end_y']
           ] = event_data[['x', 'y', 'end_x', 'end_y']] * 100

# Export event data
event_data.to_csv('./data/data_total/event_data_racing.csv', index=False)
