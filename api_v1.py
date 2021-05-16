import os
import uuid
import requests
from time import sleep

from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal
from flask_migrate import Migrate
import threading




app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

from models import db, ImageApiRequest, ImageList
from utils import get_images

migrate = Migrate(app, db)

api = Api(app)

resource_fields = {
    'image_url': fields.String,
}

class GetImages(Resource):
    def get(self):
        db.create_all()
        gallery_id = "72157717157673571" # Gallery with 120 Pics

        api_key = os.environ.get("FLICKER_API_KEY")
        api_endpoint = 'https://api.flickr.com/services/rest/? \
            method=flickr.galleries.getPhotos& \
            api_key={0}&gallery_id={1}& \
            format=json&nojsoncallback=1'.format(api_key, gallery_id)

        response = requests.get(api_endpoint)
        
        if response.status_code == 200 and response.json().get('stat') == 'ok':
            image_api_req = ImageApiRequest()
            db.session.add(image_api_req)
            db.session.commit()
            image_thread = threading.Thread(target=get_images, args=(response, image_api_req))
            image_thread.start()
            return {'status': 'Waiting to process', 'id':str(image_api_req.request_id)}, 202
        
        else:
            return {'status':'FAILED', 'details': response.json().get('message')}, response.status_code

class GetStatus(Resource):
    def get(self):
        uid = request.args.get('uid')
        try:
            image_api = ImageApiRequest.query.filter_by(request_id=uid).first()
        except Exception as e:
            return {'status':'FAILED', 'details':"Invalid Id."}, 400
        
        if not image_api.is_completed:
            msg = "In progress"
            result = []
        else:
            msg = "Completed"
            result = ImageList.query.join(ImageApiRequest).all()

        return {'status': msg, 'result':marshal(result, resource_fields)}, 200

api.add_resource(GetImages, '/get-images')
api.add_resource(GetStatus, '/get-image-status')

if __name__ == '__main__':

    app.run(debug=True)