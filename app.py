# import all from prepare_data_static_functions.py (BAD PRACTICE, AVOID import *)
from prepare_data_static_functions import *

# initialize dash instance
app = Dash(__name__)

# specify dashboard title (this is what is displayed in chrome tab)
app.title = browser_tab_name

# specify dashboard layout, display set to flex not to have H3 title defined below underneath ECB logo
app.layout = html.Div([html.H2(style = {'display': 'flex'},
                               children = [html.Img(src = ecb_header_logo,
                                                    style = {'display': 'block',
                                                             'margin-right': 'auto'}),
                                           html.H3(children = dash_header_name,
                                                   className = 'header-title')]),

                       # initialize tabs
                                 # define zero tab
                       dcc.Tabs([dcc.Tab(label = 'Reference data',
                                         className = 'tab-style',
                                         selected_className = 'tab-style-selected', 
                                         
                                                                          # define tab0-chart1 title (notify if data update is due)
                                         children = [html.Div(children = [html.Div(children = f'A new survey has been released. Update the dashboard to get the latest data.' if pd.to_datetime(time.time(), unit = 's', utc = True).tz_convert('Europe/Amsterdam') - next_release > pd.Timedelta(0) else '',
                                                                                   className = 'chart-title'),

                                                                          # embed list of participants into static table
                                                                          dcc.Graph(figure = go.Figure(layout = {'margin': dict(l = 5, r = 5, t = 5, b = 5)},
                                                                                                       data = go.Table(header = dict(values = ['Current participants', '', '', '', ''],
                                                                                                                                     fill_color = 'white',
                                                                                                                                     align = 'left',
                                                                                                                                     font = dict(family = 'Arial',
                                                                                                                                                 weight = 'bold',
                                                                                                                                                 size = 15,
                                                                                                                                                 color = ecb_colormap['ecb_blue'])),
                                                                                                                       cells = dict(values = [resps_df.col_0, resps_df.col_1, resps_df.col_2, resps_df.col_3, resps_df.col_4],
                                                                                                                                    fill_color = 'white',
                                                                                                                                    align='left',
                                                                                                                                    font = dict(family = 'Arial',
                                                                                                                                                size = 12,
                                                                                                                                                color = ecb_chart_elem_colormap['labels'])))))])]),

                                 # define first tab
                                 dcc.Tab(label = 'Key interest rates',
                                         className = 'tab-style',
                                         selected_className = 'tab-style-selected', 
                                         
                                                                          # define tab1-chart1 title
                                         children = [html.Div(children = [html.Div(children = 'Median expectations on the Euro Short-Term Rate',
                                                                                   className = 'chart-title'),
                                                                                               
                                                                          # define tab1-chart1 plot area         
                                                                          dcc.Graph(figure = update_tab1_chart1(df = df_tab1_chart1)),
                                                                          
                                                                          # define tab1-chart2 title
                                                                          html.Div(children = 'Uncertainty on policy rates by round',
                                                                                   className = 'chart-title'),

                                                                          # define tab1-chart2 subtitle
                                                                          html.Div(children = 'Shaded areas represent the interquartile range (IQR), defined as the difference between the 75\u1d57\u02b0 and 25\u1d57\u02b0 percentiles.',
                                                                                   className = 'chart-subtitle'),
                                                                                                                            # define tab1-chart2 dropdown menu 1
                                                                          html.Div(style = {'display': 'flex'}, children = [dcc.Dropdown(options = list(df_tab1_chart2.vintage.unique()),
                                                                                                                                         value = df_tab1_chart2.vintage.unique()[0],
                                                                                                                                         placeholder = 'Enter a survey round..',
                                                                                                                                         id = 'tab1-chart2-dropdown-1',
                                                                                                                                         className = 'dropdown-menu'),

                                                                                                                            # define tab1-chart2 dropdown menu 2
                                                                                                                            dcc.Dropdown(options = list(df_tab1_chart2.item.unique()),
                                                                                                                                         value = df_tab1_chart2.item.unique()[0],
                                                                                                                                         placeholder = 'Enter an interest rate..',
                                                                                                                                         id = 'tab1-chart2-dropdown-2',
                                                                                                                                         className = 'dropdown-menu'),
                                                                              
                                                                                                                            # define tab1-chart2 refresh button
                                                                                                                            html.Button('Refresh',
                                                                                                                                        id = 'tab1-chart2-button',
                                                                                                                                        className = 'refresh-button')]),
                                                                                               
                                                                          # define tab1-chart2 plot area         
                                                                          dcc.Graph(id = 'tab1-chart2')])]),

                                 # define second tab
                                 dcc.Tab(label = 'Balance sheet items and TPI',
                                         className = 'tab-style',
                                         selected_className = 'tab-style-selected',
                                         
                                                                          # define tab2-chart1 title
                                         children = [html.Div(children = [html.Div(children = 'Outstanding amount expectations by purchase program',
                                                                                   className = 'chart-title'),
                                                                          
                                                                          html.Div(style = {'display': 'flex'},
                                                                                   
                                                                                               # define tab2-chart1 dropdown menu 1
                                                                                   children = [dcc.Dropdown(options = list(df_tab2_chart1.vintage.unique()),
                                                                                                            value = df_tab2_chart1.vintage.unique()[0],
                                                                                                            placeholder = 'Enter a survey round..',
                                                                                                            id = 'tab2-chart1-dropdown-1',
                                                                                                            className = 'dropdown-menu'),

                                                                                               # define tab2-chart1 dropdown menu 2
                                                                                               dcc.Dropdown(options = list(df_tab2_chart1.measure.unique()),
                                                                                                            value = df_tab2_chart1.measure.unique()[0],
                                                                                                            placeholder = 'Enter a measure..',
                                                                                                            id = 'tab2-chart1-dropdown-2',
                                                                                                            className = 'dropdown-menu'),
                                                                              
                                                                              # define tab2-chart1 refresh button
                                                                              html.Button('Refresh',
                                                                                          id = 'tab2-chart1-button',
                                                                                          className = 'refresh-button')]),
                                                                                               
                                                                          # define tab2-chart1 plot area         
                                                                          dcc.Graph(id = 'tab2-chart1'),

                                                                          # define tab2-chart2 title
                                                                          html.Div(children = 'Average probability of TPI activation by round',
                                                                                   className = 'chart-title'),
                                                                          
                                                                          
                                                                          html.Div(style = {'display': 'flex'},
                                                                                            
                                                                                               # define tab2-chart2 dropdown menu
                                                                                   children = [dcc.Dropdown(options = opts_multi_drop,
                                                                                                            value = df_tab2_chart2.vintage.unique()[0],
                                                                                                            placeholder = 'Enter up to four survey rounds..',
                                                                                                            multi = True,
                                                                                                            clearable = False,
                                                                                                            id = 'tab2-chart2-dropdown',
                                                                                                            className = 'dropdown-menu'),
                                                                              
                                                                                               # define tab2-chart2 refresh button
                                                                                               html.Button('Refresh',
                                                                                                           id = 'tab2-chart2-button',
                                                                                                           className = 'refresh-button')]),
                                                                                               
                                                                          # define tab2-chart2 plot area         
                                                                          dcc.Graph(id = 'tab2-chart2')])]),

                                 # define third tab
                                 dcc.Tab(label = 'Macroeconomic outlook',
                                         className = 'tab-style',
                                         selected_className = 'tab-style-selected',
                                         
                                                                          # define tab3-chart1 title
                                         children = [html.Div(children = [html.Div(children = 'Expected macroeconomic paths',
                                                                                   className = 'chart-title'),
                                                                                               
                                                                          # define tab3-chart1 plot area         
                                                                          dcc.Graph(figure = update_tab3_chart1(df = df_tab3_chart1)),

                                                                          html.Div(style = {'display': 'flex',
                                                                                            'margin-top': '3%'},
                                                                                                                    # define tab3-chart2 title
                                                                                   children = [html.Div(children = [html.Div(children = 'Year-on-year comparison of long run HICP distribution',
                                                                                   className = 'chart-title'),

                                                                          html.Div(style = {'display': 'flex'},
                                                                                   
                                                                                               # define tab3-chart2 dropdown menu
                                                                                   children = [dcc.Dropdown(options = opts_tab3_chart2_dropdown,
                                                                                                            value = df_tab3_chart2.vintage_date.unique()[0],
                                                                                                            placeholder = 'Enter a survey round..',
                                                                                                            id = 'tab3-chart2-dropdown',
                                                                                                            className = 'dropdown-menu'),
                                                                                                
                                                                                               # define tab3-chart2 refresh button
                                                                                               html.Button('Refresh',
                                                                                                           id = 'tab3-chart2-button',
                                                                                                           className = 'refresh-button')]),

                                                                          # define tab3-chart2 plot area         
                                                                          dcc.Graph(id = 'tab3-chart2')]),

                                                                              html.Div(style = {'margin-left': '7%'},
                                                                                       
                                                                                                   # define tab3-chart3 title
                                                                                       children = [html.Div(children = 'Year-on-year Balance of Risks comparison by item',
                                                                                                            className = 'chart-title'),

                                                                                                   html.Div(style = {'display': 'flex'},
                                                                                                            
                                                                                                                        # define tab3-chart3 dropdown menu 1
                                                                                                            children = [dcc.Dropdown(options = opts_tab3_chart3_dropdown_1,
                                                                                                                                     value = df_tab3_chart3.vintage_date.unique()[0],
                                                                                                                                     placeholder = 'Enter a survey round..',
                                                                                                                                     id = 'tab3-chart3-dropdown-1',
                                                                                                                                     className = 'dropdown-menu'),

                                                                                                                        # define tab3-chart3 dropdown menu 2
                                                                                                                        dcc.Dropdown(options = opts_tab3_chart3_dropdown_2,
                                                                                                                                     value = df_tab3_chart3.item.unique()[0],
                                                                                                                                     placeholder = 'Enter an item..',
                                                                                                                                     id = 'tab3-chart3-dropdown-2',
                                                                                                                                     className = 'dropdown-menu'),
                                                                                                
                                                                                                                        # define tab3-chart3 refresh button
                                                                                                                        html.Button('Refresh',
                                                                                                                                    id = 'tab3-chart3-button',
                                                                                                                                    className = 'refresh-button')]),

                                                                          # define tab3-chart3 plot area         
                                                                          dcc.Graph(id = 'tab3-chart3')])])])])]),

                                 html.Div(children = [html.Label([f'Last data update: {last_update.strftime('%Y-%m-%d %H:%M')} CET.',
                                                                  html.Br(),
                                                                  f'Latest survey released on {latest_release.strftime('%d %B %Y')} at {latest_release.strftime('%H:%M')} CET. Next survey released on {next_release.strftime('%d %B %Y')} at {next_release.strftime('%H:%M')} CET.',
                                                                  html.Br(),
                                                                  html.Br(),
                                                                  'Disclaimer: The dashboard is intended to showcase Plotly Dash features, and shall only be used for entertainment purposes. No relationship exists between the author and the European Central Bank.',
                                                                  html.Br(),
                                                                  'Sources: ',
                                                                  html.A('The Survey of Monetary Analysts (ECB)',
                                                                         href = 'https://www.ecb.europa.eu/stats/ecb_surveys/sma/html/all-releases.en.html',
                                                                         target = '_blank')])],
                                          className = 'sources-disclaimer')])

