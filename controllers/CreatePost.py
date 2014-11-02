#coding:utf-8
import sys
import tornado.web
import tornado.ioloop
import MongoConn
import datetime

dbconn = MongoConn.DBConn()
conn = None


class BaseHandler(tornado.web.RequestHandler):
#   def get_current_user(self):
#       return self.get_secure_cookie("user")
    dbconn.connect()
    global conn
    conn = dbconn.getConn()
    global posts
    posts = conn.igudoo.posts

    def postfind(self,postDataInfo):
        posts.find_one(postDataInfo)
	dbconn.close()

    def savepost(self,postDataInfo):
	posts.insert(postDataInfo)
        dbconn.close()

    def updatepost(self,postDataInfo):
	pass

class CreatePostHandler(BaseHandler):
#   @tornado.web.authenticated
    def get(self):
        pass;

    def post(self):
        title = self.get_argument('title')
	if len(title) == 0:
		title="无标题"
        inline1 = self.get_argument('inline1')
	postinfo =  self.get_argument('sHTML')
	shortcut =  self.get_argument('shortcut')
	if len(shortcut) == 0:
		shortcut = "无剪辑..."
	global postData
	postData=[{"title":title,"postinfo":postinfo,"shortcut":shortcut,"createDate":datetime.datetime.now()}][0]
        #self.write("<p><span style='font-weight: bold; line-height: 22px; text-decoration: underline; font-size: 14px;'>新文章预览</span></p>"  + '<p><span style="font-weight: bold; line-height: 22px; font-size: 24px;">' +title + '</span></p>' + postinfo )
	self.render("prelook.html",title=title,postinfo=postinfo)

class ViewPostHandler(CreatePostHandler):
    def get(self,title_in):
        #dbconn.connect()
        #conn = dbconn.getConn()
        #posts = conn.igudoo.posts
        viewpostinfo = posts.find_one({"title":title_in})
	#viewpostinfo = BaseHandler.postfind(self,{"title":title_in})
        title = viewpostinfo["title"]
        postinfo = viewpostinfo["postinfo"]
	global postData
        postData = viewpostinfo
        dbconn.close()
        self.render("viewpost.html",postinfo=postinfo,title=title)
class SavePostHandler(BaseHandler):
    def post(self):
	#dbconn.connect()
        #conn = dbconn.getConn()
        #posts = conn.igudoo.posts
        #posts.insert(postData)
	BaseHandler.savepost(self,postData)

class AlterPostHandler(ViewPostHandler):
    def post(self):
	title = postData["title"]
	postinfo = postData["postinfo"]
	shortcut = postData["shortcut"]
	self.render("alterpost.html",title=title,postinfo=postinfo,shortcut=shortcut)


class ListPostHandler(BaseHandler):
    def get(self):
        postsList = posts.find().sort("createDate",-1)
        listpost = []
        for i in postsList:
                post=[i["title"],i["shortcut"],i["createDate"]]
                listpost.append(post)
	dbconn.close()	
	self.render("postslist.html",listposts=listpost)

	

if __name__ == "__main__":
	dbconn.connect()
	conn = dbconn.getConn()
	posts = conn.igudoo.posts
	postsList = posts.find().sort("createDate",-1)
	listpost = [] 
	for i in postsList:
		post=[i["title"],i["shortcut"],i["createDate"]]
		listpost.append(post)
		print listpost
