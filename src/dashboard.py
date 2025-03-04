import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
import dash_table
import re
import ast

data_path = '../data/final_dataset.csv'
df = pd.read_csv(data_path)
df = df[['Title', 'Year', 'Duration', 'Rating', 'budget', 'grossWorldWide', 'gross_US_Canada', 'opening_weekend_Gross', 'directors', 'writers', 'stars', 'genres']]
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

# Convert lists in string format to comma-separated strings
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

# Apply genre categorization
df['genres'] = df['genres'].apply(lambda x: categorize_genres(str(x)))
# Disable VegaFusion to avoid import errors
alt.data_transformers.disable_max_rows()

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('IMDB Dashboard (Preview)', style={'textAlign': 'center'}),
    
    dbc.Row([
        dbc.Col([
            html.H5("Scatter Plot"),
            dcc.Dropdown(
                id='scatter-x-widget',
                value='budget',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns],
                placeholder="Select X-axis variable"
            ),
            dcc.Dropdown(
                id='scatter-y-widget',
                value='Rating',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns],
                placeholder="Select Y-axis variable"
            ),
            html.Iframe(id='scatter', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ]),
        dbc.Col([
            html.H5("Line Plot"),
            dcc.Dropdown(
                id='line-x-widget',
                value='Year',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns],
                placeholder="Select X-axis variable"
            ),
            dcc.Dropdown(
                id='line-y-widget',
                value='Rating',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns],
                placeholder="Select Y-axis variable"
            ),
            html.Iframe(id='line_plot', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ]),
        dbc.Col([
            html.H5("Histogram"),
            dcc.Dropdown(id='hist-x-widget', value='Rating', options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns]),
            html.Iframe(id='hist_plot', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H5("Bar Chart"),
            dcc.Dropdown(id='bar-x-widget', value='grossWorldWide', options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns]),
            html.Iframe(id='bar_chart', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ]),
        dbc.Col([
            html.H5("Box Plot"),
            dcc.Dropdown(id='box-x-widget', value='budget', options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns]),
            html.Iframe(id='box_plot', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ]),
        dbc.Col([
            html.H5("Pie Chart"),
            dcc.Dropdown(id='pie-x-widget', value='wins', options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['int64', 'float64']).columns]),
            html.Iframe(id='pie_chart', style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ])
    ])
])

# Callbacks
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('scatter-x-widget', 'value'),
    Input('scatter-y-widget', 'value'))
def plot_scatter(xcol, ycol):
    chart = alt.Chart(df).mark_circle().encode(
        x=xcol,
        y=ycol,
        tooltip=['Title', 'Rating']
    ).interactive()
    return chart.to_html()

@app.callback(
    Output('line_plot', 'srcDoc'),
    Input('line-x-widget', 'value'),
    Input('line-y-widget', 'value'))
def plot_line(xcol, ycol):
    chart = alt.Chart(df).mark_line().encode(
        x=xcol,
        y=ycol
    ).interactive()
    return chart.to_html()

@app.callback(
    Output('hist_plot', 'srcDoc'),
    Input('hist-x-widget', 'value'))
def plot_histogram(xcol):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(xcol, bin=True),
        y='count()'
    ).interactive()
    return chart.to_html()

@app.callback(
    Output('bar_chart', 'srcDoc'),
    Input('bar-x-widget', 'value'))
def plot_bar(xcol):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('genres', sort='-y'),  # Sort by Y value
        y=alt.Y(f'mean({xcol})', title=f'Average {xcol}'),
        tooltip=['genres', f'mean({xcol})']
    ).interactive()
    return chart.to_html()

@app.callback(
    Output('box_plot', 'srcDoc'),
    Input('box-x-widget', 'value'))
def plot_box(xcol):
    chart = alt.Chart(df).mark_boxplot().encode(
        x='genres',
        y=xcol
    ).interactive()
    return chart.to_html()


import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
import re
import ast

data_path = '../data/final_dataset.csv'
df = pd.read_csv(data_path)
df = df[['Title', 'Year', 'Duration', 'Rating', 'budget', 'grossWorldWide', 'gross_US_Canada', 'opening_weekend_Gross', 'directors', 'writers', 'stars', 'genres']]
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

# Convert lists in string format to comma-separated strings
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

