import pandas as pd
import datetime as dt
uretim_df = pd.read_csv('uretim4.csv')
uretim2_df = uretim_df.groupby('İstasyon Adı').sum()
yesterday = dt.date.today() - dt.timedelta(days=1)
uretim_df['Tarih'] = pd.to_datetime(uretim_df['Tarih'])
yesterday = yesterday.strftime('%Y-%m-%d')
uretim2_df = uretim_df.loc[uretim_df['Tarih'] == yesterday]
uretim3_df = uretim2_df.groupby('Çalışma Grubu').sum()
print(uretim3_df.head(5))