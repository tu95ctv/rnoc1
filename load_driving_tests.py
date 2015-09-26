# -*- coding: utf-8 -*- 
import os
from unidecode import unidecode
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
import re,os
from datetime import datetime

class NoficationStruct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
        
def read_line(path,split_item):
    f =  open(path, "r")
    content = f.read().decode('utf-8')
    content = content.split(split_item)
    f.close()
    return content


def read_file_from_disk (path):
    f =  open(path, "rb") 
    a = f.read().decode('utf-8')
    f.close()
    return a


def save_file_to_disk(path,content, is_over_write):
    if is_over_write:
        with open(path, "wb") as f:
            f.write(content.encode('utf-8'))
    else:
        with open(path, "ab") as f:
            f.write(content.encode('utf-8'))
def unidecoded4 (name):
    urlencode_output = unidecode(name)
    special_characters = [" ","+","(",")","[","]","{","}",'"',",","."]
    for c in special_characters:
        urlencode_output = urlencode_output.replace(c, "-")
    
    
    urlencode_output = urlencode_output.replace("----", "-").replace("---", "-").replace("--", "-")
    if urlencode_output.endswith('-'):
        urlencode_output = urlencode_output[:-1]
    return urlencode_output
            
def insert_to_db(txt_databases,is_parent_cate):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
    from drivingtest.models import Category,Linhkien
    from django import db
    db_name = db.settings.DATABASES['default']['NAME']
    if 'prc' in  db_name or db_name=='bomdb' or is_parent_cate:
        all_cate_is_parent = False
    else:
        all_cate_is_parent = True # all category is parrent
        
        
    successful_insert_db_counter = 0
    one_notification ={}
    notification_lists=[]
    notice=u''
    len_import_db = len(txt_databases)
    for count,txt1db in enumerate(txt_databases):
        cates=[]
        catename_lits = txt1db['category']
        #print 'catename_lits',catename_lits
        for catename in catename_lits:
            cate = Category.objects.get_or_create(name = catename)[0]
            #print 'catename',catename
            if not all_cate_is_parent:
                if catename == u'Nam' or catename == u'Nữ' or catename == u'Nam-Nữ':
                    cate.is_parent_cate = True
                    cate.arrange_order_display = 2
                    parent_cate = cate
                    cate.is_show_on_main_nav = True
                else:
                    cate.is_parent_cate = False
                    cate.arrange_order_display = 1
                    parent_cate.children.add(cate)
                    cate.is_show_on_main_nav = False
            else:
                cate.is_parent_cate = True
                cate.arrange_order_display = 1
                cate.is_show_on_main_nav = False
            
            cate_encode_url = unidecoded4(catename)
            #print 'cate_encode_url',cate_encode_url
            cate.cate_encode_url=cate_encode_url
            
            cates.append(cate)
            cate.is_show_on_home_page = True
            cate.number_product_display_on_homepage = 4
            
            cate.save()
        
        
        price = int(txt1db['price'])
        old_price = int(txt1db['old_price'])
        try:
            arrange_order = int(txt1db['arrange_order'])
        except:
            arrange_order = 0
        name = txt1db['name']
        
        linhkien_encode_url = unidecoded4(name) #new add 24062015
        #print linhkien_encode_url
        show_old_price =txt1db['show_old_price']
        borrowed_icon_picture=txt1db['borrowed_icon_picture']
        borrowed_picture=txt1db['borrowed_picture']
        description=txt1db['description']
        icon_picture=txt1db['icon_picture']
        is_best_sale=txt1db['is_best_sale']
        is_promote_sale=txt1db['is_promote_sale']
        
        like_number=txt1db['like_number']
        picture=txt1db['picture']
        pub_date= datetime.now()
        last_edited_date=pub_date
        view_number=txt1db['view_number']
        '''
        print 'show_old_price',show_old_price 
        print 'borrowed_icon_picture',borrowed_icon_picture
        print 'description',description
        print 'icon_picture',icon_picture
        print 'is_best_sale',is_best_sale
        print 'is_promote_sale',is_promote_sale
        print 'last_edited_date',last_edited_date
        print 'like_number',like_number
        print 'picture',picture
        print 'pub_date',pub_date
        print 'view_number',view_number
        print 'view_number',view_number
        '''
        
    #try:
        try:
            p,caigi = Linhkien.objects.get_or_create(name = name,linhkien_encode_url=linhkien_encode_url,price = price, old_price = old_price,
                                           show_old_price =show_old_price,
                                       borrowed_picture=borrowed_picture,
                                       arrange_order=arrange_order,
                                       borrowed_icon_picture=borrowed_icon_picture
                                       ,icon_picture=icon_picture,description=description,is_best_sale=is_best_sale,
                                       is_promote_sale=is_promote_sale,last_edited_date=last_edited_date,like_number=like_number,
                                       picture=picture,
                                       pub_date=pub_date,
                                       view_number=view_number )
            
            p.category.add(*cates)
            p.save()
            successful_insert_db_counter += 1
            one_notification = {'name':name,'notification':'import ok san pham thu ' + str(successful_insert_db_counter) + '/' + str(len_import_db)}
            nofication_object = NoficationStruct(**one_notification)
            notification_lists.append(nofication_object)
        
        
        
        except Exception as e:
            #e = u"{0}".format(e)            
            #one_notification = {'name':name,'notification':e.message}
            #nofication_object = NoficationStruct(**one_notification)
            #notification_lists.append(nofication_object)
            print e 
        
        print 'successful_insert_db_counter',successful_insert_db_counter
    
    #for one_nofication in notification_lists:
        #notice =  notice + '\n' + one_nofication.notification  
        
        
            
            
            
    return '%s/%s\n%s ' %(successful_insert_db_counter,count,notice)
        
            

        
            
