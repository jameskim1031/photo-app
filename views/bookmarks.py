from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
import json
from views import get_authorized_user_ids

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id)
        print(bookmarks)
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()

        #checks if post_id is valid format
        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({"message":"'post_id' is not an int."}), mimetype="application/json",  status=400) 
        
        #checks if post_id is valid
        if post_id >= len(Post.query.all()):
            return Response(json.dumps({"message":"'post_id' does not exist."}), mimetype="application/json",  status=404) 

        # checks if post is reachable (if its a post from someone I follow)
        user_ids = get_authorized_user_ids(self.current_user)
        posts = Post.query.filter(Post.user_id.in_(user_ids)).all()
        if Post.query.filter_by(id=post_id).first() not in posts:
            return Response(json.dumps({"message":"'post_id' is not reachable."}), mimetype="application/json",  status=404) 

        # checks if I already have the post in bookmark
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        post_ids = [bookmark.post_id for bookmark in bookmarks]
        if post_id in post_ids:
            return Response(json.dumps({"message":"'post_id' is a duplicate."}), mimetype="application/json",  status=400) 
        
        
        new_bookmark = Bookmark(
            post_id= body.get('post_id'),
            user_id= self.current_user.id
        )

        db.session.add(new_bookmark)    # issues the insert statement
        db.session.commit()         # commits the change to the database 

        return Response(json.dumps(new_bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "bookmark" record where "id"=id
        print(id)
        try:
            id = int(id)
        except:
            return Response(json.dumps({"message":"'id' is not an int."}), mimetype="application/json",  status=400)

        if not Bookmark.query.get(id):
            return Response(json.dumps({"message":"'id' does not exist."}), mimetype="application/json",  status=404) 
        
        # gets ids of all the following + self
        user_ids = get_authorized_user_ids(self.current_user)
        #print(user_ids)
        if Bookmark.query.get(id).user_id not in user_ids:
            return Response(json.dumps({"message":"'id' is not authorized."}), mimetype="application/json",  status=404) 

        bookmark = Bookmark.query.get(id)
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps({"message":"Bookmark id={0} was successfully deleted.".format(id)}), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
