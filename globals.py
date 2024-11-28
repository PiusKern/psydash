from datetime import date
import seaborn as sns
import os
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# App title displayed in the browser tab
APP_TITLE = 'PsyDash'

# Page header style
PAGE_HEADER_STYLE = {
    'display': 'inline', 
    'line-height': '3rem', 
    'font-size': '2rem'
}

# Directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_FILE_PATH = os.path.join(CURRENT_DIR, "example-data", "example.json")

# Instructions
INSTRUCTIONS = '''
PsyDash is a dashboard app that helps you track psychotherapy progress.

1. **Client**: Record information on the client.
2. **Measures**: Define the measures you want to track.
3. **Practices**: Specify the therapeutic interventions you plan to implement.
4. **Sessions**: Record data for each therapy session.
5. **Dashboard**: Visualize the sessions and progress over time.
'''

# AG Grid
AG_GRID_THEME = 'ag-theme-quartz'

# Default data
DATE_TODAY = date.today().isoformat()
DEFAULT_CLIENT_INFO = {'ID': '', 'Age': '', 'Gender':  '', 'Focus': '', 'Notes': ''}
DEFAULT_ROW_MEASURE = {'Name': 'New Measure', 'Type': 'Scale', 'Min': 0, 'Max': 100, 'Rater': 'Self', 'Description': '', 'SelectMeasure': False, 'SelectRater': False}
DEFAULT_ROW_PRACTICE = {'Name': 'New Practice', 'Description': ''}
DEFAULT_ROW_SESSION = {'session_number': 1, 'session_date': DATE_TODAY}

# Color palette measures
COLORS_MEASURES = sns.color_palette('tab20').as_hex()
COLORS_MEASURES = COLORS_MEASURES[::2] + COLORS_MEASURES[1::2]

# Alert duration
ALERT_DURATION = 7000

# Help button
def create_help_button(help_text, position="bottom-end", button_position={'top': '2rem', 'right': '2rem'}):

    return html.Div([
        dmc.HoverCard(
            withArrow=True,
            width='38rem',
            position=position,
            shadow="md",
            children=[
                dmc.HoverCardTarget(
                    dmc.ActionIcon(
                        DashIconify(icon="material-symbols:question-mark", width=20),
                        size="lg",
                        radius="xl",
                        variant="filled",
                        color="blue",
                    ),
                ),
                dmc.HoverCardDropdown(
                    dcc.Markdown(help_text),
                    style={'overflowY': 'auto', 'height': 'auto'}
                ),
            ],
        )
    ], style={
        'position': 'fixed',
        'zIndex': '62rem',
        **button_position
    })

# Help texts

HELP_TEXT_HOME = """
### Help

Manage the data record.

- Start a new record by clicking **Start New**. 
- Load and edit an existing record by clicking **Load Record**. Only .json files saved from PsyDash are accepted.
- Save a record by clicking **Save Record**. In the pop-up menu, enter a filename. The filetype .json is added automatically.
- Show an example by clicking **Show example**.
"""


HELP_TEXT_CLIENT = """
### Help

Enter information on the client.

- Do not enter personally identifiable information.
- In the **Focus** field, add diagnoses or core symptoms.
"""

HELP_TEXT_MEASURES = """
### Help

Set the measures used for tracking psychotherapy progress. Changing the details of a measure later is possible.

##### Name
- Clear and short names are recommended.

##### Rater
- Specify the rater by selecting from the dropdown menu (Self, Educator, Caregiver, Therapist, Other).

##### Type, Min, Max
- Specify the type of measure by selecting Scale or Count from the dropdown menu. 
- For scale-based measures, specify the Min and Max. Only valid numbers are accepted. Use dots for decimals.
- **ATTENTION**: Changing Min and Max might delete data in *Sessions* if the session data is out of the updated range.
- For count-based measures, the Min is set to 0 automatically.

##### Description
- Add a description to specify the measure used.

##### Add and delete measures
- Add a new measure by clicking the **Add Row** button. 
- Delete selected measures by clicking the **Delete Selected** button.
"""

HELP_TEXT_PRACTICES = """
### Help

Manage the practices implemented in your psychotherapy sessions.

##### Name
- Clear and short names are recommended.
- Updating the name is always possible.

##### Description
- Add a description to specify the practice used.

##### Add and delete practices
- Add a new practice by clicking the **Add Row** button. 
- Delete selected practices by clicking the **Delete Selected** button.
"""

HELP_TEXT_SESSIONS = """
### Help

Administrate sessions and enter data.

##### Session number and date
- The **Session** number is fixed. To ensure data consistency, you can only add subsequent sessions. Changing the order of sessions is not possible.
- Edit the session **Date** by clicking on the cell. For data consistency, dates have to be in linear order.

##### Measures
- View details about a measure by hovering over the column header.
- Edit the session data for a measure by clicking on the cell. Only valid numbers in the defined Min - Max range are accepted. Use dots for decimals.

##### Practices
- Mark the implementation of a practice by clicking the checkbox.

##### Add and delete sessions
- Add a new session by clicking the **Add Row** button. 
- Delete selected sessions by clicking the **Delete Selected** button.
"""

HELP_TEXT_DASHBOARD = """
### Help

View the dashboard and set options for the visualization.

##### Measures
- Select measures to plot using the switches.
- Changing the measure switches will reset the selection of raters.

##### Raters
- Select measures based on the rater using the switches.

##### Y-Axis
- Change the scaling of the y-axis by selecting Raw or Normalized from the dropdown menu.
- Raw shows the raw values.
- Normalized shows the values normalized according to the defined Min and Max. For count-based measures, Max is set to the maximum value in the data.

##### X-Axis
- Change the unit of the x-axis by selecting Day or Session from the dropdown menu.
"""

# Retrieve selected raters from measures
def get_rater_selection(measures_data):
    rater_selection = {}
    for measure in measures_data:
        if measure['Rater'] not in rater_selection:
            rater_selection[measure['Rater']] = measure['SelectRater']
    rater_selection = dict(sorted(rater_selection.items()))

    return rater_selection

# Encode and decode text strings to handle umlauts and other special characters
from urllib.parse import quote, unquote
def encode_text(text):
    return quote(text)
def decode_text(text):
    return unquote(text)