import pandas as pd
import math
import os


OUTPUT = "ChameleonData/Angles_Outputs"

angles = {
    "hindlimb" : ["hip", "knee", "h"],
    "ankle" : ["ankle", "hip", "h"],
    "forelimb" : ["glenoid", "elbow", "h"],
    "wrist" : ["wrist", "elbow", "h"]
}


def main():
    for root, dirs, files in os.walk("ChameleonData/Chameleons", topdown=False):
        for file in files:
            if ".csv" in file:
                process_csv(os.path.join(root, file), file)


def process_csv(CSV, filename):
    output = {}
    anim_output = {}
    df = pd.read_csv(CSV, header=1)

    for index, row in df.iterrows():
        if not index == 0:
            for angle in angles:
                if not angle in output.keys():
                    output[angle] = []
                    anim_output[angle] = []
                angl = angles.get(angle)
                point1 = (row[angl[0]], row[angl[0] + ".1"])
                point2 = (row[angl[1]], row[angl[1] + ".1"])
                point3 = None
                if angl[2] == "v":
                    point3 = (row[angl[0]], float(row[angl[0] + ".1"]) - 100.0)
                elif angl[2] == "h":
                    point3 = (float(row[angl[0]]) - 100.0, row[angl[0] + ".1"])
                output.get(angle).append(get_angle(point1, point2, point3))
                anim_output.get(angle).append("{},{}:{},{}:{},{}".format(point2[0], point2[1], point1[0], point1[1], point3[0], point3[1]))
    
    anim_output = pd.DataFrame(anim_output)
    anim_output.to_excel(OUTPUT + "/anim_output.xlsx")
    output = pd.DataFrame(output)
    output.to_excel(OUTPUT + "/{}.xlsx".format(filename.split("chameleon")[0]))


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