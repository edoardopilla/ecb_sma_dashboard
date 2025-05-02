########### PREPARE DATA

# import all from sma_dash_utils.py (BAD PRACTICE, AVOID import *)
from ecb_sma_dash_utils import *

# initialize instance of ecb_sma_scraper
scraper_sma_ecb = ecb_sma_scraper()

# scrape set params to scrape or load dataset
scraper_sma_ecb.scrape_sma_data(scrape_data = user_custom_scrape_data_flag)

# assign SMA data dump attribute to new variable
df_full = scraper_sma_ecb.sma_data_full

# assign latest release attribute to new variable
latest_release = scraper_sma_ecb.reference_data.latest_release[0]

# assign next release attribute to new variable
next_release = scraper_sma_ecb.reference_data.next_release[0]

# assign last update attribute to new variable
last_update = scraper_sma_ecb.reference_data.last_update[0]

# assign respondent data attribute to new variable
resps_df = scraper_sma_ecb.respondent_data

# prepare SMA data dump for tab1_chart1
df_tab1_chart1 = df_full[df_full['series_key'].str.contains('MEDIAN.GC.I.U2._Z.ESTR')].reset_index(drop = True)

df_tab1_chart1.value = pd.to_numeric(df_tab1_chart1.value)
df_tab1_chart1.time_stamp = pd.to_datetime(df_tab1_chart1.time_stamp)

# prepare SMA data dump for tab1_chart2
df_tab1_chart2 = df_full[(df_full['series_key'].str.contains('GC.I.U2._Z')) & (df_full['measure'].str.contains('P25|MEDIAN|P75', regex = True)) & (df_full['item'].str.contains('DFR|MRO|MLF', regex = True))].reset_index(drop = True)

df_tab1_chart2.value = pd.to_numeric(df_tab1_chart2.value)
df_tab1_chart2.time_stamp = pd.to_datetime(df_tab1_chart2.time_stamp)

# prepare SMA data dump for tab2_chart1
df_tab2_chart1 = df_full[(df_full.series_key.str.contains('Q.EUR.U2._Z')) & ((df_full.item.str.contains('EUROSYSTEM_APP_HOLDINGS')) | (df_full.item.str.contains('EUROSYSTEM_PEPP_HOLDINGS')))].reset_index(drop = True)

df_tab2_chart1['item'] = df_tab2_chart1['item'].map({'EUROSYSTEM_APP_HOLDINGS': 'APP', 'EUROSYSTEM_PEPP_HOLDINGS': 'PEPP'})

df_tab2_chart1.value = pd.to_numeric(df_tab2_chart1.value)
df_tab2_chart1.time_stamp = pd.to_datetime(df_tab2_chart1.time_stamp)

# prepare SMA data dump for tab2_chart2
df_tab2_chart2 = df_full[df_full.item == 'TPI_ACTIVATION_DIST'].reset_index(drop = True)

df_tab2_chart2.value = pd.to_numeric(df_tab2_chart2.value)
df_tab2_chart2.vintage_date = pd.to_datetime(df_tab2_chart2.vintage_date)
df_tab2_chart2.time_stamp = pd.to_datetime(df_tab2_chart2.time_stamp)

df_tab2_chart2['category'] = df_tab2_chart2['category'].map({'NEXT_3M': 'Next 3 months',
                                                             'NEXT_4M_TO_6M': 'Next 4 to 6 months',
                                                             'AFTER_6M': 'After 6 months',
                                                             'NEVER': 'Never'})

# define list of dictionaries for storing dropdown options to enable multiple choices up to 4 in tab2_chart2
opts_multi_drop = [dict(zip(['value', 'label'], [vint, vint])) for vint in df_tab2_chart2.vintage.unique()]

# prepare SMA data dump for tab3_chart1
df_tab3_chart1 = df_full[(df_full.series_key.str.endswith('MEDIAN.Q.Y.U2._Z.HIC')) | (df_full.series_key.str.endswith('MEDIAN.Q.Y.U2._Z.HEF')) | (df_full.series_key.str.endswith('MEDIAN.Q.Q.U2._Z.YER')) | (df_full.series_key.str.endswith('MEDIAN.Q.PC.U2._Z.URX'))]

df_tab3_chart1.vintage_date = pd.to_datetime(df_tab3_chart1.vintage_date)
df_tab3_chart1.time_stamp = pd.to_datetime(df_tab3_chart1.time_stamp)
df_tab3_chart1.value = pd.to_numeric(df_tab3_chart1.value)

df_tab3_chart1 = df_tab3_chart1[(df_tab3_chart1.vintage_date.isin(pd.Series(df_tab3_chart1.vintage_date.unique()).nlargest(2)))]
df_tab3_chart1 = df_tab3_chart1[df_tab3_chart1.time_stamp <= df_tab3_chart1.time_stamp.unique().min() + pd.offsets.DateOffset(years = 2)].reset_index(drop = True)

df_tab3_chart1['item'] = df_tab3_chart1['item'].map({'HEF': 'Core inflation', 'HIC': 'Headline inflation',
                                                     'URX': 'Unemployment', 'YER': 'Real GDP growth'})

# prepare SMA data dump for tab3_chart2
df_tab3_chart2 = df_full[(df_full.series_key.str.contains('MEAN._Z.PR.U2')) & (df_full.series_key.str.endswith('HIC_LR_DISTRIBUTION'))].reset_index(drop = True)

df_tab3_chart2.vintage_date = pd.to_datetime(df_tab3_chart2.vintage_date)
df_tab3_chart2.value = pd.to_numeric(df_tab3_chart2.value)

