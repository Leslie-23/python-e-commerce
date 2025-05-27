import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import pandas as pd
import random
import base64
from io import BytesIO
from .dbaccess import Quarterly_sales, select_year

# Sample data
df = pd.DataFrame(
    {
        "Sales": [0, 0, 0, 0],
        "Quarters": ["Q1", "Q2", "Q3", "Q4"],
    }
)

def create_matplotlib_figure(sales_data, selected_year):
    """Create a matplotlib figure and return as base64 encoded image"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(df["Quarters"], sales_data, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    ax.set_title(f"Sales in each quarter for {selected_year}", fontsize=18, fontname='Arial')
    ax.set_xlabel('Quarters', fontsize=15, fontname='Arial')
    ax.set_ylabel('Sales', fontsize=15, fontname='Arial')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom', fontsize=12, fontname='Arial')
    
    # Customize ticks
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    plt.tight_layout()
    
    # Save it to a temporary buffer
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    
    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    years, selected_value = select_year()
    
    dash_app.layout = html.Div(
        children=[
            html.H1(
                "Total Quarterly Sales Over Years", 
                style={
                    'textAlign': 'center', 
                    'font-family': 'Arial', 
                    'font-size': '24px'
                }
            ),
            html.Div(
                "Select a year", 
                style={
                    'font-family': 'Arial', 
                    'font-size': '20px'
                }
            ),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": year[0], "value": year[0]} for year in years],
                value=selected_value,
                style={
                    'width': '50%', 
                    'font-family': 'Arial', 
                    'font-size': '20px', 
                    'border-radius': '15px'
                },
            ),
            html.Div(
                id="graph-container",
                children=[
                    html.Img(id="matplotlib-graph")
                ],
                style={'textAlign': 'center'}
            )
        ]
    )

    @dash_app.callback(
        Output("matplotlib-graph", "src"),
        [Input("year-dropdown", "value")]
    )
    def update_graph(selected_year):
        new_sales = Quarterly_sales(selected_year)
        return create_matplotlib_figure(new_sales, selected_year)

    return dash_app