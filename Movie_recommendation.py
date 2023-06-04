import pandas as pd
import spacy

# Load the nlp model.
nlp = spacy.load('en_core_web_md')

# Data used is taken from the imdb dataset on Kaggle.
data = pd.read_csv('imdb_movies.csv')

# The relevant columns for this program are the titles, the genre, and the description. These are passed to the variable df.
df = data[['names', 'genre', 'overview']]

# In order to narrow down the potential results, the similar genres will need to be collected. This variable is intialised as an empty list but it will later be passed a dataframe of
# matching genres as entries once the genre_filter function is called. 
matching_genre_df = []





# This function will first be called to find out which titles have similar genres. It takes one parameter, which is the genre of the title.
def genre_filter(genre):

    # The matching_genre_df is set as a global here because the second search function will need to have access to it.
    global matching_genre_df

    # The list of dictionary keys grouped by genre
    all_genres = df.groupby('genre').indices.keys()
    
    # List declared to save the genre entries that match the given genre. For example, if the user given genre is action, but a title has genres of action and war, the genre 'action, war' will
    # be added to the list here.
    matching_genres = []
    
    # Loop will work through the collection of all the genres saved in all_genres
    for entry in all_genres:
        
        # Condtion to check if user passed genre is in the entry of the all_genres list. If so it can be added to matching_genres list. 
        if entry.find(genre) != -1:
            matching_genres.append(entry)

    # A new dataframe is passed to matching_genre_df. The entries from the df dataframe that have genres identified in the matching_genres list act as the filter. All the titles that
    # have matching genres will be added to the new dataframe in matching_genre_df. 
    matching_genre_df = pd.DataFrame(df.loc[df['genre'].isin(matching_genres)])
    return matching_genre_df
        
        

# This function will provide the recommended similarity titles. It takes two parameters, one is description, and it will return the names of titles which have the highest NLP similarity.
# The second is recommendation_size, which will provide the user with the desired number of recommendations. 
def recommend(description, recommendation_size):
    
    # An empty dictionary is declared, it will later be filled with values for the title, description and similarity of the movie.
    similarity_dict = {}
    
    
    # Loop to compare the descriptions of the titles with similar genres in matching_genre_df to the description passed in to the function. 
    for entry in matching_genre_df['overview']:

        # This will current provide the row number of the description taken from the matching_genre_df. This will be used to access the name at the same row number when passed into similarity_dict below.
        row_num = matching_genre_df[matching_genre_df['overview'] == entry].index[0]
        
        # The description from the matching_genre_df and the description passed in by the user need to be loaded with the nlp model in order to compare similarity. This is done here in these variables here.
        nlp_entry = nlp(entry)
        nlp_description = nlp(description)

        # This rating variable stores the similarity rating of the description to the entry from the matching_genre_df
        rating = nlp_entry.similarity(nlp_description)

        # This conditional will check that the similarity is not 1.0 - if the similarity is this high, we need to skip this entry as it will end up recommended the same title back to the
        # user that they passed in. Otherwise, the similarity_dict will be updated to contain the title, description, and the similarity rating. 
        if rating == 1.0:
            continue
        else:
            similarity_dict[str(row_num)] = [matching_genre_df['names'][row_num], entry, rating]
        
       
    # The similarity_dict will be converted to a dataframe and stored in the ratings_df variable. This allows us to then sort the dataframe by highest similarity ratings. 
    ratings_df = pd.DataFrame.from_dict(similarity_dict, orient='index', columns=['title', 'description', 'similarity'])
    
    # The top_ratings variable contains the sorted version of ratings_df with the highest similarity entries at the top. 
    top_ratings = ratings_df.sort_values(by = 'similarity', ascending=False)
    
    # This loop will work through the results in top_ratings and provide the title of the movies with the most similar ratings. The number of returned recommendations depends on how many 
    # were given by the user when the function was called. 
    for entry in top_ratings.iloc[:(recommendation_size - 1), 0]:
        print(entry)




genre_filter('Fantasy')

recommend('A film with wholesome family feelings. Johnny goes on an adventure to save his sister and break the curse on his entire family', 20)
