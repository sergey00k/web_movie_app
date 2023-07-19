from flask import Flask, render_template, request
from database.db_algos.json_algo import JsonDataManager
import requests

app = Flask(__name__)
data_manager = JsonDataManager("/Users/sk/Desktop/Masterschool/web_movie_app/database/db_files/db.json")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/users', methods=['GET', 'POST'])
def list_users(flag=True):
    if request.method == 'POST' and flag:
        search = request.form['search']
        search_results = 0
        users = data_manager.get_all_users()
        matched_users = {}
        for user, user_id in users.items():
            if search.lower() == user.lower()[:len(search)]:
                matched_users[user] = user_id
                search_results += 1
        if search_results == 0:
            return render_template('no_search_results.html')
        else:
            return render_template('users.html', users=matched_users)
    else:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)

@app.route('/favourites/<user_id>')
def get_favourites(user_id):
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user_by_id(user_id)['name']
    return render_template('user_movies.html', movies=movies, user=user, user_id=user_id)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        checkbox_data = request.form.getlist('yesno')
        name = request.form['name']
        user_id = data_manager.add_user(name)
        if 'yes' in checkbox_data:
            return render_template('add_movie.html', user_id=user_id)
        else:
            return list_users(False)
    else:
        return render_template('add_user.html')

@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        checkbox_data = request.form.getlist('yesno')
        payload = {'apikey': '3d01cfe1', 't': title}
        response = requests.get('http://www.omdbapi.com/', params=payload)
        if response.status_code != 200:
            return render_template('external_api_error.html')
        else:
            content = response.json()
        if 'Error' in content:
            return render_template('external_api_error.html')
        else:
            data_manager.add_movie(user_id, title, content['imdbRating'], content['Year'], content['Director'], content['Poster'])
        if 'yes' in checkbox_data:
            return render_template('add_movie.html', user_id=user_id)
        else:
            return get_favourites(user_id)
    else:
        return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['POST', 'GET'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        director = request.form['director']
        rating = request.form['rating']
        data_manager.update_movie(user_id, movie_id, title, year, director, rating)
        return get_favourites(user_id)
    else:
        user = data_manager.get_user_by_id(user_id)
        movie_info = user['movies'][movie_id]
        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie_info=movie_info)

@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return get_favourites(user_id)

@app.route('/users/delete_user/<user_id>')
def delete_user(user_id):
    data_manager.delete_user(user_id)
    return list_users()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

