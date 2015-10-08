# -*- coding: utf-8 -*-

import datetime
import os
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from drivingtest.models import Category, Linhkien, OwnContact, Table3g, Ulnew,\
    ForumTable, PostLog, LeechSite, thongbao, postdict, Mll, Command3g, FNAME,\
    SearchHistory, H_Field, UserProfile, Doitac, CommentForMLL, Nguyennhan
    
from drivingtest.forms import CategoryForm, LinhkienForm, OwnContactForm,\
    UploadFileForm, Table3gForm, ForumChoiceForm, UlnewForm  , ExampleForm,\
    TramTable, Mllform, MllTable, CommandTable, Commandform, SearchHistoryTable,\
    CommentForMLLForm, DoitacForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count
from load_driving_tests import read_txt, insert_to_db, unidecoded4,\
    delete_db_from_load
from __main__ import sys
from create_owncontact import auto_create_owncontact_f
from django import db
#from crispy_forms.utils import render_crispy_form  # importance
from fetch_website import danhsachforum, PostObject, CountTest, leech_bai,\
    get_link_from_db, init_d4, import_ul_txt_to_myul
from drivingtest.forms import PersonTable
from django_tables2 import RequestConfig
import operator
from django.conf import settings #or from my_project import settings
from time import sleep
from itertools import chain
from toold4 import  recognize_fieldname_of_query
from LearnDriving.settings import MYD4_LOOKED_FIELD, FORMAT_TIME
import json
from xu_ly_db_3g import read_txt_database_3G, import_database_4_cai
import xlrd
import itertools
import re
from exceptions import Exception





@login_required
def omckv2(request):
    #rint 'request',request
    #mllform = Mllform(instance = Mll.objects.latest('id'))
    mllform = Mllform()
    commandform = Commandform()
    mlltable = MllTable(Mll.objects.all().order_by('-id'), prefix="mlltable-")
    lenhtable = CommandTable(Command3g.objects.all().order_by('-id'), prefix="commandtable-")

    RequestConfig(request, paginate={"per_page": 15}).configure(mlltable) 
    '''
    if 'query' in request.GET:
        print 'no dung la phuon thuc get'
        contain = request.GET['query']
        print 'bang dan seach',contain
        #fieldnames = [f.name for f in Table3g._meta.fields if isinstance(f, CharField)]
        #print 'fname',fieldnames
        try:
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME))
            kq_searchs = Table3g.objects.filter(qgroup)
            #context_dict = {'kq_searchs':kq_searchs}
        except Exception as e:
            print 'loi trong queyry',type(e),e    
        
        
        table = TramTable(kq_searchs, )
        RequestConfig(request, paginate={"per_page": 10}).configure(table)

    else:
    '''
    #table = TramTable(Table3g.objects.all(), )
    table = TramTable(Table3g.objects.all(), )
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
    RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
    comment_form = CommentForMLLForm()
    return render(request, 'drivingtest/omckv2.html',{'table':table,'mllform':mllform,'comment_form':comment_form,'commandform':commandform,'mlltable':mlltable,'lenhtable':lenhtable,'history_search_table':history_search_table})
def edit_history_search(request):
    try:
        id_h = request.GET['history_search_id']
        instance = SearchHistory.objects.get(id=id_h)
        print request.GET
        for f in H_Field:
            if f in request.GET:
                value = request.GET[f] 
                if value!= u'—':
                    setattr(instance,f,value)
                    instance.save()
        history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
        RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
        return render(request, 'drivingtest/custom_table_template_mll.html',{'table':history_search_table})           
        #return HttpResponse(request.GET['thanh_vien'])
    except Exception as e:
        print type(e),e
def config_ca(request):
    thanh_vien =   request.user
    ca_truc = request.POST['ca_truc']
    p = UserProfile.objects.get_or_create(user =thanh_vien)
    
    if p[1]: # tao:
        p[0].ca_truc = ca_truc
        p[0].save()
    else: # p exit
        p[0].ca_truc = ca_truc
        p[0].save()
    
    #profile = UserProfile() 
    #profile.user = thanh_vien
    #profile.save()
    return HttpResponse('Ca ' + p[0].ca_truc)
def search_history(request):
    history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
    RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
    return render(request, 'drivingtest/custom_table_template_mll.html',{'table':history_search_table})

def luu_doi_tac(doi_tac_inputext):
    if doi_tac_inputext:
                fieldnames= ['Full_name','Don_vi','So_dien_thoai']
                if "-" not in doi_tac_inputext:
                    taodoitac = Doitac.objects.get_or_create(Full_name = doi_tac_inputext)
                    doitac = taodoitac[0]
                    if taodoitac[1]:
                        print ' tao doi tac moi',doitac
                    else:
                        print 'co san doi tac',doitac
                        
                else: # if has - 
                    doi_tac_inputexts = doi_tac_inputext.split('-')
                    #qgroup = reduce (   operator.and_,(  Q(**{'%s'%fieldnames[count]:value}) for count,value in enumerate(doi_tac_inputexts)  )   )
                    #dictx = dict({'%s'%fieldnames[count]:value} for count,value in enumerate(doi_tac_inputexts) ) 
                    #dictx =  itertools.izip (fieldnames,doi_tac_inputexts,)
                    
                    sdtfield = fieldnames.pop(2)
                    p = re.compile('[\d\s]{3,}')
                    kq= p.search(doi_tac_inputext)
                    try:
                        phone_number_index_of_ = kq.start()
                        std_index = len(re.findall('-',doi_tac_inputext[:phone_number_index_of_]))
                        fieldnames.insert(std_index, sdtfield)
                    except:
                        pass
                    dictx = dict(zip(fieldnames,doi_tac_inputexts))
                    doitac = Doitac.objects.get_or_create(**dictx)[0]
                return doitac
    else:
        return None
def luu_mll_form(request):
    #print 'request all',request
    print 'request.POST',request.POST
    user = request.user
    thanh_vien =   request.user.username
    print thanh_vien
    if request.method == 'POST':
        print 'da vao post'
        form = Mllform(request.POST)
        tao_hay_edit = request.POST['id-mll-entry'] # if has id mll is that edit
        print tao_hay_edit
        #try:
        if not tao_hay_edit: # Create MLL entry
            mll_instance = form.save(commit=False)
            gio_mat =request.POST['gio_mat']
            doi_tac_inputext = request.POST['doi_tac_fr'].lstrip().rstrip()
            
            
            print 'doi_tac_inputext',doi_tac_inputext
            if gio_mat:
                pass
                #now = datetime.strptime(gio_mat, FORMAT_TIME)
            else:
                now = datetime.now()
                mll_instance.gio_mat = now
            mll_instance.thanh_vien = thanh_vien
            mll_instance.ca_truc = user.get_profile().ca_truc
            
            
            nguyen_nhan_inputext = request.POST['nguyen_nhan_fake'].lstrip().rstrip()
            if nguyen_nhan_inputext:
                nguyen_nhan_instance = Nguyennhan.objects.get_or_create(Name = nguyen_nhan_inputext)[0]
                mll_instance.nguyen_nhan = nguyen_nhan_instance
            doitac = luu_doi_tac(doi_tac_inputext)
            if doitac:
                mll_instance.doi_tac = doitac
            
            mll_instance.save()    
        else: # Edit MLL entry
            mll_id = int(tao_hay_edit)
            print 'mll_id',mll_id
            mllentry = Mll.objects.get(id = mll_id)
            form = Mllform(request.POST,instance=mllentry)
            form.save(commit=True)
        #except Exception as e:
            #print type(e),e
            #error_dict ={}
            #error_dict['error_notification']= form.errors
            #return HttpResponse( u'{0}'.format(error_dict))
            #data = json.dumps([v for k,v in form.errors.items()] + ['failed'])
            #data = json.dumps(form.errors)
            #return HttpResponseBadRequest(e)
            #return HttpResponse('')
    table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/custom_table_template_mll.html',{'table':table})

