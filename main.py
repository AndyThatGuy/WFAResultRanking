import os
import config as cfg
import ntpath
import pandas

#gl
def prepare_folders():
    if not os.path.isdir(cfg.ranked_folder):
        os.makedirs(cfg.ranked_folder)


def main():
    prepare_folders()
    target_file = cfg.ranked_folder + cfg.result_folder.split("/")[4] + "_results.csv"
    with open(target_file, "w") as f:
        f.write(cfg.summary_columns + "\n")
    for file in os.listdir(cfg.result_folder):
        file = cfg.result_folder + file
        strategy_name = ntpath.basename(file).split("_")[0]
        # print(strategy_name)
        df = pandas.read_csv(file)
        df = df.drop(columns=["OOS", "IS"])
        df.columns = [
            "Strategy",
            "HOReturn",
            "HOSharpe",
            "HOWin/Draw/Lose",
            # "HODrawRate",
            # "HOLoseRate",
            "BTReturn",
            "BTWin/Draw/Lose",
            "BTMarketChange",
            # "BTDrawRate",
            # "BTLoseRate",
        ]
        df["Market"] = df["Strategy"]
        markets = df["Market"].unique()
        df["HOReturn"] = df["HOReturn"].str.strip("%")
        df["HOReturn"] = df["HOReturn"].astype(float) / 100
        df["BTReturn"] = df["BTReturn"].str.strip("%")
        df["BTReturn"] = df["BTReturn"].astype(float) / 100
        df["BTMarketChange"] = df["BTMarketChange"].str.strip("%")
        df["BTMarketChange"] = df["BTMarketChange"].astype(float) / 100
        df[["HOWinRate", "HODrawRate", "HOLoseRate"]] = df["HOWin/Draw/Lose"].str.split(
            "/", expand=True
        )
        df[["BTWinRate", "BTDrawRate", "BTLoseRate"]] = df["BTWin/Draw/Lose"].str.split(
            "/", expand=True
        )
        df["HOTotalTrades"] = (
            df["HOWinRate"].astype(int)
            + df["HODrawRate"].astype(int)
            + df["HOLoseRate"].astype(int)
        )
        df["BTTotalTrades"] = (
            df["BTWinRate"].astype(int)
            + df["BTDrawRate"].astype(int)
            + df["BTLoseRate"].astype(int)
        )
        df["HOWinRate"] = df["HOWinRate"].astype(int) / df["HOTotalTrades"]
        df["HODrawRate"] = df["HODrawRate"].astype(int) / df["HOTotalTrades"]
        df["HOLoseRate"] = df["HOLoseRate"].astype(int) / df["HOTotalTrades"]
        df["BTWinRate"] = df["BTWinRate"].astype(int) / df["BTTotalTrades"]
        df["BTDrawRate"] = df["BTDrawRate"].astype(int) / df["BTTotalTrades"]
        df["BTLoseRate"] = df["BTLoseRate"].astype(int) / df["BTTotalTrades"]
        for market in markets:
            grouped = df.groupby(df.Market)
            group_df = grouped.get_group(market)
            group_df.drop(columns=["HOWin/Draw/Lose", "BTWin/Draw/Lose"])
            horeturn = group_df["HOReturn"].astype(float).mean()
            hosharpe = group_df["HOSharpe"].astype(float).mean()
            btreturn = group_df["BTReturn"].astype(float).mean()
            btmarketchange = group_df["BTMarketChange"].astype(float).mean()
            howinrate = group_df["HOWinRate"].astype(float).mean()
            hodrawrate = group_df["HODrawRate"].astype(float).mean()
            holoserate = group_df["HOLoseRate"].astype(float).mean()
            btwinrate = group_df["BTWinRate"].astype(float).mean()
            btdrawrate = group_df["BTDrawRate"].astype(float).mean()
            btloserate = group_df["BTLoseRate"].astype(float).mean()
            hototaltrades = group_df["HOTotalTrades"].astype(float).mean()
            bttotaltrades = group_df["BTTotalTrades"].astype(float).mean()
            with open(target_file, "a") as f:
                f.write(
                    f"{strategy_name},{market},{horeturn},{hosharpe},{howinrate},{hodrawrate},{holoserate},{hototaltrades},{btreturn},{btmarketchange},{btwinrate},{btdrawrate},{btloserate},{bttotaltrades}\n"
                )


if __name__ == "__main__":
    main()
