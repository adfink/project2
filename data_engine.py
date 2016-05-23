# # import code; code.interact(local=locals())
from __future__ import division
import csv

class DataEngine:

    def __init__(self, r,u,m,p):
        self.data_files = []
        ratings_file = r
        users_file = u
        movies_file = m
        predict_file = p
        self.data_files.append(ratings_file)
        self.data_files.append(users_file)
        self.data_files.append(movies_file)
        self.data_files.append(predict_file)

    def get_data(self):
        counter = 0
        for a_file in self.data_files:
            if a_file[-3] == 't':
                raw_data = []
                with open(a_file,'rU') as tsvin:
                    data = csv.reader(tsvin, delimiter='\t')
                    for row in data:
                        raw_data.append(row)
                counter += 1
                self.movie_repo = MoviesRepo(raw_data)
                self.movie_repo.populate()
            else:
                raw_data = []
                with open(a_file, 'rU') as file:
                    data = csv.DictReader(file)
                    for row in data:
                        raw_data.append(row)
                counter += 1
                if counter == 1:
                    self.ratings_repo = RatingsRepo(raw_data)
                    self.ratings_repo.compute_probabilities()
                    self.ratings_repo.collect_ids_of_ratings()
                elif counter == 2:
                    self.users_repo = UsersRepo(raw_data)
                    self.users_repo.populate()
                elif counter == 4:
                    self.empty_predictions = raw_data

    def compute_probabilities_for_users_per_ratings(self):
        ratings_list = ['1','2','3','4','5']
        ratings = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        for i in ratings_list:
            prob_data = {'M':0, 'F':0, 'age1':0,'age18':0,'age25':0,'age35':0,'age45':0,'age50':0,'age56':0}
            for user_id in self.ratings_repo.ratings_users[i]:
                user = self.users_repo.find_by_id(user_id)
                if user.gender == "M":
                    prob_data['M']+=1
                if user.gender == "F":
                    prob_data['F']+=1
                if user.age == '1':
                    prob_data['age1']+=1
                if user.age == '18':
                    prob_data['age18']+=1
                if user.age == '25':
                    prob_data['age25']+=1
                if user.age == '35':
                    prob_data['age35']+=1
                if user.age == '45':
                    prob_data['age45']+=1
                if user.age == '50':
                    prob_data['age50']+=1
                if user.age == '56':
                    prob_data['age56']+=1
            if i == '1':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_users[i])
                ratings['1'] = prob_data
            if i == '2':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_users[i])
                ratings['2'] = prob_data
            if i == '3':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_users[i])
                ratings['3'] = prob_data
            if i == '4':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_users[i])
                ratings['4'] = prob_data
            if i == '5':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_users[i])
                ratings['5'] = prob_data
        self.user_prob = ratings

    def compute_probabilities_for_movies_per_ratings(self):
        ratings_list = ['1','2','3','4','5']
        ratings = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        for i in ratings_list:
            prob_data = {'Animation':0,'Childrens':0,'Crime':0,'Mystery':0,'Musical':0,'Documentary':0,'Western':0,'Film-Noir':0, 'Adventure':0, 'Thriller':0,'Comedy':0,'Fantasy':0,'Romance':0,'Drama':0,'War':0,'Action':0,'Horror':0,'Sci-Fi':0}
            for movie_id in self.ratings_repo.ratings_movies[i]:
                movie = self.movie_repo.find_by_id(movie_id)
                for genre in movie.genres:
                    if genre != '':
                        prob_data[genre] += 1
            if i == '1':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_movies[i])
                ratings['1'] = prob_data
            if i == '2':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_movies[i])
                ratings['2'] = prob_data
            if i == '3':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_movies[i])
                ratings['3'] = prob_data
            if i == '4':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_movies[i])
                ratings['4'] = prob_data
            if i == '5':
                for data_point in prob_data:
                    prob_data[data_point] = prob_data[data_point] /len(self.ratings_repo.ratings_movies[i])
                ratings['5'] = prob_data
        self.movie_prob = ratings


    def predict(self):
        for case in self.empty_predictions:
            best_guess = self.collect_probabilties(case)
            case['rating'] = best_guess
        import code; code.interact(local=locals())

    def collect_probabilties(self, case):
        ratings_list = ['1','2','3','4','5']
        ratings_probs = {'1':0,'2':0,'3':0,'4':0,'5':0}
        user = self.users_repo.find_by_id(case['userID'])
        movie = self.movie_repo.find_by_id(case['movieID'])
        case_user_probs = []
        case_movie_probs = []
        case_probs = []
        for r in ratings_list:
            for genre in movie.genres:
                if genre != '':
                    case_probs.append(self.movie_prob[r][genre])
            case_probs.append(self.user_prob[r]["age"+user.age])
            case_probs.append(self.user_prob[r][user.gender])
            total_prob = reduce(lambda x, y: x*y, case_probs)
            ratings_probs[r] = total_prob

        return max(ratings_probs, key=ratings_probs.get)






