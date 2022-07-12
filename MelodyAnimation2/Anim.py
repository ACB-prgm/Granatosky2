from matplotlib import pyplot as plt
from pathlib import Path
import subprocess
import pandas
import os


BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = os.path.join(BASE_DIR, "FigureGraphs_sca_ed.xlsx")
IMAGES_PATH = os.path.join(BASE_DIR, "ImageOutputs")
VIDEOS_PATH = os.path.join(BASE_DIR, "VideoStuff")
RESOLUTION = (1920, 1080)

# COLORS
BLUE = "#5468AD"
YELLOW = "#F0CB58"

FIGS = {
    "Z" : {
        "lines" : ["Z FLAT", "Z POLE"],
        "ylim" : [-0.002, 0.005],
        "units" : "Vertical Position (m)"
        
    },
    "ENERGY" : {
        "lines" : ["EK POLE", "EP POLE", "EP FLAT", "EK FLAT"],
        "ylim" : [-0.006, 0.009],
        "units" : "Energy (J)"
    },
    "POWER" : {
        "lines" : ["POWER FLAT", "POWER POLE"],
        "ylim" : [-0.006, 0.005],
        "units" : "Power (W/kg)"
    }
}


def main():
    plt.style.use(os.path.join(BASE_DIR, "style.mpstyle"))
    df = pandas.read_excel(EXCEL_PATH, index_col="INDEX").fillna(0)

    for idx in range(0,101):
        print(idx, end="\r")
        for fig in FIGS:
            toplot = df.get(FIGS.get(fig).get("lines")).iloc[0:idx]
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


def add_settings(fig, line2Ds):
    plt.xlabel("Percent of Stride (%)")
    plt.ylabel(FIGS.get(fig).get("units"))
    # plt.ylabel("Force")
    plt.title(fig)
    plt.hlines(0.0, 0.0, 100, "black", linewidth=1)
    plt.ylim(FIGS.get(fig).get("ylim"))
    plt.xlim([0, 100])

    lines = FIGS.get(fig).get("lines")
    for idx, line in enumerate(lines):
        line2D = line2Ds[idx]
        
        line = line.lower()
        if "pole" in line:
            line2D.set_color(YELLOW)
        else:
            line2D.set_color(BLUE)
        if "ek" in line:
            line2D.set_linestyle("--")
        
        if not ("ek" in line or "ep" in line):
            line = line.split(" ")[-1]
        
        line2D.set_label(line.upper())
    
    plt.legend()
    plt.tight_layout()
    
    # plt.show()
    # quit()





if __name__ == "__main__":
    main()
    print("FINISH")