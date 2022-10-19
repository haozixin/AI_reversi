import pandas as pd

if __name__ == '__main__':
    # use pandas open csv file
    df = pd.read_csv('./qtable_50.csv', index_col=0)
    # df2 = pd.read_csv('./counter.csv', index_col=0)
    df3 = pd.read_csv('./Node_visits_50.csv', index_col=0)

    print("shape of qtable.csv: ", df.shape)
    print("shape of Node_visit.csv: ", df3.shape)



    # action = "('[[<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.WHITE: 1>, <Cell.BLACK: 0>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.BLACK: 0>, <Cell.WHITE: 1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>], [<Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>, <Cell.EMPTY: -1>]]0', (3, 2))"
    # a = eval(action)[0]
    # print(a)

    # get the first instance's index in qtable.csv
    # instance_index = df3.index[9]
    # # use the index to get the value in qtable2.csv
    # print("value in qtable.csv: ", df3.loc[instance_index])
    # print("value in qtable2.csv: ", df.loc[instance_index])