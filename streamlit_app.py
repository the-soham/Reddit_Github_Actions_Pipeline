import streamlit as st
import pandas as pd 
import altair as alt
import plotly.express as px




#############Sidebar
st.set_page_config(
    page_title="Trending FCs",
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="expanded")

st.title(':soccer: English Premier League: How are fans interacting on Reddit :soccer: ')
st.markdown('#')


#read the data
df = pd.read_csv('https://raw.githubusercontent.com/the-soham/Reddit_Github_Actions_Pipeline/main/Data/reddit_fc_data.csv', on_bad_lines = 'skip')
df['date'] = pd.to_datetime(df.date, format='mixed')


##sidebar
with st.sidebar:
    st.title(':soccer: Trending FCs')
    min_date = df.date.min()
    max_date = df.date.max()

    teams = list(df.name.unique())

    range = st.date_input('Select date range', (datetime.date(2024, 1, 1),max_date ),min_value= min_date, max_value= max_date)


    try:
        start_date, end_date = range
        
    except ValueError:
        st.error("You must pick a start and end date")
        st.stop()
       
        
    select_team = st.multiselect('Select your teams', teams, ['LiverpoolFC', 'ArsenalFC', 'coys'])

    st.markdown('#')
    st.markdown('#')
    st.markdown('#')

  
    with st.expander('About', expanded=True):
            st.write('''
                - Data: [Reddit](https://www.reddit.com).
                - :orange[**Usage**]: Select the date range and the soccer/football club of your interest.
                - :orange[**Number of Posts plot**]: Number of posts on the chosen team's subreddit. Don't forget to check out the chatter on the match days.
                - :orange[**Average upvotes ratio plot**]: Average upvote ratio on the chosen team's subreddit.
                - :red[**Open to Work**]: If you like this project and if you are hiring or you know someone who's hiring, please get in touch with me @ [sohambhagwat2@gmail.com](sohambhagwat2@gmail.com)
                ''')
    
            




    if select_team == []:
        st.error("Teams not selected")
        st.stop()

    else:
        selected_team_df = df[(df['name'].isin(list(select_team)) == True) & (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        
        plt_df = selected_team_df.copy()
    if selected_team_df.empty:
        st.error(f'{select_team} does not have data for the above date-range')
        st.stop()



       

    else:

        selected_team_df = selected_team_df.groupby('name').agg({
        'author': 'nunique',                     # Number of distinct authors
        'upvotes_count': 'sum',                 # Sum of upvotes count
        'num_comments': 'sum'                  # Sum of comments
        }).reset_index()

        int_columns = selected_team_df.select_dtypes(include=['int64']).columns
        selected_team_df[int_columns] = selected_team_df[int_columns].astype(float).round(2)
        selected_team_df.columns = ['name', 'distinct_authors', 'sum_upvotes', 'sum_comments']


        

#Plot functions
#plot 1 line polts about post count
def make_posts_plot(_df):
    grouped_df = _df.groupby(['name', 'date']).size().reset_index(name='count_of_posts')
    
# Create a line chart using Plotly
    fig = px.line(grouped_df, x='date', y='count_of_posts', color='name', title='Number of Posts Over Time')

    # Customize layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Posts',
        legend_title='Club',
        yaxis=dict(
            range=[-5, grouped_df['count_of_posts'].max() + 5]  # Set y-axis range from -5 to max value + 5
        )
    )

    return fig

def make_upvote_ratio_plot(_df):
    grouped_df = _df.groupby(['name','date'])['upvote_ratio'].mean().reset_index(name='mean_upvote_ratio').round(2)
   
    # Create a line chart using Plotly
    fig = px.line(grouped_df, x='date', y='mean_upvote_ratio', color='name', title='Upvotes ratio Over Time')

    # Customize layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Avg Upvote ratio',
        legend_title='Club',
        yaxis=dict(
            range=[-0.1, grouped_df['mean_upvote_ratio'].max() + 0.1]  # Set y-axis range from -5 to max value + 5
        )
    )

    return fig



#### main panel
col = st.columns((0.4,0.6), gap='small')

with col[0]:

    st.markdown('##### Soccer Clubs\' Activity on Reddit')
    st.markdown('#')
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
            ),
            "sum_comments": st.column_config.ProgressColumn(
                "Comments",
                format="%f",
                min_value=0,
                max_value = selected_team_df.sum_comments.max(),
            )

        }

    )

    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    
    

    



with col[1]:
    st.markdown('##### Fans\' Activity on Reddit')
    line_plt = make_posts_plot(plt_df)
    st.plotly_chart(line_plt, use_container_width=True)

    posts_plot = make_upvote_ratio_plot(plt_df)
    st.plotly_chart(posts_plot, use_container_width=True)
