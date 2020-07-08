"""
    Created by Ma. Micah Encarnacion on 08/07/2020
"""
import pandas as pd


def write_to_csv(mapping, file_name):
    df = pd.DataFrame(data=mapping)
    df.to_csv(file_name, index=False, encoding="utf-8")
