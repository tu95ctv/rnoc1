# -*- coding: utf-8 -*-
import os
import sha
import multiprocessing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
import requests
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')
import socket
import urllib2
from html2bbcode.parser import HTML2BBCode
import re
from string import rfind
import cookielib
import hashlib
import urllib
from time import sleep
import collections
default_timeout = 12
socket.setdefaulttimeout(default_timeout)
import os
from threading import Thread
from random import randint
import time
import threading
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
from bs4 import BeautifulSoup

from drivingtest.models import Ulnew   , AdminUl, ForumTable, PostLog, UlDaPost,\
    PostLogDaPost, LeechSite,thongbao, postdict
class check_txt_line():
    pass
def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def get_html(url):    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = None 
    for i in xrange(13):
        try:
            html = opener.open(url).read()
            break
        except:
            print 'Get html.. again for timeout'
    return html


def leech_one_entry_latin1 (ahref_title):
    print 'ahref_title',ahref_title
    entry_url = ahref_title[0]
    title = ahref_title[1]
    
    if Ulnew.objects.filter(title=title).exists():
        print 'entry nay da ton tai %s'%title
        return ''
    
    html = get_html (entry_url)
    print 'full entry html',html
    soup = BeautifulSoup(html)
    class_entry_name = 'div.'+'entry-content'
    category = soup.select('section.entry-category')[0].find('a').string
    category =  u'{0}'.format(category)
    print category
    #print 'type(category)',type(category)
    quotes_wrappers = soup.select(class_entry_name)[0]
    noidung =   u'{0}'.format(quotes_wrappers) 
    print 'type of enoidung' ,type(noidung)
    print 'noidung',noidung
    titlea = quotes_wrappers.find('h1', attrs={'class': 'entry-title'}).string
    print 'type of titlea',type(titlea)
    titlea =  u'{0}'.format(titlea)
    print 'type of titlea',type(titlea)
    #titlea =  titlea.string
    #titlea = titlea.replace(u'–', u'-')
    print 'title' , titlea

    print '#########'

    parser = HTML2BBCode()
    bbcode = parser.feed(noidung)
    #bbcode = bbcode.encode('utf-8')
    p = re.compile( '\s*Posted on.*?(?P<caiquaigi>\[img\])',re.DOTALL)
    bbcode = p.sub( '\g<caiquaigi>', bbcode)
    p = re.compile( '\[url=.*?\]',re.DOTALL)
    bbcode = p.sub( '', bbcode)
    prefix_links = ['http://rapidgator.net/file/','http://uploaded.net/file/','http://www.uploadable.ch/file/']
    stuff = map(lambda w: bbcode.find(w) , prefix_links)
    print 'stuff',stuff
    try:
        min_index_bbcode_host =  min(i for i in stuff if i > 0)
    except:
        return ''
    print 'min_index_bbcode_host',min_index_bbcode_host

    code_part = bbcode[min_index_bbcode_host:]
    n_last_index = bbcode.rfind('\n',min_index_bbcode_host-10,min_index_bbcode_host)
    description =  bbcode[:n_last_index]
    description = description.replace('[b] [/b]',u'').replace(u'[/img][/url]',u'[/img]')
    print 'description',description
    
    print '## Find links'
    prefix_links = {'rg':'http://rapidgator.net/file/','ul':'http://uploaded.net/file/','up':'http://www.uploadable.ch/file/'}
    links_dict ={}
    for key,prefix_link in prefix_links.iteritems():
        links = re.findall('('+prefix_link+'.*?)[\[\]\n\r]', code_part, re.DOTALL)
        links =  unique_list(links)
        linktxt = ''
        for link in links:
            linktxt = linktxt + urllib.unquote(link).decode('utf-8') +'\n'
        print linktxt
        links_dict[key] = linktxt
    print links_dict
    
    new_instance = Ulnew.objects.get_or_create (
                                         title= titlea
              

                                        )[0]
    new_instance.category = category                                    
    new_instance.description = description
    new_instance.rg= links_dict['rg']
    new_instance.ul = links_dict['ul']
    new_instance.up = links_dict['up']
    new_instance.save()
    print 'ok'   
