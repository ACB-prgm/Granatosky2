import pandas as pd
import matplotlib.pyplot as plt
import os


BASE_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(BASE_DIR, "representative_traces.xlsx")


def main():
    dfs = pd.read_excel(EXCEL_PATH, sheet_name=None)

    print(dfs)






if __name__ == "__main__":
    main()