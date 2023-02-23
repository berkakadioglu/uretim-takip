from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt

df = pd.read_csv('uretim-genel.csv')
df['Tarih'] = pd.to_datetime(df['Tarih'])
df = df.sort_values(by='Tarih',ascending=True)
#df['Tarih'] = df['Tarih'].dt.strftime('%d/%m/%Y')

istasyon_adlari_list = list(df['İstasyon Adı'].unique())
istasyon_adlari_list.pop()
istasyon_adlari_list.sort()
'''
Multiple Dataframe Generator
'''
total_prod_list = list()
for i in range(len(istasyon_adlari_list)):
    loc_df = df.loc[df['İstasyon Adı'] == istasyon_adlari_list[i]]
    total_prod_list.append(loc_df)
istasyon_adlari_list.insert(0,'Tümü')

perf_df2 = df.groupby(['Çalışma Grubu', 'Ürün Grubu']).mean()
perf_df2.reset_index(inplace=True)
perf_df2['Sağlam(dz)'] = perf_df2['Sağlam(dz)'].apply(lambda x : float("{:.2f}".format(x)))
perf_df2 = perf_df2.drop(columns=['Unnamed: 0', 'Miktar (kg.)', 'Yıl', 'Hafta'])
print(perf_df2.head(10))

app = Dash(external_stylesheets=[dbc.themes.LITERA])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Alert(class_name='danger',
                      children=[html.H3('Berka Tekstil Üretim Takip Platformu')])
        ], width=6, style={'text-align': 'center'})
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id='tarih-tabs', value='gunluk-tab', children=[
                dcc.Tab(label='Günlük Üretim Takibi', value='gunluk-tab')
            ]),
            html.Div(id='tabs-content'),
            html.Div(id='data-content-table'),
            html.Div(id='performance-analysis')
        ])
    ], justify='center')
])   

@app.callback(Output('tabs-content','children'),
              Input('tarih-tabs','value')) 
def graph_maker(val):
    if val == 'gunluk-tab':
        fig1 = go.Figure()
        for i in range(len(total_prod_list)):
            total_prod_list[i].reset_index(inplace=True)
            #total_prod_list[i] = total_prod_list[i].sort_values('Tarih', ascending=True)
            fig1.add_trace(go.Scatter(
                name = total_prod_list[i]['İstasyon Adı'][0],
                mode="markers+lines", x = total_prod_list[i]['Tarih'], y = total_prod_list[i]['Sağlam(dz)'],
                marker_symbol = "star",
            ))
        fig1.update_layout(title_text='Üretim Takibi')
        fig1.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=3, label="3 Gün",step='day', stepmode='backward'),
                    dict(count=7, label='1 Hafta',step='day',stepmode='backward'),
                    dict(count=1, label="1 Ay", step='month', stepmode='backward'),
                    dict(count=6, label="6 Ay", step='month',stepmode='backward'),
                    dict(step='all')
                ])
            )
        )
        return html.Div([
            dcc.Graph(id='gunluk-uretim-total',
                         figure=fig1)
        ])

@app.callback(Output('data-content-table','children'),
              Input('tarih-tabs','value'))
def datatable_maker(val):
    if val == 'gunluk-tab':
        yesterday = dt.date.today() - dt.timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')
        datatable_df = df.loc[df['Tarih'] == yesterday]
        datatable_df = datatable_df.drop(['Unnamed: 0', 'Model Ad', 'Yıl', 'Hafta'], axis=1) 
        datatable_df = datatable_df.sort_values('İstasyon Adı')

        datatable_df2 = datatable_df.groupby('İstasyon Adı').sum()
        datatable_df2 = datatable_df2.sort_values('Sağlam(dz)', ascending=True)
        datatable_df2.reset_index(inplace=True)

        datatable_df3 = datatable_df.groupby('Ürün Grubu').sum()
        datatable_df3 = datatable_df3.sort_values('Sağlam(dz)', ascending=True)
        datatable_df3.reset_index(inplace=True)

        datatable_df4 = datatable_df.groupby('Sağlam(dz)').sum()
        datatable_df4.reset_index(inplace=True)

        return html.Div([
            dbc.Row([
                dbc.Col(children=[
                    html.H2('Son Gün Üretim (Genel)'),
                    dash_table.DataTable(data=datatable_df.to_dict('records'),
                                        columns=[{'name': i, 'id': i} for i in datatable_df.columns],
                                        fixed_rows={'headers': True},
                                        style_table={'height': 300}),
                    html.Br(),
                    html.H2('Son Gün Üretim (İstasyona Göre)'),
                    dash_table.DataTable(data=datatable_df2.to_dict('records'),
                                        columns=[{'name': i, 'id': i} for i in datatable_df2.columns],
                                        fixed_rows={'headers': True},
                                        style_table={'height': 300}),
                    html.Br(),
                    html.H2('Son Gün Üretim (Çalışma Grubuna Göre)'),
                    dash_table.DataTable(data=datatable_df3.to_dict('records'),
                                        columns=[{'name': i, 'id': i} for i in datatable_df3.columns]),
                    html.Br(),
                ],align='center')
            ], style={'text-align':'center'})
        ])

@app.callback(Output('performance-analysis','children'),
              Input('tarih-tabs','value'))
def performance_analyzer(val):
    if val == 'gunluk-tab':
        perf_df = df
        perf_df = perf_df.groupby(by='Ürün Grubu').sum()
        perf_df.append({'Ürün Grubu': ['Toplam'],
                        'Sağlam(dz)': [perf_df['Sağlam(dz)'].sum()],
                        'Miktar(kg)': [perf_df['Miktar (kg.)'].sum()]}, ignore_index=True)
        perf_df.reset_index(inplace=True)


        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2('2023 Performans Analizi'),
                    dash_table.DataTable(data=perf_df.to_dict('records'),
                                         columns=[
                                            {'name': 'Ürün Grubu', 'id': 'Ürün Grubu'},
                                            {'name': 'Sağlam(dz)', 'id': 'Sağlam(dz)'},
                                            {'name': 'Miktar(kg)', 'id': 'Miktar (kg.)'}
                    ]),
                    html.H2('2023 Vardiyaya Göre Ürünleri Gruplandırarak Yapılan Performans Analizi'),
                    dash_table.DataTable(data=perf_df2.to_dict('records'),
                                        columns=[
                                            {'name': 'Çalışma Grubu', 'id': 'Çalışma Grubu'},
                                            {'name': 'Ürün Grubu', 'id': 'Ürün Grubu'},
                                            {'name': 'Sağlam(dz)', 'id': 'Sağlam(dz)'}
                                        ])
                ])
            ], style={'text-align': 'center'})
        ])


if __name__ == '__main__':
    app.run_server(debug=True)