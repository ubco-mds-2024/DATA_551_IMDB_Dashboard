import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
import re
import ast
import os
# Additional imports for modeling
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# ---------------------
# Data Loading & Preprocessing
# ---------------------
data_path = 'data/final_dataset.csv'
#df = pd.read_csv(data_path).sample(n=1000, random_state=42)
df = pd.read_csv(data_path)
df = df[['Title', 'Year', 'Duration', 'Rating', 'budget', 'grossWorldWide', 'gross_US_Canada', 
         'opening_weekend_Gross', 'directors', 'writers', 'stars', 'genres']]
df = df.dropna(subset=['budget', 'grossWorldWide', 'gross_US_Canada'])
df = df[df['budget'] != df['budget'].max()]

def convert_duration(duration):
    match = re.match(r"(\d+)h\s*(\d*)m?", str(duration))
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes
    return None

df['Duration'] = df['Duration'].apply(convert_duration).astype('Int64')

def convert_list_to_string(value):
    try:
        parsed_list = ast.literal_eval(value)
        if isinstance(parsed_list, list):
            return ", ".join(parsed_list)
    except (ValueError, SyntaxError):
        pass
    return value

df['directors'] = df['directors'].apply(convert_list_to_string)
df['writers'] = df['writers'].apply(convert_list_to_string)
df['stars'] = df['stars'].apply(convert_list_to_string)

def categorize_genres(genres):
    category_map = {
        'Action': ['Action', 'B-Action', 'Car Action', 'Gun Fu', 'One-Person Army Action',
                   'Martial Arts', 'Kung Fu', 'Wuxia', 'Swashbuckler', 'Samurai',
                   'Extreme Sport', 'Motorsport', 'Water Sport', 'Boxing', 'Football',
                   'Baseball', 'Basketball', 'Soccer'],
        'Adventure': ['Adventure', 'Sea Adventure', 'Desert Adventure', 'Jungle Adventure',
                      'Mountain Adventure', 'Urban Adventure', 'Globetrotting Adventure',
                      'Animal Adventure', 'Dinosaur Adventure', 'Quest', 'Sword & Sorcery',
                      'Sword & Sandal', 'Kaiju'],
        'Comedy': ['Comedy', 'Dark Comedy', 'Raunchy Comedy', 'Slapstick', 'Parody',
                   'Satire', 'Farce', 'Sketch Comedy', 'Buddy Comedy', 'Stoner Comedy',
                   'High-Concept Comedy', 'Body Swap Comedy', 'Quirky Comedy', 'Mockumentary',
                   'Screwball Comedy', 'Holiday Comedy'],
        'Drama': ['Drama', 'Medical Drama', 'Political Drama', 'Costume Drama', 'Period Drama',
                  'Psychological Drama', 'Legal Drama', 'Workplace Drama', 'Showbiz Drama',
                  'Cop Drama', 'Prison Drama', 'Coming-of-Age', 'Docudrama', 'Teen Drama'],
        'Thriller/Mystery': ['Thriller', 'Political Thriller', 'Conspiracy Thriller',
                             'Psychological Thriller', 'Erotic Thriller', 'Cyber Thriller',
                             'Legal Thriller', 'Mystery', 'Suspense Mystery', 'Whodunnit',
                             'Hard-boiled Detective', 'Bumbling Detective', 'Cozy Mystery'],
        'Horror': ['Horror', 'Monster Horror', 'Supernatural Horror', 'B-Horror',
                   'Body Horror', 'Folk Horror', 'Vampire Horror', 'Slasher Horror',
                   'Psychological Horror', 'Teen Horror', 'Zombie Horror', 'Splatter Horror',
                   'Witch Horror', 'Found Footage Horror'],
        'Sci-Fi/Fantasy': ['Sci-Fi', 'Dystopian Sci-Fi', 'Space Sci-Fi', 'Cyberpunk',
                           'Steampunk', 'Fantasy', 'Dark Fantasy', 'Supernatural Fantasy',
                           'Artificial Intelligence', 'Alien Invasion', 'Time Travel',
                           'Fairy Tale', 'Teen Fantasy'],
        'Crime': ['Crime', 'Heist', 'True Crime', 'Gangster', 'Drug Crime',
                  'Police Procedural', 'Serial Killer', 'Caper'],
        'Romance': ['Romance', 'Romantic Comedy', 'Dark Romance', 'Holiday Romance',
                    'Steamy Romance', 'Tragic Romance', 'Feel-Good Romance', 'Teen Romance'],
        'Musical': ['Musical', 'Rock Musical', 'Jukebox Musical', 'Pop Musical',
                    'Classic Musical'],
        'War/History': ['War', 'History', 'Historical Epic', 'War Epic'],
        'Western': ['Western', 'Contemporary Western', 'Spaghetti Western',
                    'Western Epic', 'Classical Western'],
        'Animation': ['Animation', 'Hand-Drawn Animation', 'Computer Animation',
                      'Stop Motion Animation', 'Adult Animation', 'Anime'],
        'Family': ['Family', 'Holiday Family'],
        'Sport': ['Sport'],
        'Biography': ['Biography'],
        'Disaster': ['Disaster'],
        'Documentary': ['Documentary', 'Stand-Up']
    }
    for category, keywords in category_map.items():
        if any(genre in genres for genre in keywords):
            return category
    return 'Other'