def read_txt(txt_database):
    
    #one_quest is dictionary has format {'topic':'1','id_quest':x,'question':'y':'opt':[a,b,c,d],'Anwser_Key':'1&2'}
    databases = []
    # databases is list of one_instance_db
    line_state = 'begin quest'
    #line_state info current line state in txt database, info which is question line or opt line or Anwser_key line.
    disc = []
    #opts is list of options in once quest
    questions=[]
    #questions join \n to create question of one_quest
    #txt_database = read_file_from_disk(txt_database)
    #print txt_database
    
    list_of_onedb = re.findall('#id(.*?)#end',txt_database,re.DOTALL)
    #print len(list_of_onedb)
    for one_db in list_of_onedb:
        one_instance_db={}
        name = re.findall('##name\s*=\s*(\S.*?)\s*\n', one_db, re.DOTALL)[0]
        one_instance_db.update(name=name)
        category = re.findall('##category\s*=\s*(\S.*?)\s*\n', one_db, re.DOTALL)
        one_instance_db.update(category=category)
        price = re.findall('##price\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        one_instance_db.update(price=price)
        old_price = re.findall('##old_price\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        one_instance_db.update(old_price=old_price)
        try:
            show_old_price = re.findall('##show_old_price\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
            if show_old_price=="1":
                is_best_sale=True
            else:
                show_old_price=False
        except:
            show_old_price=False
        one_instance_db.update(show_old_price=show_old_price)
        try:
            is_best_sale = re.findall('##is_best_sale\s*=\s*(.*?)\s*\n', one_db, re.DOTALL)[0]
            if is_best_sale=="1":
                is_best_sale=True
            else:
                is_best_sale=False
        except:
            is_best_sale=True
            
        one_instance_db.update(is_best_sale=is_best_sale)
        try:
            is_promote_sale = re.findall('##is_promote_sale\s*=\s*(.*?)\s*\n', one_db, re.DOTALL)[0]
            if is_promote_sale=="1":
                is_promote_sale=True
            else:
                is_promote_sale=False
        except:
            is_promote_sale =False
        one_instance_db.update(is_promote_sale=is_promote_sale)
        description = re.findall('##description\s*=\s*(.*?)##icon_picture', one_db, re.DOTALL)[0]
        one_instance_db.update(description=description)
        try:
            icon_picture = re.findall('##icon_picture\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            icon_picture=''
        one_instance_db.update(icon_picture=icon_picture)
        try:
            borrowed_icon_picture = re.findall('##borrowed_icon_picture\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            borrowed_icon_picture=''
        one_instance_db.update(borrowed_icon_picture=borrowed_icon_picture)
        
        try:
            borrowed_picture = re.findall('##borrowed_picture\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            borrowed_picture=''
        one_instance_db.update(borrowed_picture=borrowed_picture)
        
        
        try:
            picture = re.findall('##picture\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            picture=''
        
        one_instance_db.update(picture=picture)
        try:
            pub_date = re.findall('##pub_date\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            pub_date=''
        one_instance_db.update(pub_date=pub_date)
        try:
            last_edited_date = re.findall('##last_edited_date\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            last_edited_date=''
        one_instance_db.update(last_edited_date=last_edited_date)
        try:
            view_number = re.findall('##view_number\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
        except:
            view_number=0
        one_instance_db.update(view_number=view_number)
        try:
            
            like_number = re.findall('##like_number\s*=\s*(\w.*?)\s*\n', one_db, re.DOTALL)[0]
            # \w is set of [0-9] and [a-Z] so RE of ##like_number = \n# is error index of list
        except:
            like_number=0
        one_instance_db.update(like_number=like_number)
        databases.append(one_instance_db)
        #print 'one_instance_db',one_instance_db
    #print databases
    return databases        
            
def delete_db_from_load ():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
    from drivingtest.models import Category,Linhkien
    from django import db
    Linhkien.objects.all().delete()
    Category.objects.all().delete()
    print 'xoa sach'
if __name__ == '__main__':
    #Insert to database
    #dbs = read_txt_database(MEDIA_ROOT+ '/saleweb.txt')
    #dbs = read_txt( '/home/ductu/Pictures/bomdb (copy)')
    #insert_to_db(dbs,1)
    delete_db_from_load()