def get_contact_form(request):
    if request.method =="GET":
        id = request.GET['id']
        form = DoitacForm(instance = Doitac.objects.get(id=id))
        return render(request, 'drivingtest/simple_form.html',{'form':form})
    elif request.method =="POST":
        id = request.POST['id']
        form = DoitacForm(request.POST,instance = Doitac.objects.get(id=id))
        form.save()
        table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
        RequestConfig(request, paginate={"per_page": 15}).configure(table)        
        return render(request, 'drivingtest/custom_table_template_mll.html',{'table':table})
    
    
def if_yes_else_no(input):
    if input: 
        return input
    else: return ''
def if_yes_else_no_all(*args):
    output =''
    for count, input in enumerate(args):
        if input:
            output += input + ' '
    return output
def if_yes_else_no_all_x(t,*args):
    output =''
    last_index = len(args) -1 
    for count, fn in enumerate(args):
        input = getattr(t,fn)
        output += '<span class="tram_field_name">'+ MYD4_LOOKED_FIELD[fn]+': ' +'</span>'+ (input if input else '___' )+ (' , ' if not count==last_index else '') 
    return output        
def get_need_variable (request):
    print request.GET
    query   = request.GET['query'].lstrip().rstrip()
    print 'ban dang search',query
    inputfieldname = request.GET['inputfieldname']
    results = []
    if inputfieldname =='nguyen_nhan_fake':
        fieldnames = [f.name for f in Nguyennhan._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        doitac_querys = Nguyennhan.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            #doitac_dict['value'] = doitac.id
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] = doitac.Ghi_chu  if doitac.Ghi_chu else ''
            results.append(doitac_dict)
        to_json = {
            "key1": results,
            "key2": "value2"
        }
    elif inputfieldname =='doi_tac_fr' :# phai them fr de khac doi_tac 
        fieldnames = [f.name for f in Doitac._meta.fields if isinstance(f, CharField)  ]
        if '-' not in query:
            print 'fieldnames',fieldnames
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
            doitac_querys = Doitac.objects.filter(qgroup)
            for doitac in doitac_querys[:10]:
                doitac_dict = {}
                #doitac_dict['value'] = doitac.id
                doitac_dict['label'] = doitac.Full_name + ("-" + doitac.Don_vi if doitac.Don_vi else "") 
                doitac_dict['desc'] = doitac.So_dien_thoai if doitac.So_dien_thoai else 'chưa có sdt'
                results.append(doitac_dict)
            to_json = {
                "key1": results,
                "key2": "value2"
            }
        else:# there '-' in query
            contains = query.split('-')
            
            for count,contain in enumerate(contains):
                qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in fieldnames))
                kq_searchs_one_contain = Doitac.objects.filter(qgroup)
                if count==0:
                    kq_searchs = kq_searchs_one_contain
                else:
                    kq_searchs = kq_searchs & kq_searchs_one_contain    
            for doitac in kq_searchs[:10]:
                doitac_dict = {}
                doitac_dict['value'] = doitac.id
                doitac_dict['label'] = doitac.Full_name + "-" + doitac.Don_vi
                doitac_dict['desc'] = doitac.So_dien_thoai if doitac.So_dien_thoai else 'chưa có sdt'
                results.append(doitac_dict)
            to_json = {
                "key1": results,
                "key2": "value2"
            }
    elif inputfieldname =='subject' or inputfieldname =="main_suggestion":
        
        contain = query
        if contain =='':
            fieldnames = {'site_id_3g':'3G'}
        else:
            fieldnames = MYD4_LOOKED_FIELD
        print 'ban dan search',contain
        dicta ={}    
        for fieldname,sort_fieldname  in fieldnames.iteritems():
            q_query = Q(**{"%s__icontains" % fieldname: contain})
            one_kq_searchs = Table3g.objects.filter(q_query)[0:20]
            if len(one_kq_searchs)>0:
                #dicta[sort_fieldname] = [fieldname,one_kq_searchs]
                for tram in one_kq_searchs:
                    tram_dict = {}
                    try:
                        if fieldname =="site_id_3g":
                            thiet_bi = tram.Cabinet
                        elif fieldname =="site_id_2g_E":
                            thiet_bi =tram.nha_san_xuat_2G
                        else:
                            #thiet_bi =tram.Cabinet+'&'+tram.nha_san_xuat_2G
                            thiet_bi = "2G&3G"
                    except Exception as e:
                            thiet_bi = 'error' + tram.site_name_1
                            print e, tram
                    tram_dict['value'] = tram.id
                    tram_dict['sort_field'] = sort_fieldname
                    tram_dict['label'] =  getattr(tram,fieldname)
                    tram_dict['thiet_bi'] =  thiet_bi
                    tram_dict['site_name_1'] = tram.site_name_1
                    #tram_dict['desc'] = if_yes_else_no(tram.site_name_1) + ',' + if_yes_else_no(tram.site_name_2) + ',' + if_yes_else_no(tram.site_id_3g)+ ',' + if_yes_else_no(tram.site_id_2g_E)
                    #tram_dict['desc'] = if_yes_else_no_all(tram.site_name_1,tram.site_name_2,tram.site_id_3g,tram.site_id_2g_E)
                    tram_dict['desc'] = if_yes_else_no_all_x(tram ,'site_name_1','site_name_2',)
                    tram_dict['desc2'] = if_yes_else_no_all_x(tram ,'site_id_3g','site_id_2g_E')
                    if_yes_else_no_all
                    results.append(tram_dict)
            
        to_json = {
                "key1": results,
                "key2": "value2"
            }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
