from flask import Response, request
from flask_restful import Resource
from models import LikePost, db,Post
import json
from views import get_authorized_user_ids


class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()

        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({"message":"'post_id' is not an int."}), mimetype="application/json",  status=400)         

        if post_id >= len(Post.query.all()):
            return Response(json.dumps({"message":"'post_id' does not exist."}), mimetype="application/json",  status=404) 
        

        # gets ids of all the following + self
        user_ids = get_authorized_user_ids(self.current_user)
        # gets post for all following + self
        posts = Post.query.filter(Post.user_id.in_(user_ids)).all()
        if Post.query.filter_by(id=post_id).first() not in posts:
            return Response(json.dumps({"message":"'post_id' is not reachable."}), mimetype="application/json",  status=404) 
        
        #check if post_id is not in liked_posts
        #1. get list of post_ids that are already liked
        likes = LikePost.query.filter_by(user_id=self.current_user.id).all()
        post_ids = [like.post_id for like in likes]
        print(post_ids)
        #2. check if body.get(post_id) is in the list
        if post_id in post_ids:
            return Response(json.dumps({"message":"'post_id' is not an int."}), mimetype="application/json",  status=400)

        like_post = LikePost(
            post_id= post_id,
            user_id=self.current_user.id
        )

        db.session.add(like_post)    # issues the insert statement
        db.session.commit()         # commits the change to the database 
        return Response(json.dumps(like_post.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "like_post" where "id"=id
        print(id)
        try:
            id = int(id)
        except:
            return Response(json.dumps({"message":"'id' is not an int."}), mimetype="application/json",  status=400)

        if id >= len(LikePost.query.all()):
            return Response(json.dumps({"message":"'id' does not exist."}), mimetype="application/json",  status=404) 
        
        # gets ids of all the following + self
        user_ids = get_authorized_user_ids(self.current_user)
        #print(user_ids)
        if LikePost.query.get(id).user_id not in user_ids:
            return Response(json.dumps({"message":"'id' is not authorized."}), mimetype="application/json",  status=404) 

        like_post = LikePost.query.get(id)
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps({"message":"LikePost id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