# define callback for tab1-chart2
@app.callback(
    Output('tab1-chart2', 'figure'),
    State('tab1-chart2-dropdown-1', 'value'),
    State('tab1-chart2-dropdown-2', 'value'),
    Input('tab1-chart2-button', 'n_clicks'),
    prevent_initial_call = False
)

# define function to update tab1 chart2
def update_tab1_chart2(vintage, item, n_clicks):
    
    filter_df_tab1_chart2 = df_tab1_chart2.query('vintage == @vintage and item == @item')

    len_vints = len(filter_df_tab1_chart2.vintage.unique())
    len_items = len(filter_df_tab1_chart2.item.unique())

    if len_vints == 0 or len_items == 0:

        tab1_chart2_figure = go.Figure()

        tab1_chart2_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = 'white'))
        
        tab1_chart2_figure.add_annotation(showarrow = False,
                                          x = .5,
                                          xref = 'paper',
                                          y = .5,
                                          yref = 'paper',
                                          font = dict(color = ecb_colormap['ecb_blue']),
                                          text = display_error_msg)

        return tab1_chart2_figure
    
    else:
        
        filter_df_tab1_chart2_median = filter_df_tab1_chart2[filter_df_tab1_chart2.measure == 'MEDIAN'].sort_values(by = 'time_stamp').reset_index(drop = True)

        filter_df_tab1_chart2_p25 = filter_df_tab1_chart2[filter_df_tab1_chart2.measure == 'P25'].sort_values(by = 'time_stamp').reset_index(drop = True)

        filter_df_tab1_chart2_p75 = filter_df_tab1_chart2[filter_df_tab1_chart2.measure == 'P75'].sort_values(by = 'time_stamp').reset_index(drop = True)

        tab1_chart2_figure = go.Figure()

        tab1_chart2_figure.add_trace(go.Scatter(name = filter_df_tab1_chart2_median.vintage[0],
                                                x = filter_df_tab1_chart2_median.time_stamp,
                                                y = filter_df_tab1_chart2_median.value,
                                                fill = None,
                                                mode = 'lines',
                                                line_shape = 'hv',
                                                line = dict(width = 2),
                                                line_color = ecb_colormap['ecb_blue']))
                
        tab1_chart2_figure.add_trace(go.Scatter(x = filter_df_tab1_chart2_p25.time_stamp,
                                                y = filter_df_tab1_chart2_p25.value,
                                                fill = None,
                                                mode = 'lines',
                                                line_shape = 'hv',
                                                line = dict(width = 0),
                                                line_color = ecb_colormap['ecb_blue'],
                                                hoverinfo = 'skip'))

        tab1_chart2_figure.add_trace(go.Scatter(x = filter_df_tab1_chart2_p75.time_stamp,
                                                y = filter_df_tab1_chart2_p75.value,
                                                fill = 'tonexty', # fill area between trace0 and trace1
                                                mode = 'lines',
                                                line_shape = 'hv',
                                                line = dict(width = 0),
                                                line_color = ecb_colormap['ecb_blue'],
                                                hoverinfo = 'skip'))

        tab1_chart2_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         yaxis_range = [filter_df_tab1_chart2_p25.value.min() -.5,
                                                        filter_df_tab1_chart2_p75.value.max() +.5],
                                         xaxis_range = [filter_df_tab1_chart2_median.time_stamp.min(),
                                                        filter_df_tab1_chart2_median.time_stamp.max()],
                                         xaxis = dict(title = dict(text = 'Governing Council')),
                                         yaxis = dict(title = dict(text = 'Interest rate (%)')),
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = ecb_chart_elem_colormap['labels']))
        
        tab1_chart2_figure.update_xaxes(tickangle = 0,
                                        mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '%b-%y',
                                        tick0 = filter_df_tab1_chart2_median.time_stamp.min(),
                                        dtick = 'M3')
        
        tab1_chart2_figure.update_yaxes(mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '.2f')

        tab1_chart2_figure.add_hline(y = 0,
                                     line_color = ecb_chart_elem_colormap['axes'],
                                     line_width = 1)

        return tab1_chart2_figure

