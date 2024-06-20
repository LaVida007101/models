import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from db_operations import get_user_data, get_event_data, get_day_of_week, calculate_date_difference, initialize_db_connection
from db_operations import get_event_data, add_recommended

initialize_db_connection()

# Sample data 
users = get_user_data()
# users = {
#     1234567: {
#         "Celebration": [127, 3, 1],
#         "Software Engineering": [92, 2, 5],
#         "Information Technology": [0, 0, 0],
#         "Data Science": [53, 2, 1],
#         "Computer Science": [0, 0, 0],
#         "Conference": [23, 2, 0],
#         "Reviews and Study Session": [53, 6, 2],
#         "Professional Development": [0, 0, 0],
#         "Online Event": [33, 3, 0],
#         "Competitions": [67, 4, 0],
#         "Guest Speakers": [34, 12, 1],
#         "Hackathon": [50, 3, 1],
#         "Workshops and Training": [0, 0, 0],
#         "Tech Fair": [0, 0, 0],
#         "Gaming": [34, 1, 1],
#         "Creativity and Artistry": [110, 5, 1],
#         "Performing Arts and Talents": [0, 0, 0],
#         "Academic": [44, 3, 0],
#         "Non-Academic": [0, 0, 0],
#         "Computer Engineering": [0, 0, 0],
#         "ACM": [0, 0, 0],
#         "AITS": [0, 0, 0],
#         "JPCS": [0, 0, 0],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [0, 0, 0],
#         "Leadership": [0, 0, 0],
#         "Spiritual": [15, 5, 0],
#         "days": [1, 2, 0, 0, 4, 1, 0]
#     },
#     7654321: {
#         "Celebration": [0, 0, 0],
#         "Software Engineering": [34, 1, 1],
#         "Information Technology": [44, 3, 0],
#         "Data Science": [0, 0, 0],
#         "Computer Science": [33, 3, 0],
#         "Conference": [0, 0, 0],
#         "Reviews and Study Session": [0, 0, 0],
#         "Professional Development": [50, 3, 1],
#         "Online Event": [0, 0, 0],
#         "Competitions": [127, 3, 1],
#         "Guest Speakers": [53, 2, 1],
#         "Hackathon": [92, 2, 1],
#         "Workshops and Training": [0, 0, 0],
#         "Tech Fair": [67, 4, 0],
#         "Gaming": [0, 0, 0],
#         "Creativity and Artistry": [0, 0, 0],
#         "Performing Arts and Talents": [0, 0, 0],
#         "Academic": [23, 2, 0],
#         "Non-Academic": [0, 0, 0],
#         "Computer Engineering": [34, 12, 1],
#         "ACM": [0, 0, 0],
#         "AITS": [15, 5, 0],
#         "JPCS": [53, 6, 1],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [110, 5, 1],
#         "Leadership": [0, 0, 0],
#         "Spiritual": [0, 0, 0],
#         "days": [0, 3, 1, 4, 2, 0, 0]
#     },
#     1122334: {
#         "Celebration": [90, 2, 1],
#         "Software Engineering": [80, 4, 3],
#         "Information Technology": [40, 1, 0],
#         "Data Science": [20, 1, 0],
#         "Computer Science": [50, 3, 2],
#         "Conference": [30, 1, 1],
#         "Reviews and Study Session": [10, 1, 0],
#         "Professional Development": [20, 1, 0],
#         "Online Event": [15, 2, 0],
#         "Competitions": [60, 3, 0],
#         "Guest Speakers": [40, 2, 1],
#         "Hackathon": [70, 4, 2],
#         "Workshops and Training": [10, 1, 0],
#         "Tech Fair": [5, 1, 0],
#         "Gaming": [25, 1, 0],
#         "Creativity and Artistry": [30, 1, 1],
#         "Performing Arts and Talents": [15, 2, 0],
#         "Academic": [50, 2, 1],
#         "Non-Academic": [10, 1, 0],
#         "Computer Engineering": [20, 1, 0],
#         "ACM": [10, 1, 0],
#         "AITS": [5, 1, 0],
#         "JPCS": [20, 2, 1],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [25, 1, 0],
#         "Leadership": [10, 1, 0],
#         "Spiritual": [5, 1, 0],
#         "days": [2, 0, 1, 3, 4, 1, 0]
#     },
#     5566778: {
#         "Celebration": [50, 1, 0],
#         "Software Engineering": [45, 2, 1],
#         "Information Technology": [60, 2, 1],
#         "Data Science": [30, 1, 0],
#         "Computer Science": [25, 1, 0],
#         "Conference": [15, 1, 0],
#         "Reviews and Study Session": [20, 1, 1],
#         "Professional Development": [35, 2, 1],
#         "Online Event": [40, 2, 0],
#         "Competitions": [50, 2, 1],
#         "Guest Speakers": [60, 2, 1],
#         "Hackathon": [55, 3, 1],
#         "Workshops and Training": [10, 1, 0],
#         "Tech Fair": [20, 1, 0],
#         "Gaming": [35, 1, 1],
#         "Creativity and Artistry": [40, 1, 1],
#         "Performing Arts and Talents": [25, 1, 0],
#         "Academic": [60, 2, 1],
#         "Non-Academic": [10, 1, 0],
#         "Computer Engineering": [30, 1, 1],
#         "ACM": [5, 1, 0],
#         "AITS": [10, 1, 0],
#         "JPCS": [15, 1, 0],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [40, 1, 0],
#         "Leadership": [20, 1, 0],
#         "Spiritual": [10, 1, 0],
#         "days": [0, 1, 2, 1, 3, 4, 0]
#     },
#     9988776: {
#         "Celebration": [130, 4, 2],
#         "Software Engineering": [100, 3, 2],
#         "Information Technology": [50, 2, 1],
#         "Data Science": [40, 2, 1],
#         "Computer Science": [70, 3, 1],
#         "Conference": [20, 1, 0],
#         "Reviews and Study Session": [15, 1, 0],
#         "Professional Development": [30, 2, 1],
#         "Online Event": [35, 2, 0],
#         "Competitions": [90, 3, 2],
#         "Guest Speakers": [55, 3, 1],
#         "Hackathon": [80, 4, 2],
#         "Workshops and Training": [25, 1, 0],
#         "Tech Fair": [15, 1, 0],
#         "Gaming": [50, 2, 1],
#         "Creativity and Artistry": [60, 2, 1],
#         "Performing Arts and Talents": [35, 2, 0],
#         "Academic": [70, 3, 2],
#         "Non-Academic": [20, 1, 0],
#         "Computer Engineering": [40, 2, 1],
#         "ACM": [15, 1, 0],
#         "AITS": [20, 2, 0],
#         "JPCS": [30, 2, 1],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [50, 2, 1],
#         "Leadership": [25, 1, 0],
#         "Spiritual": [10, 1, 0],
#         "days": [6, 2, 0, 3, 1, 1, 4]
#     },
#     5544332: {
#         "Celebration": [75, 2, 1],
#         "Software Engineering": [85, 3, 1],
#         "Information Technology": [70, 2, 1],
#         "Data Science": [20, 1, 0],
#         "Computer Science": [60, 2, 1],
#         "Conference": [30, 1, 0],
#         "Reviews and Study Session": [40, 2, 1],
#         "Professional Development": [55, 3, 1],
#         "Online Event": [45, 2, 1],
#         "Competitions": [95, 3, 1],
#         "Guest Speakers": [70, 3, 2],
#         "Hackathon": [90, 4, 2],
#         "Workshops and Training": [35, 1, 1],
#         "Tech Fair": [20, 1, 0],
#         "Gaming": [65, 2, 1],
#         "Creativity and Artistry": [75, 2, 1],
#         "Performing Arts and Talents": [50, 2, 1],
#         "Academic": [80, 3, 2],
#         "Non-Academic": [25, 1, 0],
#         "Computer Engineering": [45, 2, 1],
#         "ACM": [20, 1, 1],
#         "AITS": [25, 2, 1],
#         "JPCS": [40, 2, 1],
#         "Artist Connection": [0, 0, 0],
#         "iTamaraw Esports Club": [55, 2, 1],
#         "Leadership": [30, 1, 0],
#         "Spiritual": [15, 1, 0],
#         "days": [7, 4, 0, 5, 0, 0, 6]
#     }
# }

