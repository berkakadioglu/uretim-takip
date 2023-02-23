import pandas as pd
import numpy as np
import datetime
df = pd.read_csv('uretim6.csv')
df['Tarih'] = pd.to_datetime(df['Tarih'])
df.loc[df['Ürün Grubu'] == 'SNİCKERS', 'Ürün Grubu'] = 'Patik'
df.loc[df['Ürün Grubu'] == 'BAYAN KISAKONC', 'Ürün Grubu'] = 'Kısa Konç'
df.loc[df['Ürün Grubu'] == 'BAYAN ERKEK HAVLU', 'Ürün Grubu'] = 'Havlu'
df.loc[df['Ürün Grubu'] == 'BAYAN SOKET', 'Ürün Grubu'] = 'Soket'
df.loc[df['Ürün Grubu'] == 'ERKEK PATİK', 'Ürün Grubu'] = 'Patik'
df.loc[df['Ürün Grubu'] == 'BAYAN PATİK', 'Ürün Grubu'] = 'Patik'
df.loc[df['Ürün Grubu'] == 'KISA KONÇ', 'Ürün Grubu'] = 'Kısa Konç'
df.loc[df['Ürün Grubu'] == 'ÇETİK', 'Ürün Grubu'] = 'Babet'
df.loc[df['Ürün Grubu'] == 'PATİK', 'Ürün Grubu'] = 'Patik'
df.loc[df['Ürün Grubu'] == 'BAYAN BAMBU BABET', 'Ürün Grubu'] = 'Babet'
df.loc[df['Ürün Grubu'] == 'SOKET TENİS', 'Ürün Grubu'] = 'Soket'
df.loc[df['Ürün Grubu'] == 'HAVLU DİZALTI', 'Ürün Grubu'] = 'Havlu Dizaltı'
df.loc[df['Ürün Grubu'] == 'BAYAN ERKEK KISAKONC HAVLU', 'Ürün Grubu'] = 'Kısa Konç'
df.loc[df['Ürün Grubu'] == 'SOKET ERKEK', 'Ürün Grubu'] = 'Soket'

df['Yıl'] = df['Tarih'].dt.isocalendar()['year']
df['Hafta'] = df['Tarih'].dt.isocalendar()['week']
print(df['Tarih'])
df.reset_index(drop=True)
df.to_csv('uretim-genel.csv')