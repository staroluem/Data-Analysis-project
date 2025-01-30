import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
ratings = pd.read_csv(r"C:\Users\anuja\OneDrive\Desktop\NexGen\ratings.dat", sep="::", engine="python", header=None, encoding="ISO-8859-1", names=["UserID", "MovieID", "Rating", "Timestamp"])
movies = pd.read_csv(r"C:\Users\anuja\OneDrive\Desktop\NexGen\movies.dat", sep="::", engine="python", header=None, encoding="ISO-8859-1", names=["MovieID", "Title", "Genres"])
users = pd.read_csv(r"C:\Users\anuja\OneDrive\Desktop\NexGen\users.dat", sep="::", engine="python", header=None, encoding="ISO-8859-1", names=["UserID", "Gender", "Age", "Occupation", "Zip-code"])

# Preprocess data
movies['Year'] = movies['Title'].str.extract(r'\((\d{4})\)', expand=False)
movies['Genres'] = movies['Genres'].str.split('|')
movies = movies.explode('Genres')

ratings = ratings.merge(movies, on='MovieID')
ratings = ratings.merge(users, on='UserID')

# Streamlit app
st.title("Movie Ratings Dashboard")

# Radio button for visualization selection
visualization = st.radio(
    "Select a visualization:",
    (
        "Distribution of Ratings by Genres and Years",
        "Popular Genres by User Demographics",
        "Heatmaps Showing Correlations",
    ),
)

if visualization == "Distribution of Ratings by Genres and Years":
    st.header("Distribution of Ratings by Genres and Years")
    
    genre_year = ratings.groupby(['Genres', 'Year'])['Rating'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=genre_year, x="Year", y="Rating", hue="Genres")
    plt.title("Average Rating by Genre Over the Years")
    plt.xticks(rotation=45)
    st.pyplot(plt)

elif visualization == "Popular Genres by User Demographics":
    st.header("Popular Genres by User Demographics")
    
    gender_genre = ratings.groupby(['Gender', 'Genres'])['Rating'].mean().unstack()
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(gender_genre, cmap="coolwarm", annot=True)
    plt.title("Average Rating by Gender and Genre")
    st.pyplot(plt)

elif visualization == "Heatmaps Showing Correlations":
    st.header("Heatmaps Showing Correlations")
    
    # Correlation matrix
    correlation_data = ratings[['Rating']].copy()
    correlation_data['Activity'] = ratings.groupby('UserID')['Rating'].transform('count')
    genre_dummies = pd.get_dummies(ratings['Genres'])
    correlation_data = pd.concat([correlation_data, genre_dummies], axis=1)
    correlation_matrix = correlation_data.corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, cmap="coolwarm", annot=False)
    plt.title("Correlation Heatmap")
    st.pyplot(plt)

st.markdown("---")
st.write("Developed using Streamlit")
