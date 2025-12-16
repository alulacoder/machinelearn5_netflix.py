import pandas as pd
import plotly.express as px

# Load the Netflix dataset
data = pd.read_csv("data science/netflix_titles.csv")

# Show the first 5 and last 5 rows
print("First 5 rows:")
print(data.head(5))
print("\nLast 5 rows:")
print(data.tail(5))

# Total number of movies and TV shows
type_counts = data['type'].value_counts()
print(f"\nTotal Movies: {type_counts.get('Movie', 0)}")
print(f"Total TV Shows: {type_counts.get('TV Show', 0)}")

# List all column names
print("\nColumn names:", data.columns.tolist())
# Check for missing values in each column
print("\nMissing values per column:\n", data.isnull().sum())

# Replace missing country values with “Unknown”
data['country'] = data['country'].fillna('Unknown')

# Remove rows with critical missing values in other columns
data.dropna(subset=['date_added', 'rating', 'duration'], inplace=True)

# Convert date_added column into datetime format
data['date_added'] = pd.to_datetime(data['date_added'].str.strip())

# Create a new column showing the year added
data['year_added'] = data['date_added'].dt.year

# Display summary statistics of numerical columns
print("\nSummary Statistics:\n", data.describe())
# How many unique countries are represented?
print("\nUnique countries:", data['country'].nunique())

# Movies added each year
movies_per_year = data[data['type'] == 'Movie']['year_added'].value_counts().sort_index()

# Shows added each year
shows_per_year = data[data['type'] == 'TV Show']['year_added'].value_counts().sort_index()

# Filter movies released in India (example)
india_movies = data[(data['type'] == 'Movie') & (data['country'].str.contains('India', na=False))]

# Filter movies released after 2015
recent_movies = data[(data['type'] == 'Movie') & (data['release_year'] > 2015)]

# Filter TV shows with more than 3 seasons
# Note: duration for TV shows is string (e.g., "4 Seasons")
tv_shows_3plus = data[(data['type'] == 'TV Show') & 
                      (data['duration'].str.extract('(\d+)').astype(int) > 3)]

# Filter movies of a specific genre (e.g., Action)
action_movies = data[(data['type'] == 'Movie') & (data['listed_in'].str.contains('Action', case=False))]
# Bar chart: Movies vs TV Shows
fig1 = px.bar(type_counts, title="Number of Movies vs TV Shows")
fig1.show()

# Line chart: Content added per year
content_by_year = data.groupby(['year_added', 'type']).size().reset_index(name='count')
fig2 = px.line(content_by_year, x='year_added', y='count', color='type', title="Content Added per Year")
fig2.show()

# Bar graph: Top 10 Countries
top_countries = data['country'].str.split(', ').explode().value_counts().head(10)
fig3 = px.bar(top_countries, title="Top 10 Countries Producing Content")
fig3.show()

# Histogram: Movie Release Years
fig4 = px.histogram(data[data['type'] == 'Movie'], x="release_year", title="Distribution of Movie Release Years")
fig4.show()

# Pie chart: Content Rating Distribution
fig5 = px.pie(data, names='rating', title='Content Rating Distribution')
fig5.show()

# Bar chart: Top 10 Genres
top_genres = data['listed_in'].str.split(', ').explode().value_counts().head(10)
fig6 = px.bar(top_genres, title="Top 10 Genres")
fig6.show()

# Boxplot: Movie Durations (minutes)
movie_durations = data[data['type'] == 'Movie'].copy()
movie_durations['duration_min'] = movie_durations['duration'].str.extract('(\d+)').astype(int)
fig7 = px.box(movie_durations, y="duration_min", title="Boxplot of Movie Durations")
fig7.show()
