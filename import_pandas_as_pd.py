
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv("youtubeanalysis.csv")

# Extract year and month from the upload_date column
df['upload_date'] = pd.to_datetime(df['upload_date'])
df['Year'] = df['upload_date'].dt.year
df['Month'] = df['upload_date'].dt.month

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("YouTube Video Analytics Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(2021, 2025)],
        value=2021,
        style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}
    ),

    dcc.Graph(id='yearly-view-count'),
    dcc.Graph(id='monthly-view-count'),
    dcc.Graph(id='top-10-videos'),
    dcc.Graph(id='view-count-pie-chart')
])

# Callback to update the yearly view count line chart
@app.callback(
    Output('yearly-view-count', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_yearly_view_count(selected_year):
    yearly_data = df[df['Year'] == selected_year]
    yearly_view_count = yearly_data.groupby('Year')['view_count'].sum().reset_index()
    fig = px.line(yearly_view_count, x='Year', y='view_count', title='Total Yearly View Count')
    return fig

# Callback to update the monthly view count line chart
@app.callback(
    Output('monthly-view-count', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_monthly_view_count(selected_year):
    monthly_data = df[df['Year'] == selected_year]
    monthly_view_count = monthly_data.groupby('Month')['view_count'].sum().reset_index()
    fig = px.line(monthly_view_count, x='Month', y='view_count', title='Total Monthly View Count')
    return fig

# Callback to update the top 10 videos bar chart
@app.callback(
    Output('top-10-videos', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_top_10_videos(selected_year):
    top_10_videos = df[df['Year'] == selected_year].nlargest(10, 'view_count')
    fig = px.bar(top_10_videos, x='video_title', y='view_count', title='Top 10 Videos by View Count')
    return fig

# Callback to update the view count pie chart
@app.callback(
    Output('view-count-pie-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_view_count_pie_chart(selected_year):
    video_view_counts = df[df['Year'] == selected_year].groupby('video_title')['view_count'].sum().reset_index()
    video_view_counts['share'] = video_view_counts['view_count'] / video_view_counts['view_count'].sum()
    video_view_counts['video_title'] = video_view_counts.apply(lambda x: x['video_title'] if x['share'] >= 0.05 else 'Others', axis=1)
    fig = px.pie(video_view_counts, names='video_title', values='view_count', title='View Count Share by Video Title')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)