import os
import pandas as pd
import matplotlib
import numpy as np
from matplotlib import pyplot as plt


SAVE_DIR = "/Users/aaronbastian/Documents/MedicalSchool/NYIT/Granatosky_Lab/Python.nosync/Granatosky2/HumanRunning/GalaVideo"
CSV_PATH = "HumanRunning/GalaVideo/20220401_EVAN_2_5mph_5__cam4DLC_resnet50_ISF_SpeedTraining_Cam4Apr4shuffle1_500000_filtered.csv"
DRAW_LINES = [
    ["Head", "ShoulderCenter", "HipCenter"],
    ["ShoulderR", "ElbowR", "WristR", "HandR"],
    ["PelvisR", "HipR", "KneeR", "AnkleR", "FootHeelR", "FootTipR"],
    ["ShoulderL", "ElbowL", "WristL", "HandL"],
    ["PelvisL", "HipL", "KneeL", "AnkleL", "FootHeelL", "FootTipL"]
]

# CREATING FIGURE
RESOLUTION = (1920, 1080)
THICKNESS = 2 # determines the THICKNESS for all lines not including fonts. default = 1
fig = plt.figure(facecolor=(0,0,0,0), dpi=150, figsize=(5, (5/RESOLUTION[0]) * RESOLUTION[1])) # figsize is in inches for some reason


def main():
    df = process_CSV(CSV_PATH)
    anim = matplotlib.animation.FuncAnimation(fig, animate, fargs=() ,frames=len(df.index), interval=1, repeat=False)
    
    SAVE_PATH = os.path.join(SAVE_DIR, "out.mov")
    anim.save(SAVE_PATH, fps=60)
    # plt.show()


def process_CSV(PATH):
    df = pd.read_csv(PATH, header=1, index_col="bodyparts").drop(["coords"])
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df[df["Head.1"] > 1.0]
    
    last_row = pd.Series()
    drop_idxs = []
    for index, row in df.iterrows():
        if not last_row.empty:
            for column in row.index:
                if not ".2" in column:
                    if abs(row[column] - last_row[column]) > 10.0:
                        drop_idxs.append(index)
                        break
        last_row = row
    
    df.loc[drop_idxs] = np.nan
    df.interpolate(inplace=True)

    return df


def add_settings(idx):
    ax = fig.add_subplot(111)
    ax.xaxis.set_tick_params(width=THICKNESS)
    ax.yaxis.set_tick_params(width=THICKNESS)
    [ax.spines[axis].set_linewidth(THICKNESS) for axis in ['top', 'bottom', 'left', 'right']]
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontweight('bold') for label in labels]

    plt.rcParams['axes.facecolor'] = (1,1,1,0)
    plt.rcParams["font.size"] = "6"
    # plt.xlabel("Time (s)")
    # plt.ylabel("Force")
    plt.title("Frame{}".format(idx))
    plt.hlines(0.0, 0.0, 1.1, "black")
    plt.ylim([RESOLUTION[1], 0])
    plt.xlim([RESOLUTION[0], 0])



def animate(idx):
    print("{}/{} | {}%".format(idx, FRAMES, round(idx/FRAMES*100, 2)), end="\r")
    lines = []
    row = DF.iloc[idx]

    for angle in ANGLES:
        args = str_point_to_tuple(row[angle])
        Xs = (args[1][0], args[0][0], args[2][0])
        Ys = (args[1][1], args[0][1], args[2][1])
        lines.append((Xs, Ys))

    plt.clf()
    add_settings(idx)

    for line in lines:
        plt.plot(line[0], line[1])


if __name__ == "__main__":
    main()