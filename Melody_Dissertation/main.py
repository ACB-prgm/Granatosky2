import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess
import shutil
import os


BASE_DIR = os.path.dirname(__file__)
EVENT_DIRS = os.path.join(BASE_DIR, "Evts")
EXPORT_DIRS = os.path.join(BASE_DIR, "Exports")

FORE_COLOR = "#334D90" # BLUE
HIND_COLOR = "#F2DB93" # YELLOW


def main():
    plt.style.use(os.path.join(BASE_DIR, "style.mpstyle"))

    # LOAD THE EXCELS INTO PANDAS DATAFRAMES AND ORGANIZE THEM
    print("## LOADING DFS INTO MEMORY... ##")
    dfs = []
    for evt in os.listdir(EVENT_DIRS):
        path = os.path.join(EVENT_DIRS, evt, "representative trace.xlsx")
        df = pd.read_excel(path)
        df.attrs["name"] = evt
        if evt == "SLFPOLE":
            df = [df.iloc[ :, np.array(range(1,6)) + (force * 5)] for force in range(3)]
        else:
            df = [df.iloc[ :, np.array(range(1,5)) + (force * 4)] for force in range(3)]
        
        for sec in df:
            sec.attrs["sec_name"] = sec.columns[0]
            sec.drop([sec.columns[-1], sec.columns[0]], axis=1, inplace=True)
        
        dfs.append(df)
    
    # MAKE THE GRAPHS AND SAVE AS PNGS
    for point in range(101):
        print(F"## MAKING FIGURES... {point}/100 ##", end="\r")
        for evt in dfs:
            num_axes = len(evt)
            fig, axes = plt.subplots(nrows=num_axes, ncols=1, tight_layout=True, figsize=(9.0, 3.0 * num_axes))
            
            for idx in range(num_axes):
                # title = evt[idx].attrs["name"]
                line2ds = axes[idx].plot(evt[idx][:point])
                add_settings(line2ds, axes[idx], evt[idx])
            
            # SAVE FIG
            NAME = evt[0].attrs["name"]
            SAVE_DIR = os.path.join(EXPORT_DIRS, NAME)
            if not os.path.isdir(SAVE_DIR):
                os.mkdir(SAVE_DIR)
            fig.savefig(os.path.join(SAVE_DIR, f"{point}.png"))

            plt.close()
    
    # CONVERT PNGS TO VIDEO
    print("## MAKING VIDEOS... ##")
    OUTPUT_DIR = os.path.join(EXPORT_DIRS, "exported_movs")
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    for evt in dfs:
        NAME = evt[0].attrs["name"]
        IMAGES_DIR = os.path.join(EXPORT_DIRS, NAME)

        input_ = f"{IMAGES_DIR}/%d.png"
        output = os.path.join(OUTPUT_DIR, f"{NAME}.mov")
        command = ["ffmpeg", "-y",
                    "-framerate", "30",
                    "-i", input_,
                    "-vf", "format=yuv420p",
                    "-vcodec", "h264",
                    output]
        subprocess.run(command)

        shutil.rmtree(IMAGES_DIR)



def add_settings(line2Ds, ax, df):
    ax.set_xlabel("Percent of Stride (%)")
    ax.set_ylabel("% BW")
    ax.set_title(df.attrs["sec_name"])
    ax.hlines(0.0, 0.0, 100, "black", linewidth=1)
    ax.set_ylim(bottom=df.min().min() * 1.2, top=df.max().max() * 1.2)
    ax.set_xlim(0, 100)

    for idx, line2D in enumerate(line2Ds):
        line_name = df.columns[idx].split(".")[0]
        line2D.set_label(line_name)

        if "fore" in line_name:
            COLOR = FORE_COLOR
        else:
            COLOR = HIND_COLOR
        
        line2D.set_color(COLOR)
        ax.fill_between(line2D.get_xdata(), line2D.get_ydata(), 0 ,color=COLOR, alpha=0.5)
    
    ax.legend(loc=1)


if __name__ == "__main__":
    print("### START ###")
    main()
    print("### FINISH ###")