# define list of dictionaries for storing dropdown options to format labels as survey rounds in tab3_chart2
opts_tab3_chart2_dropdown = [dict(zip(['value', 'label'], [vint_date, vint])) for vint_date, vint in dict(zip(df_tab3_chart2.vintage_date.unique(), df_tab3_chart2.vintage.unique())).items()]

# prepare SMA data dump for tab3_chart3
df_tab3_chart3 = df_full[(df_full.series_key.str.contains('PC.A._Z.U2')) & (df_full.series_key.str.endswith('_RISKS'))]

df_tab3_chart3.vintage_date = pd.to_datetime(df_tab3_chart3.vintage_date)
df_tab3_chart3.value = pd.to_numeric(df_tab3_chart3.value)

# define list of dictionaries for storing dropdown options to format labels as survey rounds in tab3_chart3
opts_tab3_chart3_dropdown_1 = [dict(zip(['value', 'label'], [vint_date, vint])) for vint_date, vint in dict(zip(df_tab3_chart3.vintage_date.unique(), df_tab3_chart3.vintage.unique())).items()]

# define list of dictionaries for storing dropdown options to format labels as items in tab3_chart3
opts_tab3_chart3_dropdown_2 = [dict(zip(['value', 'label'], [item_val, item_lab])) for item_val, item_lab in dict(zip(df_tab3_chart3.item.unique(), [lab[0:3] for lab in df_tab3_chart3.item.unique()])).items()]


########### STATIC FUNCTIONS

# define function to update tab1_chart1
def update_tab1_chart1(df):

    tab1_chart1_figure = px.line(df.sort_values(by = ['vintage_date', 'time_stamp'],
                                                ascending = [False, True]),
                                 x = 'time_stamp',
                                 y = 'value',
                                 color = 'vintage',
                                 labels = {'time_stamp': 'Governing Council',
                                           'value': 'ESTR (%)',
                                           'vintage': 'Survey round'},
                                 color_discrete_sequence = [col for col in ecb_colormap.values()])

    tab1_chart1_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                     height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                     yaxis_range = [df.value.min() -.5,
                                                    df.value.max() +.5],
                                     xaxis_range = [df.time_stamp.min(),
                                                    df.time_stamp.max()],
                                     plot_bgcolor = 'white',
                                     showlegend = True,
                                     margin = dict(l = 5, r = 5, t = 5, b = 5),
                                     font = dict(family = 'Arial',
                                                 size = 15,
                                                 color = ecb_chart_elem_colormap['labels']))
    
    tab1_chart1_figure.update_xaxes(tickangle = 0,
                                    mirror = True,
                                    ticks = 'inside',
                                    showline = True,
                                    linecolor = ecb_chart_elem_colormap['axes'],
                                    gridcolor = ecb_chart_elem_colormap['grid'],
                                    tickformat = '%b-%y',
                                    tick0 = df.time_stamp.min(),
                                    dtick = 'M6')
    
    tab1_chart1_figure.update_yaxes(mirror = True,
                                    ticks = 'inside',
                                    showline = True,
                                    linecolor = ecb_chart_elem_colormap['axes'],
                                    gridcolor = ecb_chart_elem_colormap['grid'],
                                    tickformat = '.2f')

    tab1_chart1_figure.add_hline(y = 0,
                                 line_color = ecb_chart_elem_colormap['axes'],
                                 line_width = 1)

    return tab1_chart1_figure

# define function to update tab3_chart1
def update_tab3_chart1(df):

    tab3_chart1_figure = make_subplots(rows = 2,
                                       cols = 2,
                                       subplot_titles = [item for item in df.item.unique()])

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[0])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[0])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['yellow'],
                                            showlegend = True,
                                            name = 'Previous round',
                                            hoverinfo = 'none'),
                                 row = 1,
                                 col = 1)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[0])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[0])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['ecb_blue'],
                                            showlegend = True,
                                            name = 'Current round',
                                            hoverinfo = 'none'),
                                 row = 1,
                                 col = 1)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[1])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[1])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['yellow'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 1,
                                 col = 2)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[1])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[1])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['ecb_blue'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 1,
                                 col = 2)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[2])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[2])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['yellow'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 2,
                                 col = 1)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[2])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[2])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['ecb_blue'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 2,
                                 col = 1)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[3])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[1]) & (df.item == df.item.unique()[3])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['yellow'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 2,
                                 col = 2)

    tab3_chart1_figure.add_trace(go.Scatter(x = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[3])].time_stamp,
                                            y = df[(df.vintage == df.vintage.unique()[0]) & (df.item == df.item.unique()[3])].value,
                                            fill = None,
                                            mode = 'lines',
                                            line = dict(width = 2),
                                            line_color = ecb_colormap['ecb_blue'],
                                            showlegend = False,
                                            hoverinfo = 'none'),
                                 row = 2,
                                 col = 2)
    
    tab3_chart1_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                     height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                     plot_bgcolor = 'white',
                                     legend = dict(itemclick = False, itemdoubleclick = False),
                                     margin = dict(l = 5, r = 5, t = 20, b = 5),
                                     font = dict(family = 'Arial',
                                                 size = 15,
                                                 color = ecb_chart_elem_colormap['labels']))
    
    tab3_chart1_figure.update_xaxes(tickangle = 0,
                                    mirror = True,
                                    ticks = 'inside',
                                    showline = True,
                                    linecolor = ecb_chart_elem_colormap['axes'],
                                    gridcolor = ecb_chart_elem_colormap['grid'],
                                    tickformat = '%b-%y',
                                    dtick = 'M3')
    
    tab3_chart1_figure.update_yaxes(mirror = True,
                                    ticks = 'inside',
                                    showline = True,
                                    linecolor = ecb_chart_elem_colormap['axes'],
                                    gridcolor = ecb_chart_elem_colormap['grid'],
                                    tickformat = '.2f')

    return tab3_chart1_figure