# Apply genre categorization
df['genres'] = df['genres'].apply(lambda x: categorize_genres(str(x)))
# Disable VegaFusion to avoid import errors
alt.data_transformers.disable_max_rows()

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Plots', children=[
            dbc.Row([
                dbc.Col([
                    html.H5("Scatter Plot"),
                    dcc.Dropdown(
                        id='scatter-x-widget',
                        value='budget',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select X-axis variable"
                    ),
                    dcc.Dropdown(
                        id='scatter-y-widget',
                        value='Rating',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select Y-axis variable"
                    ),
                    html.Iframe(id='scatter', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ]),
                dbc.Col([
                    html.H5("Line Plot"),
                    dcc.Dropdown(
                        id='line-x-widget',
                        value='Year',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select X-axis variable"
                    ),
                    dcc.Dropdown(
                        id='line-y-widget',
                        value='Rating',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns],
                        placeholder="Select Y-axis variable"
                    ),
                    html.Iframe(id='line_plot', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ]),
                dbc.Col([
                    html.H5("Histogram"),
                    dcc.Dropdown(
                        id='hist-x-widget',
                        value='Rating',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='hist_plot', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Bar Chart"),
                    dcc.Dropdown(
                        id='bar-x-widget',
                        value='grossWorldWide',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='bar_chart', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ]),
                dbc.Col([
                    html.H5("Box Plot"),
                    dcc.Dropdown(
                        id='box-x-widget',
                        value='budget',
                        options=[{'label': col, 'value': col} 
                                 for col in df.select_dtypes(include=['int64', 'float64']).columns]
                    ),
                    html.Iframe(id='box_plot', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ]),
                dbc.Col([
                    html.H5("Pie Chart"),
                    dcc.Dropdown(
                        id='pie-x-widget',
                        value='wins',
                        options=[{'label': col, 'value': col} 
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
                        value='sum',
                        placeholder="Select Aggregation Type"
                    ),
                    html.Iframe(id='pie_chart', style={'border-width': '0', 'width': '100%', 'height': '450px'})
                ])
            ])
        ]),
        dcc.Tab(label='Statistics', children=[
            dbc.Container([
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
                ], className="mb-4"),
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
                ])
            ])
        ]),
        dcc.Tab(label='Predictions', children=[
            html.Div("Predictions content goes here")
        ])
    ])
], fluid=True)


# Callbacks
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('scatter-x-widget', 'value'),
    Input('scatter-y-widget', 'value'))
def plot_scatter(xcol, ycol):
    chart = (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x=xcol,
            y=ycol,
            color=alt.Color('genres', legend=alt.Legend(title="Movie Genres")),
            tooltip=['Title', 'Rating']
        )
        .properties(width=600, height=400)  # <--- Set chart dimensions
        .interactive()
    )
    return chart.to_html()

@app.callback(
    Output('line_plot', 'srcDoc'),
    Input('line-x-widget', 'value'),
    Input('line-y-widget', 'value'))
def plot_line(xcol, ycol):
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=xcol,
            y=ycol
        )
        .properties(width=600, height=400)
        .interactive()
    )
    return chart.to_html()

@app.callback(
    Output('hist_plot', 'srcDoc'),
    Input('hist-x-widget', 'value'))
def plot_histogram(xcol):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(xcol, bin=True),
            y='count()'
        )
        .properties(width=600, height=400)
        .interactive()
    )
    return chart.to_html()

@app.callback(
    Output('bar_chart', 'srcDoc'),
    Input('bar-x-widget', 'value'))
def plot_bar(xcol):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X('genres', sort='-y'),
            y=alt.Y(f'mean({xcol})', title=f'Average {xcol}'),
            tooltip=['genres', f'mean({xcol})']
        )
        .properties(width=600, height=350)
        .interactive()
    )
    return chart.to_html()

@app.callback(
    Output('box_plot', 'srcDoc'),
    Input('box-x-widget', 'value'))
def plot_box(xcol):
    chart = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x='genres',
            y=xcol
        )
        .properties(width=600, height=350)
        .interactive()
    )
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
    
    chart = (
        alt.Chart(genre_gross)
        .mark_arc()
        .encode(
            theta=alt.Theta(field=xcol, type='quantitative'),
            color=alt.Color(field='genres', type='nominal', legend=alt.Legend(title="Genres")),
            tooltip=['genres', xcol]
        )
        .properties(width=600, height=400)
        .interactive()
    )
    return chart.to_html()

@app.callback(
    Output('stats-bar-chart', 'srcDoc'),
    [Input('genre-selector', 'value'),
     Input('person-selector', 'value'),
     Input('min-works-input', 'value')]
)
def update_stats_chart(selected_genre, person_type, min_works):
    # Map singular to plural column name
    col_map = {'writer': 'writers', 'director': 'directors', 'star': 'stars'}
    col_name = col_map.get(person_type, 'writers')
    
    # Filter rows by selected genre
    df_filtered = df[df['genres'] == selected_genre]
    
    # Create a new DataFrame that explodes the person names
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
    # Group by person and calculate average rating and movie count
    df_grouped = df_person.groupby('person', as_index=False).agg(
        mean_rating=('Rating', 'mean'),
        movie_count=('Rating', 'count')
    )
    
    # Exclude people with fewer than min_works movies
    df_grouped = df_grouped[df_grouped['movie_count'] >= min_works]
    
    # Sort by average rating descending and take the top 10
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



if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
