import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from vega_datasets import data
import pandas as pd
import os

os.chdir("/Volumes/UBC/Block5/551/Project_MDS/dashboard-project-cryptocurrency_db")
source2 = pd.read_csv("price.csv")
source2['New_date1']=pd.to_datetime(source2['New_date1'], format='%Y-%m-%d')

line_volume = alt.Chart(source2).mark_line().encode(
    x=alt.X('New_date1', sort='x'),
    y=alt.Y('Volume'),
    color='Name',
    tooltip=['Name', 'Volume']
).properties(
    width=1400,
    height=300
)


app = dash.Dash(__name__)
app.layout = html.Div([
        html.Iframe(srcDoc=line_volume.to_html())])

if __name__ == '__main__':
    app.run_server(debug=True) 