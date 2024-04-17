import os
import pandas as pd
from numpy import number

class Model:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @classmethod
    def remove_outlier(cls, df, column:list = []) -> pd.DataFrame:
        """A class method to remove outliers"""
        temp_df = df.copy()
        if not column:
            column = df.select_dtypes(include=number).columns[3:]
        for outlier_var in column:
            p5 = temp_df[outlier_var].quantile(0.05)
            p95 = temp_df[outlier_var].quantile(0.95)
            temp_df = temp_df[~((temp_df[outlier_var] < p5) | (temp_df[outlier_var] > p95))]
        return temp_df

    def distribution_graph_data(self, airline:str = '', origin:str = '', destination:str = '') -> pd.DataFrame:
        temp_df = self.df.copy()
        new_columns = ['flights_more_than_15_minutes_early_percent',
                       'flights_15_minutes_early_to_1_minute_early_percent',
                       'flights_0_to_15_minutes_late_percent',
                       'flights_between_16_and_30_minutes_late_percent',
                       'flights_between_31_and_60_minutes_late_percent',
                       'flights_between_61_and_120_minutes_late_percent',
                       'flights_between_121_and_180_minutes_late_percent',
                       'flights_between_181_and_360_minutes_late_percent',
                       'flights_more_than_360_minutes_late_percent', 'airline_name']

        if airline:
            temp_df = temp_df[temp_df['airline_name'] == airline]
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]

        temp_df = temp_df.drop([i for i in temp_df.columns if i not in new_columns], axis=1)
        return temp_df.groupby('airline_name').mean()

    def __str__(self) -> str:
        return self.df.__str__()

    def airline_flaw_data(self, airlines:list = [], origin:str = '', destination:str = '') -> pd.DataFrame:
        temp_df = self.df.copy()
        new_columns = ['average_delay_mins',
                       'number_flights_cancelled',
                       'airline_name']

        if airlines:
            temp_df = temp_df[temp_df['airline_name'].isin(airlines)]
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]

        temp_df = temp_df.drop([i for i in temp_df.columns if i not in new_columns], axis=1)
        return temp_df.groupby('airline_name').mean()

    def correlation_data(self, origin:str = '', destination:str = '') -> pd.DataFrame:
        temp_df = df.copy()
        new_columns = ['previous_year_month_average_delay', 'average_delay_mins']
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]

        temp_df = temp_df.drop([i for i in temp_df.columns if i not in new_columns])
        return temp_df

    def descriptive_stats_data(self):
        return self.df['average_delay_mins'].describe()


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(), 'data/202401_Punctuality_Statistics_Full_Analysis.csv'))
    # print(df)
    # df2 = Model.remove_outlier(df)
    # print(df2)
    df1 = Model(df)
    # df3 = df1.distribution_graph_data(origin='SOUTHAMPTON', airline='BA CITYFLYER LTD', destination='EDINBURGH')
    df3 = df[df['airline_name'] == 'WIDEROE FLYVESELSKAP A/S']['number_flights_cancelled']
    print(df1.descriptive_stats_data())
