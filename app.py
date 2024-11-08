import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Function to calculate the investments and profits
def calculate_investments(odds_a, odds_b, total_investment):
    inv_ratio_a = 1 / odds_a
    inv_ratio_b = 1 / odds_b

    total_ratio = inv_ratio_a + inv_ratio_b
    R = total_investment / total_ratio

    investment_a = R / odds_a
    investment_b = R / odds_b

    return_a = investment_a * odds_a
    return_b = investment_b * odds_b
    profit_a = return_a - total_investment
    profit_b = return_b - total_investment

    return investment_a, investment_b, profit_a, profit_b

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(
    style={
        'backgroundColor': '#f4f4f4', 
        'padding': '30px', 
        'fontFamily': 'Arial, sans-serif',
        'color': '#333'
    },
    children=[
        html.H1("Investment Ratio Calculator", style={
            'textAlign': 'center', 
            'color': '#007bff', 
            'marginBottom': '30px'
        }),

        # Hardcoded labels and empty input fields
        dbc.Row(
            [
                dbc.Col(
                    html.Label("Odds for Team A", style={'fontWeight': 'bold'}),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
                dbc.Col(
                    html.Label("Odds for Team B", style={'fontWeight': 'bold'}),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
                dbc.Col(
                    html.Label("Total Investment", style={'fontWeight': 'bold'}),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
            ],
            justify="center",
        ),

        # Input fields for odds and total investment (now empty)
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(id='odds_a', type='number', debounce=True),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
                dbc.Col(
                    dbc.Input(id='odds_b', type='number', debounce=True),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
                dbc.Col(
                    dbc.Input(id='total_investment', type='number', debounce=True),
                    width=3,
                    style={'marginBottom': '15px'}
                ),
            ],
            justify="center",
        ),

        # Display total investment value entered
        html.Div(
            id='total_investment_display', 
            style={
                'marginTop': '30px', 
                'fontSize': '18px', 
                'fontWeight': 'bold', 
                'textAlign': 'center'
            }
        ),

        # Output area for showing the calculated results in table format
        html.Div(
            id='investment_table', 
            style={
                'marginTop': '30px', 
                'backgroundColor': '#fff', 
                'padding': '20px', 
                'borderRadius': '8px', 
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'fontSize': '18px',
                'color': '#28a745'
            }
        ),
        
        html.Div(
            id='profit_display', 
            style={
                'marginTop': '20px', 
                'fontSize': '18px', 
                'fontWeight': 'bold', 
                'color': '#28a745',
                'textAlign': 'center'
            }
        ),

        html.Br(),

        # Button to trigger calculation
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Calculate", 
                    id="calculate-btn", 
                    color="primary", 
                    style={'width': 'auto', 'padding': '8px 20px', 'fontSize': '16px'}
                ),
                width=12,
                style={'textAlign': 'center'}
            ),
        ),
    ]
)

# Callback to update the output dynamically
@app.callback(
    [Output('investment_table', 'children'),
     Output('profit_display', 'children'),
     Output('total_investment_display', 'children')],
    [Input('odds_a', 'value'),
     Input('odds_b', 'value'),
     Input('total_investment', 'value')]
)
def update_output(odds_a, odds_b, total_investment):
    if odds_a and odds_b and total_investment:
        # Calculate the investments and profits
        investment_a, investment_b, profit_a, profit_b = calculate_investments(float(odds_a), float(odds_b), float(total_investment))
        
        # Generate the table with investment values and potential profits
        table = html.Table(
            style={'margin': '0 auto'},  # Center the table
            children=[
                html.Thead(
                    html.Tr([ 
                        html.Th(""), 
                        html.Th(f"Team A ({odds_a})", style={'color': 'red'}),
                        html.Th(f"Team B ({odds_b})", style={'color': 'purple'})
                    ])
                ),
                html.Tbody([ 
                    html.Tr([ 
                        html.Td("Invest value", style={'paddingRight': '40px', 'color': 'black'}),  # Black color for 'Invest value'
                        html.Td(f"₹ {investment_a:.2f}", style={'paddingRight': '40px', 'color': 'black'}),  # Black for Team A investment
                        html.Td(f"₹ {investment_b:.2f}", style={'color': 'black'})  # Black for Team B investment
                    ]),
                ])
            ]
        )

        # Calculate profit
        profit_display = f"Profit: ₹ {profit_a:.2f}" if profit_a == profit_b else f"Profit: ₹ {profit_b:.2f}"
        profit_display = html.Div(profit_display, style={'color': '#28a745'})  # Green color for profit

        # Display total investment entered
        total_investment_display = f"Total Investment: ₹ {total_investment}"

        return table, profit_display, total_investment_display

    return "", "", ""  # Return empty if inputs are not valid


# Run the app
if __name__ == '__main__':
    app.run_server()