# define callback for tab2-chart1
@app.callback(
    Output('tab2-chart1', 'figure'),
    State('tab2-chart1-dropdown-1', 'value'),
    State('tab2-chart1-dropdown-2', 'value'),
    Input('tab2-chart1-button', 'n_clicks'),
    prevent_initial_call = False
)

# define function to update tab2 chart1
def update_tab2_chart1(vintage, measure, n_clicks):

    filter_df_tab2_chart1 = df_tab2_chart1.query('vintage == @vintage and measure == @measure')
    
    len_vints = len(filter_df_tab2_chart1.vintage.unique())
    len_measure = len(filter_df_tab2_chart1.measure.unique())

    if len_vints == 0 or len_measure == 0:

        tab2_chart1_figure = go.Figure()

        tab2_chart1_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = 'white'))
        
        tab2_chart1_figure.add_annotation(showarrow = False,
                                          x = .5,
                                          xref = 'paper',
                                          y = .5,
                                          yref = 'paper',
                                          font = dict(color = ecb_colormap['ecb_blue']),
                                          text = display_error_msg)

        return tab2_chart1_figure
    
    else:

        tab2_chart1_figure = px.area(filter_df_tab2_chart1,
                                     x = 'time_stamp',
                                     y = 'value',
                                     color = 'item',
                                     color_discrete_sequence = [col for col in ecb_colormap.values()],
                                     labels = {'time_stamp': 'Horizon',
                                               'value': 'Outstanding amount (EUR bns.)',
                                               'item': 'Programme'})

        tab2_chart1_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = True,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = ecb_chart_elem_colormap['labels']))
        
        tab2_chart1_figure.update_xaxes(tickangle = 0,
                                        mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '%b-%y',
                                        tick0 = filter_df_tab2_chart1.time_stamp.min(),
                                        dtick = 'M3')
        
        tab2_chart1_figure.update_yaxes(mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '.0f')

        tab2_chart1_figure.add_hline(y = 0,
                                     line_color = ecb_chart_elem_colormap['axes'],
                                     line_width = 1)

        return tab2_chart1_figure

