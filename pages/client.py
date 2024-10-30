import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from globals import APP_TITLE, PAGE_HEADER_STYLE, DEFAULT_CLIENT_INFO, HELP_TEXT_CLIENT, create_help_button

dash.register_page(__name__, name='Client', order=1, title=APP_TITLE)

# Page layout
layout = html.Div([

    # Header
    html.H2('Client', style=PAGE_HEADER_STYLE),

    # Client info form
    # ID 
    dmc.TextInput(
        id={'type': 'client-info', 'field': 'ID'},
        label='ID',
        placeholder='ID',
        description='Anonymous identifier',
        w='19rem',
        className='mb-2',
    ),

    # Age
    dmc.NumberInput(
        id={'type': 'client-info', 'field': 'Age'},
        label='Age',
        description='In years',
        placeholder='Age',
        stepHoldDelay=500,
        stepHoldInterval=100,
        w='19rem',
        className='mb-2'
    ),

    # Gender
    dmc.TextInput(
        id={'type': 'client-info', 'field': 'Gender'},
        label='Gender',
        placeholder='Gender',
        description='Gender identity',
        w='19rem',
        className='mb-2'
    ),

    # Focus
    dmc.Textarea(
        id={'type': 'client-info', 'field': 'Focus'},
        label='Focus',
        description='Psychotherapy focus area',
        placeholder='Focus',
        autosize=True,
        minRows=1,
        w='19rem',
        className='mb-2'
    ),

    # Notes
    dmc.Textarea(
        id={'type': 'client-info', 'field': 'Notes'},
        label='Notes',
        placeholder='Notes',
        autosize=True,
        minRows=2,
        w='38rem',
        className='mb-2'
    ),  

    # Retrieve page url
    dcc.Location(id='page-url', refresh=False),

    create_help_button(HELP_TEXT_CLIENT)
])

# Callbacks

# Load client data
@callback(
    [Output({'type': 'client-info', 'field': field}, 'value') for field in DEFAULT_CLIENT_INFO.keys()],
    Input('client-store', 'data'),
    State('client-store', 'data'),
    prevent_initial_call=False
)
def load_client_data(client_data, current_data):

    if not client_data or not isinstance(client_data, list) or len(client_data) == 0:
        raise PreventUpdate
    client_info = client_data[0]
    values = [client_info.get(field, '') for field in DEFAULT_CLIENT_INFO.keys()]
    return values

# Update the client-store when leaving page
@callback(
    Output('client-store', 'data', allow_duplicate=True),
    Input('page-url', 'pathname'),
    [State({'type': 'client-info', 'field': field}, 'value') for field in DEFAULT_CLIENT_INFO.keys()],
    State('client-store', 'data'),
    prevent_initial_call=True
)
def update_client_data(pathname, id_value, age_value, gender_value, focus_value, notes_value, current_data):

    if pathname == '/client':
        raise PreventUpdate 
    
    if not current_data:
        current_data = [DEFAULT_CLIENT_INFO.copy()]
    
    current_data[0] = {
        'ID': id_value if id_value is not None else '',
        'Age': age_value if age_value is not None else None,
        'Gender': gender_value if gender_value is not None else '',
        'Focus': focus_value if focus_value is not None else '',
        'Notes': notes_value if notes_value is not None else ''
    }
    
    return current_data