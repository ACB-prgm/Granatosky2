import pandas as pd
import matplotlib
import matplotlib.animation
from matplotlib import pyplot as plt


# LINKS
# Animations: https://matplotlib.org/stable/api/animation_api.html
# Transparent Background: https://stackoverflow.com/questions/15857647/how-to-export-plots-from-matplotlib-with-transparent-background
# basic animations: https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c
# Saving Animations: https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.Animation.html#matplotlib.animation.Animation.save
# plotting NAN values: https://matplotlib.org/devdocs/gallery/lines_bars_and_markers/masked_demo.html
# NAN in Matplotlib: https://stackoverflow.com/questions/36455083/how-to-plot-and-work-with-nan-values-in-matplotlib
# Colors: https://matplotlib.org/stable/gallery/color/named_colors.html


# PROCESSING DATA
excel_file = "ForceGraphs/Actual.xlsx"

raw_data = pd.read_excel(excel_file)

TIME = list(raw_data["Time"])
BEAK = list(raw_data["Beak"])
LIMB = list(raw_data["Limb"])
TAIL = list(raw_data["Tail"])

# CREATING FIGURE
fig = plt.figure(facecolor=(0,0,0,0), dpi=300, figsize=(4.267, 3.6)) # figsize is in inches for some reason
thickness = 2 # determines the thickness for all lines not including fonts. default = 1

def add_settings():
    ax = fig.add_subplot(111)
    ax.xaxis.set_tick_params(width=thickness)
    ax.yaxis.set_tick_params(width=thickness)
    [ax.spines[axis].set_linewidth(thickness) for axis in ['top', 'bottom', 'left', 'right']]
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontweight('bold') for label in labels]

    plt.rcParams['axes.facecolor'] = (1,1,1,0)
    plt.rcParams["font.size"] = "12"
    plt.xlabel("Time (s)")
    plt.ylabel("Force")
    plt.hlines(0.0, 0.0, 1.1, "black")
    plt.ylim([-4, 4])
    plt.xlim([0, 1.1])



# ANIMATING FIGURE
time, beak, limb, tail = [], [], [], []
def animate(idx):
    time.append(TIME[idx])
    beak.append(BEAK[idx])
    limb.append(LIMB[idx])
    tail.append(TAIL[idx])

    plt.clf()
    add_settings()

    plt.plot(time, beak, "dodgerblue", label="beak", antialiased=True, linewidth=thickness, solid_capstyle="round")
    plt.plot(time, limb, "orange", label="limb", antialiased=True, linewidth=thickness, solid_capstyle="round")
    plt.plot(time, tail, "forestgreen", label="tail", antialiased=True, linewidth=thickness, solid_capstyle="round")

    plt.legend(["Beak", "Limb", "Tail"])
    if idx > 1:
        plt.fill_between(time, beak, 0,
            facecolor="lightskyblue", alpha = 0.5)
        plt.fill_between(time, limb, 0,
            facecolor="navajowhite", alpha = 0.5)
        plt.fill_between(time, tail, 0,
            facecolor="palegreen", alpha = 0.5)


anim = matplotlib.animation.FuncAnimation(fig, animate, frames=len(TIME), interval=10, repeat=False)

save_file = "ForceGraphs/output_graph.gif"
anim.save(save_file, writer='ffmpeg')
# plt.show()
print("FINISH")