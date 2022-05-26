from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
from views import get_authorized_user_ids
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        followings = Following.query.filter_by(user_id=self.current_user.id)
        return Response(json.dumps([following.to_dict_following() for following in followings]), mimetype="application/json", status=200)

    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()

        #check invalid user_id format
        try:
            new_following = int(body.get('user_id'))
        except:
            return Response(json.dumps({"message":"'user_id' is not an int."}), mimetype="application/json",  status=400)      

        #check invalid user_id
        if not User.query.get(new_following):
            return Response(json.dumps({"message":"'user_id' does not exist."}), mimetype="application/json",  status=404) 

        # check duplicates
        followings = Following.query.filter_by(user_id=self.current_user.id).all()
        followings_ids = [following.following_id for following in followings]
        if new_following in followings_ids:
            return Response(json.dumps({"message":"already following user_id"}), mimetype="application/json",  status=400)

        following = Following(
            user_id=self.current_user.id,
            following_id=new_following
        )
        db.session.add(following)    # issues the insert statement
        db.session.commit()         # commits the change to the database 
        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "following" record where "id"=id
        print(id)
        # check invalid id format
        try:
            id = int(id)
        except:
            return Response(json.dumps({"message":"'id' is not an int."}), mimetype="application/json",  status=400)
        
        #check invalid id
        if not Following.query.get(id):
            return Response(json.dumps({"message":"'id' does not exist."}), mimetype="application/json",  status=404) 

        #check unauthorized id
        # gets ids of all the following + self
        user_ids = get_authorized_user_ids(self.current_user)
        #print(user_ids)
        if Following.query.get(id).following_id not in user_ids:
            return Response(json.dumps({"message":"'id' is not authorized."}), mimetype="application/json",  status=404) 

        following = Following.query.get(id)
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps({"message":"Following id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
