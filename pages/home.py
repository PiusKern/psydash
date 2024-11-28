import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json
import base64
from globals import APP_TITLE, PAGE_HEADER_STYLE, INSTRUCTIONS, DEFAULT_CLIENT_INFO, DEFAULT_ROW_MEASURE, DEFAULT_ROW_PRACTICE, DEFAULT_ROW_SESSION, EXAMPLE_FILE_PATH, HELP_TEXT_HOME, create_help_button

dash.register_page(__name__, path='/', name='Home', order=0, title=APP_TITLE)

# Page layout

layout = html.Div([

    # Header
    html.H2('Home', style=PAGE_HEADER_STYLE),
    
    # Instructions
    dcc.Markdown(INSTRUCTIONS),
    
    # Buttons
    html.Div(
        [
            dbc.Button('New Record', id='new-record-btn', color='danger', className='mt-2 me-2'),
            dcc.Upload(
                id='load-record-btn',
                children=dbc.Button('Load Record', className='mt-2 me-2'),
                multiple=False,
                accept='.json'
            ),
            dbc.Button('Save Record', id='save-record-btn', color='success', className='mt-2 me-2'),
            dcc.Download(id='download-json'),
            dbc.Button('Show example', id='show-example-btn', color='secondary', className='mt-2 me-2'),            
        ], 
        style={'display': 'flex', 'flex-wrap': 'wrap'}
    ),

    # Modal confirm new record
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('New Record')),
        dbc.ModalBody('The current data will be deleted.'),
        dbc.ModalFooter([
            dbc.Button('Cancel', id='cancel-new-record-btn', color='secondary'),
            dbc.Button('Confirm', id='confirm-new-record-btn', color='danger')
        ]),
    ], id='new-record-modal', is_open=False),

    # Modal save record filename
    dbc.Modal([
        dbc.ModalHeader('Enter Filename'),
        dbc.ModalBody(
            dbc.Input(id='filename-input', placeholder='Enter filename', type='text')
        ),
        dbc.ModalFooter(
            dbc.Button('Save', id='confirm-save-btn', color='primary')
        ),
    ], id='filename-modal', is_open=False),

    # Alert
    dbc.Alert(id='data-alert', is_open=False, duration=4000, color='success', className='mt-2', style={'width': 'fit-content'}),
    create_help_button(HELP_TEXT_HOME)
])

# Callbacks

