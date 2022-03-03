import pandas as pd
import statistics as stats
import os
import math


INPUT_DIR = "DLC_Angles/ContactPixels/ContactInputs"
OUTPUT_DIR = "DLC_Angles/ContactPixels/ContactOutputs"



def main():
    output = {}

    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            contacts = get_DF_from_CSV(os.path.join(root, file))
            output[root.split("/")[-1] + "_" + file.split("-Cam")[0]] = contacts

    max_len = max([len(output.get(x)) for x in output])
    
    for array in output:
        array = output.get(array)
        for _i in range(max_len - len(array)):
            array.append(0)

    pd.DataFrame(output).to_excel(os.path.join(OUTPUT_DIR, "output.xlsx"))



def get_DF_from_CSV(csv_path):
    DF = pd.read_csv(csv_path, header=1)
    DF = DF.drop([0])
    point = "ankle.1"

    if not point in DF.keys():
        point = "limb.1"


    sub_Y = stats.median([float(x) for x in (list(DF["sub1.1"]) + list(DF["sub2.1"]))])
    contacts = []

    for index, row in DF.iterrows():
        contacts.append(is_in_contact(float(row[point]), sub_Y))
    return contacts


def is_in_contact(VAL, REF):
    if abs(VAL - REF) < 20:
        return int(True)
    else:
        return int(False)



if __name__ == "__main__":
    main()