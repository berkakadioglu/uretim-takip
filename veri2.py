import pandas as pd

uretim_df = pd.read_csv('uretim2.csv')
uretim_yeni = uretim_df.groupby('İstasyon Adı').sum()
print(uretim_yeni.head(10))