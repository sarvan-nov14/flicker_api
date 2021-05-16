from models import db, ImageList
import time

def get_images(response, image_api_req):
    r = response.json()
    images = r.get('photos').get('photo')
    image_list = []
    for i in images:
        url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(
            i.get('farm'),
            i.get('server'),
            i.get('id'),
            i.get('secret')
        )
        
        image = ImageList(image_url=url)
        image_api_req.image_src.append(image)
        image_list.append(image)
    
    db.session.add_all(image_list)
    time.sleep(10)
    image_api_req.is_completed = True
    db.session.commit()
    print("completed")