def leech_one_entry_freedl2u(ahref_title):
    print 'ahref_title',ahref_title
    entry_url = ahref_title[0]
    title = ahref_title[1]
    if Ulnew.objects.filter(title=title).exists():
        print 'entry nay da ton tai %s'%title
        return ''
    html = get_html (entry_url)
    #print 'full entry html',html
    soup = BeautifulSoup(html)
    title = u'{0}'.format(soup.find(id="news-title").string)
    print 'title',title
    category = soup.find_all('span', attrs={'itemprop': 'title'})[-1].string
    print 'category',category
    print 'type of category',type(category)
    '''
    dlecontent = soup.find(id="dle-content")
    print dlecontent
    '''
    class_entry_name = 'div.'+'base.fullstory'
    fullstory = soup.select(class_entry_name)[0]
    #print fullstory
    subfull = fullstory.select('div.maincont')[0]
    print 'subfull',subfull
    #category = soup.select('section.entry-category')[0].find('a').string
    #category =  u'{0}'.format(category)
    #print category
    noidung =   u'{0}'.format(subfull).replace('<br/>','\n').replace('<br>','\n').replace('Rapidgator.net:','')
    parser = HTML2BBCode()
    bbcode = parser.feed(noidung).replace('Buy Premium To Support Me  Get Resumable Support  Max Speed','')
     
    #print 'type of enoidung' ,type(noidung)
    print 'noidung',noidung,bbcode
    
    '''
    titlea = subfull.find('h1', attrs={'class': 'entry-title'}).string
    print 'type of titlea',type(titlea)
    titlea =  u'{0}'.format(titlea)
    print 'type of titlea',type(titlea)
    #titlea =  titlea.string
    #titlea = titlea.replace(u'–', u'-')
    print 'title' , titlea
    '''
    print '#########'

    '''
    #bbcode = bbcode.encode('utf-8')
    p = re.compile( '\s*Posted on.*?(?P<caiquaigi>\[img\])',re.DOTALL)
    bbcode = p.sub( '\g<caiquaigi>', bbcode)
    p = re.compile( '\[url=.*?\]',re.DOTALL)
    bbcode = p.sub( '', bbcode)
    '''
    
    prefix_links = ['http://rapidgator.net/file/','http://uploaded.net/file/','http://www.uploadable.ch/file/','http://www.nitroflare.com/view/','http://nitroflare.com/view']
    stuff = map(lambda w: bbcode.find(w) , prefix_links)
    print 'stuff',stuff
    try:
        min_index_bbcode_host =  min(i for i in stuff if i > 0)
    except:
        return ''
    print 'min_index_bbcode_host',min_index_bbcode_host

    code_part = bbcode[min_index_bbcode_host:]
    n_last_index = bbcode.rfind('\n',min_index_bbcode_host-10,min_index_bbcode_host)
    description =  bbcode[:n_last_index]
    description = description.replace('[b] [/b]',u'').replace(u'[/img][/url]',u'[/img]').replace('[img]http://sharenxs.com/photos/2014/10/24/54498d402d290/tn-f0912e470f81f8acf2c127d9a94b5983.jpg[/img]','').replace('nitroflare','')
    print 'description',description
    
    print '## Find links'
    prefix_links = {'rg':'http://rapidgator.net/file/','ul':'http://uploaded.net/file/','up':'http://www.uploadable.ch/file/'}
    links_dict ={}
    for key,prefix_link in prefix_links.iteritems():
        links = re.findall('('+prefix_link+'.*?)[\[\]\n\r]', code_part, re.DOTALL)
        links =  unique_list(links)
        linktxt = ''
        for link in links:
            linktxt = linktxt + urllib.unquote(link).decode('utf-8') +'\n'
        print linktxt
        links_dict[key] = linktxt
    print links_dict
    
    new_instance = Ulnew.objects.get_or_create (
                                         title= title
              

                                        )[0]
    new_instance.category = category                                    
    new_instance.description = description
    new_instance.rg= links_dict['rg']
    new_instance.ul = links_dict['ul']
    new_instance.up = links_dict['up']
    new_instance.save()
    print 'ok'   
    
