# -*- coding: utf-8 -*-

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
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
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
from bs4 import BeautifulSoup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.models import Ulnew   , AdminUl, ForumTable, PostLog, UlDaPost,\
    PostLogDaPost
def leech_one_entry (entry_url):
    html = get_html (entry_url)
    soup = BeautifulSoup(html)
    class_entry_name = 'div.'+'entry-content'
    category = soup.select('section.entry-category')[0].find('a').string
    category =  u'{0}'.format(category)
    print category
    print 'type(category)',type(category)
    quotes_wrappers = soup.select(class_entry_name)[0]
    noidung =  u'{0}'.format(quotes_wrappers)
    print 'type of entry-title' ,type(quotes_wrappers)
    titlea = quotes_wrappers.find('h1', attrs={'class': 'entry-title'}).string
    print 'type of titlea',type(titlea)
    titlea =  u'{0}'.format(titlea)
    #titlea = titlea.replace(u'–', u'-')
    print 'title' , titlea

    print '#########'

    parser = HTML2BBCode()
    bbcode = parser.feed(noidung)
    bbcode = bbcode.encode('utf-8')
    p = re.compile( '\s*Posted on.*?(?P<caiquaigi>\[img\])',re.DOTALL)
    bbcode = p.sub( '\g<caiquaigi>', bbcode)
    prefix_links = ['http://rapidgator.net/file/','http://uploaded.net/file/','http://www.uploadable.ch/file/']
    stuff = map(lambda w: bbcode.find(w) , prefix_links)
    print stuff
    min_index_bbcode_host =  min(i for i in stuff if i > 0)
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