df['genres'] = df['genres'].apply(lambda x: categorize_genres(str(x)))
alt.data_transformers.disable_max_rows()

# ---------------------
# Profitability & Prediction Setup
# ---------------------
df['profit'] = df['grossWorldWide'] - df['budget']
df['gross_budget_ratio'] = df['profit'] / df['budget']

def categorize_profitability(ratio):
    if ratio >= 2.0:
        return "2.0+"
    elif ratio >= 1.8:
        return "1.8+"
    elif ratio >= 1.6:
        return "1.6+"
    elif ratio >= 1.4:
        return "1.4+"
    elif ratio >= 1.2:
        return "1.2+"
    else:
        return "<1.2"

df['profitability_category'] = df['gross_budget_ratio'].apply(categorize_profitability)
# Remove rows with zero budget or missing profitability data
df = df[df['budget'] != 0]
df = df.dropna(subset=['gross_budget_ratio', 'profitability_category'])

# Create a copy for prediction
df_pred = df.copy()

# ---------------------
# Create exploded dataset for prediction only
# ---------------------
df_pred['star_exploded'] = df_pred['stars'].apply(
    lambda x: [s.strip() for s in str(x).split(',') if s.strip() and s.strip().lower() != 'nan']
)
df_pred['director_exploded'] = df_pred['directors'].apply(
    lambda x: [s.strip() for s in str(x).split(',') if s.strip() and s.strip().lower() != 'nan']
)
df_pred = df_pred.explode('star_exploded')
df_pred = df_pred.explode('director_exploded')

# For prediction, encode categorical features.
label_encoders = {}
for col in ['broad_genre', 'star_exploded', 'director_exploded']:
    le = LabelEncoder()
    if col == 'broad_genre':
        df_pred[col + '_encoded'] = le.fit_transform(df_pred['genres'])
    else:
        df_pred[col + '_encoded'] = le.fit_transform(df_pred[col])
    label_encoders[col] = le

# Train classification model to predict profitability category.
from sklearn.metrics import classification_report, accuracy_score
le_profit = LabelEncoder()
y_class = df_pred['profitability_category']
y_class_encoded = le_profit.fit_transform(y_class)
X_class = df_pred[['broad_genre_encoded', 'star_exploded_encoded', 'director_exploded_encoded', 'budget']]
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_class, y_class_encoded, test_size=0.2, random_state=42, stratify=y_class_encoded
)
rf_class = RandomForestClassifier(random_state=42)
rf_class.fit(X_train_c, y_train_c)