class PostObject(Thread):
    def __init__(self,sitedict,entry_id_lists):
        Thread.__init__(self)
        self._stop = threading.Event()
        self.stop = False
        thongbao.thongbao = " da tao object post"
        self.postlog = ""
        self.session = requests.session()
        self.khoitaohtml()
        self.login_flag = 1
        self.sitedict = sitedict
        self.entry_id_lists = entry_id_lists
        self.save_post_log_path = '/post_log_' + sitedict['url'].replace('www.','').replace('http://.','').replace('/.','') + '.html'
        self.sitename = sitedict['url'].replace('www.','').replace('http://.','').replace('/.','') 
        try:
            self.is_reply = sitedict['is_reply']
        except:
            self.is_reply = False
        self.replyWithEnry = False
        if self.is_reply :
            self.newthread_url = sitedict['url_thread_for_reply'] # for find token
            #self.url_reply = sitedict['url_reply']
            if 'showthread' in self.newthread_url:
                self.loai_forum = 0
                self.url_reply=self.newthread_url.replace('showthread.php?','newreply.php?do=postreply&')
                #in 'http://amaderforum.com/showthread.php?t=4681089'
                #'url_reply':'http://amaderforum.com/newreply.php?do=postreply&t=4681089'
        else:
            self.newthread_url = sitedict['newthread_url']
            if 'newthread.php?do' in self.newthread_url:
                self.loai_forum = 0
    def stop(self):
        self._stop.set()
        self.stop = True
    def stopped(self):
        return self._stop.isSet()
    
    def run(self):
        print 'vao ct post'
        self.siteobj = ForumTable.objects.get(url = self.sitedict['url'])
        print self.siteobj
        self.url = self.siteobj.url
        self.uname = self.siteobj.uname
        self.passwd = self.siteobj.passwd
        self.sleep_time = 60
        self.numer_entry_post = 'chua post bai nao'
        thongbao.thongbao = 'Start post'
        self.stop = False
        print thongbao.thongbao
        self.admin_instance = AdminUl.objects.get(id=1)
        if self.is_reply and not self.replyWithEnry:
            so_bai_se_post =100
        elif self.entry_id_lists ==['all']:
            print 'ban se post all'
            entry_list = Ulnew.objects.all().order_by('-id')
            so_bai_se_post = len (entry_list)
            post_all = True
        else:
            so_bai_se_post = len (self.entry_id_lists)
            print 'so_bai_se_post',so_bai_se_post
            print 'entry_id_lists',self.entry_id_lists
            post_all = False
        count = 0
        while count < so_bai_se_post:
            
            if not self.is_reply or  self.replyWithEnry:
                if post_all:
                    print 'in loop post all'
                    last_Ulnew = entry_list[count]
                else:
                    entry_id =  self.entry_id_lists[count]
                    last_Ulnew = Ulnew.objects.get(id = entry_id )
                try:
                    lenMyUl = len(last_Ulnew.myul)
                except:
                    lenMyUl = 0
                count = count + 1
                if  post_all and lenMyUl <5 :
                    print 'entry nay chua co myul'
                    continue
                self.entry = last_Ulnew
                category = last_Ulnew.category.capitalize()
                print 'category', [category]
                if self.is_reply:
                    pass
                    
                elif category==u'Music':
                    self.newthread_url = self.siteobj.music
                elif 'TV Show' in category:
                    print 'cate la TV show'
                    self.newthread_url = self.siteobj.tv_show
                    print 'self.newthread_url' ,self.newthread_url
                elif 'Movie' in category:
                    print 'cate la Movie'
                    self.newthread_url = self.siteobj.movie
                    print 'self.newthread_url' ,self.newthread_url
                else:
                    print 'chua co category de post bai'   
                    continue
                try:
                    entry_da_post = Ulnew.objects.get(forumback=self.siteobj,postLog__Ulnew=last_Ulnew)
                    print 'topic %s  post roi' %entry_da_post
                    continue
                except:
                    pass
                self.numer_entry_post = 'bai so' + str(count + 1) + ' '
                if self.stop:
                    thongbao.thongbao = "stop post"
                    print thongbao.thongbao
                    break
                self.title  = last_Ulnew.title.decode('utf-8')
                print 'sap post bai',self.title
                self.content = last_Ulnew.description.decode('utf-8')
                dllink=''
                admin_instance = self.admin_instance
                link_dict = {}
                rg_order = admin_instance.rg_order
                ul_order = admin_instance.ul_order
                up_order = admin_instance.up_order
                if  last_Ulnew.myrg:
                    rg_link =   '\n[code]' + last_Ulnew.myrg + '[/code]\n'
                    link_dict[rg_order] = rg_link
                elif admin_instance.show_not_my_link and last_Ulnew.rg:
                    rg_link =   '\n[code]' + last_Ulnew.rg + '[/code]\n'
                    link_dict[rg_order] = rg_link
                if  last_Ulnew.myul:
                    ul_link =   '\n[code]' + last_Ulnew.myul + '[/code]\n'
                    link_dict[ul_order] = ul_link
                elif admin_instance.show_not_my_link and last_Ulnew.ul:
                    ul_link =   '\n[code]' + last_Ulnew.ul + '[/code]\n'
                    link_dict[ul_order] = ul_link
                if  last_Ulnew.myup:
                    up_link =   '\n[code]' + last_Ulnew.myup + '[/code]\n'
                    link_dict[up_order] = up_link
                elif admin_instance.show_not_my_link and last_Ulnew.up:
                    up_link =   '\n[code]' + last_Ulnew.up + '[/code]\n'
                    link_dict[up_order] = up_link
                od = collections.OrderedDict(sorted(link_dict.items()))  
                for k, v in od.iteritems():
                    dllink = dllink + v
                self.content = self.content + dllink
                not_allowed_post_link = 0
                if not_allowed_post_link:
                    p = re.compile( 'http://.*?\s',re.DOTALL)
                    self.content = p.sub( '', self.content)
                print self.content
            
            if self.login_flag :
                self.login()
                self.login_flag = 0
            self.findtoken()
            print 'self.stop',self.stop
            
            try:
                if not self.stop:
                    self.post()
            except:
                pass
            
            print ' ( so bai da post)',count
            sleeptime = self.sleep_time + randint(10, 20)
            if (count != so_bai_se_post) and not self.stop:
                print '\nwait %s s' % sleeptime
                loopcount = 0
                while loopcount< 10 and not self.stop:
                    loopcount +=1
                    sleep(sleeptime/10 )
            else:
                print 'het bai stop post'
    def khoitaohtml(self):
        self.session.headers = {'Accept' :   'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':    'gzip, deflate',
'Accept-Language'  :  'en-US,en;q=0.5',
'Cache-Control'  :  'no-cache',
'Connection'  :  'keep-alive',
'Content-Type'  :  'application/x-www-form-urlencoded; charset=UTF-8',
'Pragma'   : 'no-cache',
'User-Agent'    :'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
'X-Requested-With'    :'XMLHttpRequest',}
    def login(self):
        print self.sitename,'dau cua function login'
        if self.loai_forum == 0:
            loginurl = self.url + 'login.php?do=login'
            md5 = hashlib.md5(self.passwd);md5 = md5.hexdigest()
            opts = {
            'vb_login_md5password': md5,
            'vb_login_md5password_utf': md5,
            'vb_login_username': self.uname,
            'do': 'login',
            }
            #data = urllib.urlencode(opts)   
            #response=self.opener.open(loginurl, data)
        count_repost = 0
        while count_repost < 10:
            try:
                r = self.session.post(loginurl, data=opts)
                #print r.cookies
                self.postlog = "Yes....login ok"
                thongbao.thongbao = "Login thanh cong..."
                #self.postlog = login_ct
                print self.sitename , '***login thanh cong***'
                login_ct = r.content 
                with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
                    f.write(login_ct)
                break
            except:
                thongbao.thongbao = " loi HTTP please wait for post again"
                sleep(15)
                count_repost += 1
                
            
            #print 'r.text',r.text
            #print 'r.header',r.headers
            #print 'self.session',self.session.headers
            
    def findtoken(self):
        #response2=self.opener.open(self.newthread_url)
        #token = response2.read()
        count_repost = 0
        while count_repost < 10 and not self.stop:
            print self.sitename,'find token lan thu ',count_repost+1
            #print self.sitename,'newthread url',self.newthread_url
            try:
                r = self.session.get(self.newthread_url)
                token = r.content
                self.security_token =re.findall('name="securitytoken" value="(.*?)"', token)[0]
                thongbao.thongbao = self.security_token
                print self.sitename,self.security_token
                break
            except Exception as e:
                thongbao.thongbao = " loi HTTP please wait for post again" + u'{0}'.format(type(e)) +  u'{0}'.format(e)
                print thongbao.thongbao
                sleep(15)
                count_repost += 1
                
            
            
            
        
        #with open(MEDIA_ROOT +'/token_log.html', 'wb') as f:
                #f.write(token)
        
    def post (self):
        count_repost = 0
        print self.sitename, 'trong ham post'
        
        
        print self.sitename, 'count_repost',count_repost
        if self.is_reply:
            url_post = self.url_reply
            if self.replyWithEnry:
                message = self.content.encode('cp1252')
            else:
                message = 'thank you very much ' + '[color=white]' + str(randint(0, 10000)) + '[/color]'
            posts = {
                #'subject': self.title.encode('cp1252'),
                'message': message,
                'securitytoken': self.security_token,
                'newthread_agree':'True',
                'do':'postreply',
                'prefixid':'UL'
                }
        else:
            print 'chuan bi du lien'
            url_post = self.newthread_url
            print 'url_post',url_post
            posts = {
                'subject': self.title.encode('cp1252'),
                'message': self.content.encode('cp1252'),
                'securitytoken': self.security_token,
                'newthread_agree':'True',
                'do':'postthread',
                'prefixid':'UL'
                }
            print' chuan bi xong du lieu'
        while count_repost < 10:
            print self.sitename,'count_repost in while',count_repost
            try:
                print self.sitename,'chuan bi submit...'
                r = self.session.post(url_post, data=posts)
                print self.sitename,'da submit'
                ct = r.content
                self.postlog = "Yes....post ok"
                trave_add = r.url
                if trave_add == url_post:
                        print 'send request nhung bi loi' ,trave_add
                        thongbao.thongbao = "post loi do time"
                        print ct
                        with open(MEDIA_ROOT +'/post_log.html', 'wb') as f:
                            f.write(ct)
                        print 'da save postlog vao disk'
                else:
                        print 'post ok ',trave_add
                        thongbao.thongbao = "post thanh cong " + trave_add
                        try:
                            PostLog.objects.get_or_create(forum = self.siteobj,Ulnew = self.entry,pested_link=trave_add)
                        except:
                            PostLog.objects.get_or_create(forum = self.siteobj,Ulnew = self.entry,pested_link='post ok roi')
                        '''
                        
                        postedUlDatabaseEntry = UlDaPost.objects.get_or_create(title = self.title)
                        PostLogDaPost.objects.get_or_create(forum = self.siteobj,UlDaPost = postedUlDatabaseEntry,posted_link=trave_add)
                        '''
                break
            except Exception as e:
                print ' co loi khi submit ',type(e),e
                thongbao.thongbao = " loi HTTP please wait for post again"
                sleep(15)
                count_repost += 1 
        
        


    
