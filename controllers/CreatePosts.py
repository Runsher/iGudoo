#coding:utf-8
import sys
import tornado.web
import tornado.ioloop
import MongoConn
import datetime
import json
from bson.objectid import ObjectId

dbconn = MongoConn.DBConn()
conn = None

class BaseHandler(tornado.web.RequestHandler):
	dbconn.connect()
	conn = dbconn.getConn()
	global posts
	posts = conn.igudoo.posts
	def get_current_user(self):
        	return self.get_secure_cookie("user")

	def savepost(self,postDataInfo):
		postDataInfo['createDate'] = datetime.datetime.now()
		#if !postDataInfo['_id']:
		#....
        	posts.insert(postDataInfo)
        	dbconn.close()

	def updatepost(self,postDataInfo):
		posts.update({"_id":postDataInfo['_id']},{"$set":postDataInfo})
        	dbconn.close()

class CreatePostHandler(BaseHandler):
    	@tornado.web.authenticated
	def get(self):
		pass;

	def post(self):
		global postdata
		postdata = json.loads(self.request.body)
		self.render("prelook.html",postdata=postdata)

class SavePostHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
       	 	BaseHandler.savepost(self,postdata)

class AlterPostHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.render("alterpost.html",postdata=postdata)

class ListPostHandler(BaseHandler):
    	@tornado.web.authenticated
    	def get(self):
        	name = tornado.escape.xhtml_escape(self.current_user)
        	postsList = posts.find().sort("createDate",-1)
        	dbconn.close()
        	self.render("postslist.html",listposts=postsList,userName=name)

class ViewPostHandler(BaseHandler):
	pass;
    	@tornado.web.authenticated
    	def get(self,postid):
        	name = tornado.escape.xhtml_escape(self.current_user)
        	global postdata
        	postdata = posts.find_one({"_id":ObjectId(postid)})
        	dbconn.close()
        	self.render("viewpost.html",postdata=postdata,userName=name)