# Train regression model to predict gross/budget ratio.
from sklearn.metrics import mean_absolute_error, r2_score
X_reg = df_pred[['broad_genre_encoded', 'star_exploded_encoded', 'director_exploded_encoded', 'budget']]
y_reg = df_pred['gross_budget_ratio']
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)
rf_reg = RandomForestRegressor(random_state=42)
rf_reg.fit(X_train_r, y_train_r)

# Update the prediction function using the exploded columns
def predict_profitability(genre, star, director, budget, model_class, model_reg):
    genre_encoded = label_encoders['broad_genre'].transform([genre])[0]
    star_encoded = label_encoders['star_exploded'].transform([star])[0]
    director_encoded = label_encoders['director_exploded'].transform([director])[0]
    movie_features = [[genre_encoded, star_encoded, director_encoded, budget]]
    prediction_class = model_class.predict(movie_features)
    predicted_category = le_profit.inverse_transform(prediction_class)[0]
    prediction_reg = model_reg.predict(movie_features)[0]
    return predicted_category, prediction_reg

# ---------------------
# App Layout & Callbacks
# ---------------------
friendly_names = {
    'Year': 'Year of Release',
    'Duration': 'Duration (minutes)',
    'Rating': 'Movie Rating',
    'budget': 'Movie Budget',
    'grossWorldWide': 'Movie Gross Worldwide',
    'gross_US_Canada': 'Movie Gross in North America',
    'opening_weekend_Gross': 'Opening Weekend Gross',
    'profit': 'Profit',
    'gross_budget_ratio': 'Gross/Budget Ratio'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="IMDB Dashboard")
# Expose the Flask server for deployment
server = app.server

app.layout = dbc.Container([
    html.H1('IMDB Dashboard', style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Plots', children=[
            dbc.Row([
                dbc.Col([
                    html.H5("Scatter Plot"),
                    dcc.Dropdown(
                        id='scatter-x-widget',
                        value='Rating',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select X-axis variable"
                    ),
                    dcc.Dropdown(
                        id='scatter-y-widget',
                        value='grossWorldWide',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select Y-axis variable"
                    ),
                    html.Iframe(id='scatter', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ]),
                dbc.Col([
                    html.H5("Line Plot"),
                    dcc.Dropdown(
                        id='line-x-widget',
                        value='Rating',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select X-axis variable"
                    ),
                    dcc.Dropdown(
                        id='line-y-widget',
                        value='grossWorldWide',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select Y-axis variable"
                    ),
                    html.Iframe(id='line_plot', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ]),
                dbc.Col([
                    html.H5("Histogram"),
                    dcc.Dropdown(
                        id='hist-x-widget',
                        value='Rating',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='hist_plot', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Bar Chart"),
                    dcc.Dropdown(
                        id='bar-x-widget',
                        value='grossWorldWide',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='bar_chart', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ]),
                dbc.Col([
                    html.H5("Box Plot"),
                    dcc.Dropdown(
                        id='box-x-widget',
                        value='Rating',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='box_plot', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ]),
                dbc.Col([
                    html.H5("Pie Chart"),
                    dcc.Dropdown(
                        id='pie-x-widget',
                        value='grossWorldWide',
                        options=[{'label': friendly_names.get(col, col), 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select metric"
                    ),
                    dcc.Dropdown(
                        id='aggregation-type',
                        options=[
                            {'label': 'Sum', 'value': 'sum'},
                            {'label': 'Average', 'value': 'average'},
                            {'label': 'Count', 'value': 'count'}
                        ],
                        value='average',
                        placeholder="Select Aggregation Type"
                    ),
                    html.Iframe(id='pie_chart', style={'border-width': '0', 'width': '100%', 'height': '225px'})
                ])
            ])
        ]),
        dcc.Tab(label='Statistics', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H5("Top 10 by Average Rating"),
                        html.Label("Select Genre"),
                        dcc.Dropdown(
                            id='genre-selector',
                            options=[{'label': genre, 'value': genre} for genre in sorted(df['genres'].unique())],
                            value=sorted(df['genres'].unique())[0],
                            placeholder="Select Genre"
                        ),
                        html.Br(),
                        html.Label("Select Person Type"),
                        dcc.Dropdown(
                            id='person-selector',
                            options=[
                                {'label': 'Writer', 'value': 'writer'},
                                {'label': 'Director', 'value': 'director'},
                                {'label': 'Star', 'value': 'star'},
                            ],
                            value='writer',
                            placeholder="Select Person Type"
                        ),
                        html.Br(),
                        html.Label("Minimum Number of Works"),
                        dcc.Input(id='min-works-input', type='number', value=5),
                        html.Br(), html.Br(),
                        html.Iframe(id='stats-bar-chart', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                    ], width=12)
                ], className="mb-4"),
                dbc.Row([
                    dbc.Col([
                        html.H5("DataFrame Preview"),
                        dash_table.DataTable(
                            id='df-table',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'),
                            page_size=10,
                            style_table={'overflowX': 'auto'}
                        )
                    ], width=12)
                ])
            ])
        ]),
        dcc.Tab(label='Predictions', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H5("Predict Movie Profitability"),
                        html.Label("Select Genre"),
                        dcc.Dropdown(
                            id='pred-genre',
                            options=[{'label': g, 'value': g} for g in sorted(df['genres'].unique())],
                            value=sorted(df['genres'].unique())[0]
                        ),
                        html.Br(),
                        html.Label("Enter Star"),
                        dcc.Input(id='pred-star', type='text', value=""),
                        html.Br(),
                        html.Label("Enter Director"),
                        dcc.Input(id='pred-director', type='text', value=""),
                        html.Br(),
                        html.Label("Enter Budget"),
                        dcc.Input(id='pred-budget', type='number', value=1000000),
                        html.Br(), html.Br(),
                        html.Button("Predict", id='predict-button', n_clicks=0),
                        html.Div(id='pred-output', style={'marginTop': '20px'})
                    ], width=12)
                ])
            ])
        ])
    ])
], fluid=True)

