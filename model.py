class Movie:
    def __init__(self, id, name=''):
        self.id = id
        self.name = name


class User:
    def __init__(self, id):
        self.id = id


class Rating:
    def __init__(self, users, movies):
        self.rowLength = len(users)
        self.columnLength = len(movies)
        self.matrix = [[0 for row in range(self.rowLength)] for col in range(
            self.columnLength)]
        for user in users:
            for movie_id in user['movies']:
                self.matrix[user['user_id'] - 1][movie_id - 1] = 1

    def who_has_seen(self, movie):
        users = []
        for index in range(self.rowLength):
            if self.matrix[index][movie.id - 1] != 0:
                users.append(User(index + 1))

        return users

    def get_movies_by_user(self, user):
        return self.matrix[user.id - 1]

    def get_id_movies_not_seen_by(self, user_id):
        nsmIds = []

        for index in range(self.columnLength):
            if self.matrix[user_id - 1][index] == 0:
                nsmIds.append(index + 1)

        return nsmIds

    def get_id_movies_seen_by(self, user_id):
        smIds = []

        for index in range(self.columnLength):
            if self.matrix[user_id - 1][index] == 1:
                smIds.append(index + 1)

        return smIds


class MoviesMatrix:
    def __init__(self, movies):
        self.rowLength = len(movies)
        self.columnLength = len(movies)
        self.matrix = [[0.0 for row in range(self.rowLength)] for col in range(
            self.columnLength)]

    def insert_value(self, x, y, value):
        self.matrix[x][y] = value

    def record_relation(self, movieA_id, movieB_id):
        self.matrix[movieA_id][movieB_id] += 1.0

    def compute_similarity(self, movieA_id, movieB_id):
        numerator = self.matrix[movieA_id][movieB_id]
        denominator = self.matrix[movieA_id][movieA_id] * \
                      self.matrix[movieB_id][movieB_id]

        return float(numerator / denominator)


class Prediction:
    def __init__(self, user):
        self.user = user
        self.similarities = {}

    def update(self, smovie_id, nsmovie_id, sim):
        self.similarities.update({(smovie_id, nsmovie_id): sim})

    def get_n_greatest(self, size):
        pred = {}
        count = 0
        for k, v in self.similarities.iteritems():
            if k[1] in pred:
                if pred[k[1]] < v:
                    pred[k[1]] = v
            elif count < size:
                pred.update({k[1]: v})
                count += 1
            else:
                remove_id = 0
                for movie_id, sim in pred.iteritems():
                    if remove_id == 0:
                        if sim < v:
                            remove_id = movie_id
                    elif sim < pred[remove_id]:
                        remove_id = movie_id
                if remove_id != 0:
                    del pred[remove_id]
                    pred.update({k[1]: v})

        return pred