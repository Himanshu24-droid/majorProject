import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Step 1: Load the dataset
dataset = pd.read_csv('Bollywood_Songs.csv')

# Step 2: Preprocess the data (if required)
# Handle missing values, perform data normalization, or any other preprocessing steps here.

# Step 3: Choose a recommendation approach (Content-based filtering)
# We will use song attributes for similarity calculations.

# Step 4: Implement the recommendation system

# Create a TF-IDF vectorizer to convert song attributes into numeric representations
tfidf_vectorizer = TfidfVectorizer()

# Combine the relevant columns into a single 'song_attributes' column
dataset['song_attributes'] = dataset[
    ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
     'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
     'time_signature']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

# Apply TF-IDF vectorization on the song attributes
tfidf_matrix = tfidf_vectorizer.fit_transform(dataset['song_attributes'].fillna(''))

# Calculate cosine similarity between songs based on TF-IDF vectors
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

def autocomplete_suggestions(user_input, suggestion_list):
    pattern = re.compile(f".{user_input}.", re.IGNORECASE)
    suggestions = [suggestion for suggestion in suggestion_list if re.match(pattern, suggestion)]
    return suggestions

def recommend_songs_by_similarity(song_name, top_n=5):
    # Find the index of the input song in the dataset
    song_indices = dataset[dataset['song_name'] == song_name].index
    if len(song_indices) == 0:
        print("Song not found in the dataset.")
        return []

    index = song_indices[0]

    # Get the cosine similarity scores of the input song with all other songs
    similarity_scores = list(enumerate(cosine_similarities[index]))

    # Sort the songs based on similarity scores
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top N similar songs (excluding the input song itself)
    top_songs = [dict(dataset.iloc[song[0]]) for song in similarity_scores[1:top_n + 1]]

    return top_songs

def recommend_songs_by_artist(artist_name, top_n=5):
    # Find songs by the input artist (case-insensitive)
    songs_by_artist = dataset[dataset['artist_name'].str.lower() == artist_name.lower()]

    # Get the top N songs by the artist
    top_songs = songs_by_artist.head(top_n).copy().to_dict('records')

    return top_songs

# Step 5: Display recommendations

# Ask the user whether they want to provide a song or artist as input
#input_choice = input("Enter 'song' to provide a song name or 'artist' to provide an artist name: ")

# if input_choice.lower() == 'song':
#     # Ask the user for a song name
#     user_input = input("Enter a song name: ")

#     # Autocomplete song name suggestions
#     suggestions = autocomplete_suggestions(user_input, dataset['song_name'])

#     if len(suggestions) > 0:
#         print("Autocomplete Suggestions:")
#         for suggestion in suggestions:
#             print(suggestion)
#         print()

#         # Get recommendations based on similar songs
#         similar_songs = recommend_songs_by_similarity(user_input, top_n=5)

#         if len(similar_songs) > 0:
#             # Display the recommended songs based on similarity
#             print("Recommended Songs based on Similarity:")
#             for song in similar_songs:
#                 print(f"Song Name: {song['song_name']}")
#                 print(f"Artist Name: {song['artist_name']}")
#                 print(f"Album Name: {song['album_name']}")
#                 print(f"Song URL: {song['song_url']}")
#                 print("-----------")
#         else:
#             print("No recommendations found for the given song.")

#     else:
#         print("No song suggestions found for the given input.")

# elif input_choice.lower() == 'artist':
#     # Ask the user for an artist name
#     user_input = input("Enter an artist name: ")

#     # Autocomplete artist name suggestions
#     suggestions = autocomplete_suggestions(user_input, dataset['artist_name'])

#     if len(suggestions) > 0:
#         print("Autocomplete Suggestions:")
#         for suggestion in suggestions:
#             print(suggestion)
#         print()

#         # Get recommendations based on the artist
#         artist_songs = recommend_songs_by_artist(suggestions[0], top_n=5)

#         if len(artist_songs) > 0:
#             # Display the recommended songs by the artist
#             print(f"Recommended Songs by {suggestions[0]}:")
#             for song in artist_songs:
#                 print(f"Song Name: {song['song_name']}")
#                 print(f"Artist Name: {song['artist_name']}")
#                 print(f"Album Name: {song['album_name']}")
#                 print(f"Song URL: {song['song_url']}")
#                 print("-----------")
#         else:
#             print("No recommendations found for the given artist.")

#     else:
#         print("No artist suggestions found for the given input.")

# else:
#     print("Invalid input. Please choose 'song' or 'artist' as input.")