# Open filename modal
@callback(
    Output('filename-modal', 'is_open'),
    [Input('save-record-btn', 'n_clicks'), Input('confirm-save-btn', 'n_clicks')],
    [State('filename-modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_modal(save_clicks, confirm_clicks, is_open):
    if save_clicks or confirm_clicks:
        return not is_open
    return is_open

# Save data
@callback(
    Output('download-json', 'data'),
    Output('data-alert', 'children', allow_duplicate=True),
    Output('data-alert', 'is_open', allow_duplicate=True),
    Output('data-alert', 'color', allow_duplicate=True),
    Input('confirm-save-btn', 'n_clicks'),
    State('filename-input', 'value'),
    State('client-store', 'data'),
    State('measures-store', 'data'),
    State('sessions-store', 'data'),
    State('practices-store', 'data'),
    prevent_initial_call=True
)
def save_data(n_clicks, filename, client_data, measures_data, sessions_data, practices_data):
    if n_clicks is None or not filename:

        alert_message = 'Record not saved. Please enter a filename.'
        show_alert = True
        alert_color = 'warning'

        return dash.no_update, alert_message, show_alert, alert_color
    
    # Default the filename if not provided
    if not filename.endswith('.json'):
        filename += '.json'

    combined_data = {
        'client': client_data,
        'measures': measures_data,
        'sessions': sessions_data,
        'practices': practices_data
    }
    
    data_download = dict(content=json.dumps(combined_data, indent=2), filename=filename)
    alert_message = 'Record saved.'
    show_alert = True
    alert_color = 'success'

    return data_download, alert_message, show_alert, alert_color

# Show example
@callback(
    Output('client-store', 'data', allow_duplicate=True),
    Output('measures-store', 'data', allow_duplicate=True),
    Output('sessions-store', 'data', allow_duplicate=True),
    Output('practices-store', 'data', allow_duplicate=True),
    Output('data-alert', 'children', allow_duplicate=True),
    Output('data-alert', 'is_open', allow_duplicate=True),
    Output('data-alert', 'color', allow_duplicate=True),
    Input('show-example-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_example(show_example_clicks):

    if not show_example_clicks:
        raise PreventUpdate
    with open(EXAMPLE_FILE_PATH, 'r') as file:
        data = json.load(file)
    
    # Extract data from the JSON structure
    client_data = data.get('client', [])
    measures_data = data.get('measures', [])
    sessions_data = data.get('sessions', [])
    practices_data = data.get('practices', [])

    alert_message = 'Example loaded.'
    show_alert = True
    alert_color = 'success'
    
    return client_data, measures_data, sessions_data, practices_data, alert_message, show_alert, alert_color


# Load data
@callback(
    Output('client-store', 'data', allow_duplicate=True),
    Output('measures-store', 'data', allow_duplicate=True),
    Output('sessions-store', 'data', allow_duplicate=True),
    Output('practices-store', 'data', allow_duplicate=True),
    Output('data-alert', 'children', allow_duplicate=True),
    Output('data-alert', 'is_open', allow_duplicate=True),
    Output('data-alert', 'color', allow_duplicate=True),
    Input('load-record-btn', 'contents'),
    prevent_initial_call=True
)
def load_data(contents):
    if contents is None:
        raise PreventUpdate
    
    # Parse the contents of the uploaded file
    content_type, content_string = contents.split(',')
    
    # Decode the base64 encoded file content
    decoded = base64.b64decode(content_string)
    
    try:
        data = json.loads(decoded.decode('utf-8'))
        
        # Extract measures and sessions data from the JSON structure
        client_data = data.get('client', [])
        measures_data = data.get('measures', [])
        sessions_data = data.get('sessions', [])
        practices_data = data.get('practices', [])

        # Clean measures data
        for measure in measures_data:
            measure['SelectMeasure'] = bool(measure.get('SelectMeasure', False))
            measure['SelectRater'] = bool(measure.get('SelectRater', False))
        # Clean session data
        for session in sessions_data:
            for practice in practices_data:
                if practice['Name'] != 'New Practice':
                    session[practice['Name']] = bool(session.get(practice['Name'], False))

        alert_message = 'Record uploaded.'
        show_alert = True
        alert_color = 'success'
        
        return client_data, measures_data, sessions_data, practices_data, alert_message, show_alert, alert_color
    
    except:
        alert_message = 'Record not uploaded. Invalid file format.'
        show_alert = True
        alert_color = 'danger'
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, alert_message, show_alert, alert_color

# Start new record
@callback(
    Output('new-record-modal', 'is_open'),
    Output('data-alert', 'children', allow_duplicate=True),
    Output('data-alert', 'is_open', allow_duplicate=True),
    Output('data-alert', 'color', allow_duplicate=True),
    Output('client-store', 'data', allow_duplicate=True),
    Output('measures-store', 'data', allow_duplicate=True),
    Output('sessions-store', 'data', allow_duplicate=True),
    Output('practices-store', 'data', allow_duplicate=True),
    Input('new-record-btn', 'n_clicks'),
    Input('cancel-new-record-btn', 'n_clicks'),
    Input('confirm-new-record-btn', 'n_clicks'),
    State('client-store', 'data'),
    State('measures-store', 'data'),
    State('sessions-store', 'data'),
    State('practices-store', 'data'),
    prevent_initial_call=True
)
def start_new_record(new_clicks, cancel_clicks, confirm_clicks, 
                     client_data, measures_data, sessions_data, practices_data):
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    
    current_data_is_default = (
        client_data == [DEFAULT_CLIENT_INFO] and 
        measures_data == [DEFAULT_ROW_MEASURE] and 
        sessions_data == [DEFAULT_ROW_SESSION] and 
        practices_data == [DEFAULT_ROW_PRACTICE]
    )
    
    if trigger == 'new-record-btn' and current_data_is_default and new_clicks:
        return False, 'New record initialized.', True, 'success', *[dash.no_update] * 4
    
    if trigger == 'new-record-btn' and new_clicks:
        return True, *[dash.no_update] * 7  # Show modal
        
    if trigger == 'confirm-new-record-btn':
        return False, 'New record initialized.', True, 'success', [DEFAULT_CLIENT_INFO], [DEFAULT_ROW_MEASURE], [DEFAULT_ROW_SESSION], \
               [DEFAULT_ROW_PRACTICE]
    
    if trigger == 'cancel-new-record-btn':
        return False, *[dash.no_update] * 7
        
    raise PreventUpdate