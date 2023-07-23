import unittest
import pandas as pd
import os

class TestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        users_path = os.path.join(os.getcwd(),'ml-100k','u.user')
        dump_path = os.path.join(os.getcwd(),'ml-100k','u.data')
        movie_path = os.path.join(os.getcwd(),'ml-100k','u.item')

        item_cols = ["movie id","movie title","release date","video release date",
        "IMDb URL","unknown","Action","Adventure","Animation",
        "Childre's","Comedy","Crime","Documentary","Drama","Fantasy",
        "Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi",
        "Thriller","War","Western"]

        cls.user_df = pd.read_csv(filepath_or_buffer=users_path,sep='|',header=None,\
                names=['user id','age','gender','occupation','zip code'],encoding='latin1')

        cls.data_df = pd.read_csv(filepath_or_buffer=dump_path,sep='\t',header=None,\
                names=['Userid','Itemid','Rating','Timestamp'],encoding='latin1')

        cls.movie_df =  pd.read_csv(filepath_or_buffer=movie_path,sep='|',header=None,\
                names=item_cols,encoding='latin1')

    def test_users_exists(self):

        full_users = pd.unique(TestClass.user_df['user id']).tolist()
        given_users = pd.unique(TestClass.data_df['Userid']).tolist()

        self.assertEqual(first = all(user in full_users for user in given_users),second = True,\
             msg = 'There are users not part of the master list')

    def test_movies_exists(self):
        count = 0
        
        full_movies = pd.unique(TestClass.movie_df['movie id']).tolist()
        given_movies = pd.unique(TestClass.data_df['Itemid']).tolist()

        self.assertEqual(first = all(movie in full_movies for movie in given_movies),second = True,\
        msg = 'There are movies not part of the master list')

    def test_target_exists(self):
        
        target_path = os.path.isdir(os.path.join(os.getcwd(),'target'))
        self.assertEqual(first=target_path,second=True,msg="Target directory doesn't exist")

    @classmethod
    def tearDownClass(cls):
        
        del cls.user_df
        del cls.data_df
        del cls.movie_df