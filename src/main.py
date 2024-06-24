from src.data_fetcher import get_hourly_data
from src.strategy import strat_test
from src.telegram_bot import post_message

def main():
    data = get_hourly_data('BTCUSDT', '2020-01-01')
    data.dropna(inplace=True)
    data["shifted_high"] = data.High.shift(-1)
    data["shifted_low"] = data.Low.shift(-1)
    data["buy"] = (data.ema50 > data.ema200) & (data.ema50.shift(1) > data.ema200.shift(1)) & (data.ema50.shift(2) > data.ema200.shift(2))

    filtered_data = data.loc['2024-04-01 01:00:00':'2024-05-01 01:00:00']
    result = strat_test(filtered_data, 0.9997, 1.01)

    post_message(f"Strategy result: {result}")

if __name__ == "__main__":
    main()