class importUL(object):
    def __init__(self,imported_link):
        self.imported_link = imported_link
        
    def create_openner(self):
        print 'ban dang import vao ul'
        self.session = requests.session()
        self.session.headers = {
         'Accept':    'text/javascript, text/html, application/xml, text/xml, */*',
'Accept-Encoding'  :  'gzip, deflate',
'Accept-Language'   : 'en-US,en;q=0.5',
'Cache-Control'   :'no-cache',
'Connection'   : 'keep-alive',
'Content-Length' :   '0',
'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8',
'Host'   : 'uploaded.net',
'Pragma'  :  'no-cache',
'Referer'  :  'http://uploaded.net/upload',
'User-Agent' :   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
'X-Prototype-Version' :   '1.6.1',
'X-Requested-With'  :  'XMLHttpRequest'}
        #print self.session .headers
    def uploaded_to_login(self):
        
        loginurl = 'http://uploaded.net/io/login'
        opts = {
        'id': '7397033',
        'pw': 'Tu228787',
        
        }
        r = self.session.post(loginurl, data=opts)
        login_ul = r.content
        print 'url dirrect',r.url
        print 'after login reposnse header',r.headers
        self.postlog = "Yes....login ok"
        thongbao.thongbao = "Login thanh cong..."
        print 'login thanh cong gia tri tra ve\n', 
        with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
            f.write(login_ul)
    def import_link_submit(self):
        
        #importULlink ='http://uploaded.net/file/a8mdgmvf/VA_-_Magic_Mike_XXL_(Soundtrack)_(2015).rar'

        loginurl = 'http://uploaded.net/io/import'
        opts = {
        'urls': self.imported_link,
        }
        #data = urllib.urlencode(opts)
        #print data  
        #response=self.opener.open(loginurl, data)
        r = self.session.post(loginurl, data=opts)
        #ct = u'{0}'.format(r.text)
        ct =r.text
        print 'after post reposnse ',ct
        print 'type of ct',type(ct)
        return ct
        self.postlog = "Yes....post ok"
        thongbao.thongbao = "post thanh cong..."
        print '%s %post thanh cong ' ,ct
        with open(MEDIA_ROOT +'/login_post.html', 'wb') as f:
            f.write(ct)          
    def import_to_ul(self):
        self.create_openner()
        self.uploaded_to_login()  
        ct = self.import_link_submit()
        return ct            
           
