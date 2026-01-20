#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# 1. Home Resource - A simple welcome message
class Home(Resource):
    def get(self):
        return make_response({"message": "Welcome to the Newsletter RESTful API"}, 200)

# 2. Newsletters Resource - Handles List (GET) and Create (POST)
class Newsletters(Resource):
    def get(self):
        # Fetch all records and convert to dicts
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        return make_response(newsletters, 200)

    def post(self):
        # Create a new record from form data
        new_record = Newsletter(
            title=request.form.get('title'),
            body=request.form.get('body')
        )
        db.session.add(new_record)
        db.session.commit()
        
        return make_response(new_record.to_dict(), 201)

# 3. NewsletterByID Resource - Handles specific record retrieval
class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if not newsletter:
            return make_response({"error": "Newsletter not found"}, 404)
        
        return make_response(newsletter.to_dict(), 200)

# Register the routes
api.add_resource(Home, '/')
api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)