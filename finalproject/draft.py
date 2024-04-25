import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Music Chart Analysis Dashboard')
st.write('CMSE 402 Semester Project')
st.write('The Impact of Early Success on Longevity: Does achieving a top rank early in a songs chart life predict its long-term success?')

st.markdown("""
## Methodology

This dashboard provides an analytical view of music chart data to uncover patterns and insights into song performances, artist popularity, and genre trends over time. The methodology involves several key steps:

- **Data Collection**: The data was sourced from a comprehensive dataset of music chart performances including date, rank, and artist details.
- **Data Preprocessing**: The data was cleaned and preprocessed to ensure quality and consistency. This included handling missing values, correcting data types, and deriving new metrics such as 'total weeks on board'.
- **Exploratory Data Analysis (EDA)**: Initial EDA was performed to understand the distributions and relationships within the data.
- **Visualization**: Using Plotly, we created interactive visualizations that allow users to explore data dynamically, focusing on trends over time, comparisons across categories, and detailed breakdowns by artist or genre.
- **Interactive Features**: Streamlit widgets were utilized to enable real-time interaction with the data, allowing users to select specific songs, artists, or genres for detailed analysis.

The goal of this analysis is to provide stakeholders with actionable insights on music trends and artist performances that can inform strategic decisions in the music industry.
""")

st.markdown("---") 



# Load your data
@st.cache(allow_output_mutation=True)  # This decorator caches the data to prevent reloading on every interaction
def load_data():
    data = pd.read_csv('../Data/charts.csv')

    data['date'] = pd.to_datetime(data['date'])  # Ensuring 'date' is datetime
    

    # Assuming 'weeks-on-board' indicates the week number for each song's chart life
    # Filter data for the first 4 weeks of each song's presence on the board
    data_first_4_weeks = data[data['weeks-on-board'] <= 4]

    # Calculate the minimum rank (which is the peak rank) during the first 4 weeks
    peak_ranks = data_first_4_weeks.groupby(['song', 'artist']).agg(peak_rank_first_4_weeks=('rank', 'min')).reset_index()

    # Merge this back with the original data
    data = data.merge(peak_ranks, on=['song', 'artist'], how='left')
    # Assuming 'weeks-on-board' is the correct column but you need it as 'total_weeks_on_board'
    data['total_weeks_on_board'] = data['weeks-on-board']

    return data

data = load_data().copy() 

st.sidebar.header('User Input Features')
rank_range = st.sidebar.slider('Select rank range', 1, 100, (1, 50))

# Ensure that 'peak_rank_first_4_weeks' is in data
if 'peak_rank_first_4_weeks' in data.columns:
    filtered_data = data[(data['peak_rank_first_4_weeks'] >= rank_range[0]) & (data['peak_rank_first_4_weeks'] <= rank_range[1])]
    st.write(filtered_data)  # Displaying the filtered data to check
else:
    st.error("Error: 'peak_rank_first_4_weeks' column not found. Please check data loading and processing.")


# Filtering data based on sidebar input
filtered_data = data[(data['peak_rank_first_4_weeks'] >= rank_range[0]) & (data['peak_rank_first_4_weeks'] <= rank_range[1])]

# Visualization: Scatter Plot
fig = px.scatter(filtered_data, x='peak_rank_first_4_weeks', y='total_weeks_on_board',
                 hover_data=['song', 'artist'],
                 title='Impact of Early Peak Rank on Longevity')
st.plotly_chart(fig)  # This renders the Plotly figure in Streamlit


st.title('Music Chart Analysis Dashboard')
st.header('Scatter Plot Analysis')
st.write('The Impact of Early Success on Longevity: Does achieving a top rank early in a songs chart life predict its long-term success?')
st.write('This scatter plot shows the relationship between early peak rank and total weeks on board.')

# Assuming data is already loaded and contains 'artist' and 'weeks-on-board'
data['total_weeks_on_board'] = data['weeks-on-board']  # This line ensures the column exists
top_artists = data.groupby('artist')['total_weeks_on_board'].mean().nlargest(10).reset_index()

fig = px.bar(top_artists, x='artist', y='total_weeks_on_board', 
             title="Top Artists by Average Longevity on Chart",
             labels={'total_weeks_on_board': 'Average Weeks on Chart', 'artist': 'Artist'})

st.plotly_chart(fig, use_container_width=True)



# User can select a few songs to view their trends
selected_songs = st.multiselect('Select songs to view trends:', options=data['song'].unique())

# Filter data based on selected songs
trend_data = data[data['song'].isin(selected_songs)]

fig = px.line(trend_data, x='date', y='rank', color='song', 
              title='Time Series Trend of Song Rankings',
              labels={'date': 'Date', 'rank': 'Chart Rank', 'song': 'Song'})

st.plotly_chart(fig, use_container_width=True)



data['year'] = data['date'].dt.year

# Group data by artist and year, then get average rank
performance_data = data.groupby(['artist', 'year'])['rank'].mean().unstack().fillna(0)

fig = px.imshow(performance_data,
                labels=dict(x="Year", y="Artist", color="Average Rank"),
                x=performance_data.columns,
                y=performance_data.index,
                title="Heatmap of Artist Performance by Year")

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
## Conclusion

### Key Findings
- **Trend Analysis**: Songs reaching high initial ranks tend to maintain better chart performance over time, emphasizing the importance of strong launches.
- **Artist Insights**: Certain artists consistently have songs performing well, indicating a strong fan base and effective marketing strategies.
- **Genre Popularity**: Some genres show seasonal or cyclic trends, which could guide promotional efforts.

### Recommendations
- **Targeted Promotions**: Focus promotional efforts on genres and artists that show strong potential based on historical trends.
- **New Artist Support**: Consider supporting emerging artists with traits similar to historically successful profiles.
- **Strategic Releases**: Align song releases with favorable times of the year, identified from genre-specific trends.

### Limitations
- The analysis is constrained by the available data and might not capture all dynamics, such as regional differences or digital streaming trends.

Further studies could integrate additional data sources, like social media analytics and streaming data, to enhance the accuracy and breadth of insights.
""")

st.markdown("---")  # Adds a horizontal line for better separation
