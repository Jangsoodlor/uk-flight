import os
import pandas as pd
from numpy import number

class Model:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.__df = dataframe

    @classmethod
    def remove_outlier(cls, dataframe, column:list = []) -> pd.DataFrame:
        """A class method to remove outliers"""
        temp_df = dataframe.copy()
        if not column:
            column = dataframe.select_dtypes(include=number).columns[3:]
        for outlier_var in column:
            p5 = temp_df[outlier_var].quantile(0.05)
            p95 = temp_df[outlier_var].quantile(0.95)
            temp_df = temp_df[~((temp_df[outlier_var] < p5) | (temp_df[outlier_var] > p95))]
        return temp_df

    @property
    def df(self):
        return self.__df

    def filter_origin_destination(self, temp_df:pd.DataFrame, origin:str, destination:str):
        """Filters the origin and destination of a flight"""
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]
        return temp_df

    def desc_stat_data(self, airport:str):
        """Returns data for Descriptive Statistics"""
        temp_df =  self.__df[self.__df['reporting_airport'] == airport]
        return temp_df['average_delay_mins'].describe()

    def corr_data(self, airline:str, origin:str=None, destination:str=None):
        """Returns data for Correlation Plot"""
        temp_df = self.__df[self.__df['airline_name'] == airline]
        temp_df = self.filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['average_delay_mins', 'previous_year_month_average_delay']]
        return temp_df.corr()

    def bar_graph_data(self, airlines, origin:str=None, destination:str=None):
        """Returns data for bar graph"""
        temp_df = self.__df[self.__df['airline_name'].isin(airlines)]
        temp_df = self.filter_origin_destination(temp_df, origin, destination)
        return temp_df

    def pie_chart_data(self, airline, origin:str=None, destination:str=None):
        """Returns data for pie chart"""
        temp_df = temp_df[temp_df['airline_name'] == airline]
        temp_df = self.filter_origin_destination(temp_df, origin, destination)
        return temp_df.loc[:, ['number_flights_matched', 'number_flights_cancelled']]

    def get_airport_name(self):
        return list(self.__df['reporting_airport'].unique())


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  'data/202401_Punctuality_Statistics_Full_Analysis.csv'))

    df_model = Model(df)
    # print(df_model.corr_data('LOGANAIR LTD'))
    # print(df_model.bar_graph_data(['LOGANAIR LTD', 'EASTERN AIRWAYS']))
    print(df_model.get_airport_name())
