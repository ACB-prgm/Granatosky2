import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess
import os


BASE_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(BASE_DIR, "representative_traces.xlsx")
IMAGES_DIR = os.path.join(BASE_DIR, "IMAGES")
OUTPUT_DIR = os.path.join(BASE_DIR, "EXPORTS")

FORCES = ["Fore/aft", "Tangential" , "Mediolateral"]
LIMBS = ["forelimb","hindlimb"]
NAMES = ["Avery", "Graham"]
YLIMS = [(-110, 110), (-20, 320), (-60, 75)]

# COLORS
FORE_COLOR = "#5468AD" # BLUE
HIND_COLOR = "#F0CB58" # YELLOW


def main():
    plt.style.use(os.path.join(BASE_DIR, "style.mpstyle"))
    dfs = pd.read_excel(EXCEL_PATH, sheet_name=[0,1])

    dfs[0].attrs["name"] = NAMES[0]
    dfs[1].attrs["name"] = NAMES[1]
    Avery_dfs = [dfs[0].iloc[ :, np.array([1,2,3]) + (force * 3)] for force in range(len(FORCES))]
    Graham_dfs = [dfs[1].iloc[ :, np.array([1,2,3]) + (force * 3)] for force in range(len(FORCES))]


    for idx in range(len(dfs[0])):
        print(idx, end="\r")
        for vid in [Avery_dfs, Graham_dfs]:
            for force_idx, df in enumerate(vid):
                line2Ds = plt.plot(df.iloc[:, [1,2]].iloc[0:idx])
                add_settings(force_idx, line2Ds)
                
                dirs = os.path.join(IMAGES_DIR, df.attrs["name"], FORCES[force_idx].replace("/", ""))
                if not os.path.isdir(dirs):
                    os.makedirs(dirs)
                plt.savefig(os.path.join(dirs, f"{idx}.png"))
                plt.clf()
    print("finished creating images.")

    for name in NAMES:
        for force in FORCES:
            input_ = f"{os.path.join(IMAGES_DIR, name, force.replace('/', ''))}/%d.png"
            output = os.path.join(OUTPUT_DIR, f"{name}_{force.replace('/', '')}.mov")
            if not os.path.isdir(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)
            command = ["ffmpeg", "-y",
                        "-framerate", "30",
                        "-i", input_,
                        "-vf", "format=yuv420p",
                        "-vcodec", "h264",
                        output]
            subprocess.run(command)



def add_settings(force_idx, line2Ds):
    plt.xlabel("Percent of Stride (%)")
    plt.ylabel("% BW")
    # plt.ylabel("Force")
    plt.title(FORCES[force_idx])
    plt.hlines(0.0, 0.0, 100, "black", linewidth=1)
    plt.ylim(YLIMS[force_idx])
    plt.xlim([0, 100])

    for idx, line in enumerate(LIMBS):
        line2D = line2Ds[idx]
        
        line = line.lower()

        if "fore" in line:
            line2D.set_color(FORE_COLOR)
        else:
            line2D.set_color(HIND_COLOR)
        # if "ek" in line:
        #     line2D.set_linestyle("--")
        
        # if not ("ek" in line or "ep" in line):
        #     line = line.split(" ")[-1]
        
        line2D.set_label(line.upper())
    
    plt.legend()
    plt.tight_layout()
    
    # plt.show()
    # quit()






if __name__ == "__main__":
    main()