class CountTest():
    def __init__(self):
        
        self.first_note = 'this is first note'
        print_output = 0
        print 'countest'
        self.print_output = 0
    def dem(self):
        while 1:
            sleep(0.2)
            self.print_output += 1
            print 'gia tri in ra cua Countest',self.print_output
                   
        
class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
kho = {'url':'http://1kho.com/',
          'uname':'cuchladoda',
          'passwd':'228787',
          'newthread_url':'http://1kho.com/newthread.php?do=newthread&f=57',
          'movie':'http://1kho.com/newthread.php?do=newthread&f=57',
          }
amaderforum = {'url':'http://amaderforum.com/',
        'is_reply':True,
       'uname':'dicochno5',
       'passwd':'228787',
       'url_thread_for_reply':'http://amaderforum.com/showthread.php?t=4682391',
       #'url_reply':'http://amaderforum.com/newreply.php?do=postreply&t=4681089',#
       'newthread_url':'http://amaderforum.com/newthread.php?do=newthread&f=21',
       'music':'http://amaderforum.com/newthread.php?do=newthread&f=21',
       'tv_show':'http://amaderforum.com/newthread.php?do=newthread&f=13',
       'movie':'http://amaderforum.com/newthread.php?do=newthread&f=8',
       }
shaanig = {'url':'http://www.shaanig.com/',
       'uname':'mothtrdo5',
       'passwd':'228787',
       'newthread_url':'http://www.shaanig.com/newthread.php?do=newthread&f=68',
       'music':'http://www.shaanig.com/newthread.php?do=newthread&f=68',
       'tv_show':'http://www.shaanig.com/newthread.php?do=newthread&f=8',
       'movie':'http://www.shaanig.com/newthread.php?do=newthread&f=9',
       'HDmovie':'http://www.shaanig.com/newthread.php?do=newthread&f=60',
       'software':'http://www.shaanig.com/newthread.php?do=newthread&f=76',
       'game':'http://www.shaanig.com/newthread.php?do=newthread&f=77',
       'anime':'http://www.shaanig.com/newthread.php?do=newthread&f=5',
       'mobile':'http://www.shaanig.com/newthread.php?do=newthread&f=88',
       'ebook':'http://www.shaanig.com/newthread.php?do=newthread&f=87',
       }
