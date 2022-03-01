import pandas as pd

original_path = "Python/FeatherScrape/Feather.xlsx"
new_path = "Python/FeatherScrape/Feather_cleaned.xlsx"



def main():
    df = pd.read_excel(original_path)
    data = {
        "Species" : None,
        "Specimen Number" : None,
        "Sex" : None,
        "Age" : None,
        "Body Mass" : None,
        "Feather Number" : None,
        "Total Length (cm)" : None,
        "Vane Length (cm)" : None,
    }

    new_df = []

    for row in df.index:
        first = df[0][row]

        if first == "Feather Metadata": # new DF
            data["Specimen Number"] = df[1][row+1]
            data["Species"] = df[1][row+3]
            data["Sex"] = df[1][row+7]
            data["Age"] = df[1][row+8]

        feather_length = df[3][row]
        if not (pd.isna(feather_length) or feather_length == "Feather Total Length"):
            data["Feather Number"] = [df[2][row]]
            data["Total Length (cm)"] = [feather_length]
            data["Vane Length (cm)"] = [df[5][row]]
            new_df.append(pd.DataFrame.from_dict(data))
        
    new_df = pd.concat(new_df, ignore_index=True)
    new_df.to_excel(new_path)


    # df.to_excel(new_path)



if __name__ == "__main__":
    main()