import pandas as pd
import os


# THIS IS COMPLEX (CSVs).  ITS CALLED A LAMBDA FUNCTION.  IT JUST PUTS A FOR LOOP INTO ONE LINE TO MAKLE A LIST
# HERE I GET ALL OF THE FILES IN THE DIRECTORY AND APPEND THE FIRST PART OF THE FILE PATH
# THIS GENERATES A LIST OF PATHS TO ALL THE CSV FILES
GEN_PATH = "MelodyTask/COM_pole"
CSVs = [GEN_PATH + "/" + x for x in os.listdir(GEN_PATH)]
OUTPUT_PATH = GEN_PATH + "_Averaged.xlsx"


def main():
    # CREATE NEW DATAFRAME TO STORE OUTPUT AVERAGES THAT HAS THE SAME COLUMN HEADERS
    columns = pd.read_excel(CSVs[0]).columns
    avgs = pd.DataFrame(columns=columns)

    # LOOP OVER ALL EXCEL FILES
    for csv in CSVs:
        # GET A DICTIONARY OF ALL THE SHEETS IN THE FILE
        sheets = pd.read_excel(csv, sheet_name=None)
        
        # GET THE MEAN OF ALL THE COLUMNS IN THE FILE
        # THIS IS SOMETHING CALLED A SERIES IN PANDAS.  HERE I NAME IT AND ADD IT TO THE ARRAY WE MADE ABOVE
        for sheet in sheets:
            means = sheets.get(sheet).mean()
            filename = "{}-{}".format(csv.replace(GEN_PATH + "/", ""), sheet)
            means.name = filename
            avgs = avgs.append(means)
    
    # THIS JUST SAVES THE DATA FRAME TO AN EXCEL FILE
    avgs.to_excel(OUTPUT_PATH)


# THIS IS NOT NECESSARY.  THIS IS JUST SOMETHING PEOPLE DO TO KEEP THINGS ORGANIZED
if __name__ == "__main__":
    main()