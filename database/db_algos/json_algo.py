from database.db_algos.db_algos_interface import DataManagerInterface as DMI
import json

class JsonDataManager(DMI):
    def __init__(self, file_path):
        self.file = file_path

    def read_data(self):
        with open(self.file, "r") as fileobj:
            users = json.load(fileobj)
        return users

    def unique_id(self, user_id=-1):
        id_list = []
        users = self.read_data()
        if int(user_id) >= 0:
            for movie_id in users[user_id]["movies"]:
                id_list.append(movie_id)
            for number in range(1000000000):
                if str(number) not in id_list:
                    return number
        else:
            for user_id in users:
                id_list.append(user_id)
            for number in range(1000000000):
                if str(number) not in id_list:
                    return number
                
    def get_user_by_id(self, user_id):
        users = self.read_data()
        return users[user_id]
         
    def write_new_data(self, data):
        with open(self.file, "w") as fileobj:
            users = json.dumps(data, indent=2)
            fileobj.write(users)

    def get_all_users(self):
        users_to_id = {}
        users = self.read_data()
        for user, value in users.items():
            users_to_id[value["name"]] = user
        return users_to_id

    def get_user_movies(self, user_id):
        movies = {}
        users = self.read_data()
        for movie_id, movie in users[user_id]["movies"].items():
            movies[movie_id] = movie
        return movies
    
    def add_movie(self, user_id, title, rating, year, director, image_url):
        users = self.read_data()
        users[user_id]["movies"][self.unique_id(user_id)] = {"title": title, "rating": rating, "year": year, "director": director, "image_url": image_url}
        self.write_new_data(users)
        return "SUCCESS"

    def delete_movie(self, user_id, movie_id):
        users = self.read_data()
        del users[user_id]["movies"][movie_id]
        self.write_new_data(users)
        return "SUCCESS"

    def update_movie(self, user_id, movie_id, title, year, director, rating):
        users = self.read_data()
        users[user_id]["movies"][movie_id]['title'] = title
        users[user_id]["movies"][movie_id]['year'] = year
        users[user_id]["movies"][movie_id]['director'] = director
        users[user_id]["movies"][movie_id]['rating'] = rating
        self.write_new_data(users)
        return "SUCCESS"
    
    def add_user(self, name):
        users = self.read_data()
        new_id = self.unique_id()
        users[new_id] = {'name': name, 'movies': {}}
        self.write_new_data(users)
        return new_id
    
    def delete_user(self, user_id):
        users = self.read_data()
        del users[user_id]
        self.write_new_data(users)
        return "SUCCESS"
    
obj = JsonDataManager("/Users/sk/Desktop/Masterschool/web_movie_app/database.db/db_files/db.json")
