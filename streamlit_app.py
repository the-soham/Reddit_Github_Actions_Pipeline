import streamlit as st
import pandas as pd 
import altair as alt
import plotly.express as px

#############
st.set_page_config(
    page_title="Trending FCs",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

df = pd.read_csv('Data\\reddit_fc_data.csv')
df['date'] = pd.to_datetime(df.date)

with st.sidebar:
    st.title('🏂 Trending FCs')
    min_date = df.date.min()
    max_date = df.date.max()

    teams = list(df.name.unique())

    range = st.date_input('Select date range', (min_date,max_date ),min_value= min_date, max_value= max_date)

    try:
        start_date, end_date = range
        print(type(range))
    except ValueError:
        st.error("You must pick a start and end date")
        st.stop()
       
        
    select_team = st.multiselect('Select your teams', teams, ['LiverpoolFC', 'ArsenalFC', 'ManchesterUnited'])

    if select_team == []:
        st.error("Teams not selected")
        st.stop()

    else:
        selected_team_df = df[(df['name'].isin(list(select_team)) == True) & (df['date'] >= pd.to_datetime(start_date)) & (df['date'] >= pd.to_datetime(end_date))]
    
    if selected_team_df.empty:
        st.error(f'{select_team} does not have data for the above date-range')
        st.stop()

    else:

        selected_team_df = selected_team_df.groupby('name').agg({
        #'title': 'count',                        # Total number of posts
        'author': 'nunique',                     # Number of distinct authors
        'upvotes_count': 'sum',                 # Sum of upvotes count
        #'upvote_ratio': 'mean',                 # Average upvote ratio
        'num_comments': 'sum'                  # Sum of comments
        }).reset_index()

        int_columns = selected_team_df.select_dtypes(include=['int64']).columns
        selected_team_df[int_columns] = selected_team_df[int_columns].astype(float).round(2)
        #selected_team_df['upvote_ratio'] = selected_team_df['upvote_ratio'].round(2)
        print(selected_team_df.dtypes)
        selected_team_df.columns = ['name', 'distinct_authors', 'sum_upvotes', 'sum_comments']

#### main panel
col = st.columns((0.3,0.7), gap='medium')

with col[0]:

    try:
        st.dataframe(
            selected_team_df,
            hide_index=True,
            width=None,
            column_config= {
                "name": st.column_config.TextColumn("Club Name", ),
                "distinct_authors": st.column_config.ProgressColumn(
                    "Authors",
                    format = "%f",
                    max_value = selected_team_df.distinct_authors.max(),
                ),
                "sum_upvotes": st.column_config.ProgressColumn(
                    "Upvotes",
                    format = "%f",
                    min_value = 0,
                    max_value = selected_team_df.sum_upvotes.max(),
                )
            }

        )

    except ValueError:
        st.stop


