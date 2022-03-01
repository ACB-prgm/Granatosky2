import os
import math
import pandas as pd


CSVs_DIR = "WoodpeckerVelocities/Small_pole_DLC_CSV"
OUTPUT_DIR = "WoodpeckerVelocities/Output"


def main():
    DF = pd.DataFrame()

    for file in os.listdir(CSVs_DIR):
        event = file.split("-Camera")[0]
        points_raw, SPF = get_points_from_csv(CSVs_DIR + "/" + file)
        
        if points_raw.empty:
            print(file)
            continue

        diffs = [(float(row["woodR"][0]) - float(row["woodL"][0])) for i, row in points_raw.iterrows()]
        REF = (sum(diffs) / len(diffs)) / 10.0
        vels = []

        for index, row in points_raw.iterrows():
            dist = 0
            try:
                dist = get_distance_between(row["neck"], points_raw["neck"][index-1], REF)
            except:
                dist = get_distance_between(row["neck"], points_raw["neck"][index+1], REF)
            vels.append(dist / SPF)
        
        velocities = pd.DataFrame()
        velocities["Event"] = [event]
        velocities["Avg Vel (MpS)"] = [sum(vels) / len(vels)]

        DF = pd.concat([DF, velocities])
    
    DF = DF.reset_index().drop(['index'], axis=1)
    
    DF.to_excel(OUTPUT_DIR + "/" + CSVs_DIR.split("/")[1].split("_DLC")[0] + "_Velocity.xlsx")


def get_points_from_csv(file_path):
    excel_file = pd.read_csv(file_path)
    DF = pd.DataFrame()
    DF.name = file_path.split("/")[-1].replace(".csv", "")

    x_coords = []
    y_coords = []
    bad_rows = []

    for column in excel_file:
        column = excel_file[column]
        
        if column[1] == "x":
            x_coords = list(column[2:])
        elif column[1] == "y":
            y_coords = list(column[2:])
        elif column[1] == "likelihood":
            for index, value in column.iteritems():
                if not index in [0,1] and float(value) < 0.9:
                    if not index-2 in bad_rows and column[0] in ["woodL", "woodR", "neck"]:
                        bad_rows.append(index - 2)
            DF[column[0]] = list(zip(x_coords, y_coords))

    DF = DF.drop(bad_rows)
    return DF.reset_index() , (len(excel_file.index - 2) / 125.0) / len(excel_file.index - 2)


def get_distance_between(P1, P2, REF):
    raw_dist = math.sqrt( ((float(P1[0]) - float(P2[0])) **2)+((float(P1[1]) - float(P2[1])) **2) )
    return (raw_dist / REF) / 100


if __name__ == "__main__":
    main()