def add_command(request):
    print 'request.POST',request.POST
    try:
        id_command_entry = request.POST['id-command-entry']
    except:
        id_command_entry= "" # tao 1enh moi
    print  id_command_entry
    if id_command_entry:
        try:
            command_instance = Command3g.objects.get(id = int(id_command_entry))
            form = Commandform(request.POST,instance=command_instance)
            form.save(commit=True)
        except Exception as e:
            print type(e),e
    else:    
        thanh_vien =   request.user.username
        print thanh_vien
        if request.method == 'POST':
            print 'da vao post'
            
            form = Commandform(request.POST)
            form.save(commit=True)
    table = CommandTable(Command3g.objects.all().order_by('-id'),prefix="3-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/table2_template.html',{'table':table})

#from django.db.models import CharField
def mll_filter(request):
    
    if 'thiet_bi' not in request.GET:
        kq_searchs = Mll.objects.all().order_by('-id')
    else:
        #foreinkey_fields = [f.name for f in Mll._meta.fields if isinstance(f, ForeignKey)  ]
        
        
        
        
        
        
        
        fieldnames = [f.name for f in Mll._meta.fields if isinstance(f, CharField) and'gio_mat'not in f.name  ]
        print 'tong so  charfield' ,len(fieldnames)
        try:
            for fieldname in fieldnames:
                print fieldname, request.GET[fieldname]
        except Exception as e:
            print 'loi for',type(e),e 
        try:
            try:
                qgroup = reduce(operator.and_, (Q(**{"%s__icontains" % fieldname: request.GET[fieldname]}) for fieldname in fieldnames if request.GET[fieldname]))
            except:
                qgroup = Q(thiet_bi__icontains='')
            if request.GET['ung_cuu']=='True':
                print 'ung cuu true'
                q_ungcuu = Q(ung_cuu=True)
                qgroup = qgroup & q_ungcuu
            nguyen_nhan_inputext = request.GET['nguyen_nhan_fake'].lstrip().rstrip()
            if nguyen_nhan_inputext:
                #nguyen_nhan_instance = Nguyennhan.objects.get_or_create(Name = nguyen_nhan_inputext)[0]
                q_foreignkey_group = Q(nguyen_nhan__Name__icontains=nguyen_nhan_inputext)|Q(nguyen_nhan__Name_khong_dau__icontains=nguyen_nhan_inputext)   
                qgroup = qgroup & q_foreignkey_group
                
            gio_mat_str = request.GET['gio_mat']
            gio_mat2 = request.GET['gio_mat2']
            if request.GET['gio_mat']:
                d = datetime.strptime(gio_mat_str, FORMAT_TIME)
                q_gio_mat = Q(gio_mat__lte=d)
                qgroup = qgroup & q_gio_mat
            if request.GET['gio_mat2']:
                print 'ok co gio mat'
                d = datetime.strptime(gio_mat2, FORMAT_TIME)
                q_gio_mat2 = Q(**{'gio_mat__gte':d})
                qgroup = qgroup & q_gio_mat2
            kq_searchs = Mll.objects.filter(qgroup).order_by('-id')
        except Exception as e:
            print 'loi trong queyry',type(e),e 
    if 'download' in request.GET:
        return show_excel(request,Mll,kq_searchs)
    else:       
        table = MllTable(kq_searchs,prefix="mlltable-")
        RequestConfig(request, paginate={"per_page": 15}).configure(table)
        return render(request, 'drivingtest/custom_table_template_mll.html', {'table': table})
def edit_mll_entry(request):
    mll_id = request.GET['mll_id']
    print 'mll_id',mll_id
    mllform = Mllform(instance=Mll.objects.get(id = int(mll_id)))
    return render(request, 'drivingtest/mllformfilter.html',{'mllform':mllform,'id_mll_entry':mll_id})
def edit_command(request):
    print request
    print 'hjghj hjgjhghjg'
    mll_id = request.GET['mll_id']
    #mll_id = request.GET['mll_id']
    print 'mll_id',mll_id
    cmform = Commandform(instance=Command3g.objects.get(id = int(mll_id)))
    return render(request, 'drivingtest/crispy_form.html',{'form':cmform,'id_mll_entry':mll_id})
def lenh_table(request):
    print 'ban dang vao trang lenhtable'
    print 'ban dang query',request.GET['query']
def delete_mll (request):
    id = request.GET['query']
    mll_instance  = Mll.objects.get(id=int(id))
    mll_instance.delete()
    table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/custom_table_template.html',{'table':table})
def load_edit_comment(request):
    comment_id = request.GET['comment_id']
    comment_instance = CommentForMLL.objects.get(id = comment_id)
    form = CommentForMLLForm(instance=comment_instance,)
    return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form})
def add_comment(request):
    
    try:
        #print request.POST
        
        comment_id = request.POST['comment_id']
        id = request.POST['selected_instance_mll']
        mll_instance  = Mll.objects.get(id=id)
        print 'mll_instance,comment_id',id,comment_id
        #print mll_instance
        if comment_id =="new": # ADD comment
            print 'add comment'
            form = CommentForMLLForm(request.POST)
            comment_instance = form.save(commit = False)
            if not request.POST['datetime']:
                comment_instance.datetime =datetime.now()
            comment_instance.thanh_vien = request.user.username
            comment_instance.mll = mll_instance
            
            
            doi_tac_inputext = request.POST['doi_tac_fr'].lstrip().rstrip()
            doitac = luu_doi_tac(doi_tac_inputext)
            if doitac:
                comment_instance.doi_tac = doitac
            
            
            
            comment_instance.save() # if not foreinkey field in form
            #form.save_m2m()  # for foreinkey
            #mll_instance.comments.add(comment_instance)
            #mll_instance.commentForMLL_set.add(comment_instance)
        else: # Edit
            print 'edit'
            comment_instance = mll_instance.comments.get(id = request.POST['comment_id'])
            print 'comment_instance.comment',comment_instance.comment
            form = CommentForMLLForm(request.POST,instance=comment_instance)
            #comment_instance.comment = request.POST['comment']
            form.save()
            #comment_instance.save()
            #form.save_m2m()
            #comment_instance.datetime= datetime.now()
            
        table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
        RequestConfig(request, paginate={"per_page": 15}).configure(table)        
        return render(request, 'drivingtest/custom_table_template.html',{'table':table})
    
    
    
    except Exception as e:
        print type(e),e
        #error_dict ={}
        #error_dict['error_notification']= form.errors
        #return HttpResponse( u'{0}'.format(error_dict))
        #data = json.dumps([v for k,v in form.errors.items()] + ['failed'])
        try:
            bad_request_render = str(form.errors)
        except Exception as e:
            bad_request_render = str(e) + str(type(e))
            
        return HttpResponseBadRequest(bad_request_render)


from django.core.servers.basehttp import FileWrapper
def show_detail_tram1(request):
        
        print 'show_detail_tram '
        
        context = RequestContext(request)
        
        
        if request.method == 'GET':
            id = request.GET['id']
            tram = Table3g.objects.get(id=id)
            example_form =Table3gForm (instance=tram)
            
            
        context_dict = {'example_form':example_form,}
        return render_to_response('drivingtest/show_detail_tram.html', context_dict, context)
def show_detail_tram(request):
        
        print 'show_detail_tram '
        context = RequestContext(request)
        fieldnames = MYD4_LOOKED_FIELD
        if 'id' in request.GET:
            print 'co id torn gsearch dau phong sao khogn vo day'
            id = request.GET['id']
            print 'id in search',id
            tram = Table3g.objects.get(id=id)
        elif request.method == 'GET':
            contain = request.GET['query']
            typesite = request.GET['type']
            try:
                if typesite =="all":
                    for fieldname in fieldnames.iterkeys():
                        print fieldname
                    qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in fieldnames.iterkeys()))
                    kq_searchs_one_contain = Table3g.objects.filter(qgroup)
                    r = list(kq_searchs_one_contain)
                    print 'len r',len(r)
                    if r:
                        tram =  r[0]
                    else:
                        tram =  None
                else:
                    fieldname = fieldnames.keys()[fieldnames.values().index(typesite)]
                    #print 'fieldname',fieldname
                    print 'contain',contain
                    q_query = Q(**{"%s" % fieldname: contain})
                    tram = Table3g.objects.get(q_query)
                
            except Exception as e:
                print type(e),e
        example_form =Table3gForm (instance=tram)    
        context_dict = {'example_form':example_form,}
        return render_to_response('drivingtest/show_detail_tram.html', context_dict, context)
def save_history(query):
    if (SearchHistory.objects.all().count() > 200 ):
                oldest_instance= SearchHistory.objects.all().order_by('search_datetime')[0]
                oldest_instance.query_string = query
                oldest_instance.search_datetime = datetime.now()
                oldest_instance.save()
    else:
        instance = SearchHistory(query_string=query,search_datetime = datetime.now())
        instance.save()
def tram_table(request):
    print 'tram_table'
    if 'id' in request.GET:
        id = request.GET['id']
        kq_searchs =[]
        kq_searchs_one_contain = Table3g.objects.get(id=id)
        kq_searchs.append(kq_searchs_one_contain)
        print 'in in tram_table',id
        query = request.GET['query']
        save_history(query)
    elif 'query' not in request.GET and 'id' not in request.GET :
        kq_searchs = Table3g.objects.all()
    else: # tuc la if request.GET['query']:
        query = request.GET['query']
        if '&' in query:
            print 'co &'
            contains = request.GET['query'].split('&')
            query_sign = 'and'
        else:
            contains = request.GET['query'].split(',')
            query_sign = 'or'
        kq_searchs = Table3g.objects.none()
        for count,contain in enumerate(contains):
            contain_reconize_tuple = recognize_fieldname_of_query(contain,MYD4_LOOKED_FIELD)
            contain = contain_reconize_tuple[1]
            print 'contain',contain
            fieldnameKey = contain_reconize_tuple[0]
            try:
                if query_sign=="or":
                    if fieldnameKey=="all field":
                        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME))
                    else:
                        print fieldnameKey,contain
                        qgroup = Q(**{"%s__icontains" % fieldnameKey: contain})
                    kq_searchs_one_contain = Table3g.objects.filter(qgroup)
                    kq_searchs = list(chain(kq_searchs, kq_searchs_one_contain))
                else: # dieu kien AND but loop all field with or condition
                    qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME))
                    kq_searchs_one_contain = Table3g.objects.filter(qgroup)
                    if count==0:
                        kq_searchs = kq_searchs_one_contain
                    else:
                        kq_searchs_one_contain = Table3g.objects.filter(qgroup)
                        kq_searchs = kq_searchs & kq_searchs_one_contain
            except Exception as e:
                print 'loi trong queyry',type(e),e
        save_history(query)    
            
    table = TramTable(kq_searchs,)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'drivingtest/custom_search_table.html', {'table': table})
