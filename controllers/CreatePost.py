#coding:utf-8
import sys
import tornado.web
import tornado.ioloop
import MongoConn
import datetime
from bson.objectid import ObjectId

dbconn = MongoConn.DBConn()
conn = None
postData = []


class BaseHandler(tornado.web.RequestHandler):
    dbconn.connect()
    #global conn
    conn = dbconn.getConn()
    global posts
    posts = conn.igudoo.posts
    def get_current_user(self):
       	return self.get_secure_cookie("user")

    def postfind(self,postDataInfo):
        posts.find_one(postDataInfo)
	dbconn.close()

    def savepost(self,postDataInfo):
	posts.insert(postDataInfo)
        dbconn.close()

    def updatepost(self,postDataInfo):
	pass

class CreatePostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass;

    def post(self):
	name = tornado.escape.xhtml_escape(self.current_user)
        title = self.get_argument('title')
	if len(title) == 0:
		title="无标题"
        inline1 = self.get_argument('inline1')
	postinfo =  self.get_argument('sHTML')
	shortcut =  self.get_argument('shortcut')
	imgurl = self.get_argument('imgurl')
	if len(shortcut) == 0:
		shortcut = "无剪辑..."
	global postData
	postData=[{"title":title,"postinfo":postinfo,"shortcut":shortcut,"imgurl":imgurl,"createDate":datetime.datetime.now()}][0]

	self.render("prelook.html",title=title,postinfo=postinfo,userName=name)

class CreateExistPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass;

    def post(self):
	name = tornado.escape.xhtml_escape(self.current_user)
	#global postid
	#postid = self.get_argument('postid')
	#return postid
        title = self.get_argument('title')
        if len(title) == 0:
                title="无标题"
        inline1 = self.get_argument('inline1')
        postinfo =  self.get_argument('sHTML')
        shortcut =  self.get_argument('shortcut')
	imgurl = self.get_argument('imgurl')
        if len(shortcut) == 0:
                shortcut = "无剪辑..."
        global postData
        postData=[{"title":title,"postinfo":postinfo,"shortcut":shortcut,"imgurl":imgurl,"createDate":datetime.datetime.now()}][0]
        self.render("prexistlook.html",postid=postid,title=title,postinfo=postinfo,userName=name)

class SaveExistPostHandler(CreateExistPostHandler):
    @tornado.web.authenticated
    def post(self):
	posts.remove({"_id":ObjectId(postid)})
	BaseHandler.savepost(self,postData)
	

class ViewPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,postid):
	name = tornado.escape.xhtml_escape(self.current_user)
	global viewpostinfo
        viewpostinfo = posts.find_one({"_id":ObjectId(postid)})
	postid = viewpostinfo["_id"]
        title = viewpostinfo["title"]
        postinfo = viewpostinfo["postinfo"]
	imgurl = self.get_argument('imgurl')
        postData = viewpostinfo
        dbconn.close()
        self.render("viewpost.html",postinfo=postinfo,title=title,postid=postid,userName=name)
class SavePostHandler(CreatePostHandler):
    @tornado.web.authenticated
    def post(self):
	BaseHandler.savepost(self,postData)

class AlterPostHandler(CreatePostHandler):
    @tornado.web.authenticated
    def post(self):
	name = tornado.escape.xhtml_escape(self.current_user)
	title = postData["title"]
	postinfo = postData["postinfo"]
	shortcut = postData["shortcut"]
	imgurl = self.get_argument('imgurl')
	self.render("alterpost.html",title=title,postinfo=postinfo,shortcut=shortcut,imgurl=imgurl,userName=name)

class AlterExistPostHandler(ViewPostHandler):
    @tornado.web.authenticated
    def post(self):
	name = tornado.escape.xhtml_escape(self.current_user)
	global postid
	postid = viewpostinfo["_id"]
        title = viewpostinfo["title"]
        postinfo = viewpostinfo["postinfo"]
        shortcut = viewpostinfo["shortcut"]
	imgurl = self.get_argument('imgurl')
        self.render("alterexistpost.html",postid=postid,title=title,postinfo=postinfo,shortcut=shortcut,imgurl=imgurl,userName=name)

class DelPostHandler(ViewPostHandler):
    def post(self):
	postid = viewpostinfo["_id"]
	posts.remove({"_id":ObjectId(postid)})

class ListPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
	name = tornado.escape.xhtml_escape(self.current_user)
        postsList = posts.find().sort("createDate",-1)
        listpost = []
        for i in postsList:
                post=[i["title"],i["shortcut"],i["createDate"],i["_id"]]
                listpost.append(post)
	dbconn.close()	
	self.render("postslist.html",listposts=listpost,userName=name)

	

if __name__ == "__main__":
	postsList = posts.find().sort("createDate",-1)
	listpost = [] 
	for i in postsList:
		post=[i["title"],i["shortcut"],i["createDate"]]
		listpost.append(post)
		print listpost
