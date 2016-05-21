# # import code; code.interact(local=locals())
from __future__ import division
import csv

class RatingsMuncher:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_data(self):
        raw_data = []
        with open(self.file_name, 'rU') as file:
            data = csv.DictReader(file)
            for row in data:
                raw_data.append(row)
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

minion = RatingsMuncher("ratings.csv")
minion.get_data()
minion.compute_probabilities()

# import code; code.interact(local=locals())

#find probabilities for the ratings (categories)
#   probability of a 1,2,3,4,5
#find probabilities for each set of features for each category
#   for instance, for ratings of 1, what are the probability
#   that the user was male vs female,
#   that the user was 25 vs 45 vs 18 vs 35 vs 50 vs 1 vs 56
#to predict, take the user info and the movie info and multiply
#the probabilities for each category and pick the largest