forumwizard = {'url':'https://forumwizard.net/',
       'uname':'rimogiha',
       'passwd':'228787',
       'newthread_url':'https://forumwizard.net/newthread.php?do=newthread&f=25',
        'movie':'https://forumwizard.net/newthread.php?do=newthread&f=25',
       }
final4ever = {'url':'http://final4ever.com/',
       'uname':'mothtrdo1',
       'passwd':'228787',
       'newthread_url':'http://final4ever.com/newthread.php?do=newthread&f=25',
        'movie':'http://final4ever.com/newthread.php?do=newthread&f=25',
       }
expresshare = {'url':'http://www.expresshare.com/',
       'uname':'mothtrdo',
       'passwd':'228787',
       'newthread_url':'http://www.expresshare.com/newthread.php?do=newthread&f=9',
       'movie':'http://www.expresshare.com/newthread.php?do=newthread&f=9',
       }
majaa = {'url':'http://www.majaa.net/',
       'uname':'mothtrdo5',
       'passwd':'228787',
       'newthread_url':'http://www.majaa.net/newthread.php?do=newthread&f=188',
       'movie':'http://www.majaa.net/newthread.php?do=newthread&f=188',

       }

danhsachforum = [kho,amaderforum,shaanig,expresshare,majaa,forumwizard,final4ever]
def get_entry_link(topiclink):
    html = get_html (topiclink)
    soup = BeautifulSoup(html)
    class_entry_name = 'h2'+'.entry-title'
    entries = soup.select(class_entry_name)
    print entries
    entry_lists = []
    for entry in entries:
        atag =  entry.find('a')
        ahref =atag.get('href')
        title = u'{0}'.format(atag.string)
        print ahref
        entry_lists.append((ahref,title))
    return entry_lists
    #category =  u'{0}'.format(category)
    #print category
def get_entry_link_freedl2u(topiclink):
    html = get_html (topiclink)
    soup = BeautifulSoup(html)
    class_entry_name = 'div'+'.lcol.argcat'
    entries = soup.select(class_entry_name)
    print entries
    print 'len of entries',len(entries)
    entry_lists = []
    for entry in entries:
        atag =  entry.find('a')
        ahref =atag.get('href')
        title = u'{0}'.format(atag.string)
        print ahref
        print'title',title
        entry_lists.append((ahref,title))
    return entry_lists
    #category =  u'{0}'.format(category)
    #print category
def get_link_from_db():
    ul_text = ""
    linhkien_lists = Ulnew.objects.exclude(myul__icontains='http').filter(ul__icontains='http')
    ullink = linhkien_lists.values_list('ul')
    for tuplelink in ullink:
        #print tuplelink
        ul_text = ul_text + tuplelink[0]
    thongbao.thongbao = ul_text
    print ul_text
    return ul_text
