from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np

import pandas as pd
import plotly.express as px



data = pd.read_csv('train.csv')
new = data[['Order Date','Sales']]
new['days'] = pd.to_datetime(new['Order Date'],format='%d/%m/%Y').dt.strftime("%A")
new['color'] = new.apply(lambda x: "Weekend" if x['days'] in ["Saturday","Sunday"] else "weekday",axis=1)


app = Dash(__name__)

fig = px.histogram(new, x="days",y="Sales",color="color",hover_name="Order Date",category_orders=dict(days=["Thursday", "Friday", "Saturday", "Sunday","Monday","Wednesday","Tuesday"]))
fig.update_layout(bargap=0.6)


def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


fig2 = px.line(new,x="days",y="Sales")

app.layout = html.Div(
    
    
    
    style = {'color':'green','textAlign':'left','padding-left':'20px',"padding-right":'20px'},children=[
    html.H1('Daily Total Sale '),
    
    dcc.Graph(
    id="bar-1",
    figure=fig
    ),

    dcc.Graph(
    id="bar-2",
    figure=fig2
    ),

    html.H1("Sales Data"),
    html.Div(style={"backgroundColor":"white",'color':"black"},children=[
    generate_table(data)

    ])

    
])





if __name__ == "__main__":
    app.run_server(debug=True)
