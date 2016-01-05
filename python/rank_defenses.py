import pandas as pd


def main():
    data = pd.read_csv("2009-2014.csv")
    print(data.tail())
    defPA = getPointsAgainst(data)


def getPointsAgainst(data):
    dataGroup = data.groupby(["opponent"])

if __name__ == '__main__':
    main()
