import pandas as pd
import os


GEN_PATH = "MelodyTask/Power_flat"
CSVs = [GEN_PATH + "/" + x for x in os.listdir(GEN_PATH)]
OUTPUT_PATH = GEN_PATH + "_Scaled.xlsx"


def main():
    # CREATE DICTIONARY OF DATA FRAMES FOR THE SCALED DATA
    columns = pd.read_excel(CSVs[0]).columns
    export_DFs = {}
    for column in columns:
        if column != "Time (s)":
            export_DFs[column] = pd.DataFrame()

    # LOOP OVER ALL EXCEL FILES
    total = float(len(CSVs))
    current = 0.0
    for csv in CSVs:
        current += 1.0
        percent = round((current/total) * 100, 2)
        print("PERCENT COMPLETE: {}% ({}/{})".format(percent, int(current), int(total)), end = "\r")
        
        # GET A DICTIONARY OF ALL THE SHEETS IN THE FILE
        sheets = pd.read_excel(csv, sheet_name=None)
        
        for sheet in sheets:
            scaled_sheet = sheets.get(sheet).apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
            scaled_sheet = scale_dataframe(scaled_sheet)

            for column in scaled_sheet.columns:
                column_name = "{}_{}".format(csv.replace(GEN_PATH + "/", ""), sheet)
                if column != "Time (s)":
                    export_DFs.get(column)[column_name] = scaled_sheet[column].values
            
            
    print("\nEXPORTING...")
    with pd.ExcelWriter(OUTPUT_PATH) as writer:
        for df in export_DFs:
            sheet_name = "{}_Scaled".format(df.replace(" ", "_"))
            sheet_name = ''.join(e for e in sheet_name if e.isalnum())
            export_DFs.get(df).to_excel(writer, sheet_name=sheet_name)


def scale_dataframe(DF):
    # GET THE STEP
    time_column = DF["Time (s)"]
    _min = time_column.min()
    step = (time_column.max() - _min) / 100.0

    # CREATE LIST OF DESIRED TIME POINTS
    points = [point * step + _min for point in range(0, 101)]
    new_points = []

    # REMOVE POINTS THAT ALREADY EXIST
    for point in points:
        if not (point in time_column.values):
            new_points.append(point)
    
    # CONVERT TO DATAFRAME
    new_points_df = pd.DataFrame({"Time (s)" : new_points})
    
    # CONCATENATE THE DFS AND SORT THEM SO THEY ARE ORDERED BY TIME
    DF = pd.concat([DF, new_points_df]).sort_values(by=["Time (s)"])
    # FILL THE NAN VALUES WITH INTERPOLATED VALUES
    DF = DF.interpolate()

    new_DF = pd.DataFrame()
    for point in points:
       new_DF = new_DF.append(DF[DF["Time (s)"] == point])
    new_DF = new_DF.drop_duplicates(subset=["Time (s)"])

    return new_DF




if __name__ == "__main__":
    main()
    print("#### FINISHED ####")