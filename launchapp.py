import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Step 1. Launch the application
app = dash.Dash()

# Step 2. Import the dataset
st = pd.read_csv("data.csv")

# dropdown options
features = st.columns[1:-1]
opts = [{'label' : i, 'value' : i} for i in features]

# range slider options
st['Date'] = pd.to_datetime(st.Date)
dates = ['21/02/2017','21/03/2017', '21/04/2017', '21/05/2017', '21/06/2017',
         '21/07/2017', '21/08/2017', '21/09/2017', '21/10/2017', '21/11/2017', '21/12/2017','21/01/2018','20/02/2018']


# Step 3. Create a plotly figure
trace_1 = go.Scatter(x = st.Date, y = st['Bitcoin_CLOSE'],
                    name = 'Bitcoin_CLOSE',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)


# Step 4. Create a Dash layout
app.layout = html.Div([
                # a header and a paragraph
                html.Div([
                    html.H1("This is my first dashboard"),
                    html.P("Dash is so interesting!!")
                         ],
                     style = {'padding' : '50px' ,
                              'backgroundColor' : '#3aaab2'}),
                # adding a plot
                dcc.Graph(id = 'plot', figure = fig),
                # dropdown
                html.P([
                    html.Label("Choose a feature"),
                    dcc.Dropdown(id = 'opt', options=[{'label': col, 'value': col} for col in st.columns])],
                                value = 'Bitcoin_CLOSE')
                        ], style = {'width': '400px',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
                # range slider
                html.P([
                    html.Label("Time Period"),
                    dcc.RangeSlider(id = 'slider',
                                    marks = {i : dates[i] for i in range(0, 13)},
                                    min = 0,
                                    max = 12,
                                    value = [1, 6])
                        ], style = {'width' : '80%',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})
                      ])


# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value'),
             Input('slider', 'value')])
def update_figure(input1, input2):
    # filtering the data
    st2 = st[(st.Date > dates[input2[0]]) & (st.Date < dates[input2[1]])]
    # updating the plot
    trace_1 = go.Scatter(x = st2.Date, y = st2['Bitcoin_CLOSE'],
                        name = 'Bitcoin_CLOSE',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = st2.Date, y = st2[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig = go.Figure(data = [trace_1, trace_2], layout = layout)
    return fig
  
# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)