def leech_one_entry_latin1 (ahref_title):
    entry_url = ahref_title[0]
    title = ahref_title[1]
    if Ulnew.objects.filter(title=title).exists():
        print 'entry nay da ton tai %s'%title
        return ''
    html = get_html (entry_url)
    soup = BeautifulSoup(html)
    class_entry_name = 'div.'+'entry-content'
    category = soup.select('section.entry-category')[0].find('a').string
    category =  repr(category.string)
    print category
    print 'type(category)',type(category)
    quotes_wrappers = soup.select(class_entry_name)[0]
    noidung =  repr(quotes_wrappers).encode('utf-8')
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
    prefix_links = ['http://rapidgator.net/file/','http://uploaded.net/file/','http://www.uploadable.ch/file/']
    stuff = map(lambda w: bbcode.find(w) , prefix_links)
    print stuff
    min_index_bbcode_host =  min(i for i in stuff if i > 0)
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
class PostObject():
    def __init__(self):
        self.posting_flag = False
        self.stop = False
        self.thongbao = " da tao object post"
        self.postlog = ""
        self.session = requests.session()
        #self.session.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}) 
        '''
        self.session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}
    '''
        '''
        self.session.headers = {
         'Accept':    'text/javascript, text/html, application/xml, text/xml, */*',
'Accept-Encoding'  :  'gzip, deflate',
'Accept-Language'   : 'en-US,en;q=0.5',
'Cache-Control'   :'no-cache',
'Connection'   : 'keep-alive',
'Content-Length' :   '0',

'Host'   : 'uploaded.net',
'Pragma'  :  'no-cache',
'Referer'  :  'http://uploaded.net/upload',
'User-Agent' :   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
'X-Prototype-Version' :   '1.6.1',
'X-Requested-With'  :  'XMLHttpRequest'}'''
        
        self.khoitaohtml()
        self.login_flag = 1
    def post_entry(self,sitedict,entry_id_lists):
        print 'vao ct post'
        self.siteobj = ForumTable.objects.get(url = sitedict['url'])
        print self.siteobj
        self.url = self.siteobj.url
        self.uname = self.siteobj.uname
        self.passwd = self.siteobj.passwd
        #self.newthread_url = self.siteobj.newthread_url
        self.loai_forum = 0
        self.sleep_time = 60
        self.numer_entry_post = 'chua post bai nao'
        self.thongbao = 'Start post'
        self.stop = False
        print self.thongbao
        if entry_id_lists ==['all']:
            entry_list = Ulnew.objects.all().order_by('-id')
            so_bai_se_post = len (entry_list)
            
            post_all = True
        else:
            so_bai_se_post = len (entry_id_lists)
            print 'so_bai_se_post',so_bai_se_post
            print 'entry_id_lists',entry_id_lists
            post_all = False
        count = 0
        while count < so_bai_se_post:
            if post_all:
                last_Ulnew = entry_list[count]
            else:
                entry_id =  entry_id_lists[count]
                last_Ulnew = Ulnew.objects.get(id = entry_id )
            count = count + 1
            self.entry = last_Ulnew
            category = last_Ulnew.category
            print 'category', [category]
            if category==u'Music':
                self.newthread_url = self.siteobj.music
            if 'TV Show' in category:
                print 'cate la TV show'
                self.newthread_url = self.siteobj.tv_show
                
                print 'self.newthread_url' ,self.newthread_url
            else:
                print 'chua co category de post bai'   
            
            
            try:
                entry_da_post = Ulnew.objects.get(forumback=self.siteobj,postLog__Ulnew=last_Ulnew)
                print 'topic %s  post roi' %entry_da_post
                continue
            except:
                pass
            self.numer_entry_post = 'bai so' + str(count + 1) + ' '
            if self.stop:
                self.thongbao = "stop post"
                print self.thongbao
                break
            self.posting_flag = True
            self.title  = last_Ulnew.title.decode('utf-8')
            print 'sap post bai',self.title
            self.content = last_Ulnew.description.decode('utf-8')
            dllink=''
            admin_instance = AdminUl.objects.get(id=1)
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
            try:
                
                if not self.stop:
                    self.post()
            except:
                pass
            
            
            if (count < so_bai_se_post -1) and not self.stop:
                self.thongbao += '\nwait %s s' % self.sleep_time
                print self.thongbao 
                loopcount = 0
                while loopcount< 10 and not self.stop:
                    loopcount +=1
                    sleep(self.sleep_time/10 )
            else:
                print 'het bai stop post'
        self.posting_flag = False
    def khoitaohtml(self):
        '''
        jar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        #self.opener.addheaders = [("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")]
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        '''
        self.session.headers = {'Accept' :   'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':    'gzip, deflate',
'Accept-Language'  :  'en-US,en;q=0.5',
'Cache-Control'  :  'no-cache',
'Connection'  :  'keep-alive',
'Content-Type'  :  'application/x-www-form-urlencoded; charset=UTF-8',
'Pragma'   : 'no-cache',
'User-Agent'    :'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
'X-Requested-With'    :'XMLHttpRequest',}
        #print self.session.headers
    def login(self):
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
            r = self.session.post(loginurl, data=opts)
            #print 'r.text',r.text
            #print 'r.header',r.headers
            #print 'self.session',self.session.headers
            #login_ct = r.content
            print r.cookies
            
            self.postlog = "Yes....login ok"
            self.thongbao = "Login thanh cong..."
            #self.postlog = login_ct
            print '%s %slogin thanh cong' 
            #with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
                #f.write(login_ct)
    def findtoken(self):
        #response2=self.opener.open(self.newthread_url)
        #token = response2.read()
        r = self.session.get(self.newthread_url)
        token = r.content
        with open(MEDIA_ROOT +'/token_log.html', 'wb') as f:
                f.write(token)
        self.security_token=re.findall('name="securitytoken" value="(.*?)"', token)[0]
        self.thongbao = self.security_token
        print self.security_token
    def post (self):
        posts = {
                'subject': self.title.encode('cp1252'),
                'message': self.content.encode('cp1252'),
                'securitytoken': self.security_token,
                'newthread_agree':'True',
                'do':'postthread',
                }
        #print 'posts',posts
        #data = urllib.urlencode(posts)
        #print 'data',data
        #response2=self.opener.open(self.newthread_url,data)
        #ct = response2.read()
        
        #print posts['message']
        r = self.session.post(self.newthread_url, data=posts)
        
        ct = r.content
        #print 'r.headers póting',r.headers
        self.postlog = "Yes....post ok"
        
        #self.postlog = ct
        
        trave_add = r.url
        with open(MEDIA_ROOT +'/post_log.html', 'wb') as f:
                f.write(ct) 
        if trave_add == self.newthread_url:
                print 'send request nhung bi loi' ,trave_add
                self.thongbao = "post loi do time"
        else:
                ''
                print 'post ok ',trave_add
                self.thongbao = "post thanh cong" + trave_add
                '''
                
                postedUlDatabaseEntry = UlDaPost.objects.get_or_create(title = self.title)
                PostLogDaPost.objects.get_or_create(forum = self.siteobj,UlDaPost = postedUlDatabaseEntry,posted_link=trave_add)
                '''
        PostLog.objects.get_or_create(forum = self.siteobj,Ulnew = self.entry,pested_link=trave_add)
