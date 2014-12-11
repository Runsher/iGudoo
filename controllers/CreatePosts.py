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
		postDataInfo['status'] = 1
        	posts.insert(postDataInfo)
        	dbconn.close()

	def updatepost(self,postDataInfo):
		update_id = postDataInfo['_id']
		del postDataInfo['_id']
		postDataInfo['createDate'] = datetime.datetime.now()
		postDataInfo['status'] = 1
		posts.update({"_id":update_id},{"$set":postDataInfo},True)
        	dbconn.close()

	def delpost(self,postDataInfo):
		del_id = postDataInfo['_id']
		posts.update({"_id":del_id},{"$set":{'status':0}},True)
	
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
		if postdata.has_key("_id"):
			postdata['_id'] = ObjectId(postdata['_id'])
			BaseHandler.updatepost(self,postdata)
		else:
       	 		BaseHandler.savepost(self,postdata)

class AlterPostHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.render("alterpost.html",postdata=postdata)

class DelPostHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		if postdata.has_key("_id"):
            		BaseHandler.delpost(self,postdata)
		else:
			pass;

class ListPostHandler(BaseHandler):
    	@tornado.web.authenticated
    	def get(self):
        	name = tornado.escape.xhtml_escape(self.current_user)
        	postsList = posts.find({'status':1}).sort("createDate",-1)
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