# ---------------------
# Callbacks for Existing Plots
# ---------------------
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('scatter-x-widget', 'value'),
    Input('scatter-y-widget', 'value'))
def plot_scatter(xcol, ycol):
    chart = alt.Chart(df).mark_circle().encode(
        x=xcol,
        y=ycol,
        tooltip=['Title', 'Rating'],
        color=alt.Color('genres:N', legend=alt.Legend(title="Genres"))
    ).properties(width=250, height=170).interactive()
    return chart.to_html()

@app.callback(
    Output('line_plot', 'srcDoc'),
    Input('line-x-widget', 'value'),
    Input('line-y-widget', 'value'))
def plot_line(xcol, ycol):
    chart = alt.Chart(df).mark_line().encode(
        x=xcol,
        y=ycol,
        color=alt.Color('genres:N', legend=alt.Legend(title="Genres"))
    ).properties(width=250, height=170).interactive()
    return chart.to_html()

@app.callback(
    Output('hist_plot', 'srcDoc'),
    Input('hist-x-widget', 'value'))
def plot_histogram(xcol):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(xcol, bin=alt.Bin(maxbins=30)),
        y='count()',
        tooltip=[
            alt.Tooltip(xcol, bin=alt.Bin(maxbins=30), title=xcol),
            alt.Tooltip('count()', title='Count'),
            alt.Tooltip('genres:N', title='Genre')
        ],
        color=alt.Color('genres:N', legend=alt.Legend(title="Genres"))
    ).properties(width=280, height=170).interactive()
    return chart.to_html()

@app.callback(
    Output('bar_chart', 'srcDoc'),
    Input('bar-x-widget', 'value'))
def plot_bar(xcol):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('genres', sort='-y'),
        y=alt.Y(f'mean({xcol})', title=f'Average {xcol}'),
        tooltip=['genres', f'mean({xcol})'],
        color=alt.Color('genres:N', legend=alt.Legend(title="Genres"))
    ).properties(width=250, height=100).interactive()
    return chart.to_html()