class importUL(object):
    def __init__(self,imported_link):
        self.imported_link = imported_link
        
    def create_openner(self):
        #jar = cookielib.CookieJar()
        #self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        #self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #self.opener.addheaders.append(("Content-Type", "application/x-www-form-urlencoded"))
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
        print self.session .headers
    def uploaded_to_login(self):
        
        loginurl = 'http://uploaded.net/io/login'
        opts = {
        'id': '7397033',
        'pw': 'Tu228787',
        
        }
        r = self.session.post(loginurl, data=opts)
        login_ct = r.content
        print 'url dirrect',r.url
        print 'after login reposnse header',r.headers
        self.postlog = "Yes....login ok"
        self.thongbao = "Login thanh cong..."
        print 'login thanh cong gia tri tra ve\n', 
        with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
            f.write(login_ct)
    def import_link_submit(self):
        
        #importULlink ='http://uploaded.net/file/a8mdgmvf/VA_-_Magic_Mike_XXL_(Soundtrack)_(2015).rar'

        loginurl = 'http://uploaded.net/io/import'
        opts = {
        'urls': self.imported_link,
        }
        #data = urllib.urlencode(opts)
        #print data  
        #response=self.opener.open(loginurl, data)
        #login_ct = response.read()
        r = self.session.post(loginurl, data=opts)
        #ct = u'{0}'.format(r.text)
        ct =r.text
        print 'after post reposnse ',ct
        print 'type of ct',type(ct)
        return ct
        self.postlog = "Yes....post ok"
        self.thongbao = "post thanh cong..."
        #self.postlog = login_ct
        print '%s %post thanh cong ' ,ct
        with open(MEDIA_ROOT +'/login_post.html', 'wb') as f:
            f.write(ct)          
    def import_to_ul(self):
        self.create_openner()
        self.uploaded_to_login()  
        ct = self.import_link_submit()
        return ct            