def import_ul_txt_to_myul (ullink):
    importULObject = importUL(ullink)
    json_import_ul_txt = importULObject.import_to_ul()
    myUlTxt = convert_jsonUl_to_txt (json_import_ul_txt)
    thongbao.log = myUlTxt
    update_my_ul_link_to_db (myUlTxt)
def get_name_of_link(link):
    back_flash_i = link.rfind('/')
    nameoflink = link[back_flash_i+1:]
    return nameoflink
    

def update_my_ul_link_to_db(ullink_txt):
    entry_dbs = Ulnew.objects.exclude(myul__icontains='http').filter(ul__icontains='http')#
    #entry_dbs = Ulnew.objects.all()
    #for entry_db in entry_dbs:
    
    my_uls = ullink_txt.split('\n')
    print 'so file input',len(my_uls)
    for entry_db in entry_dbs:
        print entry_db.title
        leech_ul_text = entry_db.ul
        leech_uls = leech_ul_text.split('\n')
        my_ul_this_entry = ''
        for leech_ullink in leech_uls:
            if len(leech_ullink)<2:
                continue
            nameof_leech_link = get_name_of_link(leech_ullink)
            for myUl in my_uls:
                myUl = urllib.unquote(myUl).decode('utf-8')
                my_ul_one_entry_name =  get_name_of_link (myUl)
                if my_ul_one_entry_name in nameof_leech_link:
                    my_ul_this_entry = my_ul_this_entry + myUl+ '\n'
            print 'my_ul_one_entry',my_ul_this_entry
            try:
                entry_db.myul = my_ul_this_entry
                entry_db.save()
            except Exception as e:
                print 'luu myul nhung bi loi nay',e 
                print 'my ul muon luu ma khong duoc la', my_ul_this_entry
    print 'da thay the my ul xong xui'
import json    # or `import simplejson as json` if on Python < 2.6
                
def json_to_dict(json_string):
    #json_string = u'{ "id":"123456789", ... }'
    obj = json.loads(json_string)
    return obj
def list_to_text (imput_list):
    text =''
    for x in imput_list:
        text = text + x +'\n'
    return text         
def create_admin_ul():
    new_instance = AdminUl.objects.get_or_create (id= 1)[0]
    new_instance.show_not_my_link  = False
    new_instance.save()
def createForumTable(**kwarg):
    new_instance = ForumTable.objects.get_or_create (url= kwarg['url'])[0]
    new_instance.uname = kwarg['uname']
    new_instance.passwd = kwarg['passwd'] 
    new_instance.newthread_url = kwarg['newthread_url'] 
    try:
        new_instance.music = kwarg['music']
    except:
        pass 
    try:
        new_instance.tv_show = kwarg['tv_show']
    except:
        pass 
    try:
        new_instance.movie = kwarg['movie']
    except:
        pass 
    try:
        new_instance.HDmovie = kwarg['HDmovie']
    except:
        pass 
    try:
        new_instance.software = kwarg['software']
    except:
        pass 
    try:
        new_instance.game = kwarg['game']
    except:
        pass 
    try:
        new_instance.anime = kwarg['anime']
    except:
        pass 
    try:
        new_instance.mobile = kwarg['mobile']
    except:
        pass  
    try:
        new_instance.ebook = kwarg['ebook']
    except:
        pass 
    new_instance.save()
    print "da insert forum to  table"
lastestmovie = {'url':'http://lastestmovie.com',
       'music':'http://lastestmovie.com/category/music/',
       'tv_show':'http://lastestmovie.com/category/tv-show/',
       'movie':'http://lastestmovie.com/category/movie/',
       'HDmovie':'http://lastestmovie.com/category/hd-720p-to-1080p-movie/',
       'software':'http://lastestmovie.com/category/applications/',
       'game':'',
       'anime':'',
       'mobile':'',
       'ebook':'',
       }
tinydl = {'url':'http://tinydl.com/',
       'music':'http://tinydl.com/music',
       'tv_show':'http://tinydl.com/tv-shows',
       'movie':'http://tinydl.com/movies',
       'HDmovie':'',
       'software':'http://tinydl.com/applications',
       'game':'',
       'anime':'',
       'mobile':'',
       'ebook':'',
       }
