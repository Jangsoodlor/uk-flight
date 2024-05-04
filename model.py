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

    def __filter_origin_destination(self, temp_df:pd.DataFrame, origin:str, destination:str):
        """Filters the origin and destination of a flight"""
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]
        return temp_df

    def desc_stat_data(self, origin:str):
        """Returns data for Descriptive Statistics"""
        temp_df =  self.__df[self.__df['reporting_airport'] == origin]
        return temp_df['average_delay_mins'].describe()

    def corr_data(self, airline:str, origin:str=None, destination:str=None):
        """Returns data for Correlation Plot"""
        temp_df = self.__df[self.__df['airline_name'] == airline]
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['average_delay_mins', 'previous_year_month_average_delay']]
        title = f'Average delay of {airline}'
        if origin:
            title += f' from {origin}'
        if destination:
            title += f' to {destination}'
        corr = temp_df.corr()['average_delay_mins']['previous_year_month_average_delay']
        coefficient = f'Correlation Coefficient = {corr}'
        return temp_df, (title, coefficient)

    def bar_graph_data(self, airlines, compare, origin:str=None, destination:str=None):
        """Returns data for bar graph"""
        temp_df = self.__df[self.__df['airline_name'].isin(airlines)]
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['airline_name', compare]]
        title = f'Comparing {compare}'
        return (temp_df.iloc[:,0], temp_df.iloc[:,1]), title

    def pie_chart_data(self, airline:str, origin:str=None, destination:str=None):
        """Returns data for pie chart"""
        temp_df = self.__df[self.__df['airline_name'] == airline]
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['number_flights_matched', 'number_flights_cancelled']]
        series = temp_df.sum()
        title = f'Flights cancellation of {airline} from {origin} to {destination}'
        return series, title

    def distribution_data(self, airline:str, origin:str, destination:str):
        """Returns data for distribution graph"""
        temp_df = self.__df[self.__df['airline_name'] == airline]
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        filters = ['flights_more_than_15_minutes_early_percent',
                   'flights_15_minutes_early_to_1_minute_early_percent',
                   'flights_0_to_15_minutes_late_percent',
                   'flights_between_16_and_30_minutes_late_percent',
                   'flights_between_31_and_60_minutes_late_percent',
                   'flights_between_61_and_120_minutes_late_percent',
                   'flights_between_121_and_180_minutes_late_percent',
                   'flights_between_181_and_360_minutes_late_percent',
                   'flights_more_than_360_minutes_late_percent']
        temp_df = temp_df.loc[:, filters]
        temp_df = temp_df.reset_index()
        temp_df = temp_df.loc[0]
        temp_df = temp_df.reset_index()
        temp_df = temp_df.loc[1:9]
        temp_df.columns = ['Interval', 'Percent']
        temp_df.groupby('Interval')
        title = f'Distribution of Delay Intervals of {airline}'
        return temp_df, title

    def get_selector_data(self, name:str, filter:dict=None):
        translate = {'Airline':'airline_name',
                          'Origin (Optional)' : 'reporting_airport',
                          'Origin' : 'reporting_airport',
                          'Destination (Optional)' : 'origin_destination',
                          'Destination' : 'origin_destination'}

        temp_df = self.__df.copy()
        if filter:
            for key, val in filter.items():
                column = translate[key]
                if val:
                    temp_df = temp_df[temp_df[column] == val]
        return list(temp_df[translate[name]].unique())

    def get_graph_data(self, name, options):
        """Get the data depending on the graph's type"""
        translate = {'Corr':self.corr_data,
                     'Pie' : self.pie_chart_data,
                     'Dist' : self.distribution_data
                     }
        airline = None
        origin = None
        destination = None
        for key, val in options.items():
            if 'airline' in key.lower():
                airline = val
            elif 'origin' in key.lower():
                origin = val
            elif 'destination' in key.lower():
                destination = val
        if 'compare' in options:
            compare = options['compare']
            return self.bar_graph_data(airline, compare, origin, destination)
        return translate[name](airline, origin, destination)

if __name__ == '__main__':
    df = df = pd.read_csv(os.path.join(os.getcwd(),
                                'data/202401_Punctuality_Statistics_Full_Analysis.csv'))
    m = Model(df)
    a = m.bar_graph_data(['WIZZ AIR', 'EASTERN AIRWAYS'], 'average_delay_mins')
    print(a[0])
