import heapq
import pandas as pd

class Pathfinder:
    """Find a path from one airport to another based on flights cancellation and average delays.
    This is the same algorithm in 01219217 Data Structure and Algorithm I Course Project with some
    modifications to return the flight route instead of printing it."""
    def __init__(self, df):
        self.df = df
        self.adj_cancel = self.read_csv_to_adj_list(0)
        self.adj_delay = self.read_csv_to_adj_list(1)

    def read_csv_to_adj_list(self, index):
        """Reads the dataset and convert it into an adjoint list using python dictionary
        Due to Python's limitations, I could not implement multiple edges from the same origin to
        the same destination. Instead, the algorithm will decide what edge it should choose

        If there exists another edge that has less "index" (see below) than the current one,
        replaces the current edge.

        If there exists another edge that has the same "index" as the current one,
        and the other "index" is less than the current one, replaces the current edge.

        Args:
            index (int): aka. "Weight". 0 = cancellation rate, 1 = average delay in minutes

        Returns:
            The adjoint dict in the following format
            {
                'Origin1' : {'Destination1': [cancel_rate, average_delay_mins, airline_name],
                            'Destination2': [cancel_rate, average_delay_mins, airline_name]}

                'Origin2' : {} (In case that that airport has no outbound routes)
            }
        """
        adj = {}

        for i in range(len(self.df)):
            origin = self.df.loc[i, 'reporting_airport']
            destination = self.df.loc[i, 'origin_destination']
            cancel_rate = self.df.loc[i, 'flights_cancelled_percent']
            average_delay_mins = self.df.loc[i, 'average_delay_mins']
            airline_name = self.df.loc[i, 'airline_name']
            thing = [cancel_rate, average_delay_mins, airline_name]

            if origin not in adj:
                adj[origin] = {destination: thing}

            elif destination in adj[origin]:
                if adj[origin][destination][index] > thing[index]:
                    adj[origin][destination] = thing
                elif adj[origin][destination][index] == thing[index]\
                and adj[origin][destination][(index+1)%2] > thing[(index+1)%2]:
                    adj[origin][destination] = thing
            else:
                adj[origin][destination] = thing

        for i in range(len(self.df)):
            if self.df.loc[i, 'origin_destination'] not in adj:
                adj[self.df.loc[i, 'origin_destination']] = {}
        return adj

    def dijkstra(self, adj_list, s, index=0):
        """Dijkstra's Algorithm"""
        dist = {node:[float('inf'), float('inf')] for node in adj_list}
        dist[s] = [0,0]
        parent = {}
        parent_airline = {}
        bag = [(s, [0,0])]

        while bag:
            u, dist_u = heapq.heappop(bag)
            if dist_u[index] > dist[u][index]:
                continue
            for v, w in adj_list[u].items():
                if dist_u[index] + w[index] < dist[v][index]:
                    dist[v][index] = dist_u[index] + w[index]
                    # Keep tracks of the other attribute
                    dist[v][(index+1)%2] = dist_u[(index+1)%2] + w[(index+1)%2]
                    parent[v] = u
                    parent_airline[v] = w[2]    # keep tracks of the airline
                    heapq.heappush(bag, (v, [dist_u[index] + w[index], dist_u[(index+1)%2] + w[(index+1)%2]]))
        return parent, parent_airline, dist

    def linear_search(self, adj_list,start,destination):
        """Linear Search Algorithm"""
        try:
            direct_path = adj_list[start][destination]
            return direct_path
        except KeyError:
            return None

    def return_linear(self, start, stop, direct_path):
        """Return Linear Search Results"""
        airline = direct_path[2]
        dist = direct_path[0:2]
        return [[airline, start, stop, dist[0], dist[1]]]

    def return_dijkstra(self, start, stop, parent, parent_airline, delay_or_cancel):
        """Return Dijkstra's Algorithm search results"""
        airline_stop = ''
        stop_list = []
        airline_list = []
        while stop != start:
            stop_list.append(stop)
            try:
                airline_stop = parent_airline[stop]
            except KeyError:
                return None, None, None
            airline_list.append(airline_stop)
            stop = parent[stop]
        stop_list.reverse()
        airports = [start] + stop_list
        airline_list.reverse()

        ret_list = []

        for i in range(1, len(airports)):
            origin = airports[i-1]
            airline = airline_list[i-1]
            destination = airports[i]
            if delay_or_cancel == 'delay':
                adj = self.adj_delay[origin][destination]
            elif delay_or_cancel == 'cancel':
                adj = self.adj_cancel[origin][destination]
            cancel = adj[0]
            delay = adj[1]
            temp_lst = [airline, origin, destination, cancel, delay]
            ret_list.append(temp_lst)

        return ret_list

    def find_flight_path(self, start, stop):
        """Find the flight path from city A to city B"""
        if not start or not stop:
            raise ValueError('Please Select Both Origin and Destination')
        if start == stop:
            raise ValueError('The Origin airport cannot be the same as the destination')
        direct_path = self.linear_search(self.adj_cancel, start, stop)
        if direct_path:
            direct_path2 = self.linear_search(self.adj_delay, start, stop)
            # Compares the cancellation rate
            if abs(direct_path[0] - direct_path2[0])*100 <= 5:
                return self.return_linear(start, stop, direct_path2)
            return self.return_linear(start, stop, direct_path)
        parent, parent_airline, dist = self.dijkstra(self.adj_cancel, start, 0)
        parent2, parent_airline2, dist2 = self.dijkstra(self.adj_delay, start, 0)
        # Compares the cancellation rate
        if abs(dist[stop][0] - dist2[stop][0])*100 <= 5:
            return self.return_dijkstra(start, stop, parent2, parent_airline2, 'delay')
        return self.return_dijkstra(start, stop, parent, parent_airline, 'cancel')
