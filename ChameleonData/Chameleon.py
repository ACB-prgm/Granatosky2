import pandas as pd
import statistics as stats
import math
import os


STRIDE_INFO_PATH = "ChameleonData/StrideTimes/Spatiotemporalvariables.xlsx"
stride_info_DF = pd.read_excel(STRIDE_INFO_PATH).fillna("OK")
OUTPUT = "ChameleonData/Angles_Outputs"
FPS = 120.0

ANGLES = {
    "hindlimb" : ["hip", "knee", "h"],
    "ankle" : ["ankle", "hip", "h"],
    "forelimb" : ["glenoid", "elbow", "h"],
    "wrist" : ["wrist", "elbow", "h"]
}

SVLs = {
    "dopey" : 0.049,
    "megan" : 0.055,
    "abby" : 0.057,
    "snow" : 0.106,
    "mia" : 0.054,
} # in meters


def main():
    fix_event_mismatches()

    for root, dirs, files in os.walk("ChameleonData/Chameleons", topdown=False):
        TOTAL_FILES = len(files)
        count = 0
        for file in files:
            count += 1
            if ".csv" in file:
                chameleon_name = root.split("/")[-1].lower()
                process_csv(os.path.join(root, file), file, chameleon_name)

                print("{} PROGRESS... {}/{}".format(chameleon_name.upper(), count, TOTAL_FILES), end="\r")
        print("")


def process_csv(CSV, filename, chameleon):
    output = {
        "FRAME" : []
    }
    # anim_output = {}
    df = pd.read_csv(CSV, header=1)

    ref_file = filename.split("DLC")[0]
    if ref_file in stride_info_DF.index:
        strides_df = []
        for _index, row in stride_info_DF.loc[[ref_file]].iterrows():  # REMOVES ALL VALUES NOT IN STRIDE(S)
            if row["OK trial?"] == "OK":
                FRAMES = get_stride_frames(row["a"], row["b"], row["c"])
                AC = df.iloc[FRAMES[0]:FRAMES[2]]
                strides_df.append(AC)
                output["FRAME"] += range(FRAMES[0], FRAMES[2])
                # print(ref_file, len(AC.index), len(range(FRAMES[0], FRAMES[2])), range(FRAMES[0], FRAMES[2]))
        if strides_df:
            strides_df = pd.concat(strides_df) # NOTE: MUST USE .loc INSTEAD OF .iloc AFTER CONCATENATION **************************************
        else:
            return

        REF = []
        SUB_Y = []

        for _idx, row in strides_df.iterrows():
            REF.append(get_distance_between( (row["snout"], row["snout.1"]) , (row["vent"], row["vent.1"]) ))
            SUB_Y.append((float(row["ankle.1"]) + float(row["wrist.1"])) / 2.0)

            for angle in ANGLES: # ANGLE PROCESSING
                if not angle in output.keys():
                    output[angle] = []
                    # anim_output[angle] = []
                angl = ANGLES.get(angle)
                point1 = (row[angl[0]], row[angl[0] + ".1"])
                point2 = (row[angl[1]], row[angl[1] + ".1"])
                point3 = None
                if angl[2] == "v":
                    point3 = (row[angl[0]], float(row[angl[0] + ".1"]) - 100.0)
                elif angl[2] == "h":
                    point3 = (float(row[angl[0]]) - 100.0, row[angl[0] + ".1"])
                output.get(angle).append(get_angle(point1, point2, point3))
                # anim_output.get(angle).append("{},{}:{},{}:{},{}".format(point2[0], point2[1], point1[0], point1[1], point3[0], point3[1]))

        REF = stats.mean(REF) / SVLs.get(chameleon)
        SUB_Y = stats.median(SUB_Y)

        output["glenoid_height"] = []
        output["hip_height"] = []

        for _idx, row in strides_df.iterrows():
            output.get("glenoid_height").append((SUB_Y - float(row["glenoid.1"])) / REF)
            output.get("hip_height").append((SUB_Y - float(row["hip.1"])) / REF)
        
        # anim_output = pd.DataFrame(anim_output)
        # anim_output.to_excel(OUTPUT + "/anim_output.xlsx")
        output = pd.DataFrame(output)
        output.to_excel(OUTPUT + "/{}.xlsx".format(filename.split("chameleon")[0]))
        # ankle = [float(x) for x in df.get("ankle.1") if x != "y"]


def fix_event_mismatches():
    global stride_info_DF
    for index, row in stride_info_DF.iterrows():
        file_name = row["File name"].split("Event_")
        if str(row["Event"]) != file_name[1]:
            stride_info_DF.iloc[index, [0]] = file_name[0] + str(row["Event"])
    stride_info_DF.set_index("File name", inplace=True)


def get_angle(P1, P2, P3):
    a = get_side(P2, P3)
    b = get_side(P1, P3)
    c = get_side(P1, P2)

    try:
        return math.degrees(math.acos((b**2 + c**2 - a**2) / (2*b*c)) - 1.5708)
    except:
        return None


def get_side(A, B):
    return math.sqrt( (float(A[0]) - float(B[0]))**2 + (float(A[1]) - float(B[1]))**2 )


def get_distance_between(P1, P2, REF=None):
    pixel_dist = math.sqrt( ((float(P1[0]) - float(P2[0])) **2)+((float(P1[1]) - float(P2[1])) **2) )
    
    if REF: # RETURNS DISTANCE IN METERS (REF IS pixel/meter)
        return (pixel_dist / REF)
    else: # RETURNS DISTANCE IN PIXELS
        return pixel_dist


def get_stride_frames(a, b, c):
    A = round(a * FPS)
    B = round(b * FPS)
    C = round(c * FPS) + 1

    return [A, B, C]


if __name__ == "__main__":
    main()


# TODO
# CLIP TO STRIDE TIMES √
# calculate hip and shoulder height √