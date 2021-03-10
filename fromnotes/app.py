#import dash
#import dash_html_components as html


#app = dash.Dash()
#app.layout = html.Div('I am alive!!')
#app.run_server()


import dash
import dash_html_components as html


app = dash.Dash(__name__)

app.layout = html.Div('I am alive finally!!')

if __name__ == '__main__':
    app.run_server(debug=True)

    