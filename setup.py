from math import sqrt
import pandas as pd
import numpy as np
import model

data = pd.read_csv("data(1).txt")
data.to_csv('data.csv', index=None )
def find_prediction_by(user_id, um_matrix, mm_matrix):
    prediction = model.Prediction(model.User(user_id))
    smovie_ids = um_matrix.get_id_movies_seen_by(user_id)
    nsmovie_ids = um_matrix.get_id_movies_not_seen_by(user_id)
    for sm_id in smovie_ids:
        for nsm_id in nsmovie_ids:
            if sm_id < nsm_id:
                sim = mm_matrix.matrix[nsm_id - 1][sm_id - 1]
            else:
                sim = mm_matrix.matrix[sm_id - 1][nsm_id - 1]
            prediction.update(sm_id, nsm_id, sim)

    return prediction


def register_relations(moviea, um_matrix, mm_matrix):
    """Users that have watched the movie"""
    audience = um_matrix.who_has_seen(moviea)
    mm_matrix.insert_value(moviea.id - 1, moviea.id - 1, float(
        sqrt(len(audience))))
    for user in audience:
        usm = um_matrix.get_movies_by_user(user)
        for movieb_id in range(moviea.id, len(usm)):
            if usm[movieb_id] == 1:
                mm_matrix.record_relation(moviea.id - 1, movieb_id)


def run(n_movies, json_file):
    """The main method for the movie recommender"""
    json = data(json_file)
    users = json['users']
    movies = [model.Movie(int(k), v) for k, v in json['movies'].items()]
    usermoviematrix = model.UsersMoviesMatrix(users, movies)
    moviemoviematrix = model.MoviesMatrix(movies)

    # Register relation between movies
    for movie in movies:
        register_relations(movie, usermoviematrix, moviemoviematrix)

    # Compute cosine similarity between movies
    for moviea in movies:
        for movieb_id in range(moviea.id, len(movies)):
            sim = moviemoviematrix.compute_similarity(moviea.id - 1,
                                                      movieb_id)
            moviemoviematrix.insert_value(movieb_id, moviea.id - 1, sim)

    # Find which movies should be recommended
    predictions = []
    for user in users:
        predictions.append(
            find_prediction_by(user['user_id'], usermoviematrix,
                               moviemoviematrix))
    for pred in predictions:
        recommendation = pred.get_n_greatest(n_movies)
        print '# The recommended movie for the user: %s' % pred.user.id
        for key, value in recommendation.iteritems():
            print filter(lambda x: x.id == key, movies)[0].name