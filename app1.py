import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1("Hello !!"),
    dcc.Graph(id='toto',
        figure={
            'data': [
                {'x':[1,2,3,4], 'y':[6,7,8,9], 'type':'bar','name':'boats'},
                {'x':[1,2,3,4], 'y':[12,4,8,17], 'type':'line','name':'boats'}],
            'layout':  {
                'title':'Basic Dash Example'
            }
        })
])

if __name__ == "__main__":
    app.run_server(debug=True)

