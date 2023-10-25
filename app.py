import imp
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
from models import db, Instagram
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from instagram import instagramScrap
from waitress import serve
import settings
# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
class instagram(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'You are not allowed to access this resource'})

    # Corresponds to POST request
    def post(self):
        obj = instagramScrap()
        # Call the my_function method
        data = request.json  # status code
        #{"userName":"neeraj88maurya21","passWord":"Admin@del21","page":"https://www.instagram.com/bjp4india/","pageName":"bjp4india"}
        if settings.insta_name and settings.insta_password and data['page'] and data['pageName']:
            driver = obj.login_to_instagram(settings.insta_name,settings.insta_password)
            print(driver)
            page = data['page']
            page_name = data['pageName']
            obj.scrap_post(driver,page,page_name)

            return jsonify({'message':"Instagram Webscraping Successfully done"})
        else:
            return jsonify({'message':"You are not accessing the right way"})

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
class twitter(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):
        data = request.json  # status code
        return jsonify({'you sent ':data})

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
class facebook(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):
        data = request.json  # status code
        return jsonify({'you sent ':data})

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
class default(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        return jsonify({'message': 'You are not accessing the right way'})

    # Corresponds to POST request
    def post(self):
        return jsonify({'message': 'You are not accessing the right way'})
    
# # another resource to calculate the square of a number
# class twitter(Resource):

#     def get(self, num):
#         return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
#api.add_resource(twitter, '/square/<int:num>')
api.add_resource(default, '/')
api.add_resource(instagram, '/instagram/')
api.add_resource(twitter, '/twitter/')
api.add_resource(facebook, '/facebook/')

# driver function
if __name__ == '__main__':
    with app.test_client() as c:
        # First method call by GET
        response_get = c.get('/')
        print(response_get.get_json())

        # Second method call by POST
        response_post = c.post('/', json={'key': 'value'})
        print(response_post.get_json())

    #app.run(debug=True)
    app.run(debug=True, port=5001)
    # serve(app, host="0.0.0.0", port=8080)

