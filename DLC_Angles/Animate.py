import pandas as pd
import matplotlib
import matplotlib.animation
from matplotlib import pyplot as plt


SAVE_FILE = "DLC_Angles/ANIMATION.mp4"
EXCEL_FILE = "DLC_Angles/anim_points.xlsx"
DF = pd.read_excel(EXCEL_FILE)

ANGLES = {
    "tail_angle" : ["tailbase", "wing", "tailtip"],
    "body_axis_angle" : ["tailbase", "COM", "sub_midpoint"],
    "hindlimb_angle" : ["COM", "sub_midpoint", "ankle"],
    "tail_retraction_angle" : ["COM", "sub_midpoint", "tailtip"],
    "beak_protraction_angle" : ["COM", "sub_midpoint", "beaktip"],
    "craniofacial_join_angle" : ["beakbase", "beaktip", "head"],
    "mandible_joint_angle" : ["eye", "mandbase", "mandtip"]
}

# CREATING FIGURE
fig = plt.figure(facecolor=(0,0,0,0), dpi=300, figsize=(4.267, 3.6)) # figsize is in inches for some reason
THICKNESS = 2 # determines the THICKNESS for all lines not including fonts. default = 1


def main():
    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=len(DF.index), interval=1, repeat=False)
    # anim.save(SAVE_FILE, writer="ffmpeg")
    plt.show()
    print("FINISH")


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
    plt.ylim([1000, 0])
    plt.xlim([1000, 0])



def animate(idx):
    lines = []
    row = DF.iloc[idx]

    for angle in ANGLES:
        args = [row[x] for x in ANGLES.get(angle)]
        args = [str_point_to_tuple(arg) for arg in args]
        Xs = (args[1][0], args[0][0], args[2][0])
        Ys = (args[1][1], args[0][1], args[2][1])
        lines.append((Xs, Ys))

    plt.clf()
    add_settings(idx)

    for line in lines:
        plt.plot(line[0], line[1])
    # plt.plot(time, beak, "dodgerblue", label="beak", antialiased=True, linewidth=THICKNESS, solid_capstyle="round")
    # plt.plot(time, limb, "orange", label="limb", antialiased=True, linewidth=THICKNESS, solid_capstyle="round")
    # plt.plot(time, tail, "forestgreen", label="tail", antialiased=True, linewidth=THICKNESS, solid_capstyle="round")

    # plt.legend(["Beak", "Limb", "Tail"])

def str_point_to_tuple(point):
    for char in ["(", ")", "'", "'", " "]:
        point = point.replace(char, "")
    point = point.split(",")
    return (float(point[0]), float(point[1]))


if __name__ == "__main__":
    main()