freedl2u = {'url':'http://freedl2u.co/',
       'music':'http://freedl2u.co/movies/',
       'tv_show':'http://freedl2u.co/movies/',
       'movie':'http://freedl2u.co/movies/',
       'HDmovie':'',
       'software':'http://freedl2u.co/movies/',
       'game':'',
       'anime':'',
       'mobile':'',
       'ebook':'',
       }
danhsachLeechSite=[lastestmovie,freedl2u]
def createLeechSiteTable(kwarg):
    new_instance = LeechSite.objects.get_or_create (url= kwarg['url'])[0]
    try:
        new_instance.music = kwarg['music']
    except:
        pass 
    try:
        new_instance.tv_show = kwarg['tv_show']
    except:
        pass 
    try:
        new_instance.movie = kwarg['movie']
    except:
        pass 
    try:
        new_instance.HDmovie = kwarg['HDmovie']
    except:
        pass 
    try:
        new_instance.software = kwarg['software']
    except:
        pass 
    try:
        new_instance.game = kwarg['game']
    except:
        pass 
    try:
        new_instance.anime = kwarg['anime']
    except:
        pass 
    try:
        new_instance.mobile = kwarg['mobile']
    except:
        pass  
    try:
        new_instance.ebook = kwarg['ebook']
    except:
        pass 
    new_instance.save()
    print "da insert forum to  table"
def convert_jsonUl_to_txt(json_string):
    #json_string = '[' + json_string + ']'
    json_string = '[' + json_string[:-1] + ']'
    #replacement = {u'{auth:':u'{"auth":',u',newAuth:':u',"newAuth":' , u',filename:':u',"filename":' , u',size:':u',"size":',u',err:':u',"err":'}
    replacement = {'{auth:':'{"auth":',',newAuth:':',"newAuth":' , ',filename:':',"filename":' , ',size:':',"size":',',err:':',"err":'}

    for key, value in replacement.iteritems():
        json_string = json_string.replace(key, value)
    print 'json_string',json_string
    print 'type json_string',type (json_string)
    return_dict = json.loads(json_string)
    print 'return_dict fo json',return_dict
    return_list = []
    for x in return_dict:
        one_return_ul = ''
        if 'err' in x:
            continue
        else:
            #size = x['size']
            newAuth = x['newAuth']
            filename = x['filename']
            one_return_ul = 'http://uploaded.net/file/'+ newAuth + '/' + filename
            print 'one_return_ul',one_return_ul
            return_list.append(one_return_ul)
    txt = list_to_text(return_list)
    return txt
def leech_bai(cate_page,begin_page,end_page):
    #cate_page= 'http://lastestmovie.com/category/tv-show/'
    #cate_page= 'http://lastestmovie.com/category/movie/'
    if 'lastestmovie.com' in cate_page:
        
        for page_num in range(begin_page,end_page):
            page_url = cate_page + 'page/' + str(page_num) + '/'
            entry_lists = get_entry_link(page_url)
            print entry_lists
            print 'so topic trong trang se leech nay',len(entry_lists)
            for ahref_title in entry_lists:
                leech_one_entry_latin1 (ahref_title)
    elif 'freedl2u.co' in cate_page:
        for page_num in range(begin_page,end_page):
            page_url = cate_page + 'page/' + str(page_num) + '/'
            entry_lists = get_entry_link_freedl2u(page_url)
            print entry_lists
            print 'so topic trong trang se leech nay',len(entry_lists)
            for ahref_title in entry_lists:
                leech_one_entry_freedl2u (ahref_title)
        
def init_d4():
    
    for forum in danhsachforum:
        createForumTable(**forum)
    for site in danhsachLeechSite:
        createLeechSiteTable(site)
    create_admin_ul()
def Postfunction(sitedict):
    sitename = sitedict['url']
    count = 0
    while 1:
        if count ==30:
            sys.exit()
        count +=1
        print sitename ,count ,'\n'
        sleep(0.1) 
if __name__ == '__main__':
    #leech_bai('http://freedl2u.co/movies/', 1, 2)
    #txt = get_link_from_db()
    #import_ul_txt_to_myul(txt)
    #Postfunction(shaanig)
    '''
    postdict[amaderforum['url']] = PostObject(amaderforum,['all'])
    postdict[shaanig['url']] = PostObject(shaanig,['all'])
    postdict[shaanig['url']].start()
    postdict[amaderforum['url']].start()
    sleep(20)
    
    postdict[amaderforum['url']].stop()
    '''
    postdict[shaanig['url']] = PostObject(shaanig,['all'])
    postdict[shaanig['url']].start()
    #newpost = PostObject(amaderforum,['all'])
    #newpost.start()