# define callback for limiting dropdown menu options
@app.callback(
    Output(component_id = 'tab2-chart2-dropdown', component_property = 'options'),
    Input(component_id = 'tab2-chart2-dropdown', component_property = 'value')
)

# define function to prevent adding more than 4 options in tab2-chart2
def update_dropdown_options(values):

    if len(values) == 4:

        return [option for option in opts_multi_drop if option['value'] in values]
    
    else:
        
        return opts_multi_drop

# define callback for tab2-chart2
@app.callback(
    Output('tab2-chart2', 'figure'),
    State('tab2-chart2-dropdown', 'value'),
    Input('tab2-chart2-button', 'n_clicks'),
    prevent_initial_call = False
)

# define function to update tab2-chart2
def update_tab2_chart2(vintages, n_clicks):
    
    filter_df_tab2_chart2 = df_tab2_chart2.query('vintage in @vintages')

    len_vints = len(filter_df_tab2_chart2.vintage.unique())

    if len_vints == 0:

        tab2_chart2_figure = go.Figure()

        tab2_chart2_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = 'white'))
        
        tab2_chart2_figure.add_annotation(showarrow = False,
                                          x = .5,
                                          xref = 'paper',
                                          y = .5,
                                          yref = 'paper',
                                          font = dict(color = ecb_colormap['ecb_blue']),
                                          text = display_error_msg)
        
        return tab2_chart2_figure
    
    else:

        tab2_chart2_figure = make_subplots(rows = 1,
                                           cols = len_vints)

        # assign colors to type using a dictionary
        colors = {'Next 3 months': ecb_colormap['ecb_blue'],
                  'Next 4 to 6 months': ecb_colormap['yellow'],
                  'After 6 months': ecb_colormap['orange'],
                  'Never': ecb_colormap['light_green']}
        
        fig_conts = [go.Figure() for i in range(len_vints)]

        filter_df_tab2_chart2_lst = [filter_df_tab2_chart2[filter_df_tab2_chart2.vintage == filter_df_tab2_chart2.vintage.unique()[i]] for i in range(len_vints)]

        for i in range(len_vints):
            for t in filter_df_tab2_chart2.category.unique():
                dfp = filter_df_tab2_chart2_lst[i][filter_df_tab2_chart2_lst[i]['category'] == t]
                fig_conts[i].add_traces(go.Bar(x = dfp['vintage'],
                                               y = dfp['value'],
                                               name = t,
                                               marker_color = colors[t],
                                               showlegend = True if i == 0 else False))
                
            for trac in fig_conts[i].data:
                # added + 1 to counter as index starts from 0, else col value out of range error
                tab2_chart2_figure.append_trace(trac,
                                                row = 1,
                                                col = i + 1)

        tab2_chart2_figure.update_layout(width = (width_standalone_cm / 2.54) * ppi / scale_factor,
                                         height = (height_standalone_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = True,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         legend_title_text = 'Horizon',
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = ecb_chart_elem_colormap['labels']))
        
        tab2_chart2_figure.update_xaxes(tickangle = 0,
                                        mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'])
        
        tab2_chart2_figure.update_yaxes(mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '.1f')

        return tab2_chart2_figure

# define callback for tab3-chart2
@app.callback(
    Output('tab3-chart2', 'figure'),
    State('tab3-chart2-dropdown', 'value'),
    Input('tab3-chart2-button', 'n_clicks'),
    prevent_initial_call = False
)

# define function to update tab3-chart2
def update_tab3_chart2(vintage_date, n_clicks):

    try:

        prev_year = pd.to_datetime(vintage_date) - pd.offsets.DateOffset(years = 1)

        filter_df_tab3_chart2 = df_tab3_chart2.query('vintage_date == @vintage_date or vintage_date == @prev_year')

        tab3_chart2_figure = px.bar(data_frame = filter_df_tab3_chart2,
                                    x = 'bin_descr',
                                    y = 'value',
                                    color = 'vintage',
                                    barmode = 'group',
                                    color_discrete_sequence = [col for col in ecb_colormap.values()],
                                    labels = {'bin_descr': '',
                                              'value': 'Average probability (%)',
                                              'vintage': 'Survey round'})
        
        tab3_chart2_figure.update_layout(width = (width_coupled_cm / 2.54) * ppi / scale_factor,
                                         height = (height_coupled_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = True,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = ecb_chart_elem_colormap['labels']))
    
        tab3_chart2_figure.update_xaxes(tickangle = -90,
                                        mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'])
        
        tab3_chart2_figure.update_yaxes(mirror = True,
                                        ticks = 'inside',
                                        showline = True,
                                        linecolor = ecb_chart_elem_colormap['axes'],
                                        gridcolor = ecb_chart_elem_colormap['grid'],
                                        tickformat = '.1f')

        return tab3_chart2_figure
    
    except:

        tab3_chart2_figure = go.Figure()

        tab3_chart2_figure.update_layout(width = (width_coupled_cm / 2.54) * ppi / scale_factor,
                                         height = (height_coupled_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 11,
                                                     color = 'white'))
        
        tab3_chart2_figure.add_annotation(showarrow = False,
                                          x = .5,
                                          xref = 'paper',
                                          y = .5,
                                          yref = 'paper',
                                          font = dict(color = ecb_colormap['ecb_blue']),
                                          text = display_error_msg)

        return tab3_chart2_figure

# define callback for tab3-chart3
@app.callback(
    Output('tab3-chart3', 'figure'),
    State('tab3-chart3-dropdown-1', 'value'),
    State('tab3-chart3-dropdown-2', 'value'),
    Input('tab3-chart3-button', 'n_clicks'),
    prevent_initial_call = False
)

# define function to update tab3-chart3
def update_tab3_chart3(vintage_date, item, n_clicks):

    try:

        prev_year = pd.to_datetime(vintage_date) - pd.offsets.DateOffset(years = 1)

        filter_df_tab3_chart3_curr = df_tab3_chart3.query('vintage_date == @vintage_date and item == @item')
        filter_df_tab3_chart3_curr = filter_df_tab3_chart3_curr[filter_df_tab3_chart3_curr.date_descr == filter_df_tab3_chart3_curr.date_descr.min()]

        filter_df_tab3_chart3_prev = df_tab3_chart3.query('vintage_date == @prev_year and item == @item')
        filter_df_tab3_chart3_prev = filter_df_tab3_chart3_prev[filter_df_tab3_chart3_prev.date_descr == filter_df_tab3_chart3_prev.date_descr.min()]

        filter_df_tab3_chart3 = pd.concat([filter_df_tab3_chart3_curr, filter_df_tab3_chart3_prev], axis = 0).reset_index(drop = True)

        tab3_chart3_figure = make_subplots(rows = 1,
                                           cols = 2,
                                           specs = [[{'type': 'domain'}, {'type': 'domain'}]],
                                           subplot_titles = [item for item in filter_df_tab3_chart3.vintage.unique()])

        tab3_chart3_figure.add_trace(go.Pie(hole = .2,
                                            labels = filter_df_tab3_chart3_curr.category,
                                            values = filter_df_tab3_chart3_curr.value,
                                            hoverinfo = 'none'),
                                     row = 1,
                                     col = 1)
        
        tab3_chart3_figure.add_trace(go.Pie(hole = .2,
                                            labels = filter_df_tab3_chart3_prev.category,
                                            values = filter_df_tab3_chart3_prev.value,
                                            hoverinfo = 'none'),
                                     row = 1,
                                     col = 2)
        
        # increase size of plot area - commented out as share labels sometimes are covered by plot area
        #tab3_chart3_figure.data[0]['domain']['x'] = (0, .49)
        #tab3_chart3_figure.data[1]['domain']['x'] = ( .51, 1)

        # pull down subplot titles
        tab3_chart3_figure.layout['annotations'][0]['y'] = .9
        tab3_chart3_figure.layout['annotations'][1]['y'] = .9

        tab3_chart3_figure.update_traces(marker = dict(colors = [col for col in ecb_colormap.values()]))
        
        tab3_chart3_figure.update_layout(width = (width_coupled_cm / 2.54) * ppi / scale_factor,
                                         height = (height_coupled_cm / 2.54) * ppi / scale_factor,
                                         legend_title_text = 'Category',
                                         plot_bgcolor = 'white',
                                         showlegend = True,
                                         margin = dict(l = 5, r = 5, t = 20, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 15,
                                                     color = ecb_chart_elem_colormap['labels']))
        
        tab3_chart3_figure.add_annotation(align = 'left',
                                          showarrow = False,
                                          x = 0,
                                          xref = 'paper',
                                          y = .1,
                                          yref = 'paper',
                                          font = dict(family = 'Arial',
                                                      size = 10,
                                                      color = ecb_colormap['ecb_blue']),
                                          text = 'Note: From the perspective of each survey round, percentages refer to the closest horizon (e.g. July 2022 - 2022).')

        return tab3_chart3_figure
    
    except:

        tab3_chart3_figure = go.Figure()

        tab3_chart3_figure.update_layout(width = (width_coupled_cm / 2.54) * ppi / scale_factor,
                                         height = (height_coupled_cm / 2.54) * ppi / scale_factor,
                                         plot_bgcolor = 'white',
                                         showlegend = False,
                                         margin = dict(l = 5, r = 5, t = 5, b = 5),
                                         font = dict(family = 'Arial',
                                                     size = 11,
                                                     color = 'white'))
        
        tab3_chart3_figure.add_annotation(showarrow = False,
                                          x = .5,
                                          xref = 'paper',
                                          y = .5,
                                          yref = 'paper',
                                          font = dict(color = ecb_colormap['ecb_blue']),
                                          text = display_error_msg)

        return tab3_chart3_figure

# host dashboard locally
if __name__ == '__main__':

    app.run_server(debug = False)