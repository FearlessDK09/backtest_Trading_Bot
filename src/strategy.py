import pandas as pd

def strat_test(data, sl, tp):
    in_position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []
    win_trades, lose_trades = 0, 0

    for index, row in data.iterrows():
        if not in_position and row['buy'] == 1:
            buyprice = row['shifted_open']
            buydates.append(index)
            buyprices.append(buyprice)
            in_position = True

        if in_position:
            if row['shifted_low'] < (buyprice * sl):
                sellprice = buyprice * sl
                sellprices.append(sellprice)
                selldates.append(index)
                in_position = False
                lose_trades += 1
            elif row['shifted_high'] > (buyprice * tp):
                sellprice = buyprice * tp
                sellprices.append(sellprice)
                selldates.append(index)
                in_position = False
                win_trades += 1

    profits = pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)])
    print("Total Trades: ", len(sellprices))
    print("Win Trades: ", win_trades, "Lose Trades: ", lose_trades)
    return (profits + 1).prod()
