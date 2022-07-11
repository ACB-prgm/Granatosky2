from matplotlib import pyplot as plt
from pathlib import Path
import subprocess
import shutil
import pandas as pd
import ffmpeg # Just to remind you to download ffmpeg.
import os


BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = os.path.join(BASE_DIR, "posandenergy.xlsx") # excel file name (path will be generated if file is in same dir as this)
IMAGES_PATH = os.path.join(BASE_DIR, "ImageOutputs")
VIDEOS_PATH = os.path.join(BASE_DIR, "VideoOutputs")
plt.style.use(os.path.join(BASE_DIR, "style.mpstyle")) # LOADS DEFAULT GRAPH VISUAL SETTINGS. YOU CAN CHANGE THERE.

# COLORS
COLOR_1 = "#5468AD" # BLUE
COLOR_2 = "#F0CB58" # YELLOW

INVERTED = False


FIGS = {
    "POSITION" : {
        "lines" : ["Pos X (m)", "Pos Y (m)", "Pos Z (m)"],
        "ylim" : [-0.27, 1.43],
        "units" : "Position (m)"
        
    },
    "ENERGY" : {
        "lines" : ["EK Total (J)", "EP (J)", "E Total (J)"],
        "ylim" : [0.0, 1255.0],
        "units" : "Energy (J)"
    },
}


def main():
    if not os.path.isdir(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
        for fig in FIGS:
            os.mkdir(os.path.join(IMAGES_PATH, fig))
    if not os.path.isdir(VIDEOS_PATH):
        os.mkdir(VIDEOS_PATH)

    df = pd.read_excel(EXCEL_PATH).fillna(0)
    df_len = len(df) + 1

    for idx in range(0, df_len):
        print(idx, end="\r")
        for fig in FIGS:
            toplot = df.get(FIGS.get(fig).get("lines")).iloc[0:idx]
            cur_len = len(toplot)
            
            if INVERTED:
                lines = []
                for line in toplot:
                    line = plt.plot(toplot.get(line), range(cur_len)) 
                    lines.append(line[0])
            else:
                lines = plt.plot(toplot)

            add_settings(fig, lines)
            plt.savefig(os.path.join(IMAGES_PATH, fig, f"{idx}.png"))
            plt.clf()
    
    print("finished creating images.")

    for fig in FIGS:
        input_dir = f"{os.path.join(IMAGES_PATH, fig)}/%d.png"
        output_dir = os.path.join(VIDEOS_PATH, f"{fig}.mov")
        command = ["ffmpeg", "-y",
                    "-framerate", "30",
                    "-i", input_dir,
                    "-vf", "format=yuv420p",
                    "-vcodec", "h264",
                    output_dir]
        subprocess.run(command)
    
    shutil.rmtree(IMAGES_PATH)
    
    


def add_settings(fig, line2Ds):
    if INVERTED:
        plt.xlabel(FIGS.get(fig).get("units"))
        plt.ylabel("Percent Stride (%)")
        # plt.ylabel("Force")
        plt.title(fig)
        plt.vlines(0.0, 0.0, 101, "black", linewidth=1)
        plt.xlim(FIGS.get(fig).get("ylim"))
        plt.ylim([0, 101])
    else:
        plt.ylabel(FIGS.get(fig).get("units"))
        plt.xlabel("Percent Stride (%)")
        plt.title(fig)
        plt.hlines(0.0, 0.0, 101, "black", linewidth=1)
        plt.ylim(FIGS.get(fig).get("ylim"))
        plt.xlim([0, 101])

    lines = FIGS.get(fig).get("lines")
    for idx, line in enumerate(lines):
        line2D = line2Ds[idx]
        for rm in [" (J)", " (m)"]:
            line = line.replace(rm, "")
        line2D.set_label(line.upper())
        
        # line = line.lower()
        # if "pole" in line:
        #     line2D.set_color(COLOR_2)
        # else:
        #     line2D.set_color(COLOR_1)
        # if "ek" in line:
        #     line2D.set_linestyle("--")
        
        # if not ("ek" in line or "ep" in line):
        #     line = line.split(" ")[-1]
    
    plt.legend()
    plt.tight_layout()


if __name__ == "__main__":
    main()
    print("FINISH")