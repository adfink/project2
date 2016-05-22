# # import code; code.interact(local=locals())
from __future__ import division
import csv

# class RatingsMuncher:
#
#     def __init__(self, file_name):
#         self.file_name = file_name
#
#     def get_data(self):
#         raw_data = []
#         with open(self.file_name, 'rU') as file:
#             data = csv.DictReader(file)
#             for row in data:
#                 raw_data.append(row)
#         self.raw_data = raw_data
#
#     def compute_probabilities(self):
#         ratings = {'1':0,'2':0,'3':0,'4':0,'5':0}
#         for viewing in self.raw_data:
#             for num in ratings:
#                 if viewing['rating'] == num:
#                     ratings[num] += 1
#         for num in ratings:
#             ratings[num] = ratings[num]/len(self.raw_data)
#         self.check_prob(ratings)
#
#     def check_prob(self,thing):
#         sum = 0
#         for num in thing:
#             sum = sum + thing[num]
#         if sum != 1:
#             raise ValueError('A very specific bad thing happened... the probabilties dont add to 1')
#
#     def collect_ids_of_ratings(self):
#         ratings_movie_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
#         ratings_user_ids = {'1':[],'2':[],'3':[],'4':[],'5':[]}
#         for viewing in self.raw_data:
#             rating = viewing['rating']
#             userID = viewing['userID']
#             movieID = viewing['movieID']
#
#             ratings_movie_ids[rating].append(movieID)
#             ratings_user_ids[rating].append(userID)
#         self.ratings_movies = ratings_movie_ids
#         self.ratings_users = ratings_user_ids
#
#
#
#
# class UsersMuncher:
#
#     def __init__(self, file_name, ratings_users):
#         self.file_name = file_name
#         self.ratings_users = ratings_users
#
#     def get_data(self):
#         raw_data = []
#         with open(self.file_name, 'rU') as file:
#             data = csv.DictReader(file)
#             for row in data:
#                 raw_data.append(row)
#         self.raw_data = raw_data
#
#     def compute_probabilities(self):
#         ratings_list = ['1','2','3','4','5']
#         ratings = {'data1':[],'data2':[],'data3':[],'data4':[],'data5':[]}
#         prob_data = {'male':0, 'female':0, 'age1':0,'age18':0,'age25':0,'age35':0,'age45':0,'age56':0}
#         for i in ratings_list:
#             for user in self.ratings_users[i]:
#                 user.gender
#




class DataEngine:

    def __init__(self, r,u,m):
        self.data_files = []
        ratings_file = r
        users_file = u
        movies_file = m
        self.data_files.append(ratings_file)
        self.data_files.append(users_file)
        self.data_files.append(movies_file)

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

    def compute_probabilities_for_users_per_ratings(self):
        ratings_list = ['1','2','3','4','5']
        ratings = {'data1':[],'data2':[],'data3':[],'data4':[],'data5':[]}
        prob_data = {'male':0, 'female':0, 'age1':0,'age18':0,'age25':0,'age35':0,'age45':0,'age56':0}
        for i in ratings_list:
            for user_id in self.ratings_repo.ratings_users[i]:
                user = self.users_repo.find_by_id(user_id)
                if user.gender == "M":
                    prob_data['male']+=1
                if user.gender == "F":
                    prob_data['female']+=1
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
                if user.age == '56':
                    prob_data['age56']+=1
            if i == '1':
                ratings['data1'] = prob_data
            if i == '2':
                ratings['data2'] = prob_data
            if i == '3':
                ratings['data3'] = prob_data
            if i == '4':
                ratings['data4'] = prob_data
            if i == '5':
                ratings['data5'] = prob_data
        print ratings


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


data_engine = DataEngine("ratings.csv", "users.csv", "movies.tsv")
data_engine.get_data()
data_engine.compute_probabilities_for_users_per_ratings()

# minion = RatingsMuncher("ratings.csv")
# minion.get_data()
# minion.compute_probabilities()
# minion.collect_ids_of_ratings()
#
#
# top_minion = DataMuncher(minion)
# top_minion.compute_probabilities()

# import code; code.interact(local=locals())

#find probabilities for the ratings (categories)
#   probability of a 1,2,3,4,5
#find probabilities for each set of features for each category
#   for instance, for ratings of 1, what are the probability
#   that the user was male vs female,
#   that the user was 25 vs 45 vs 18 vs 35 vs 50 vs 1 vs 56
#       so action step: collect all userIDs and all movieIDs for ratings of 1
#to predict, take the user info and the movie info and multiply
#the probabilities for each category and pick the largest