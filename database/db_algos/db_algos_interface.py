from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_new_data(self, data):
        pass
    
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
    
    @abstractmethod
    def add_user(self, name):
        pass
    
    @abstractmethod
    def add_movie(self, user_id, title, rating, year, director, image_url):
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, new_data={}):
        pass
