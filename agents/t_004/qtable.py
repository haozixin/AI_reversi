from collections import defaultdict
from agents.t_004.qfunction import QFunction
import pandas as pd


class QTable(QFunction):
    def __init__(self, default=0.0):
        self.qtable = defaultdict(lambda: default)

    def update(self, state, action, delta):
        self.qtable[(state, action)] = self.qtable[(state, action)] + delta

    def get_q_value(self, state, action):
        return self.qtable[(state,  action)]

    def initial_q_table(self, filename):
        """
        filename: the csv file name (get from different opponent and round)
        get q_table from csv file
        using pandas
        """
        # using pandas
        # format:
        #         0
        # (1, 2)  3
        # (4, 5)  6

        # read the csv file
        df = pd.read_csv(filename, index_col=0)
        # convert the dataframe to dictionary (index is the key)
        df.reset_index(inplace=True)

        data = df["index"].apply(lambda x: eval(x))
        values = df["0"].apply(lambda x: float(x))
        # zip the data and values together
        data = dict(zip(data, values))

        """ data = 
        ('[[<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], 
        [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.WHITE: 1>, <Cell.BLACK: 0>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.BLACK: 0>, 
        <Cell.WHITE: 1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], 
        [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, 
        <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>]]0', (3, 2)): 0.000775420793609
        """
        self.qtable = defaultdict(lambda: 0.0, data)

        # self.qtable = df.to_dict(orient='index')
        return self


