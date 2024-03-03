import pandas as pd

class MyModel():
    
    def __init__(self, data:pd.DataFrame=None):
        self.set_data(data)

    def set_data(self, data:pd.DataFrame):
        self.data = data

    def calc_corr(self, ca1:str, ca2:str):
        return self.data[ca1].corr(self.data[ca2])