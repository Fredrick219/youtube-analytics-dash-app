import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the dataset
csv_url = 'https://raw.githubusercontent.com/Fredrick219/youtube-analytics-dash-app/main/youtubeanalysis.csv'
df = pd.read_csv(csv_url)

# Extract year from the upload_date column
df['upload_date'] = pd.to_datetime(df['upload_date'])
df['Year'] = df['upload_date'].dt.year

# Create the Dash app
app = Dash(__name__)
server = app.server

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
    dcc.Graph(id='top-10-videos'),
    dcc.Graph(id='view-count-pie-chart')
])

# Callback to update the yearly view count line chart
@app.callback(
    Output('yearly-view-count', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_yearly_view_count(selected_year):
    # Filter data for selected year
    year_df = df[df['Year'] == selected_year]
    
    # Total yearly view count
    fig = px.line(year_df, x='Year', y='view_count', title='Total Yearly View Count')
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
