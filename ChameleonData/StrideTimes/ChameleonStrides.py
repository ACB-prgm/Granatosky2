import statistics as stats
import pandas as pd
import os

FPS = 120.0
LIMBS = {
    "forelimb" : ["forelimb", "wrist"], 
    "hindlimb" : ["hindlimb", "ankle"]
}
STRIDE_DATA_FILES_PATH = "ChameleonData/Angles_Outputs"
DLC_EXTENSION = "DLC_resnet50_.xlsx"
OUTPUT_PATH = "ChameleonData/StrideTimes/StrideOutputs"
STRIDE_INFO_PATH = "ChameleonData/StrideTimes/Spatiotemporalvariables.xlsx"
stride_info_DFs = pd.read_excel(STRIDE_INFO_PATH, sheet_name=None)

Export_DFs = {}


def main():
    # PROCESS THE EXCEL
    for SHEET in stride_info_DFs:
        if SHEET != "hindlimb":  # REMOVE ########################################### !!
            continue
        
        SHEET_DF = stride_info_DFs.get(SHEET).fillna("OK")

        for index, row in SHEET_DF.iterrows(): # Fixes all event mismatches
            file_name = row["File name"].split("Event_")
            if str(row["Event"]) != file_name[1]:
                SHEET_DF.iloc[index, [0]] = file_name[0] + str(row["Event"])
        
        for index, row in SHEET_DF.iterrows():
            print("PROCESSING... {} {}/{}".format(SHEET, index, len(SHEET_DF.index)), end="\r")
            if row["OK trial?"] == "OK":
                FRAMES = get_stride_frames(row["a"], row["b"], row["c"])
                file_name = row["File name"]
                file_path = os.path.join(STRIDE_DATA_FILES_PATH, file_name + DLC_EXTENSION)
                if os.path.exists(file_path):
                    DF = pd.read_excel(file_path, index_col="FRAME").interpolate()

                    if not file_name in Export_DFs:
                        Export_DFs[file_name] = {}
                        for limb in LIMBS:
                            for bodypart in LIMBS.get(limb):
                                Export_DFs[file_name]["AB_{}".format(bodypart)] = {}
                                Export_DFs[file_name]["AC_{}".format(bodypart)] = {}
                    
                    # print(file_name, FRAMES, "\n", DF)
                    try:
                        AB = DF.loc[FRAMES[0]:FRAMES[1]]
                        AC = DF.loc[FRAMES[0]:FRAMES[2]]
                    except KeyError:
                        print("Duplicate", file_name)

                    AC = scale_dataframe(AC)

                    for bodypart in LIMBS.get(SHEET):
                        Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}".format(row["Stride"])] = list(AB[bodypart])
                        Export_DFs[file_name]["AC_{}".format(bodypart)]["stride_{}".format(row["Stride"])] = list(AC[bodypart])
                        Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}_angle_A".format(row["Stride"], bodypart)] = [AB.iloc[0][bodypart]] + [None for x in range(0, len(AB.index)-1)]
                        Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}_angle_B".format(row["Stride"], bodypart)] = [AB.iloc[-1][bodypart]] + [None for x in range(0, len(AB.index)-1)]
                        Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}_AB_midpoint".format(row["Stride"])] = [AB[bodypart].median()] + [None for x in range(0, len(AB.index)-1)]
                        
                        joint = None
                        if bodypart == "forelimb":
                            joint = "glenoid_height"
                        elif bodypart == "hindlimb":
                            joint = "hip_height"
                        if joint:
                            Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}_max_{}_height".format(row["Stride"], joint)] = [AB[joint].max()] + [None for x in range(0, len(AB.index)-1)]
                            Export_DFs[file_name]["AB_{}".format(bodypart)]["stride_{}_min_{}_height".format(row["Stride"], joint)] = [AB[joint].min()] + [None for x in range(0, len(AB.index)-1)]

    
    print("\nEXPORTING")
    for file_name in Export_DFs:
        with pd.ExcelWriter(os.path.join(OUTPUT_PATH, file_name + ".xlsx")) as writer:
            sheets = Export_DFs.get(file_name)
            for sheet in sheets:
                pd.DataFrame.from_dict(sheets.get(sheet), orient="index").transpose().to_excel(writer, sheet_name=sheet)    
    

def get_stride_frames(a, b, c):
    A = round(a * FPS)
    B = round(b * FPS)
    C = round(c * FPS)

    return (A, B, C)


def scale_dataframe(DF):
    # GET THE STEP
    TOTAL_POINTS = len(DF.index)
    step = TOTAL_POINTS / 100.0

    # CREATE LIST OF DESIRED TIME POINTS
    points = [round(point * step) for point in range(0, 100)]
    points.append(TOTAL_POINTS - 1)

    return DF.iloc[points]


if __name__ == "__main__":
    main()
    print("FINISHED")


# TODO
# Split to 1 sheet per body part, so for AB there will be AB hindlimb and AB ankle √
# angle @ A √
# angle @ B √
# AB Midpoint (median) √
# min and max hip and glenoid heights 