import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


BASE_DIR = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(BASE_DIR, "representative_traces.xlsx")

FORCES = ["Fore/aft", "Tangential" , "Mediolateral"]
LIMBS = ["forelimb","hindlimb"]
LINES = {
    "Avery" : {},
    "Graham": {}
}
# COLORS
BLUE = "#5468AD"
YELLOW = "#F0CB58"


def main():
    dfs = pd.read_excel(EXCEL_PATH, sheet_name=[0,1])

    Avery_dfs = [dfs[0].iloc[ :, np.array([1,2,3]) * (force + 1)] for force in range(len(FORCES))]

    print(Avery_dfs)






if __name__ == "__main__":
    main()