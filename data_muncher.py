# # import code; code.interact(local=locals())
from __future__ import division
import csv

class DataMuncher:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_data(self):
        if self.file_name[-3] == 't':
            raw_data = []
            with open(self.file_name,'rU') as tsvin:
                data = csv.reader(tsvin, delimiter='\t')
                for row in data:
                    raw_data.append(row)
        else:
            raw_data = []
            with open(self.file_name, 'rU') as file:
                data = csv.DictReader(file)
                for row in data:
                    raw_data.append(row)



##### take in the data

minion_1 = DataMuncher("users.csv")
minion_1.get_data()

minion_2 = DataMuncher("ratings.csv")
minion_2.get_data()

minion_3 = DataMuncher("movies.tsv")
minion_3.get_data()




# from __future__ import division
# import csv
# import matplotlib.pyplot as plt
#
# class DataParser:
#     'reads in CSV and does things with it'
#
#     def __init__(self, file_name,):
#         self.file_name = file_name
#         self.years = range(1962,2014)
#         ########################################################################################
#         self.title_name = "Food Production Index (2004-2006 = 100)"
#         self.y_axis = "index"
#         ########################################################################################
#     def process_data(self):
#         #take in data from CSV as a list of dictionaries
#         raw_data = []
#         with open(self.file_name, 'rU') as file:
#             data = csv.DictReader(file)
#             for row in data:
#                 raw_data.append(row)
#         #compile a list of all the countries
#         countries = []
#         for r in raw_data:
#             countries.append(r['Country Name'])
#
#         country_data = {}
#         for c in countries:
#             for r in raw_data:
#                 if r['Country Name'] == c :
#                     data=[]
#                     for y in self.years:
#                         data.append(r[str(y)])
#                     country_data[c] = data
#
#         processed_country_data = {}
#
#         for c in country_data:
#             data = country_data[c]
#             #convert empty strings to zeros
#             counter = 0
#             for d in data:
#                 if d == '':
#                     data[counter] = 0
#                 else:
#                     data[counter] = float(d)
#                 counter += 1
#             #trim zeros
#             trim_zeros = []
