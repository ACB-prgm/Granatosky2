import pandas as pd
import statistics as stats
import os
import math


OUTPUT_DIR = "DLC_Angles/Outputs/"
FILES_DIR = "DLC_Angles/Testfiles"

# FIX SUB MIDPOINT AND SUBS BECAUSE THEY ARE STATIONARY
# BODY AXIS, USE WING AND TAILBASE
#cf angle, manible, eye_to_COM

angles = {
    "tail_angle" : ["tailbase", "wing", "tailtip"],
    "body_axis_angle" : ["tailbase", "COM", "sub_midpoint"],
    "hindlimb_angle" : ["COM", "sub_midpoint", "ankle"],
    "tail_retraction_angle" : ["COM", "sub_midpoint", "tailtip"],
    "beak_protraction_angle" : ["COM", "sub_midpoint", "beaktip"],
    "craniofacial_join_angle" : ["beakbase", "beaktip", "head"],
    "mandible_joint_angle" : ["eye", "mandbase", "mandtip"]
}
distances = {
    "COM_to_substrate" : ["COM", "sub_midpoint"],
    "support_to_tailtip" : ["topclaw", "tailtip"],
    "grid1_to_grid2" : ["grid1", "grid2"],
    "eye_to_wing" : ["eye", "wing"],
    "eye_to_COM" : ["eye", "COM"]
}
contacts = {
    "tail_con_sub" : ["sub_midpoint", "tailtip", 0],
    "maxilla_con_sub" : ["sub_midpoint", "beaktip", 0],
    "mandible_con_sub" : ["sub_midpoint", "mandtip", 0],
    "topfoot_con_sub" : ["sub_midpoint", "topclaw", 0],
    "botfoot_con_sub" : ["sub_midpoint", "botclaw", 0],
}
output = {}


def main():
    for root, dirs, files in os.walk(FILES_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            points_DF = get_points_from_csv(filepath)

            for _index, row in points_DF.iterrows():
                for angle in angles:
                    if not angle in output:
                        output[angle] = []
                    
                    args = [row[x] for x in angles.get(angle)]
                    output.get(angle).append(get_angle(args[0], args[1], args[2]))

                for distance in distances:
                    if not distance in output:
                        output[distance] = []
                    
                    args = [row[x] for x in distances.get(distance)]
                    output.get(distance).append(get_distance_between(args[0], args[1], row["REF"]))

                for contact in contacts:
                    if not contact in output:
                        output[contact] = []
                    
                    args = [row[x] for x in contacts.get(contact)]
                    output.get(contact).append(are_in_contact(args[0], args[1], row["REF"]))

            final = pd.DataFrame(output)
            final.to_excel(OUTPUT_DIR + points_DF.name + ".xlsx")
            output.clear()


def get_points_from_csv(file_path):
    excel_file = pd.read_csv(file_path)
    DF = pd.DataFrame()
    path = file_path.split("/")
    DF.name = path[-2] + path[-1].replace(".csv", "")

    x_coords = []
    y_coords = []

    for column in excel_file:
        column = excel_file[column]
        
        if column[1] == "x":
            x_coords = list(column[2:])
        elif column[1] == "y":
            y_coords = list(column[2:])
        elif column[1] == "likelihood":
            DF[column[0]] = list(zip(x_coords, y_coords))
    
    subx = stats.mean([float(x[0]) for x in (DF["sub1"] + DF["sub2"])])
    sub_midpoints = []
    COM = []
    REFS = []
    for _index, row in DF.iterrows():
        _COM = get_midpoint(row["wing"], row["tailbase"])
        COM.append(_COM)
        sub_midpoints.append((subx, _COM[1]))
        try:
            REFS.append(abs(float(row["grid1"][1]) - float(row["grid2"][1])) / 10.0)
        except ZeroDivisionError:
            pass

    DF["sub_midpoint"] = sub_midpoints
    DF["COM"] = COM
    DF["REF"] = stats.mean(REFS)

    return DF


def get_angle(P1, P2, P3):
    a = get_side(P2, P3)
    b = get_side(P1, P3)
    c = get_side(P1, P2)

    return math.degrees(math.acos((b**2 + c**2 - a**2) / (2*b*c)))


def get_side(A, B):
    return math.sqrt( (float(A[0]) - float(B[0]))**2 + (float(A[1]) - float(B[1]))**2 )


def get_midpoint(P1, P2):
    return ( (float(P1[0]) + float(P2[0]))/2.0, (float(P1[1]) + float(P2[1]))/2.0 )


def get_distance_between(P1, P2, REF):
    # RETURNS DISTANCE IN METERS
    raw_dist = math.sqrt( ((float(P1[0]) - float(P2[0])) **2)+((float(P1[1]) - float(P2[1])) **2) )
    return (raw_dist / REF) / 100.0



def are_in_contact(P1, P2, REF, xy=0):
    # XY == 0 (X AXIS), XY == 1 (Y AXIS)
    # REF is 1cm
    return int(not abs(float(P1[xy]) - float(P2[xy])) > REF * 0.5)



if __name__ == "__main__":
    main()
    print("FINISHED")