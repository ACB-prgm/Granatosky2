from matplotlib import pyplot as plt
import matplotlib.animation
import pandas as pd
import numpy as np
import matplotlib
import os


SAVE_DIR = "/Users/aaronbastian/Documents/MedicalSchool/NYIT/Granatosky_Lab/Python.nosync/Granatosky2/HumanRunning/Outputs"
INPUT_DIR = "HumanRunning/GalaVideo"
DRAW_LINES = [
    ["Head", "ShoulderCenter", "HipCenter"],
    ["ShoulderL", "ElbowL", "WristL", "HandL"],
    ["PelvisL", "HipL", "KneeL", "AnkleL", "FootHeelL", "FootTipL"],
    # ["ShoulderR", "ElbowR", "WristR", "HandR"],
    # ["PelvisR", "HipR", "KneeR", "AnkleR", "FootHeelR", "FootTipR"]
]

# CREATING FIGURE
RESOLUTION = (1920, 1080)
THICKNESS = 2 # determines the THICKNESS for all lines not including fonts. default = 1
fig = plt.figure(facecolor=(1,0,1,1), dpi=300, figsize=(5, (5/RESOLUTION[0]) * RESOLUTION[1])) # figsize is in inches for some reason
# fig.patch.set_alpha(0.0)


def main():

    df = process_CSV("HumanRunning/GalaVideo/20220401_EDDIE_2_5mph_5__cam4DLC_resnet50_ISF_SpeedTraining_Cam4Apr4shuffle1_500000_filtered.csv")
    FRAMES = len(df.index)
    anim = matplotlib.animation.FuncAnimation(fig, anim_single, fargs=(df, FRAMES, "AnkleL") ,frames=FRAMES, interval=1, repeat=False)
    SAVE_PATH = os.path.join(SAVE_DIR, "{}.mov".format("EDDIE_ANKLE"))
    # plt.show()
    anim.save(SAVE_PATH, writer="ffmpeg", fps=60, savefig_kwargs={'transparent': True, 'facecolor': (1,1,1,1)})

    return
    for file in os.listdir(INPUT_DIR):
        if ".csv" in file:
            path = os.path.join(INPUT_DIR, file)
            name = file.split("_")[1]
            print("\nPROCESSING... {}".format(name))
            df = process_CSV(path)
    
            FRAMES = len(df.index)
            anim = matplotlib.animation.FuncAnimation(fig, animate, fargs=(df, FRAMES) ,frames=FRAMES, interval=1, repeat=False)
            SAVE_PATH = os.path.join(SAVE_DIR, "{}.mov".format(name))
            # plt.show()
            anim.save(SAVE_PATH, writer="ffmpeg", fps=60, savefig_kwargs={'transparent': True, 'facecolor': (1,0,1,1)})



def process_CSV(PATH):
    df = pd.read_csv(PATH, header=1, index_col="bodyparts").drop(["coords"])
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df[df["Head.1"] > 1.0]
    
    last_row = pd.DataFrame()
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

    plt.rcParams['axes.facecolor'] = (0,0,0,0)
    plt.rcParams["font.size"] = "6"
    # plt.xlabel("Time (s)")
    # plt.ylabel("Force")
    plt.title("Frame{}".format(idx))
    # plt.hlines(0.0, 0.0, 1.1, "black")
    plt.ylim([RESOLUTION[1], 0])
    plt.xlim([0, RESOLUTION[0]])



def animate(idx, DF, FRAMES):
    print("{}/{} | {}%".format(idx, FRAMES, round(idx/FRAMES*100, 2)), end="\r")
    lines = []
    row = DF.iloc[idx]

    for line in DRAW_LINES:
        x = []
        y = []
        for point in line:
            x.append(row[point])
            y.append(row[point + ".1"])
        lines.append((x, y))

    plt.clf()
    add_settings(idx)

    for line in lines:
        plt.plot(line[0], line[1])


X = []
def anim_single(idx, DF, FRAMES, point):
    print("{}/{} | {}%".format(idx, FRAMES, round(idx/FRAMES*100, 2)), end="\r")

    if idx == 0:
        X.clear()
    
    row = DF.iloc[idx]
    X.append(row[point])

    plt.clf()
    add_settings(idx)
    plt.rcParams["font.size"] = "12"
    plt.xlim([0, len(DF.index)])
    plt.title("Ankle Cycle")
    plt.plot(X)


def notify(text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, (__file__).split("/")[-1]))


if __name__ == "__main__":
    main()
    notify("Process completed.")