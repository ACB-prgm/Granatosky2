import pandas as pd
import matplotlib
from matplotlib import pyplot as plt


CSV_PATH = "HumanRunning/Gala Video/20220401_EVAN_2_5mph_5__cam4DLC_resnet50_ISF_SpeedTraining_Cam4Apr4shuffle1_500000_filtered.csv"


def main():
    df = pd.read_csv(CSV_PATH, header=1, index_col="bodyparts").drop(["coords"])
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df[df["Head.1"] > 1.0]
    print(df)
    # plt.plot(df["Head.1"])
    # plt.show()


if __name__ == "__main__":
    main()