# import code; code.interact(local=locals())
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
class UsersRepo:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.users = []
    def populate(self):
        for user in self.raw_data:
            user_id = user['userID']
            gender = user['gender']
            age = user['age']
            new_user = User(user_id,gender,age)
            self.users.append(new_user)

    def find_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user


class User:
    def __init__(self, user_id, gender, age):
        self.user_id = user_id
        self.gender = gender
        self.age = age


class RatingsRepo:
    def __init__(self, raw_data):
        self.raw_data = raw_data
    def compute_probabilities(self):
        ratings = {'1':0,'2':0,'3':0,'4':0,'5':0}
        for viewing in self.raw_data:
            for num in ratings:
                if viewing['rating'] == num:
                    ratings[num] += 1
        for num in ratings:
            ratings[num] = ratings[num]/len(self.raw_data)
        self.check_prob(ratings)

    def check_prob(self,thing):
        sum = 0
        for num in thing:
            sum = sum + thing[num]
        if sum != 1:
            raise ValueError('A very specific bad thing happened... the probabilties dont add to 1')

    def collect_ids_of_ratings(self):
        ratings_movie_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        ratings_user_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
        for viewing in self.raw_data:
            rating = viewing['rating']
            userID = viewing['userID']
            movieID = viewing['movieID']

            ratings_movie_ids[rating].append(movieID)
            ratings_user_ids[rating].append(userID)
        self.ratings_movies = ratings_movie_ids
        self.ratings_users = ratings_user_ids




class MoviesRepo:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.movies = []
    def populate(self):
        self.clean_data()
        for movie in self.cleaned_data:
            movie_id = movie['movieID']
            year = movie['year']
            name = movie['name']
            genres = movie['genres']
            new_movie = Movie(movie_id,name,year,genres)
            self.movies.append(new_movie)

    def clean_data(self):
        self.cleaned_data = []
        #remove header row
        self.raw_data.pop(0)
        #create hash with keys of movieID, year, genres, name
        for movie in self.raw_data:
            cleaned_movie_data = {'movieID':0, 'year':0, 'name':0, 'genres':[]}
            movieID = movie[0]
            name = movie[1]
            year = movie[2]
            genres = []
            counter = 0
            for i in movie:
                if counter > 2:
                    if i == "Children's":
                        i = 'Childrens'
                    genres.append(i)
                counter +=1
            cleaned_movie_data['movieID'] = movieID
            cleaned_movie_data['name'] = name
            cleaned_movie_data['year'] = year
            cleaned_movie_data['genres'] = genres
            self.cleaned_data.append(cleaned_movie_data)

    def find_by_id(self, movie_id):
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie

class Movie:
    def __init__(self, movie_id,name,year,genres):
        self.movie_id = movie_id
        self.genres = genres
        self.year = year
        self.name = name


data_engine = DataEngine("ratings.csv", "users.csv", "movies.tsv", "predict.csv")
data_engine.get_data()
data_engine.compute_probabilities_for_movies_per_ratings()
data_engine.compute_probabilities_for_users_per_ratings()
data_engine.predict()



# import code; code.interact(local=locals())
#
# try:
#     case_probs.append(self.movie_prob[r][genre])
# except Exception:
#     import code; code.interact(local=locals())

#find probabilities for the ratings (categories)
#   probability of a 1,2,3,4,5
#find probabilities for each set of features for each category
#   for instance, for ratings of 1, what are the probability
#   that the user was male vs female,
#   that the user was 25 vs 45 vs 18 vs 35 vs 50 vs 1 vs 56
#       so action step: collect all userIDs and all movieIDs for ratings of 1
#to predict, take the user info and the movie info and multiply
#the probabilities for each category and pick the largest
