import pandas as pd
import statistics as stats
import math
import os



def get_DF_from_DLCcsv(PATH):
    DF = pd.read_csv(PATH, header=1, index_col="bodyparts").drop(["coords"])
    DF = DF.apply(pd.to_numeric, errors='coerce')

    return DF


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


def get_distance_between(P1, P2, REF=None):
    pixel_dist = math.sqrt( ((float(P1[0]) - float(P2[0])) **2)+((float(P1[1]) - float(P2[1])) **2) )
    
    if REF: # RETURNS DISTANCE IN METERS (REF IS pixel/meter)
        return (pixel_dist / REF)
    else: # RETURNS DISTANCE IN PIXELS
        return pixel_dist