import pandas as pd

df = pd.read_csv('uretim-genel.csv')

df.groupby('Ürün Grubu')