def mll_table(request):
    pass
def suggestion(request):
        print 'suggestion'
        context = RequestContext(request)
        if request.method == 'GET':
                contain = request.GET['query']
                if contain =='':
                    fieldnames = {'site_id_3g':'3G'}
                else:
                    fieldnames = MYD4_LOOKED_FIELD
        print 'ban dan search',contain
        recognize = recognize_fieldname_of_query(contain, fieldnames)
        dicta ={}    
        for fieldname,sort_fieldname  in fieldnames.iteritems():
            q_query = Q(**{"%s__icontains" % fieldname: contain})
            one_kq_search = Table3g.objects.filter(q_query)[0:20]
            if len(one_kq_search)>0:
                dicta[sort_fieldname] = [fieldname,one_kq_search]
        context_dict = {'dict':dicta}
                
        return render_to_response('drivingtest/kq_searchs.html', context_dict, context)        
def suggestion1(request):
    
        
        print 'suggestion'
        context = RequestContext(request)
        
        if request.method == 'GET':
                contain = request.GET['query']
                if contain =='':
                    fieldnames = {'site_id_3g':'3G'}
                else:
                    fieldnames = MYD4_LOOKED_FIELD
        print 'ban dan search',contain
        recognize = recognize_fieldname_of_query(contain, fieldnames)
   
        dicta ={}    
        
        for fieldname,sort_fieldname  in fieldnames.iteritems():
            q_query = Q(**{"%s__icontains" % fieldname: contain})
            one_kq_search = Table3g.objects.filter(q_query)[0:20]
            if len(one_kq_search)>0:
                dicta[sort_fieldname] = [fieldname,one_kq_search]
        context_dict = {'dict':dicta}
                
        return render_to_response('drivingtest/kq_searchs.html', context_dict, context)    
def lenh_suggestion(request):
    if request.method == 'GET':
            contain = request.GET['query']
    #kq_searchs = Table3g.objects.filter(site_id_3g__icontains=contain)    
    fieldnames = [f.name for f in Command3g._meta.fields if isinstance(f, CharField)]

    print 'fname',fieldnames
    try:
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in fieldnames))
        kq_searchs = Command3g.objects.filter(qgroup)
        #context_dict = {'kq_searchs':kq_searchs}
    except Exception as e:
        print 'loi trong queyry',type(e),e    
    table = CommandTable(kq_searchs,)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'drivingtest/table.html', {'table': table})


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/omckv2/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('drivingtest/login.html', {}, context) 
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/omckv2/')

