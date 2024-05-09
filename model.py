"""Contains models of the program"""
import os
import pandas as pd
from numpy import number

class Model:
    """The model class"""
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.__df = dataframe[dataframe['number_flights_matched'] > 0]
        self.__df.reset_index(inplace=True)

    @classmethod
    def remove_outlier(cls, dataframe, column:list = None) -> pd.DataFrame:
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
        """Returns the dataframe"""
        return self.__df

    def __filter_origin_destination(self, temp_df:pd.DataFrame, origin:str, destination:str):
        """Filters the origin and destination of a flight"""
        if origin:
            temp_df = temp_df[temp_df['reporting_airport'] == origin]
        if destination:
            temp_df = temp_df[temp_df['origin_destination'] == destination]
        return temp_df

    def desc_stat_data(self, origin:str=''):
        """Returns data for Descriptive Statistics"""
        temp_df = self.df.copy()
        if origin:
            title = f'Average delay of flights departed from {origin} (minutes)\n'
            temp_df =  temp_df[temp_df['reporting_airport'] == origin]
        else:
            title = 'Average delay of all Flights (minutes)\n'            
        return title + str(temp_df['average_delay_mins'].describe())[:-41]

    def corr_data(self, airline:str='', origin:str='', destination:str=''):
        """Returns data for Correlation Plot"""
        temp_df = self.df.copy()
        title = 'Average delay of All Airlines'
        if airline:
            temp_df = self.df[self.df['airline_name'] == airline]
            title = title[:13] + f' of {airline}'
            if origin:
                title += f' from {origin}'
            if destination:
                title += f' to {destination}'

        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['average_delay_mins', 'previous_year_month_average_delay']]
        corr = temp_df.corr()['average_delay_mins']['previous_year_month_average_delay']
        coefficient = f'\nCorrelation Coefficient = {corr:.4f}'
        return temp_df, title+coefficient

    def bar_graph_data(self, airlines:list, compare, origin:str='', destination:str=''):
        """Returns data for bar graph"""
        if not airlines:
            raise ValueError('Please select at least 1 airline')
        temp_df = self.df[self.df['airline_name'].isin(airlines)]
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['airline_name', compare]]
        temp_df = temp_df.groupby('airline_name').mean()
        temp_df = temp_df.reset_index()
        title = f'Comparing {compare}'
        return (temp_df.iloc[:,0], temp_df.iloc[:,1]), title

    def pie_chart_data(self, airline:str='', origin:str='', destination:str=''):
        """Returns data for pie chart"""
        temp_df = self.df.copy()
        title = 'Flights cancellation rate'
        if airline:
            temp_df = self.df[self.df['airline_name'] == airline]
            title += f' of {airline}'
        if origin:
            title+= f' from {origin}'
        if destination:
            title += f' to {destination}'
        temp_df = self.__filter_origin_destination(temp_df, origin, destination)
        temp_df = temp_df.loc[:, ['number_flights_matched', 'number_flights_cancelled']]
        return temp_df.sum(), title

    def distribution_data(self, airline:str, origin:str, destination:str):
        """Returns data for distribution graph"""
        if not(airline and origin and destination):
            raise ValueError('Please fill in all fields')
        temp_df = self.df[self.df['airline_name'] == airline]
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
        title = f'Histogram of Delays of {airline}'
        return temp_df, title

    def __busiest_flight_route(self):
        """Returns the busiest flight routes"""
        df2 = self.df.sort_values(by='number_flights_matched', ascending=False)
        df2.reset_index(inplace=True)
        return df2.loc[0, :]

    def __busiest_airlines(self) -> str:
        """returns top 3 airlines by number of flights"""
        airlines = self.df.groupby('airline_name')['number_flights_matched'].sum()
        airlines.sort_index(ascending=False, inplace=True)
        return list(airlines.index[0:3])

    def data_storytelling(self):
        """Returns graphs for data storytelling tab"""
        pie, pie_title = self.pie_chart_data()
        corr, corr_title = self.corr_data()
        box = Model.remove_outlier(self.df)['average_delay_mins']
        box_title = 'Average Delays of all Flights'
        df2 = self.__busiest_flight_route()
        hist, hist_title = self.distribution_data(df2['airline_name'],
                                      df2['reporting_airport'],
                                      df2['origin_destination'])
        hist_title = 'Delay of the most Frequent Flight Route'
        df3 = self.__busiest_airlines()
        cancel, cancel_title = self.bar_graph_data(airlines=df3, compare='flights_cancelled_percent')
        delay, delay_title = self.bar_graph_data(airlines=df3, compare='average_delay_mins')
        cancel_title = 'Cancellation Rate of\ntop 3 airlines with the most flights'
        delay_title = 'Delays of top 3 airlines\nwith the most flights'

        return [[pie, pie_title] ,
                [corr, corr_title],
                [box, box_title],
                [hist, hist_title],
                [cancel, cancel_title],
                [delay, delay_title]], self.desc_stat_data()

    def get_selector_data(self, name:str, filters:dict=None):
        """Get the appropriate data for a selector object"""
        translate = {'Airline':'airline_name',
                          'Origin (Optional)' : 'reporting_airport',
                          'Origin' : 'reporting_airport',
                          'Destination (Optional)' : 'origin_destination',
                          'Destination' : 'origin_destination'}

        temp_df = self.df.copy()
        if filters:
            for key, val in filters.items():
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
    import matplotlib.pyplot as plt
    import seaborn as sns
    df = pd.read_csv(os.path.join(os.getcwd(),
                                'data/202401_Punctuality_Statistics_Full_Analysis.csv'))

    m = Model(df)
    a = m.desc_stat_data()[:-41]
    b = a.split('\n')
    print(b)