# Step 1: Data Preparation
data = []
for user in users:
    for user_id, categories in user.items():
        days = categories.pop("days")
        for category, values in categories.items():
            data.append([user_id, category] + values + days)

df = pd.DataFrame(data, columns=["user_id", "category", "total_time", "taps", "bookmarks"] + ["day_" + str(i) for i in range(7)])

# Step 2: Feature Vector Construction
# Normalize the features to bring them to a common scale
scaler = MinMaxScaler()
df[["total_time", "taps", "bookmarks"]] = scaler.fit_transform(df[["total_time", "taps", "bookmarks"]])

# Calculate preference as a weighted sum of normalized features
df["preference"] = df["total_time"] * 0.45 + df["taps"] * 0.25 + df["bookmarks"] * 0.3

# Create a user preference vector
user_preference = df.pivot(index="user_id", columns="category", values="preference").fillna(0)

# Dummy event data with days
# events = {
#     "event_1": ["Celebration", "Guest Speakers", [0, 0, 0, 0, 1, 0, 0]],
#     "event_2": ["Software Engineering", "Hackathon", [0, 1, 1, 0, 0, 0, 0]],
#     "event_3": ["Information Technology", "Competitions", [0, 0, 0, 1, 1, 0, 0]],
#     "event_4": ["Data Science", "Workshops and Training", [1, 1, 0, 0, 0, 0, 0]],
#     "event_5": ["Conference", "Professional Development", [0, 0, 1, 1, 0, 0, 0]],
#     "event_6": ["Online Event", "Tech Fair", [0, 0, 0, 0, 1, 1, 0]],
#     "event_7": ["Gaming", "Competitions", [0, 0, 1, 0, 0, 0, 0]],
#     "event_8": ["Creativity and Artistry", "Workshops and Training", [1, 0, 0, 0, 0, 0, 0]],
#     "event_9": ["Performing Arts and Talents", "Celebration", [0, 1, 0, 0, 0, 0, 0]],
#     "event_10": ["Computer Engineering", "Hackathon", [0, 0, 0, 1, 0, 0, 0]],
#     "event_11": ["Spiritual", "Guest Speakers", [0, 0, 0, 0, 1, 0, 0]],
#     "event_12": ["Reviews and Study Session", "Professional Development", [0, 1, 1, 0, 0, 0, 0]],
#     "event_13": ["Celebration", "Online Event", [0, 0, 0, 1, 0, 0, 0]],
#     "event_14": ["Data Science", "Conference", [0, 0, 0, 0, 0, 1, 0]],
#     "event_15": ["Computer Science", "Competitions", [0, 1, 0, 0, 0, 0, 0]],
#     "event_16": ["Tech Fair", "Workshops and Training", [0, 0, 1, 0, 0, 0, 0]],
#     "event_17": ["Gaming", "Creativity and Artistry", [0, 0, 0, 1, 0, 0, 0]],
#     "event_18": ["Information Technology", "Conference", [0, 0, 0, 0, 0, 0, 1]],
#     "event_19": ["Spiritual", "Celebration", [0, 1, 0, 0, 0, 0, 0]],
#     "event_20": ["Computer Engineering", "Tech Fair", [1, 0, 0, 0, 0, 0, 0]]
# }
events = get_event_data()