class PostObject1():
    def __init__(self):
        self.posting_flag = False
        self.stop = False
        self.thongbao = " da tao object post"
        self.postlog = ""
        self.khoitaohtml()
        self.login_flag = 1

    
    def post_entry(self,sitedict,entry_id_lists):
        print 'vao ct post'
        self.siteobj = ForumTable.objects.get(url = sitedict['url'])
        print self.siteobj
        self.url = self.siteobj.url
        self.uname = self.siteobj.uname
        self.passwd = self.siteobj.passwd
        self.newthread_url = self.siteobj.newthread_url
        self.loai_forum = 0
        self.sleep_time = 60
        self.numer_entry_post = 'chua post bai nao'
        self.thongbao = 'Start post'
        self.stop = False
        print self.thongbao
        entry_list = Ulnew.objects.all().order_by('id')
        count = 0
        while count < len(entry_list):
            last_Ulnew = entry_list[count]
            count = count + 1
            self.entry = last_Ulnew
            try:
                entry = Ulnew.objects.get(forumback=self.siteobj,postLog__Ulnew=last_Ulnew)
                print 'topic %s  post roi' %entry
                continue
            except:
                pass
            self.numer_entry_post = 'bai so' + str(count + 1) + ' '
            if self.stop:
                self.thongbao = "stop post"
                print self.thongbao
                break
            self.posting_flag = True
            #last_Ulnew = Ulnew.objects.get(id = entry_id)
            self.title  = last_Ulnew.title.encode('utf-8')
            self.content = last_Ulnew.description

            dllink=''
            admin_instance = AdminUl.objects.get(id=1)
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
            #self.content = self.content.replace('[code]','').replace('[/code]','')
            self.content =self.content.encode('utf-8')
            not_allowed_post_link = 0
            if not_allowed_post_link:
                p = re.compile( 'http://.*?\s',re.DOTALL)
                self.content = p.sub( '', self.content)
            
            print self.content
            if self.login_flag :
                self.login()
                self.login_flag = 0
            self.findtoken()
            try:
                
                if not self.stop:
                    self.post()
            except:
                pass
            
            
            if (count != len(entry_list)-1) and not self.stop:
                self.thongbao += '\nwait %s s' % self.sleep_time
                print self.thongbao 
                loopcount = 0
                while loopcount< 10 and not self.stop:
                    loopcount +=1
                    sleep(self.sleep_time/10 )
            else:
                print 'self.stop',self.stop
        self.posting_flag = False
    def khoitaohtml(self):
        jar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        #self.opener.addheaders = [("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")]
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    def login(self):
        if self.loai_forum == 0:
            loginurl = self.url + 'login.php?do=login'
            md5 = hashlib.md5(self.passwd);md5 = md5.hexdigest()
            opts = {
            'vb_login_md5password': md5,
            'vb_login_md5password_utf': md5,
            'vb_login_username': self.uname,
            'do': 'login',
            }
            data = urllib.urlencode(opts)   
            response=self.opener.open(loginurl, data)
            login_ct = response.read()
            self.postlog = "Yes....login ok"
            self.thongbao = "Login thanh cong..."
            #self.postlog = login_ct
            print '%s %slogin thanh cong' 
            with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
                f.write(login_ct)
    def findtoken(self):
        response2=self.opener.open(self.newthread_url)
        token = response2.read()
        with open(MEDIA_ROOT +'/token_log.html', 'wb') as f:
                f.write(token)
        self.security_token=re.findall('name="securitytoken" value="(.*?)"', token)[0]
        self.thongbao = self.security_token
        print self.security_token
    def post (self):
        posts = {
                'subject': self.title.encode('cp1252'),
                'message': self.content.encode('cp1252'),
                'securitytoken': self.security_token,
                #'preview':'Preview Post',
                'newthread_agree':'True',
                'do':'postthread',
                }
        
        data = urllib.urlencode(posts)
        print data
        
        response2=self.opener.open(self.newthread_url,data)
        print 'header content-type',response2.info().getheader('Content-Type')
        ct = response2.read()
        self.postlog = "Yes....post ok"
        
        #self.postlog = ct
        
        trave_add = response2.geturl()
        with open(MEDIA_ROOT +'/post_log.html', 'wb') as f:
                f.write(ct) 
        if trave_add == self.newthread_url:
                print 'send request nhung bi loi' ,trave_add
                self.thongbao = "post loi do time"
        else:
                print 'post ok ',trave_add
                self.thongbao = "post thanh cong" + trave_add
        PostLog.objects.get_or_create(forum = self.siteobj,Ulnew = self.entry,pested_link=trave_add)                         
  