@app.callback(
    Output('box_plot', 'srcDoc'),
    Input('box-x-widget', 'value'))
def plot_box(xcol):
    chart = alt.Chart(df).mark_boxplot().encode(
        x='genres',
        y=xcol,
        color=alt.Color('genres:N', legend=alt.Legend(title="Genres"))
    ).properties(width=300, height=100).interactive()
    return chart.to_html()

@app.callback(
    Output('pie_chart', 'srcDoc'),
    Input('pie-x-widget', 'value'),
    Input('aggregation-type', 'value'))
def plot_pie(xcol, agg_type):
    if agg_type == 'sum':
        genre_gross = df.groupby('genres')[xcol].sum().reset_index()
    elif agg_type == 'average':
        genre_gross = df.groupby('genres')[xcol].mean().reset_index()
    elif agg_type == 'count':
        genre_gross = df.groupby('genres')[xcol].count().reset_index()
    else:
        genre_gross = df.groupby('genres')[xcol].sum().reset_index()
    
    chart = alt.Chart(genre_gross).mark_arc().encode(
        theta=alt.Theta(field=xcol, type='quantitative'),
        color=alt.Color(field='genres', type='nominal', legend=alt.Legend(title="Genres")),
        tooltip=['genres', xcol]
    ).properties(width=300, height=200).interactive()
    return chart.to_html()

@app.callback(
    Output('stats-bar-chart', 'srcDoc'),
    [Input('genre-selector', 'value'),
     Input('person-selector', 'value'),
     Input('min-works-input', 'value')]
)
def update_stats_chart(selected_genre, person_type, min_works):
    col_map = {'writer': 'writers', 'director': 'directors', 'star': 'stars'}
    col_name = col_map.get(person_type, 'writers')
    df_filtered = df[df['genres'] == selected_genre]
    records = []
    for _, row in df_filtered.iterrows():
        value = row[col_name]
        if pd.isnull(value):
            continue
        persons = [name.strip() for name in str(value).split(',')
                   if name.strip() and name.strip().lower() != 'nan']
        for person in persons:
            records.append({'person': person, 'Rating': row['Rating']})
    if not records:
        empty_df = pd.DataFrame(columns=['person', 'Rating'])
        chart = alt.Chart(empty_df).mark_bar().encode(
            x=alt.X('person:N'),
            y=alt.Y('Rating:Q')
        ).properties(width=350, height=450)
        return chart.to_html()
    df_person = pd.DataFrame(records)
    df_grouped = df_person.groupby('person', as_index=False).agg(
        mean_rating=('Rating', 'mean'),
        movie_count=('Rating', 'count')
    )
    df_grouped = df_grouped[df_grouped['movie_count'] >= min_works]
    df_grouped = df_grouped.sort_values('mean_rating', ascending=False).head(10)
    chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X('mean_rating:Q', title='Average Rating'),
        y=alt.Y('person:N', sort='-x', title=person_type.capitalize()),
        tooltip=[
            alt.Tooltip('mean_rating:Q', title='Average Rating'),
            alt.Tooltip('movie_count:Q', title='Movie Count')
        ]
    ).properties(width=350, height=450).interactive()
    return chart.to_html()

@app.callback(
    Output('pred-output', 'children'),
    Input('predict-button', 'n_clicks'),
    State('pred-genre', 'value'),
    State('pred-star', 'value'),
    State('pred-director', 'value'),
    State('pred-budget', 'value')
)
def update_prediction(n_clicks, genre, star, director, budget):
    if n_clicks > 0:
        if not star or not director:
            return "Please enter both a Star and a Director."
        try:
            predicted_category, predicted_ratio = predict_profitability(
                genre, star, director, budget, rf_class, rf_reg
            )
            return html.Div([
                html.P(f"Predicted Profitability Category: {predicted_category}"),
                html.P(f"Predicted Gross/Budget Ratio: {predicted_ratio:.2f}")
            ])
        except Exception as e:
            return f"Error in prediction: {str(e)}"
    return ""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host='0.0.0.0', port=port)