# Create an event feature matrix
event_features = {}
for event, details in events.items():
    categories, days = details[:-1], details[-1]
    feature_vector = [1 if category in categories else 0 for category in user_preference.columns]
    feature_vector.extend(days)
    event_features[event] = feature_vector

# Convert to DataFrame
event_feature_columns = list(user_preference.columns) + ["day_" + str(i) for i in range(7)]
event_features_df = pd.DataFrame(event_features).T
event_features_df.columns = event_feature_columns

# Step 3: Cosine Similarity and KNN
def recommend_events(user_id, min_similarity=0.3):
    user_vector = np.concatenate((user_preference.loc[user_id].values, [0]*7)).reshape(1, -1)
    
    # Compute cosine similarity between the user vector and event feature matrix
    cosine_similarities = cosine_similarity(user_vector, event_features_df)
    
    # Combine the cosine similarity with the event data
    combined_scores = cosine_similarities.flatten()
    
    # Filter events based on minimum similarity threshold
    valid_indices = combined_scores >= min_similarity
    
    if valid_indices.sum() == 0:
        print("No events meet the minimum similarity threshold.")
        return []
    
    # Dynamically adjust 'k' based on the number of valid events
    k = valid_indices.sum()  # Adjust 'k' to include all valid events
    
    # Use KNN to find the nearest neighbors based on combined scores
    knn = NearestNeighbors(n_neighbors=k, metric='cosine')
    knn.fit(event_features_df)
    distances, indices = knn.kneighbors(user_vector)
    
    # Get the event recommendations
    event_recommendations = [(event_features_df.index[i], combined_scores[i]) for i in indices.flatten() if combined_scores[i] >= min_similarity]
    
    return event_recommendations

# Example usage
users = get_user_data()
for user in users:
    for id, category in user.items():
        recommendations = recommend_events(id)
        print(f"Recommended events and their similarity scores for {id}:")
        for event, score in recommendations:
            # print(f"Event: {event}, Score: {score}")
            add_recommended(id, str(event))

        # print("\n\n")