class importUL1(object):
    def khoitaohtml(self):
        jar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #self.opener.addheaders.append(("Content-Type", "application/x-www-form-urlencoded"))
                
    def login(self):
        
        loginurl = 'http://uploaded.net/io/login'
        opts = {
        'id': '7397033',
        'pw': 'Tu228787',
        
        }
        data = urllib.urlencode(opts)   
        response=self.opener.open(loginurl, data)
        login_ct = response.read()
        self.postlog = "Yes....login ok"
        self.thongbao = "Login thanh cong..."
        #self.postlog = login_ct
        print 'login thanh cong gia tri tra ve\n', 
        with open(MEDIA_ROOT +'/login_log.html', 'wb') as f:
            f.write(login_ct)
    def post(self):
        
        importULlink ='''http://uploaded.net/file/a8mdgmvf/VA_-_Magic_Mike_XXL_(Soundtrack)_(2015).rar
'''
        loginurl = 'http://uploaded.net/io/import'
        #loginurl = 'http://uploaded.net/me'

        #md5 = hashlib.md5(self.passwd);md5 = md5.hexdigest()
        opts = {
        'urls': importULlink,
        
        
        }
        data = urllib.urlencode(opts)
        print data  
        response=self.opener.open(loginurl, data)
        login_ct = response.read()
        self.postlog = "Yes....post ok"
        self.thongbao = "post thanh cong..."
        #self.postlog = login_ct
        print '%s %post thanh cong ' ,login_ct
        #with open(MEDIA_ROOT +'/login_post.html', 'wb') as f:
            #f.write(login_ct)          
    def import_to_ul(self):
        self.khoitaohtml()
        self.login()  
        self.post()             
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
          }
amaderforum = {'url':'http://amaderforum.com/',
       'uname':'mothtrdo5',
       'passwd':'228787',
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
expresshare = {'url':'http://www.expresshare.com/',
       'uname':'mothtrdo',
       'passwd':'228787',
       'newthread_url':'http://www.majaa.net/newthread.php?do=newthread&f=201',
       }
majaa = {'url':'http://www.majaa.net/',
       'uname':'mothtrdo5',
       'passwd':'228787',
       'newthread_url':'http://www.majaa.net/newthread.php?do=newthread&f=201',
       }

danhsachforum = [kho,amaderforum,shaanig]
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
def get_link_from_db():
    ul_text = ""
    linhkien_lists = Ulnew.objects.exclude(myul__icontains='http')
    ullink = linhkien_lists.values_list('ul')
    for tuplelink in ullink:
        ul_text = ul_text + tuplelink[0].replace('\n','') +'\n'
    return ul_text
def get_name_of_link(link):
    back_flash_i = link.rfind('/')
    nameoflink = link[back_flash_i+1:]
    return nameoflink
    

def update_my_ul_link_to_db(ullink_txt):
    entry_dbs = Ulnew.objects.exclude(myul__icontains='http')
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
            entry_db.myul = my_ul_this_entry
            entry_db.save()
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
if __name__ == '__main__':
    #for forum in danhsachforum:
        #createForumTable(**forum)
    #newPostProcess = PostObject1()
    #newPostProcess.post_entry(amaderforum,[''])
    
    ullink = get_link_from_db() #
    print ullink
    importULObject = importUL(ullink)
    json_import_ul_txt = importULObject.import_to_ul()
    myUlTxt = convert_jsonUl_to_txt (json_import_ul_txt)
    update_my_ul_link_to_db (myUlTxt)
    
    #update_my_ul_link_to_db (txt)
    #returned_import_uls = json_string.split(',')
    #print returned_import_uls
    '''
    for page_num in range(2,3):
        page_url = 'http://lastestmovie.com/category/tv-show/page/'+ str(page_num) + '/'
        entry_lists = get_entry_link(page_url)
        print entry_lists
        print 'so topic trong trang se leech nay',len(entry_lists)
        for ahref_title in entry_lists:
            leech_one_entry_latin1 (ahref_title)
    '''
    
    
    
    '''
    ullink = get_link_from_db()
    print ullink
    '''
    '''
    last_Ulnew = Ulnew.objects.latest('id')
    print last_Ulnew.title
    a = PostObject(kho,last_Ulnew)
    siteobj = Struct (**kho)
    print siteobj.url
    print a
    '''
 
    
   
    #update_my_ul_link_to_db (myuls)
    #create_admin_ul()
    #createForumTable(**expresshare)