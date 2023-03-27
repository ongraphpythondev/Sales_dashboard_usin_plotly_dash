# Import libraries
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import plotly.express as px


# Load data set
data = pd.read_csv('train.csv')

new = data[['Order Date', 'Sales']]

# filter day from Order date column
new['days'] = pd.to_datetime(
    new['Order Date'], format='%d/%m/%Y').dt.strftime("%A")

# filter weekday and weekends
new['color'] = new.apply(lambda x: "Weekend" if x['days'] in [
                         "Saturday", "Sunday"] else "weekday", axis=1)


# creating dash app
app = Dash(__name__)    

# creating histogram
fig = px.histogram(new, x="days", y="Sales", color="color", hover_name="Order Date", category_orders=dict(
    days=["Thursday", "Friday", "Saturday", "Sunday", "Monday", "Wednesday", "Tuesday"]))
fig.update_layout(bargap=0.6)


#creating pie chart , total sales in weekdays
fig_pie = px.pie(new, values='Sales', names='days')
fig_pie.update_layout(bargap=0.6)


#creating pie chart, total sales in weekend and weekdays  
fig_pie1 = px.pie(new, values='Sales', names='color')
fig_pie1.update_layout(bargap=0.6)

# display the 20 rows of the dataset on the dash app
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


# creating Line chat
fig2 = px.line(new, x="days", y="Sales")

app.layout = html.Div(



    style={'color': 'green', 'textAlign': 'left', 'padding-left': '20px', "padding-right": '20px'}, children=[
        html.H1('Daily Total Sale '),

        dcc.Graph(
            id="bar-1",
            figure=fig
        ),


        html.H1("Total Sales in weekdays"),
        dcc.Graph(
            id="pie-1",
            figure=fig_pie
        ),
          html.H1("Total Sales in weekdays and weekends"),
        dcc.Graph(
            id="pie-2",
            figure=fig_pie1
        ),

        html.H1("Sales Data"),
        html.Div(style={"backgroundColor": "white", 'color': "black"}, children=[
            generate_table(data)

        ]),

        dcc.Graph(
            id="line-1",
            figure=fig2
        ),

    ])


# main
if __name__ == "__main__":
    app.run_server(debug=True)
