import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Sample data for demonstration
df = pd.DataFrame({
    'Education Field': ['Computer Science', 'Computer Science', 'Engineering', 'Engineering'],
    'Skill Needed': ['Python', 'JavaScript', 'Matlab', 'C++'],
    'Skill Demand (%)': [75, 65, 50, 40]
})

# Dash application setup
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Youth Education and skill gap analysis"),
    
    html.Div([
        html.Label("Select Education Field:"),
        dcc.Dropdown(
            id='education-field-dropdown',
            options=[{'label': field, 'value': field} for field in df['Education Field'].unique()],
            value=df['Education Field'].unique()[0]
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label("Select Skill Needed:"),
        dcc.Dropdown(
            id='skill-needed-dropdown',
            options=[{'label': skill, 'value': skill} for skill in df['Skill Needed'].unique()],
            value=df['Skill Needed'].unique()[0]
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'margin-left': '20px'}),
    
    html.Div([
        html.Label("Demand Threshold:"),
        dcc.Slider(
            id='demand-threshold-slider',
            min=0,
            max=100,
            step=5,
            value=50,
            marks={i: f'{i}%' for i in range(0, 101, 10)}
        )
    ], style={'width': '80%', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='bar-chart'),
    ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between'}),
    
    html.Div(id='prediction-result', style={'padding': '20px', 'fontSize': 20, 'color': 'blue'}),
    html.Div(id='future-projection', style={'padding': '20px', 'fontSize': 18, 'color': 'green'}),
])

# Dummy prediction functions
def predict_skill_demand(field, skill):
    return f"Predicted demand for {skill} in {field} will rise by 10%."

def project_skill_demand(current_demand):
    return f"Projected future demand based on current demand of {current_demand}%."

# Callback for updating charts and prediction results
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('prediction-result', 'children'),
     Output('future-projection', 'children')],
    [Input('education-field-dropdown', 'value'),
     Input('skill-needed-dropdown', 'value'),
     Input('demand-threshold-slider', 'value')]
)
def update_charts_and_prediction(selected_field, selected_skill, demand_threshold):
    # Filter data for pie and bar charts based on the demand threshold
    filtered_data = df[(df['Education Field'] == selected_field) & (df['Skill Demand (%)'] >= demand_threshold)]
    
    # Create pie chart
    pie_chart = px.pie(
        filtered_data,
        names='Skill Needed',
        values='Skill Demand (%)',
        title="Skill Demand Distribution"
    )
    
    # Create bar chart
    bar_chart = px.bar(
        filtered_data,
        x='Skill Needed',
        y='Skill Demand (%)',
        color='Skill Needed',
        title="Skill Demand by Skill Needed"
    )
    
    # Check if data exists for the selected field and skill
    matching_data = df[(df['Education Field'] == selected_field) & (df['Skill Needed'] == selected_skill)]
    if not matching_data.empty:
        current_demand = matching_data['Skill Demand (%)'].values[0]
        prediction_message = predict_skill_demand(selected_field, selected_skill)
        future_projection_message = project_skill_demand(current_demand)
    else:
        prediction_message = f"No data available for {selected_skill} in {selected_field}."
        future_projection_message = ""

    return pie_chart, bar_chart, prediction_message, future_projection_message

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
