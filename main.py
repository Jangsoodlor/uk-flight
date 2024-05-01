import os
import pandas as pd
from controller import Controller
from model import Model
from view import TabManager
df = pd.read_csv(os.path.join(os.getcwd(),
                                'data/202401_Punctuality_Statistics_Full_Analysis.csv'))
m = Model(df)
v = TabManager()
c = Controller(v,m)
c.run()
