from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post
from views import get_authorized_user_ids

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "Comment" based on the data posted in the body 
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
        
        if not body.get('text'):
            return Response(json.dumps({"message":"empty text"}), mimetype="application/json",  status=400) 

        new_comment = Comment(
            post_id=body.get('post_id'),
            user_id=self.current_user.id,
            text=body.get('text')
        )

        db.session.add(new_comment)    # issues the insert statement
        db.session.commit()         # commits the change to the database 

        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        if id >= len(Comment.query.all()):
            return Response(json.dumps({"message":"'id' is invalid."}), mimetype="application/json",  status=404)
        
        # gets ids of all the following + self
        user_ids = get_authorized_user_ids(self.current_user)
        if Comment.query.get(id).user_id not in user_ids:
            return Response(json.dumps({"message":"'post_id' is not authorized."}), mimetype="application/json",  status=404) 

        comment = Comment.query.get(id)
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps({"message":"Comment id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
