from matplotlib import pyplot as plt
import pandas as pd
import math
import os


FILES_PATH = "Potus_flavus/Kinkajoo"
TOUCH_FRAMES_PATH = os.path.join(FILES_PATH, "Kinkakjoo_Touchdown_Timestamps.xlsx")
TOUCH_FRAMES_DF = pd.read_excel(TOUCH_FRAMES_PATH)
EXPORT_DIR = "Potus_flavus/Exports"

# angle is between Humerus (apex), Elbow, and Y


def main():
    export_dict = {
        "file_name" : [],
        "angle" : []
    }

    for idx, row in TOUCH_FRAMES_DF.iterrows():
        FILE_NAME =  row["EventName"]
        PATH = os.path.join(FILES_PATH, FILE_NAME).replace("'", "")
        TOUCH_FRAME = int(row["Touchdown Frame"])
        
        angle = get_touch_angle(PATH, TOUCH_FRAME, FILE_NAME)

        export_dict.get("file_name").append(FILE_NAME)
        export_dict.get("angle").append(angle)

    pd.DataFrame(export_dict).to_excel(os.path.join(EXPORT_DIR, FILES_PATH.split("/")[-1] + "_Angles.xlsx"), index=False)




def get_touch_angle(PATH, TOUCH_FRAME, FILE_NAME):
    DF = pd.read_csv(PATH, header=1, index_col="bodyparts").drop(["coords"])
    DF = DF.apply(pd.to_numeric, errors='coerce')

    # GET DIRECTION
    humerus = DF["Humerus"]
    min_idx = int(humerus[humerus == humerus.min()].index[0])
    max_idx = int(humerus[humerus == humerus.max()].index[-1])

    direction = -1  # MOVING RIGHT
    if  max_idx < min_idx:  # BECAUSE IN PIXEL SPACE, 0 IS ON THE LEFT.  THUS, IF THE MAX VALUE COMES AFTER THE MIN VALUE, THEN THE X POSITION IS GETTING BIGGER OVER TIME (IE MOVING TO THE RIGHT).
        direction = 1  # MOVING LEFT

    touch_data = DF.iloc[TOUCH_FRAME]

    P1 = (touch_data["Humerus"], touch_data["Humerus.1"])
    P2 = (touch_data["Wrist"], touch_data["Wrist.1"])
    P3 = (touch_data["Humerus"], touch_data["Humerus.1"] + 50.0)
    
    return get_angle(P1, P2, P3) * direction

    



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



if __name__ == "__main__":
    main()