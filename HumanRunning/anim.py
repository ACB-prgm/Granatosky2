import pandas as pd
import matplotlib
import matplotlib.animation
from matplotlib import pyplot as plt

RESOLUTION = (1920, 1080)
EXCEL_FILE = "ChameleonData/animations/anim_output.xlsx"
SAVE_FILE = "ChameleonData/animations/animation.mp4"
DF = pd.read_excel(EXCEL_FILE)
FRAMES = len(DF.index)

ANGLES = {
    "hindlimb" : ["hip", "knee", "v"],
    "ankle" : ["ankle", "hip", "h"],
    "forelimb" : ["glenoid", "elbow", "v"],
    "wrist" : ["wrist", "elbow", "h"]
}

# CREATING FIGURE
fig = plt.figure(facecolor=(0,0,0,0), dpi=150, figsize=(5, (5/RESOLUTION[0]) * RESOLUTION[1])) # figsize is in inches for some reason
THICKNESS = 2 # determines the THICKNESS for all lines not including fonts. default = 1


def main():
    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=FRAMES, interval=1, repeat=False)
    anim.save(SAVE_FILE, fps=60)
    # plt.show()


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


def str_point_to_tuple(string):
    output = []
    points = string.split(":")
    for point in points:
        point = point.split(",")
        output.append((float(point[0]), float(point[1])))
    
    return output
        


if __name__ == "__main__":
    main()
    print("\nFINISH")