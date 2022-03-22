from fileinput import filename
import pandas as pd
import os

STRIDE_INFO_PATH = "ChameleonData/StrideTimes/Spatiotemporalvariables.xlsx"
STRIDE_DATA_FILES_PATH = "ChameleonData/Angles_Outputs"
DLC_EXTENSION = "DLC_resnet50_.xlsx"
OUTPUT_PATH = "ChameleonData/StrideTimes/StrideOutputs"
FPS = 120

Export_DFs = {}


def main():
    # PROCESS THE EXCEL
    stride_info_DF = pd.read_excel(STRIDE_INFO_PATH)
    stride_info_DF = stride_info_DF.fillna("OK")

    for index, row in stride_info_DF.iterrows():
        print("PROCESSING... {}/{}".format(index, len(stride_info_DF.index)), end="\r")
        if row["OK trial?"] == "OK":
            FRAMES = get_stride_frames(row["a"], row["b"], row["c"])
            file_name = row["File name"]
            file_path = os.path.join(STRIDE_DATA_FILES_PATH, file_name + DLC_EXTENSION)
            if os.path.exists(file_path):
                DF = pd.read_excel(file_path).interpolate()

                if not file_name in Export_DFs:
                    Export_DFs[file_name] = {
                        "AB hindlimb" : {},
                        "AB ankle" : {},
                        "AC hindlimb" : {},
                        "AC ankle" : {}
                        }
                
                AB = DF.iloc[FRAMES[0]:FRAMES[1]]
                AC = DF.iloc[FRAMES[0]:FRAMES[2]]
                AC = scale_dataframe(AC)

                for bodypart in ["hindlimb", "ankle"]:
                    Export_DFs[file_name]["AB {}".format(bodypart)]["stride_{}".format(row["Stride"])] = list(AB[bodypart])
                    Export_DFs[file_name]["AC {}".format(bodypart)]["stride_{}".format(row["Stride"])] = list(AC[bodypart])
    
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

    return [A, B, C]


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
# calculate hip and shoulder height
# angle @ A (max AB)
# angle @ B (min AB)
# AB Midpoint
# min and max hip and houlder heights