@login_required
def upload_excel_file(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result_handle_file ="form is valid"
            
            #handle_uploaded_file(request.FILES['file'])
            fcontain = request.FILES['file'].read()
            workbook = xlrd.open_workbook(file_contents=fcontain)
            import_database_4_cai(workbook)
            return render_to_response('drivingtest/upload_excel_file.html', {'form': form,'result_handle_file':result_handle_file},context)
    else:
        form = UploadFileForm()
    return render_to_response('drivingtest/upload_excel_file.html', {'form': form},context)

def download_script1(request):
    id_3g = request.GET['id_3g']
    print 'id_3g',id_3g
    #print settings.MEDIA_ROOT
    filename = settings.MEDIA_ROOT + '/for_user_download_folder/KG5733_IUB_W12_3.mo' # Select your file here.                                
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=test.txt'

    response['Content-Length'] = os.path.getsize(filename)
    return response
import tempfile, zipfile

def download_script(request):
    """                                                                         
    Create a ZIP file on disk and transmit it in chunks of 8KB,                 
    without loading the whole file into memory. A similar approach can          
    be used for large dynamic PDF files.                                        
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    file_names = ['KG5733_IUB_W12_3.mo','KG5733_OAM_W12_1.xml','KG5733_SE-2carriers_2.xml']
    for file_name in  file_names:
        filename = settings.MEDIA_ROOT + '/for_user_download_folder/' + file_name # Select your file here.                              
        archive.write(filename, file_name)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


import csv
from StringIO import StringIO
from django.http import HttpResponse
#https://docs.djangoproject.com/en/1.8/howto/outputting-csv/
def show_excel1(request):
    # use a StringIO buffer rather than opening a file
    output = StringIO()
    w = csv.writer(output)
    for i in range(10):
        w.writerow(range(10))
    # rewind the virtual file
    output.seek(0)
    return HttpResponse(output.read(), mimetype='application/ms-excel')
    
def show_excel2(request):
    fields = Mll._meta.fields
    
    
    # write your header first
    
    # use a StringIO buffer rather than opening a file
    output = StringIO()
    writer = csv.writer(output)
    #for i in range(10):
        #writer.writerow(range(10))
    # rewind the virtual file
    for obj in Mll.objects.all()[:10]:
        row = []
        for field in fields:
            row.append(str(getattr(obj, field.name)))
            #row += str(getattr(obj, field.name)) + ","
        writer.writerow(row)
    output.seek(0)
    return HttpResponse(output.read(),
    mimetype='application/ms-excel',content_type='text/csv')
from django.utils import timezone, simplejson
def show_excel(request,model=None,kqsearchs=None):
    if not model:
        model = Table3g
        kqsearchs=model.objects.all()[:20]
    fields = model._meta.fields
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    header_row =[]
    for field in fields:
        header_row.append(field.verbose_name)
    writer.writerow(header_row)
    for obj in kqsearchs:
        row = []
        
        for field in fields:
            if isinstance(field, DateTimeField):
                giomat = getattr(obj, field.name)
                if giomat:
                    dt = timezone.localtime(giomat).strftime(FORMAT_TIME)
                    print dt
                    row.append(dt)
                else:
                    row.append(str(getattr(obj, field.name)))
            elif field.name == "cac_buoc_xu_ly":
                querysetcm = obj.comments.all().order_by("id")
                cms =  obj.cac_buoc_xu_ly 
                for comment in querysetcm:
                    cms = cms + ' '   +(timezone.localtime(comment.datetime)).strftime(FORMAT_TIME)+ '(' +  comment.thanh_vien + "): " + comment.comment +'\n'
                row.append(cms)
            else:
                row.append(str(getattr(obj, field.name)))
            #row += str(getattr(obj, field.name)) + ","
        writer.writerow(row)

    return response
'''
import djqscsv


def get_csv(request):
    qs = Mll.objects.all()
    return djqscsv.render_to_csv_response(qs)
    '''
#############################################################################







def init(request):
    init_d4()
    return HttpResponse("ok")
        
 
def order_linhkien(linhkien_lists):
    #linhkien_lists = linhkien_lists.order_by('-arrange_order')
    linhkien_lists = linhkien_lists.extra(order_by = ['-arrange_order'])
    return linhkien_lists
def one_product_list_index(linhkien_lists, id_product_list, name, number_product_display):
        if number_product_display ==0:
            number_product_display = len(linhkien_lists)
        paginator = Paginator(linhkien_lists, number_product_display)  # Show 25 contacts per page
        linhkien_lists = paginator.page(1)
        linhkien_lists.id_product_list = id_product_list
        linhkien_lists.name = name
        linhkien_lists.number_product_display =  str(number_product_display)
        if linhkien_lists.paginator.num_pages == 1:
            linhkien_lists.one_page = "none"
        return linhkien_lists



        
    
def index(request):
    forum_choice_form = ForumChoiceForm()
    # [('1','a'),('2','b')] [(x['url'],x['url']) for x in danhsachforum]
    print 'danh sach',[(x['url'],x['url']) for x in danhsachforum]
    forum_choice_form.fields['forumchoice'].choices = [(x['url'],x['url']) for x in danhsachforum]
    #return render(request, 'drivingtest/index.html', context_dict)
    leech_entry_lists = Ulnew.objects.all().order_by('-id')
    table = PersonTable(Ulnew.objects.all())
    RequestConfig(request, paginate={"per_page": 40}).configure(table)

    #return render(request, 'drivingtest/people.html', {'table': table})
    
    siteobj = ForumTable.objects.get(url = 'http://amaderforum.com/')
    shaanigsite = ForumTable.objects.get(url = 'http://www.shaanig.com/')
    for entry in leech_entry_lists:
        try:
                #posted_ama = Ulnew.objects.get(forumback=siteobj,postLog__Ulnew=entry)
                posted_ama= PostLog.objects.get(forum=siteobj, Ulnew=entry)
                entry.is_post_amaforum = posted_ama.pested_link
               
                #entry.is_post_amaforum = 'yes'
        except:
            entry.is_post_amaforum = 'N'
        try:
                #posted_ama = Ulnew.objects.get(forumback=siteobj,postLog__Ulnew=entry)
          
                posted_shaanigsite= PostLog.objects.get(forum=shaanigsite, Ulnew=entry)
                entry.is_post_shaanig = posted_shaanigsite.pested_link
                #entry.is_post_amaforum = 'yes'
        except:
            entry.is_post_shaanig = 'N'
    
    leechsites = LeechSite.objects.all()
    for leechsite in leechsites:
        leechsite.leech_categories=[]
        
        one_cate = leechsite.music
        if one_cate:
            leechsite.leech_categories.append(one_cate)
        one_cate = leechsite.tv_show 
        if one_cate:
            leechsite.leech_categories.append(one_cate)
        one_cate = leechsite.anime
        if one_cate:
            leechsite.leech_categories.append(one_cate)
        one_cate = leechsite.movie
        if one_cate:
            leechsite.leech_categories.append(one_cate)
    
    '''
    
    leechsite.HDmovie
    leechsite.software
    leechsite.game
    leechsite.anime
    leechsite.mobile
    leechsite.ebook
    '''
    #context_dict = {'forum_choice_form':forum_choice_form,'leech_entry_lists':leech_entry_lists,'leechsites':leechsites}
    context_dict = {'forum_choice_form':forum_choice_form,'leech_entry_lists':leech_entry_lists,'table': table,'leechsites':leechsites}

    return render_to_response("drivingtest/index.html",
                          context_dict, context_instance=RequestContext(request))

def select_forum(request):
    try:
        forum_choice_form = ForumChoiceForm(request.POST)
        if forum_choice_form.is_valid():
            print 'valid'
        else:
            print 'notvalid'
        print 'type(request.POST)',type(request.POST)
        print 'request.POST',request.POST
        notification =  u'{0}'.format(request.body) + '\n' + u'{0}'.format(request.POST['forumchoice'])
        btn = request.POST['btn']
        #return render(request, 'drivingtest/notice.html', {'notification':notification})
        site_will_posts = request.POST.getlist('forumchoice')
        print 'site_will_post',site_will_posts
        #print 'type of site_will_post', type(site_will_post)
        post_sitedict_list = []
        #stuff = map(lambda w: bbcode.find(w) , prefix_links)
        for site_will_post in site_will_posts:
            for site in danhsachforum:
                    if site['url'] == site_will_post:
                        post_sitedict_list.append(site)
        print >>sys.stderr ,'you choice',post_sitedict_list
        print 'so luong hien dang ton tai',len(postdict)
        if btn == 'start':
        
            if 'choiceallentry' in request.POST:
                print 'ban chon het topic'
                entry_id_lists = ['all']
            else:
                entry_id_lists = request.POST.getlist('selection')
            print 'entry_id_lists',entry_id_lists
            
            
            
            
            for dict_site in post_sitedict_list:
                try:
                    if postdict[dict_site['url']].is_alive():
                        print 'luong dang chay bam stop cai da'
                        return render(request, 'drivingtest/notice.html', {'notification':'luong dan chay bam stop cai da'})
                    else:
                        pass
                except:
                    print 'New program...let post '
                postdict[dict_site['url']] = PostObject(dict_site,entry_id_lists)
                postdict[dict_site['url']].login_flag = 1
                postdict[dict_site['url']].start()
                print 'chuan bi vao ct post o view'
        elif btn == 'stop':
            print 'dang stop...o view'
            for dict_site in post_sitedict_list:
            
            
                print 'postdict',postdict
                print 'dict_site',dict_site['url']
                print 'luong dang ton tai',postdict[dict_site['url']]
                print 'type of postdict truoc stop ',type(postdict)
                print 'type luong dang ton tai',type (postdict[dict_site['url']])
                try:
                    #if postdict[dict_site['url']].is_alive():
                    postdict[dict_site['url']].stop  = True
                    print 'type of postdict sau stop ',type(postdict)
                    postdict[dict_site['url']].join()
                    print 'type of postdict sau join ',type(postdict)
                    notification = 'luong da stop xong, bat dau chay'
                    print 'luong da stop xong, bat dau chay'
                except Exception as e:
                    print 'luong chua ton tai' ,e
            
        
        return render(request, 'drivingtest/notice.html', {'notification':notification})
    except Exception as e:
        print type(e),e
        return render(request, 'drivingtest/notice.html', {'notification':"loi gi do"})
    
def leech(request):
    notification = u'{0}'.format(request.POST)
    print 'type of notification',type(notification)
    print notification
    cate_page = request.POST['cate-select']
    begin_page = int(request.POST['rangepagebegin'])
    end_page = int(request.POST['rangepageend'])
    #notification = 'notification'
    leech_bai(cate_page, begin_page, end_page)
    return render(request, 'drivingtest/notice.html', {'notification':notification})
def importul(request):
    #notification = u'dang import ul'
    
    txt = get_link_from_db()
    import_ul_txt_to_myul(txt)
    log=thongbao.log 
    return render(request, 'drivingtest/notice.html', {'notification':thongbao.thongbao,'log':log})
def get_thongbao(request):
    #del abcdef
    try:
        notification = thongbao.thongbao
        log = thongbao.thongbao

        '''
        notification = newPostProcess.numer_entry_post + newPostProcess.thongbao
        log = newPostProcess.postlog
        '''
    except Exception as e:
        print e
        notification = thongbao.thongbao
    #notification = 'da xoa'
    return render(request, 'drivingtest/notice.html', {'notification':notification,'log':log})
def stop_post(request):
    #del abcdef
    
    site_will_post = request.POST['forumchoice']
    print 'site_will_stop',site_will_post
    print 'type of site_will_post', type(site_will_post)
    for site in danhsachforum:
        if site['url'] == site_will_post:
            dict_site = site
    print >>sys.stderr ,'you choice',dict_site
    print 'so luong hien dang ton tai',len(postdict)
    try:
        exit_thread = postdict[dict_site['url']]
        if exit_thread.is_alive():
            postdict[dict_site['url']].stop()
            postdict[dict_site['url']].join()
            notification = 'luong da stop xong, bat dau chay'
            print 'luong da stop xong, bat dau chay'
    except Exception as e:
        print 'luong chua ton tai' ,e
    return render(request, 'drivingtest/notice.html', {'notification':notification})
def edit_entry(request,entry_id):
    entry = Ulnew.objects.get(id = entry_id)
    entryformsave = UlnewForm(request.POST,instance = entry)
    entryformsave.save()
    if entryformsave.is_valid():
        print 'valid'
    else:
        print entryformsave.errors
    notification = 'ban dang sua entry'
    #notification =  u'{0}'.format(request.body)
    #notification = 'da xoa'
    return render(request, 'drivingtest/notice.html', {'notification':notification})
import bbcode

def get_description(request):
    parser = bbcode.Parser()
    parser.add_simple_formatter('img', '<img  src="%(value)s">',replace_links=False)
    if request.method == 'GET':
        
        entry_id = request.GET['entry_id']
    entry = Ulnew.objects.get(id = entry_id)
    dllink=''
    if  entry.rg:
        dllink = dllink + '\n[code]' + entry.rg + '[/code]\n'
    if  entry.ul:
        dllink = dllink + '\n[code]' + entry.ul + '[/code]\n'    
    content = entry.description  + dllink
    html = parser.format(content)
    entry_form = UlnewForm(instance = entry) 
    #html = bbcode.render_html(content)
    notification =  html
    #notification = 'da xoa'
    return render(request, 'drivingtest/load_entry.html', {'notification':notification,'form':entry_form,'entry_id':entry_id})

def table(request):
    #return render(request, "drivingtest/people.html", {"people": Ulnew.objects.all()})
    table = PersonTable(Ulnew.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'drivingtest/people.html', {'table': table})

def tablep(request):
    table = PersonTable(Ulnew.objects.all())
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(request, 'drivingtest/people.html', {'table': table})












   
def index1(request):
    cate_list = Category.objects.annotate(num_linhkien=Count('linhkien')).order_by('-arrange_order_display')
    #cate_list.extra(order_by = ['-arrange_order_display'])
    last_OwnContact = OwnContact.objects.latest('id')
    
    
    id_product_list = "general_list"
    name = 'Sản Phẩm'
    
    try :
        number_product_display = int(last_OwnContact.number_product_san_pham)
    except:   
        number_product_display =7
    linhkien_lists = Linhkien.objects.all()
    linhkien_lists = order_linhkien(linhkien_lists)

    linhkien_lists = one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
    list_of_linhkien_lists = [linhkien_lists]
    if last_OwnContact.is_show_promote_product:
        linhkien_lists = Linhkien.objects.exclude(is_promote_sale__isnull=True).exclude(is_promote_sale__exact=0).order_by( '-is_promote_sale')
        if len(linhkien_lists) != 0:
            id_product_list = "promote"
            name = "ĐANG GIẢM GIÁ"
            try :
                number_product_display = int(last_OwnContact.number_product_promote)
            except:   
                number_product_display =4
            
            linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
            list_of_linhkien_lists.append(linhkien_lists)
    
    
    if last_OwnContact.is_best_sale_product:
        #linhkien_lists = Linhkien.objects.all().annotate(null_position=Count('is_best_sale')).order_by('-null_position', 'is_best_sale')
        linhkien_lists = Linhkien.objects.exclude(is_best_sale__isnull=True).exclude(is_best_sale__exact=0).order_by( '-is_best_sale')
        #linhkien_lists = Linhkien.objects.all().extra(select= {'null_position': 'CASE WHEN drivingtest_linhkien.is_best_sale IS NULL THEN 0 ELSE 1 END'}).order_by('-null_position', 'is_best_sale')


        if len(linhkien_lists) != 0:

            id_product_list = "best_sale"
            name = "SẢN PHẨM BÁN CHẠY"
            try :
                number_product_display = int(last_OwnContact.number_product_bestsell)
            except:   
                number_product_display =4
            linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
            list_of_linhkien_lists.append(linhkien_lists)
            
    
    showed_cate_list = Category.objects.all().filter(is_show_on_home_page=True).order_by('-arrange_order_display')
    for cate in showed_cate_list:
        
        linhkien_lists = Linhkien.objects.filter(category=cate)
        if len(linhkien_lists) == 0:
            continue
        try :
            number_product_display = int(cate.number_product_display_on_homepage)
        except:   
            number_product_display =8
        id_product_list = cate.cate_encode_url
        name = cate.name
        linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
        list_of_linhkien_lists.append(linhkien_lists)
    
    
    
    
    
    context_dict = {'list_of_linhkien_lists':list_of_linhkien_lists, 'cate_list':cate_list,'False':False, 'last_OwnContact':last_OwnContact}
   
    return render(request, 'drivingtest/index.html', context_dict)
def pagination_handle(request):
    context = RequestContext(request)
    if request.method == 'GET':
        
        page = request.GET['page']
        number_product_display = int(request.GET['number_product_display'])
        id_product_list = request.GET['id_product_list']
        if id_product_list == "general_list":
            #linhkien_lists = Linhkien.objects.all().annotate(null_position=Count('arrange_order')).order_by('-null_position', 'arrange_order')

            linhkien_lists = Linhkien.objects.all()
            linhkien_lists.extra(order_by = ['-last_edited_date','-arrange_order'])
            #linhkien_lists = Linhkien.objects.all().extra(select= {'null_position': 'CASE WHEN drivingtest_linhkien.arrange_order IS NULL THEN 0 ELSE 1 END'}).order_by('-null_position', '-arrange_order')
            paginator = Paginator(linhkien_lists, number_product_display)
            
        elif id_product_list == "promote":
            linhkien_lists = Linhkien.objects.exclude(is_promote_sale__isnull=True).exclude(is_promote_sale__exact=0).order_by( '-is_promote_sale')
            paginator = Paginator(linhkien_lists, number_product_display)
            
        elif id_product_list == "best_sale":
            linhkien_lists = Linhkien.objects.exclude(is_best_sale__isnull=True).exclude(is_best_sale__exact=0).order_by( '-is_best_sale')
            paginator = Paginator(linhkien_lists, number_product_display)
        elif id_product_list == "tim_kiem":
            query = request.GET['query']
            linhkien_lists = Linhkien.objects.filter(name__icontains=query)
            paginator = Paginator(linhkien_lists, number_product_display)    
        else:
            cate = Category.objects.get(cate_encode_url=id_product_list)
            linhkien_lists = Linhkien.objects.filter(category=cate)
            linhkien_lists.extra(order_by = ['-last_edited_date','-arrange_order'])
            paginator = Paginator(linhkien_lists, number_product_display)
        try:
            linhkien_lists = paginator.page(page)
        except PageNotAnInteger:
            linhkien_lists = paginator.page(1)
        except EmptyPage:
            linhkien_lists = paginator.page(paginator.num_pages)
        linhkien_lists.id_product_list = id_product_list
        
        context_dict = {'linhkien_lists':linhkien_lists}
    return render_to_response('drivingtest/pagination.html', context_dict, context)
def category(request, cate_encode_url):
    
    choose_cates=[]
    last_OwnContact = OwnContact.objects.latest('id')
    cate_list = Category.objects.annotate(num_linhkien=Count('linhkien')).order_by('-arrange_order_display')
    cate_encode_url_splits = cate_encode_url.split('&')
    name =''
    for x in cate_encode_url_splits[::-1]:
        
        choose_cate = Category.objects.get(cate_encode_url=x)
        choose_cates.append(choose_cate)
        name = name + " " + choose_cate.name
    
    id_product_list = cate_encode_url 
    #name = choose_cate.name
    
    try :
        number_product_display = int(last_OwnContact.number_product_san_pham)
    except:   
        number_product_display =7
    linhkien_lists =  Linhkien.objects.all()
    for choose_cate in choose_cates:
        linhkien_lists = linhkien_lists.filter(category=choose_cate)
    
    
    linhkien_lists = linhkien_lists.order_by('-last_edited_date').order_by('-arrange_order')
    
    linhkien_lists = one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
    list_of_linhkien_lists = [linhkien_lists]
    
    
    if last_OwnContact.is_show_promote_product:
        linhkien_lists = Linhkien.objects.exclude(is_promote_sale__isnull=True).exclude(is_promote_sale__exact=0).order_by( '-is_promote_sale')
        if len(linhkien_lists) != 0:
            id_product_list = "promote"
            name = "ĐANG GIẢM GIÁ"
            try :
                number_product_display = int(last_OwnContact.number_product_promote)
            except:   
                number_product_display =4
            
            linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
            list_of_linhkien_lists.append(linhkien_lists)
    
    
    if last_OwnContact.is_best_sale_product:
        #linhkien_lists = Linhkien.objects.all().annotate(null_position=Count('is_best_sale')).order_by('-null_position', 'is_best_sale')
        linhkien_lists = Linhkien.objects.exclude(is_best_sale__isnull=True).exclude(is_best_sale__exact=0).order_by( '-is_best_sale')
        #linhkien_lists = Linhkien.objects.all().extra(select= {'null_position': 'CASE WHEN drivingtest_linhkien.is_best_sale IS NULL THEN 0 ELSE 1 END'}).order_by('-null_position', 'is_best_sale')


        if len(linhkien_lists) != 0:

            id_product_list = "best_sale"
            name = "SẢN PHẨM BÁN CHẠY"
            try :
                number_product_display = int(last_OwnContact.number_product_bestsell)
            except:   
                number_product_display =4
            linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
            list_of_linhkien_lists.append(linhkien_lists)
    '''
    showed_cate_list = cate_list.filter(is_show_on_home_page=True).filter(~Q(id=cate_int_id))
    for cate in showed_cate_list:
        linhkien_lists = Linhkien.objects.filter(category=cate)
        if len(linhkien_lists) == 0:
            continue
        number_product_display = 4
        id_product_list = cate.id
        name = cate.name
        linhkien_lists =  one_product_list_index(linhkien_lists, id_product_list, name, number_product_display)
        list_of_linhkien_lists.append(linhkien_lists)
    '''
    
    
    
    context_dict = {'list_of_linhkien_lists':list_of_linhkien_lists, 'cate_list':cate_list,'False':False, 'last_OwnContact': OwnContact.objects.latest('id')}
   
    return render(request, 'drivingtest/index.html', context_dict)
def auto_create_owncontact (request):
    auto_create_owncontact_f()
    notification = "Da tao ok"
    return render(request, 'drivingtest/note.html', {'notification':notification})






def search_product(request):
        context = RequestContext(request)
        
        if request.method == 'GET':
                contain = request.GET['query']
        #print >>sys.stderr ,'abc',contain
        kq_searchs = Table3g.objects.filter(site_id_3g__icontains=contain)
        if not Table3g:
            kq_searchs = Table3g.objects.filter(site_id_2g_E__icontains=contain)
             
        context_dict = {'kq_searchs':kq_searchs}
        
        
        return render_to_response('drivingtest/kq_searchs.html', context_dict, context)
from django.db.models import CharField,DateTimeField

    





@login_required
def upload_file(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result_handle_file ="form is valid"
            if 'is_parent_category' not in request.POST:
                is_parent_category = False
            else:
                
                is_parent_category = request.POST['is_parent_category']
            #handle_uploaded_file(request.FILES['file'])
            fcontain = request.FILES['file'].read().decode('utf-8')
            result_handle_file = insert_to_db(read_txt(fcontain),is_parent_category)
            return render_to_response('drivingtest/upload_file.html', {'form': form,'result_handle_file':result_handle_file},context)
    else:
        form = UploadFileForm()
    return render_to_response('drivingtest/upload_file.html', {'form': form},context)
def handle_uploaded_file(f):
    SETTINGS_DIR = os.path.dirname(__file__)
    PROJECT_PATH1 = os.path.join(SETTINGS_DIR, os.pardir)
    PROJECT_PATH = os.path.abspath(PROJECT_PATH1)
    with open(PROJECT_PATH +'/media/upload/upload_file.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@login_required
def add_file(request):
    
    if 'picture' in request.FILES:
                saved_file_name= request.FILES['picture']
                return render(request, 'drivingtest/add_file.html', {'saved_file_name':saved_file_name})
    return render(request, 'drivingtest/add_file.html', {})
@login_required
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)
    
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cate = form.save(commit=False)
            cate.cate_encode_url = unidecoded4(cate.name)
            cate.save()
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
            return HttpResponse(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
    context_dict = {'form':form}
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('drivingtest/add_category.html', context_dict, context)

@login_required
def edit_category1(request, category_id):
    edited = False
    context = RequestContext(request)
    cate = Category.objects.get(id=int(category_id))
    if request.method == 'POST':
        if 'delete' in request.POST:
            cate.delete()
            return index(request)
        else:    
            cate.name = request.POST['name']
            if 'is_show_on_home_page' not in request.POST:
                cate.is_show_on_home_page = False
            else:
                cate.is_show_on_home_page = True
            if request.POST['arrange_order_display']:
                cate.arrange_order_display = request.POST['arrange_order_display']
                
            cate.save()
            edited = True
            return category(request, category_id)
    else:
        form = CategoryForm(instance=cate)
        return render_to_response('drivingtest/edit_category.html',
                {'form': form, 'edited':edited, 'category_id':category_id},
                 context)



@login_required
def edit_category(request, cate_encode_url):
    edited = False
    context = RequestContext(request)
    cate = Category.objects.get(cate_encode_url=cate_encode_url)
    if request.method == 'POST':
        
        if 'delete' in request.POST:
            cate.delete()
            return index(request)
        else:
            # http://stackoverflow.com/questions/3946036/how-do-i-update-an-instance-of-a-django-model-with-request-post-if-post-is-a-nes
            form = CategoryForm(request.POST, instance=cate)    
            cate = form.save(commit=False)
            
            form.save_m2m()
            edited = True
            
            
    
    form = CategoryForm(instance=cate)
    return render_to_response('drivingtest/edit_category.html',
            {'form': form, 'edited':edited, 'cate_encode_url':cate_encode_url},
             context)

@login_required
def add_owncontact(request):
    # Get the context from the request.
    context = RequestContext(request)
    
    
    if request.method == 'POST':
        form = OwnContactForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
            return HttpResponse(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = OwnContactForm()
    context_dict = {'form':form}
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('drivingtest/add_owncontact.html', context_dict, context)
@login_required
def edit_owncontact(request):
    context = RequestContext(request)
    last_OwnContact = OwnContact.objects.latest('id')
    db_name = db.settings.DATABASES['default']['NAME']
    if request.method == 'POST':
        form = OwnContactForm(request.POST, instance=last_OwnContact)
        # print >>sys.stderr ,request.POST
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            form.save()
            last_OwnContact = OwnContact.objects.latest('id')
            form = OwnContactForm(instance=last_OwnContact)
            #return render_to_response('drivingtest/edit_owncontact.html',
                #{'form': form}, context)
            return HttpResponseRedirect('/')
        else:
            print form.errors
            return HttpResponse(form.errors)
    else:
        form = OwnContactForm(instance=last_OwnContact)
        return render_to_response('drivingtest/edit_owncontact.html',
                {'form': form,'db_name':db_name}, context)
    
    
    
    
@login_required
def add_linhkien(request):
    try:
        last_linhkien = Linhkien.objects.latest('id')
    except:
        pass
    context = RequestContext(request)
    # pub_date = timezone.now()
    pub_date = datetime.now()
    # print >>sys.stderr ,pub_date
    # category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = LinhkienForm(request.POST, request.FILES)
        # print >>sys.stderr ,request.POST
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            linhkien = form.save(commit=False)
            linhkien.pub_date = pub_date
            linhkien.last_edited_date = pub_date
            linhkien.linhkien_encode_url = unidecoded4(linhkien.name)
            linhkien.save()
            
            form.save_m2m()
            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            return index(request)
        else:
            print form.errors
    else:
        try:
            form = LinhkienForm(initial={'arrange_order':str(last_linhkien.id + 1)})
        except:
            form = LinhkienForm()
            

    return render_to_response('drivingtest/add_linhkien.html',
            {'form': form},
             context)
@login_required
def add_linhkien1(request):
    try:
        last_linhkien = Linhkien.objects.latest('id')
    except:
        pass
    context = RequestContext(request)
    # pub_date = timezone.now()
    pub_date = datetime.now()
    # print >>sys.stderr ,pub_date
    # category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = LinhkienForm(request.POST)
        # print >>sys.stderr ,request.POST
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            linhkien = form.save(commit=False)
            linhkien.pub_date = pub_date
            linhkien.last_edited_date = pub_date
            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(id=request.POST['category'])
                linhkien.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('drivingtest/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            
            if 'picture' in request.FILES:
                linhkien.picture = request.FILES['picture']
            # With this, we can then save our new model instance.
            linhkien.save()

            # Now that the page is saved, display the category instead.
            return index(request)
        else:
            print form.errors
    else:
        try:
            form = LinhkienForm(initial={'arrange_order':str(last_linhkien.id + 1)})
        except:
            form = LinhkienForm()
            

    return render_to_response('drivingtest/add_linhkien.html',
            {'form': form},
             context)
@login_required
def delete_db(request):
    if 'are_you_sure' in request.POST:
        delete_db_from_load()
    else:
        return render(request,'drivingtest/delete_database.html')
    return HttpResponseRedirect('/')
@login_required
def edit_linhkien(request, linhkien_encode_url):
    edited = False
    context = RequestContext(request)
    last_edited_date = datetime.now()
    if request.method == 'POST':
        #linhkien = Linhkien.objects.get(id=int(linhkien_id))
        linhkien = Linhkien.objects.get(linhkien_encode_url=linhkien_encode_url)
        if 'delete' in request.POST:
            linhkien.delete()
            return index(request)
        form = LinhkienForm(request.POST, request.FILES, instance=linhkien)
        form.save(commit=False)
        linhkien.last_edited_date = last_edited_date
        linhkien.linhkien_encode_url = unidecoded4(linhkien.name)
        linhkien.save()
           
        form.save_m2m()
        #linhkien = Linhkien.objects.get(linhkien_encode_url=linhkien_encode_url)
        form = LinhkienForm(instance=linhkien)
        edited = True
        return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_encode_url':linhkien_encode_url},
             context)
    else:
        linhkien = Linhkien.objects.get(linhkien_encode_url=linhkien_encode_url)
        form = LinhkienForm(instance=linhkien)
    return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_encode_url':linhkien_encode_url},
             context)
@login_required
def edit_linhkien11(request, linhkien_id):
    edited = False
    context = RequestContext(request)
    last_edited_date = datetime.now()
    if request.method == 'POST':
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        if 'delete' in request.POST:
            linhkien.delete()
            return index(request)
        form = LinhkienForm(request.POST, instance=linhkien)
        form.save(commit=False)
        

     
        if 'picture' in request.FILES:
            linhkien.picture = request.FILES['picture']
        if 'icon_picture' in request.FILES:
            linhkien.icon_picture = request.FILES['icon_picture']
        linhkien.last_edited_date = last_edited_date
        linhkien.save()
        edited = True
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
        return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
    else:
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
    return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
    

@login_required
def edit_linhkien1(request, linhkien_id):
    edited = False
    context = RequestContext(request)
    last_edited_date = datetime.now()
    if request.method == 'POST':
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        if 'delete' in request.POST:
            linhkien.delete()
            return index(request)
        form = LinhkienForm(request.POST, instance=linhkien)
        form.save(commit=False)
        

     
        if 'picture' in request.FILES:
            linhkien.picture = request.FILES['picture']
        if 'icon_picture' in request.FILES:
            linhkien.icon_picture = request.FILES['icon_picture']
        linhkien.last_edited_date = last_edited_date
        linhkien.save()
        edited = True
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
        return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
    else:
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
    return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
    
@login_required
def edit_linhkien12(request, linhkien_id):
    edited = False
    context = RequestContext(request)
    last_edited_date = datetime.now()
    # category_name = decode_url(category_name_url)
    if request.method == 'POST':
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        if 'delete' in request.POST:
            # print >>sys.stderr ,'delete'
            linhkien.delete()
            return index(request)
            
        # print >>sys.stderr ,request.POST
        linhkien.pub_date = request.POST['pub_date']
        linhkien.description = request.POST['description']
        linhkien.name = request.POST['name']
        linhkien.price = request.POST['price']
        linhkien.old_price = request.POST['old_price']
        # print >>sys.stderr , request.POST['description']
        linhkien.borrowed_picture = request.POST['borrowed_picture']
        linhkien.borrowed_icon_picture = request.POST['borrowed_icon_picture']
        try:
            linhkien.arrange_order = request.POST['arrange_order']
        except:
            pass
        try:
            cat = Category.objects.get(id=request.POST['category'])
            linhkien.category = cat
        except Category.DoesNotExist:
  
            return render_to_response('drivingtest/add_category.html', {}, context)

        # Also, create a default value for the number of views.
        if 'icon_picture-clear' in request.POST:
            linhkien.icon_picture = ''
        if 'show_old_price' not in request.POST:
            linhkien.show_old_price = False
        else:
            linhkien.show_old_price = True
              
        if 'picture-clear' in request.POST:
            linhkien.picture = ''
        if 'picture' in request.FILES:
            linhkien.picture = request.FILES['picture']
        if 'icon_picture' in request.FILES:
            linhkien.icon_picture = request.FILES['icon_picture']
        linhkien.last_edited_date = last_edited_date
        # With this, we can then save our new model instance.
        linhkien.save()
        edited = True
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
        # Now that the page is saved, display the category instead.
        return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
    
    else:
        linhkien = Linhkien.objects.get(id=int(linhkien_id))
        form = LinhkienForm(instance=linhkien)
        

    return render_to_response('drivingtest/edit_linhkien.html',
            {'form': form, 'edited':edited, 'linhkien_id':linhkien_id},
             context)
        
def detail_linhkien(request, linhkien_encode_url):
    cate_list = Category.objects.annotate(num_linhkien=Count('linhkien')).order_by('-arrange_order_display')

    #linhkien = Linhkien.objects.get(id=int(linhkien_id))
    linhkien = Linhkien.objects.get(linhkien_encode_url=linhkien_encode_url)
    linhkien.view_number = linhkien.view_number + 1
    linhkien.save()
    context_dict = {'linhkien':linhkien, 'last_OwnContact': OwnContact.objects.latest('id'), 'cate_list':cate_list}
    return render(request, 'drivingtest/detail_linhkien.html', context_dict)




    


def about(request):
    
    return render(request, 'drivingtest/about.html', {'last_OwnContact':OwnContact.objects.latest('id')})

from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'drivingtest/crispy.html'
    form_class = ExampleForm
    username = 'nguyen ductu'
def ContactViewf (request):
    example_form = ExampleForm()
    #redirect_url = request.GET.get('next')
    template_name = 'drivingtest/crispy.html'
    #if redirect_url is not None:
        #example_form.helper.form_action = reverse('submit_survey') + '?next=' + redirectUrl

    return render_to_response(template_name, {'form': example_form,'username' : 'nguyen ductu'}, context_instance=RequestContext(request))