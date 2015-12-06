# -*- coding: utf-8 -*-
#from django.db.models import F
from crispy_forms.layout import Submit
from django.http.response import StreamingHttpResponse
from drivingtest.models import SpecificProblem, FaultLibrary
from time import sleep

print 'in views 5'
from django.views import generic

import datetime
import os
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from models import Category, Linhkien, OwnContact, Table3g, Ulnew,\
    ForumTable, PostLog, LeechSite, thongbao, postdict, Mll, Command3g, FNAME,\
    SearchHistory, H_Field, UserProfile, Doitac, CommentForMLL, Nguyennhan,\
    Catruc, TrangThaiCuaTram, Duan
    
from drivingtest.forms import CategoryForm, LinhkienForm, OwnContactForm,\
    UploadFileForm, Table3gForm, ForumChoiceForm, UlnewForm ,\
    TramTable, Mllform, MllTable, CommandTable, Commandform, SearchHistoryTable,\
    CommentForMLLForm, DoitacForm, ConfigCaForm, NTPform, Table3gForm_NTP_save,\
    NTP_Field, D4_DATETIME_FORMAT, DoitacFormFull, DoitacTable,\
    ConfigCaFilterMLLTable, SpecificProblemForm, FaultLibraryForm,\
    MllformForMLLFilter
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Count
from load_driving_tests import read_txt, insert_to_db, unidecoded4,\
    delete_db_from_load
from __main__ import sys
from create_owncontact import auto_create_owncontact_f
from django import db, forms
#from crispy_forms.utils import render_crispy_form  # importance
from fetch_website import danhsachforum, PostObject, CountTest, leech_bai,\
    get_link_from_db, init_d4, import_ul_txt_to_myul
from drivingtest.forms import PersonTable
from django_tables2 import RequestConfig
import operator
from django.conf import settings #or from my_project import settings
#from time import sleep
from itertools import chain
from toold4 import  recognize_fieldname_of_query
from LearnDriving.settings import MYD4_LOOKED_FIELD, FORMAT_TIME
#import json
from xu_ly_db_3g import tao_script_r6000_w12, import_database_4_cai_new
import xlrd
import itertools
import re
from exceptions import Exception
#from pip._vendor import requests
import ntpath
#from django.http.request import HttpRequest
from sendmail import send_email
from django_tables2_reports.config import RequestConfigReport as RequestConfig
#from twisted.web.test import requesthelper

#from django.views.generic.list import ListView

from django.db.models import CharField,DateTimeField,BooleanField
class QuanLyTrangThai(generic.ListView):
    template_name = 'drivingtest/quan_ly_trang_thai.html'
    context_object_name = 'trangthais'

    def get_queryset(self):
        """Return the last five published questions."""
        return TrangThaiCuaTram.objects.order_by('-id')[:5]
class DetailView(generic.DetailView):
    model = TrangThaiCuaTram
    template_name = 'polls/detail.html'
@login_required
def omckv2(request):
    #print 'request',request
    #mllform = Mllform(instance = Mll.objects.latest('id'))
    mllform = Mllform()
    commandform = Commandform()
    mlltable = MllTable(Mll.objects.all().order_by('-id'), prefix="mlltable-")
    lenhtable = CommandTable(Command3g.objects.all().order_by('-id'), prefix="commandtable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(mlltable) 
    #table = TramTable(Table3g.objects.all(), )
    table = TramTable(Table3g.objects.all(), )
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
    RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
    comment_form = CommentForMLLForm()
    #comment_form.fields['datetime'].widget = forms.HiddenInput()
    return render(request, 'drivingtest/omckv2.html',{'table':table,'mllform':mllform,'comment_form':comment_form,'commandform':commandform,'mlltable':mlltable,'lenhtable':lenhtable,'history_search_table':history_search_table})

def tram_table(request,no_return_httpresponse = False): # include search tram 
    print 'tram_table'
    if 'id' in request.GET:
        id = request.GET['id']
        querysets =[]
        kq_searchs_one_contain = Table3g.objects.get(id=id)
        querysets.append(kq_searchs_one_contain)
        print 'in in tram_table',id
        query = request.GET['query']
        save_history(query)
    elif 'query' not in request.GET and 'id' not in request.GET or (request.GET['query']=='')  : # khong search, khong chose , nghia la querysets khi load page index
        querysets = Table3g.objects.all()
    else: # tuc la if request.GET['query'], nghia la dang search:
        query = request.GET['query']
        if '&' in query:
            contains = request.GET['query'].split('&')
            query_sign = 'and'
        else:
            contains = request.GET['query'].split(',')
            query_sign = 'or'
        kq_searchs = Table3g.objects.none()
        for count,contain in enumerate(contains):
            contain_reconize_tuple = recognize_fieldname_of_query(contain,MYD4_LOOKED_FIELD)#return (longfieldname, searchstring)
            contain = contain_reconize_tuple[1]
            print 'contain',contain
            fieldnameKey = contain_reconize_tuple[0]
            if fieldnameKey=="all field":
                    qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME))
            else:
                print 'fieldnameKey %s,contain%s'%(fieldnameKey,contain)
                qgroup = Q(**{"%s__icontains" % fieldnameKey: contain})
            if not contain_reconize_tuple[2]:
                kq_searchs_one_contain = Table3g.objects.filter(qgroup)
            else:
                kq_searchs_one_contain = Table3g.objects.exclude(qgroup)
            if query_sign=="or": #tra nhieu tram.
                kq_searchs = list(chain(kq_searchs, kq_searchs_one_contain))
            elif query_sign=="and": # dieu kien AND but loop all field with or condition
                if count==0:
                    kq_searchs = kq_searchs_one_contain
                else:
                    kq_searchs = kq_searchs & kq_searchs_one_contain
        querysets = kq_searchs    
        save_history(query)    
    table = TramTable(querysets,)
    dict_context = {'table': table}
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    if no_return_httpresponse:
        return dict_context
    else:
        if 'download' in request.GET:
            return show_excel(request,Table3g,querysets) 
        return render(request, 'drivingtest/custom_table_template_mll.html', dict_context)
#URL  =  $.get('/omckv2/search_history/'

def mll_filter(request):
    print 'ban dang vao mll-filter trong view'
    user_profile_instance=request.user.get_profile()
    config_ca_filters = user_profile_instance.config_ca_filter_in_mll_table.all()
    if config_ca_filters:
        q_config_ca = reduce(operator.or_,(Q(ca_truc=config_ca_filter) for config_ca_filter in config_ca_filters))
    else:
        q_config_ca = None
    if 'subject' not in request.GET:#Nghia la not filter
        querysets = Mll.objects.all().order_by('-id')
        if q_config_ca:
            querysets = querysets.filter(q_config_ca)
        table = MllTable(querysets,prefix="mlltable-")
        RequestConfig(request, paginate={"per_page": 15}).configure(table)
        t = Template('''{% load render_table from django_tables2 %}{% render_table table "drivingtest/custom_table_template_mll.html" %}''')
        c = RequestContext(request,{'table':table})
        return HttpResponse(t.render(c))
    else: #Filter
        form = MllformForMLLFilter(request.GET)
        form.fields['subject'].required = False
        if not form.is_valid():
            notification_error_form = '<h3 class="error">Check wrong field again!</h3>'
            return render(request, 'drivingtest/mllformfilter.html',{'mllform':form,'notification':notification_error_form},status=400)
        else:
            not_auto_filter_fields = ['gio_mat','gio_tot','trang_thai','ca_truc','specific_problem']
            #fieldnames = [f.name for f in Mll._meta.fields if isinstance(f, CharField)]
            BooleanFieldnames = [f.name for f in Mll._meta.fields if (isinstance(f, BooleanField) and form.cleaned_data[f.name]==True)]
            charfieldnames = [f.name for f in Mll._meta.fields if (f.name not in not_auto_filter_fields and f.name not in BooleanFieldnames)]
            try:
                qgroup = reduce(operator.and_, (Q(**{fieldname: form.cleaned_data[fieldname]}) for fieldname in charfieldnames if form.cleaned_data[fieldname]))
            except TypeError:
                qgroup = Q(thiet_bi__icontains='')
            '''
            otherfieldnames = [f.name for f in Mll._meta.fields if (not isinstance(f, CharField) and f.name not in not_auto_filter_fields and f.name not in BooleanFieldnames)]
            try:
                q_other = reduce(operator.and_, (Q(**{fieldname: form.cleaned_data[fieldname]}) for fieldname in otherfieldnames if form.cleaned_data[fieldname]))
                qgroup = qgroup&q_other
            except TypeError:
                pass
            '''
            for fieldname in BooleanFieldnames:
                qgroup = qgroup & Q(**{fieldname:True})
            if request.GET['trang_thai']:
                qgroup = qgroup & Q(**{'trang_thai':form.cleaned_data['trang_thai']})
            if request.GET['comment']:
                print request.GET['comment']
                q_across = Q(comments__comment__icontains=request.GET['comment'])
                qgroup = qgroup&q_across
            if request.GET['gio_mat_lon_hon']: # loc nhung mll record co gio mat be hon gia tri nay
                d = form.cleaned_data['gio_mat']
                q_gio_mat = Q(gio_mat__lte=d)
                qgroup = qgroup & q_gio_mat
            if request.GET['gio_mat_lon_hon']:
                d = form.cleaned_data['gio_mat_lon_hon']
                q_gio_mat2 = Q(**{'gio_mat__gte':d})
                qgroup = qgroup & q_gio_mat2
            if request.GET['specific_problem_m2m']:
                q_across_fault = Q(specific_problems__fault__Name__icontains=request.GET['specific_problem_m2m'])
                q_across_object_name = Q(specific_problems__object_name__icontains=request.GET['specific_problem_m2m'])
                q_specific_problem_m2m = q_across_fault | q_across_object_name
                qgroup = qgroup & q_specific_problem_m2m
            if request.GET['doi_tac']:
                q_across_doi_tac = Q(comments__doi_tac__Full_name__icontains=request.GET['doi_tac'])
                #q_specific_problem_m2m = q_across_fault | q_across_object_name
                qgroup = qgroup & q_across_doi_tac
            kq_searchs = Mll.objects.filter(qgroup).order_by('-id')
            table = MllTable(kq_searchs,prefix="mlltable-")
            RequestConfig(request, paginate={"per_page": 15}).configure(table)
            notifcation_successfully_create = '<h3>ban vua loc, %s kq hien thi o table</h3>'%len(kq_searchs)     
            return render(request, 'drivingtest/mllformfilter_bundal.html',{'mllform':form,'notification':notifcation_successfully_create,'table':table})
            
            '''
            #Old
            t = Template({% load render_table from django_tables2 %}{% render_table table "drivingtest/custom_table_template_mll.html" %}')
            c = RequestContext(request,{'table':table})
            return HttpResponse(t.render(c))
            '''  
        
        '''
        if request.GET['ung_cuu']=='True':
            print 'ung cuu true'
            q_ungcuu = Q(ung_cuu=True)
            qgroup = qgroup & q_ungcuu
        nguyen_nhan_inputext = request.GET['nguyen_nhan']
        if nguyen_nhan_inputext:
            q_foreignkey_group = Q(nguyen_nhan__Name__icontains=nguyen_nhan_inputext)|Q(nguyen_nhan__Name_khong_dau__icontains=nguyen_nhan_inputext)   
            qgroup = qgroup & q_foreignkey_group
        
        
        gio_mat_str = request.GET['gio_mat']
        print 'gio_mat_str',gio_mat_str
        gio_mat2 = request.GET['gio_mat2']
        if gio_mat_str:
            d = datetime.strptime(gio_mat_str, D4_DATETIME_FORMAT)
            q_gio_mat = Q(gio_mat__lte=d)
            qgroup = qgroup & q_gio_mat
        if gio_mat2:
            print 'ok co gio mat'
            d = datetime.strptime(gio_mat2, D4_DATETIME_FORMAT)
            q_gio_mat2 = Q(**{'gio_mat__gte':d})
            qgroup = qgroup & q_gio_mat2
        doi_tac_text_input = request.GET['doi_tac_fr'].lstrip().rstrip()
        if doi_tac_text_input:
            doi_tac = luu_doi_tac(doi_tac_text_input)
            if doi_tac:
                g_doi_tac= Q(comments__doi_tac = doi_tac)
            qgroup = qgroup & g_doi_tac
            
        '''
        
    '''   
    if 'download' in request.GET:
        return show_excel(request,Mll,kq_searchs)
    else:
    '''       
        


        #return render(request, 'drivingtest/custom_table_template_mll.html', {'table': table})

def handlemodal(request,form_name,entry_id):
    form_class = eval(form_name)
    model_class = eval(form_name[:-4])
    print 'form_name,entry_id',form_name,entry_id
    #if form_name =='SpecificProblemForm':
    if request.method == "GET":
        form = form_class(instance = model_class.objects.get(id = entry_id ) )
        return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form,'modal_title':'EDIT','modal_title_style':""})
    elif request.method == "POST":
        if request.user.has_perm('drivingtest.can add on modal code'):
            pass
        else:
            return HttpResponse(u'Ban khong co quyen edit',status=403)
        if entry_id =="new":
            form = form_class(request.POST )
        else:
            form = form_class(request.POST,instance = model_class.objects.get(id = entry_id ) )
        if form.is_valid():
            form.save()
            return render_table_mll_with_notification(request,'ban vua edit 1 doi tuong cua %s '%form_name)
        else:
            return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form,'modal_title':'EDIT','modal_title_style':""},status=400)
    '''
    if form_name == 'FaultLibraryForm':
        if request.method == "GET":
            form = FaultLibraryForm(instance = FaultLibrary.objects.get(id = entry_id ) )
            return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form,'modal_title':'EDIT Fault Code','modal_title_style':""})
        elif request.method == "POST":
            form = FaultLibraryForm(request.POST,instance = FaultLibrary.objects.get(id = entry_id ) )
            form.save()
            return render_table_mll(request)
    '''
#from django.core.urlresolvers import resolve

def handelCommentForMLLForm(request,entry_id):
    comment_id = entry_id
    print '**entry_id**',entry_id
    if request.method == "GET":
        selected_instance_mll  = request.GET['selected_instance_mll']
        if comment_id =="new":
            form = CommentForMLLForm(initial={'mll':selected_instance_mll})
            modal_title = "ADD COMMENT"
            modal_title_style = "background-color:#337ab7"
        else: 
            comment_id = int(comment_id)
            comment_instance = CommentForMLL.objects.get(id = comment_id)
            form = CommentForMLLForm(instance=comment_instance)
            modal_title = "EDIT COMMENT"
            modal_title_style = "background-color:#ec971f"
        return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form,'modal_title':modal_title,'modal_title_style':modal_title_style})
    elif request.method == "POST":
        print '****POST***'
        #mll_instance  = Mll.objects.get(id=request.GET['selected_instance_mll'])
        
        if comment_id =="new": # ADD comment
            comment_instance = None
            modal_title = "ADD COMMENT"
            modal_title_style = "background-color:#337ab7"
            mll_instance  = Mll.objects.get(id=request.POST['mll'])
        else: # Edit
            modal_title = "EDIT COMMENT"
            modal_title_style = "background-color:#ec971f"
            comment_instance = CommentForMLL.objects.get(id= comment_id)
            mll_instance = comment_instance.mll    
            current_user = request.user
            author_user = comment_instance.thanh_vien
            if current_user!=author_user:
                return HttpResponse(u'Ban khong co quyen sua vi comment nay cua nguoi khac',status=403)
            olddatetime = comment_instance.datetime
        form = CommentForMLLForm(request.POST,instance=comment_instance)
        if form.is_valid():
            pass
        else:
            #current_url = resolve(request.path_info).url_name
            #print 'current_url',current_url
            form.helper.form_action = '/omckv2/adfasdfdf/'
            print 'form.errors.as_text()',form.errors.as_text()
            return render(request, 'drivingtest/edit-comment-form.html',{'comment_form':form,'modal_title':modal_title,'modal_title_style':modal_title_style},status=400)
        if form.cleaned_data['trang_thai'].Name==u'Cập nhập giờ tốt':
            # chi cap nhap gio tot khong luu comment form
            mll_instance.gio_tot = form.cleaned_data['datetime']
            mll_instance.save()
        else: # khong phai cap nhap gio tot
            comment_instance = form.save(commit = False)
            
            if comment_id !="new": 
                if not request.POST['datetime']:
                    comment_instance.datetime = olddatetime
            else:#if new
                
                comment_instance.mll = mll_instance
            comment_instance.thanh_vien = request.user
            comment_instance.save()
            form.save_m2m() 
            if form.cleaned_data['trang_thai'].is_cap_nhap_gio_tot:
                mll_instance.gio_tot = form.cleaned_data['datetime']
                mll_instance.save()
            if form.cleaned_data['trang_thai'].Name==u'Báo ứng cứu':
                mll_instance.ung_cuu = True
                mll_instance.save()
            
        update_trang_thai_cho_mll(mll_instance)    
        table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
        RequestConfig(request, paginate={"per_page": 15}).configure(table)        
        return render(request, 'drivingtest/custom_table_template_mll.html',{'table':table})
def prepare_value_for_specificProblem(x):
    return (x.fault.Name if x.fault else '') + (('**'+ x.object_name) if x.object_name else '')
def mll_form(request):
    mll_id = request.GET['mll_id']
    print 'mll_id',mll_id
    if mll_id =='submit-id-cancel': # For loading New form
        mllform = Mllform()
        notification = '<h3> Create new item </h3>'
    else: # for Edit
        mll_instance =  Mll.objects.get(id = int(mll_id))
        #specific_problem_m2m_value = ''
        specific_problem_m2m_value = '\n'.join(map(prepare_value_for_specificProblem,mll_instance.specific_problems.all()))
            
        mllform = Mllform(instance=mll_instance,initial = {'specific_problem_m2m':specific_problem_m2m_value})
        #mllform.helper.inputs[0].value = "EDIT"
        #mllform.helper.inputs.pop(0)
        #mllform.helper.inputs.insert(0,Submit('mll', 'MLL in view',css_class="right-btn-first"))
        mllform.fields['trang_thai'].widget.attrs.update({"readonly":"readonly"})
        mllform.id_value = mll_id
        notification = u'<h3>Editing item has ID:{0}, subject:{1}</h3>'.format(mll_instance.id,mll_instance.subject)
    return render(request, 'drivingtest/mllformfilter.html',{'mllform':mllform,'notification':notification})
   
@permission_required('drivingtest.d4_create_truc_ca_permission',raise_exception=True)
def luu_mll_form(request):
    #print 'request.POST',request.POST
    which_button = request.GET['which-button']
    if which_button =='Cancle':
        form = Mllform()
        notifcation = '<h3>Ready for create new item</h3>'
        
    else:
        mll_instance_id = request.POST['id'] # if has id mll is that edit , id is a field has hideninput widget
        print mll_instance_id
        is_create_MLL_entry = True if not mll_instance_id else False
        if is_create_MLL_entry: # Create MLL entry
            form = Mllform(request.POST)
        else:
            mll_id = int(mll_instance_id)
            instance = Mll.objects.get(id = int(mll_instance_id))
            form = Mllform(request.POST,instance=instance)
        
        if form.is_valid():
            mll_instance = form.save(commit=False)
        else:
            notification_error_form = '<h3 class="error">Check wrong field again!</h3>'
            return render(request, 'drivingtest/mllformfilter.html',{'mllform':form,'notification':notification_error_form},status=400)
        
        if is_create_MLL_entry:
            user = request.user
            mll_instance.thanh_vien = user
            mll_instance.ca_truc = user.get_profile().ca_truc
        else:#Edit mll
            update_trang_thai_cho_mll(mll_instance)
        now = datetime.now()
        mll_instance.last_update_time = now
        mll_instance.save()
        
        #if form.cleaned_data['specific_problem_m2m']:
        if not is_create_MLL_entry:
            specific_problems = mll_instance.specific_problems.all()
        specific_problem_m2ms = form.cleaned_data['specific_problem_m2m'].split('\n')
        print 'specific_problem_m2ms',specific_problem_m2ms
        for count,specific_problem_m2m in enumerate(specific_problem_m2ms):
            if '**' in specific_problem_m2m:
                faulcode_hyphen_objects = specific_problem_m2m.split('**')
                faultLibrary_instance = FaultLibrary.objects.get_or_create(Name = faulcode_hyphen_objects[0])[0] # dung de gan (fault = faultLibrary_instance)
                if len(faulcode_hyphen_objects) > 1:
                    object_name = faulcode_hyphen_objects[1]
                else:
                    object_name=None
                if not is_create_MLL_entry:
                    try:
                        specific_problem = specific_problems[count]
                        print 'current specific_problems',specific_problem.object_name
                        specific_problem.fault = faultLibrary_instance
                        specific_problem.object_name = object_name
                        specific_problem.save()
                    except IndexError:
                        SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=mll_instance)
                    
                else:
                    SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=mll_instance)
                    
            else:
                if not is_create_MLL_entry:
                    try:
                        specific_problem = specific_problems[count]
                        specific_problem.fault=None
                        specific_problem.object_name = specific_problem_m2m
                        specific_problem.save()
                    except IndexError:
                        SpecificProblem.objects.create(fault=None,object_name = specific_problem_m2m,mll=mll_instance)
                else:
                    SpecificProblem.objects.create(fault=None,object_name = specific_problem_m2m,mll=mll_instance)
        if not is_create_MLL_entry:
            for x in specific_problems[count+1:]:
                x.delete()
        if is_create_MLL_entry:
            CommentForMLLForm_i = CommentForMLLForm(request.POST)
            if CommentForMLLForm_i.is_valid():
                print "CommentForMLLForm_i['datetime']",CommentForMLLForm_i.cleaned_data['datetime']
                first_comment = CommentForMLLForm_i.save(commit=False)
                first_comment.thanh_vien = user
                first_comment.mll = mll_instance
                first_comment.save()
            else:
                return HttpResponseBadRequest('khong valid',CommentForMLLForm_i.errors.as_text())
            notifcation = '<h3>One item has been created successfully %s, continue with editing or click Cancel button for new item</h3>'%mll_instance.subject
        else:
            notifcation = '<h3>Object %s has Id %s edited successfully, continue with editing or click Cancel button for new item</h3>'%(mll_instance.subject,mll_id)    
        #RELOad new form
        form = Mllform(instance=mll_instance)
    
    
    table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)
    return render(request, 'drivingtest/mllformfilter_bundal.html',{'mllform':form,'notification':notifcation,'table':table})


from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def show_excel(request,model=None,kqsearchs=None):
    if not model:
        model = Table3g
        kqsearchs=model.objects.all()[:20]
    fields = model._meta.fields
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    header_row =[]
    for field in fields:
        header_row.append(field.verbose_name)
    writer.writerow(header_row)
    for count,obj in enumerate(kqsearchs):
        print count
        row = []
        for field in fields:
            if isinstance(field, DateTimeField):
                giomat = getattr(obj, field.name)
                if giomat:
                    dt = timezone.localtime(giomat).strftime(D4_DATETIME_FORMAT)
                    print dt
                    row.append(dt)
                else:
                    row.append(str(getattr(obj, field.name)))
            elif field.name == "cac_buoc_xu_ly":
                querysetcm = obj.comments.all().order_by("id")
                cms =  obj.cac_buoc_xu_ly 
                for comment in querysetcm:
                    cms = cms + ' '   +(timezone.localtime(comment.datetime)).strftime(D4_DATETIME_FORMAT)+ '(' +  comment.thanh_vien + "): " + comment.comment +'\n'
                row.append(cms)
            else:
                row.append(str(getattr(obj, field.name)))
        writer.writerow(row)
    return response
def generator_csv(kqsearchs,fields,writer):
    for obj in kqsearchs:
        row = []
        for field in fields:
            if isinstance(field, DateTimeField):
                giomat = getattr(obj, field.name)
                if giomat:
                    dt = timezone.localtime(giomat).strftime(D4_DATETIME_FORMAT)
                    print dt
                    row.append(dt)
                else:
                    row.append(str(getattr(obj, field.name)))
            elif field.name == "cac_buoc_xu_ly":
                querysetcm = obj.comments.all().order_by("id")
                cms =  obj.cac_buoc_xu_ly 
                for comment in querysetcm:
                    cms = cms + ' '   +(timezone.localtime(comment.datetime)).strftime(D4_DATETIME_FORMAT)+ '(' +  comment.thanh_vien + "): " + comment.comment +'\n'
                row.append(cms)
            else:
                row.append(str(getattr(obj, field.name)))
        yield row
class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
    
def show_excel_old(request,model=None,kqsearchs=None):
    if not model:
        model = Table3g
        kqsearchs=model.objects.all()[:20]
    fields = model._meta.fields
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    #writer = csv.writer(response)
    generator_csv_generator = generator_csv(kqsearchs,fields,writer)
    #response = StreamingHttpResponse((writer.writerow(row) for row in generator_csv_generator),
    #                                content_type="text/csv")
    response = StreamingHttpResponse((writer.writerow(row) for row in generator_csv_generator),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

    header_row =[]
    for field in fields:
        header_row.append(field.verbose_name)
    writer.writerow(header_row)
    generator_csv(kqsearchs,fields,writer)
        
    return response
def download_script_ntp(request):
    sendmail=0
    site_id = request.GET['site_id']
    print 'site_id',site_id
    instance_site = Table3g.objects.get(id=site_id)
    sitename = instance_site.site_id_3g
    if not sitename:
        return HttpResponseBadRequest('khong ton tai site 3G cua tram nay')
    tao_script= tao_script_r6000_w12( instance_site,ntpServerIpAddressPrimary = request.GET['ntpServerIpAddressPrimary'],\
                              ntpServerIpAddressSecondary= request.GET['ntpServerIpAddressSecondary'],\
                               ntpServerIpAddress1= request.GET['ntpServerIpAddress1'],\
                                ntpServerIpAddress2 = request.GET['ntpServerIpAddress2'])
    if tao_script[0]:
        file_names = tao_script[0]
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        for file_name in  file_names:
            filename = settings.MEDIA_ROOT + '/for_user_download_folder/' + file_name # Select your file here.                              
            archive.write(filename, ntpath.basename(filename))
        archive.close()
    else: # neu khong co list file, tuc la tao_script_r6000_w12 da tao file zip roi
        temp = tao_script[1]
    loai_tu = tao_script[2]
    basename = sitename+"_"+ loai_tu +'.zip'
    if sendmail:
        send_email(files= temp,filetype='tempt',fname = basename)
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s'%(basename)
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response 

def edit_history_search(request):
    
    try:
        id_h = request.GET['history_search_id']
        try:
            print 'id_h',id_h
            instance = SearchHistory.objects.get(id=int(id_h))
        except:
            print 'loi tai instance nay'
        if request.GET['action']=="edit":
            #instance = SearchHistory.objects.get(id=id_h)
            print request.GET
            for f in H_Field:
                if f in request.GET:
                    value = request.GET[f] 
                    if value!= u'—':
                        setattr(instance,f,value)
                        instance.save()
                        history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
        else:
            
            instance.delete()
            #request.session.flush()
        history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
        RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
        return render(request, 'drivingtest/custom_table_template_mll.html',{'table':history_search_table})           
    except Exception as e:
        print type(e),e
        return HttpResponse(str(e))
from django.template import Context,Template 
def load_form_config_ca(request):
    if request.GET['loai_form'] =='config_ca':
        form = ConfigCaForm(initial = {'ca_truc':request.user.get_profile().ca_truc})
        t = Template('''
        <form>
        {% csrf_token %}
        {{form}}
        <button type="submit" class="btn btn-primary" id="config_ca_btn">Chọn Ca Trực</button>
        </form>
        ''')
   
        c = RequestContext(request,{ 'form': form })
        #c = Context({ 'form': form })
        #rendered = t.render(c)
        return HttpResponse(t.render(c))
    elif request.GET['loai_form'] =='NTP':
        instance_site = Table3g.objects.get(id = request.GET['site_id'])
        #form = NTPform()
        form = Table3gForm_NTP_save(instance = instance_site)
        rnc = instance_site.RNC
        IUB_VLAN_ID = instance_site.IUB_VLAN_ID
        same_sites = Table3g.objects.filter(RNC=rnc,IUB_VLAN_ID=IUB_VLAN_ID)
        table = TramTable(same_sites)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'drivingtest/ntpform.html',{'form':form,'table':table}) 
def ntpform(request):
    form = NTPform()
    table = TramTable(Table3g.objects.all(), )
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    return render(request, 'drivingtest/ntpform.html',{'form':form,'table':table})
def config_ca_filter_mll_table(request):
    
    if request.method =='GET':
        user_profile_instance=request.user.get_profile()
        form = ConfigCaFilterMLLTable(instance =user_profile_instance)
        return render(request, 'drivingtest/modal_config_ca.html',{'form':form})
    elif request.method =='POST':
        user_profile_instance=request.user.get_profile()
        form = ConfigCaFilterMLLTable(request.POST,instance =user_profile_instance)
        form.save()
        #form.save(commit=False)
        #form.save_m2m()
        print '###ca_muon_show',request.POST.getlist('ca_muon_show')
        return render(request, 'drivingtest/modal_config_ca.html',{'form':form})
        #return HttpResponse('ok')
@login_required
def config_ca(request):#response the request form:
    print 'request.POST',request.POST
    loai_form = request.POST['loai_form']
    print 'loai_form',loai_form
    if loai_form =='config_ca':
        print 'branch config ca'
        thanh_vien =   request.user
        ca_truc = Catruc.objects.get(id= request.POST['ca_truc'])
        profile = UserProfile.objects.get_or_create(user =thanh_vien)
        if profile[1]: # tao:
            profile[0].ca_truc = ca_truc
            profile[0].save()
        else: # p exit
            profile[0].ca_truc = ca_truc
            profile[0].save()
        return HttpResponse('Ca ' + profile[0].ca_truc.Name)
    elif loai_form == 'NTP': #UPdate NTP ip to database
        site_id = request.POST['site_id']
        print 'site_id',site_id
        instance_site = Table3g.objects.get(id=site_id)
        rnc = instance_site.RNC
        IUB_VLAN_ID = instance_site.IUB_VLAN_ID
        same_sites = Table3g.objects.filter(RNC=rnc,IUB_VLAN_ID=IUB_VLAN_ID)
        same_sites.update(**dict([(fn,request.POST[fn])for fn in NTP_Field]))
        form = Table3gForm_NTP_save(request.POST,instance=instance_site)
        table = TramTable(same_sites)
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'drivingtest/ntpform.html',{'form':form,'table':table}) 
        
        
        form.save()
        t = Template('''{{form.as_p}}''')
        c = RequestContext(request,{'form':form})
        return HttpResponse(t.render(c))
         


def edit_doi_tac_table_save(request):
    id = request.GET['history_search_id']
    if id :
        doitac_instance = Doitac.objects.get(id = id)
    else:
        doitac_instance = None
    print doitac_instance
    form = DoitacFormFull(request.GET,instance = doitac_instance)
    if form.is_valid():
        form.save()
        print 'da save doi tac form'
    else:
        form_e = form.errors
        print form_e
        return HttpResponse(str(form_e))
    doi_tac_table = DoitacTable(Doitac.objects.all() )
    RequestConfig(request, paginate={"per_page": 10}).configure(doi_tac_table)
    t = Template('''{% load render_table from django_tables2 %}{% render_table table %}''')
    c = RequestContext(request,{'table':doi_tac_table})
    return HttpResponse(t.render(c))
        

def quan_ly_doi_tac(request):
    form = DoitacFormFull()
    doi_tac_table = DoitacTable(Doitac.objects.all() )
    RequestConfig(request, paginate={"per_page": 10}).configure(doi_tac_table)
    return render(request, 'drivingtest/quan_ly_doi_tac.html',{'form':form,'table':doi_tac_table})
from django.utils.safestring import SafeString
def testcontext(request):
    return HttpResponse(SafeString('<h3>dfdsdfdfd</h3>'))
    #return render(request, 'drivingtest/testcontext.html',{'some_list':range(5)})

def doitac_table_sort(request):
    doi_tac_table = DoitacTable(Doitac.objects.all() )
    RequestConfig(request, paginate={"per_page": 10}).configure(doi_tac_table)
    t = Template('''{% load render_table from django_tables2 %}{% render_table table %}
    ''')
    c = RequestContext(request,{'table':doi_tac_table})
        #rendered = t.render(c)
    return HttpResponse(t.render(c))
    
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
                    sdtfield = fieldnames.pop(2)
                    p = re.compile('[\d\s]{3,}')
                    kq= p.search(doi_tac_inputext)
                    try:
                        phone_number_index_of_ = kq.start()
                        #Define the index of number phone in array, 0 or 1, or 2, or 3
                        std_index = len(re.findall('-',doi_tac_inputext[:phone_number_index_of_]))
                        fieldnames.insert(std_index, sdtfield)
                    except:
                        pass
                    dictx = dict(zip(fieldnames,doi_tac_inputexts))
                    doitac = Doitac.objects.get_or_create(**dictx)[0]
                return doitac
    else:
        return None

def load_empty_mll_form(request):
    form = Mllform()
    return render(request, 'drivingtest/mllformfilter.html',{'mllform':form})


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
    
def description_for_search_tram_autocomplete(tram,*args):
    output =''
    last_index = len(args) -1 
    for count, fieldname in enumerate(args):
        value = getattr(tram,fieldname)
        sortname =  MYD4_LOOKED_FIELD[fieldname]
        output += '<span class="tram_field_name">'+sortname+ ': ' +'</span>'+ (value if value else '___' )+ (' , ' if not count==last_index else '') 
    return output        
def autocomplete (request):
    print request.GET
    query   = request.GET['query'].lstrip().rstrip()
    print 'ban dang search',query
    name_attr = request.GET['name_attr']
    results = [] # results la 1 list gom nhieu dict, moi dict la moi li , moi dict la moi ket qua tim kiem
    if name_attr =='nguyen_nhan':
        fieldnames = [f.name for f in Nguyennhan._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        doitac_querys = Nguyennhan.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] = doitac.Ghi_chu  if doitac.Ghi_chu else ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
    elif name_attr =='du_an':
        fieldnames = [f.name for f in Duan._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        doitac_querys = Duan.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] =  ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
    elif 'trang_thai' in name_attr:
        fieldnames = [f.name for f in TrangThaiCuaTram._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        doitac_querys = TrangThaiCuaTram.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] =  ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
        
    elif name_attr =='doi_tac' :
        fieldnames = [f.name for f in Doitac._meta.fields if isinstance(f, CharField)  ]
        if '-' not in query:
            print 'fieldnames',fieldnames
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
            doitac_querys = Doitac.objects.filter(qgroup)
            for doitac in doitac_querys[:10]:
                doitac_dict = {}
                doitac_dict['label'] = doitac.Full_name + ("-" + doitac.Don_vi if doitac.Don_vi else "") 
                doitac_dict['desc'] = doitac.So_dien_thoai if doitac.So_dien_thoai else 'chưa có sdt'
                results.append(doitac_dict)
            to_json = {
                "key_for_list_of_item_dict": results,
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
                "key_for_list_of_item_dict": results,
            }
    elif name_attr =='subject' or name_attr =="main_suggestion":
        contain = query
        if contain =='':
            fieldnames = {'site_id_3g':'3G'}
        else:
            fieldnames = MYD4_LOOKED_FIELD
        
        for fieldname,sort_fieldname  in fieldnames.iteritems(): #Loop through all field
            q_query = Q(**{"%s__icontains" % fieldname: contain})
            one_kq_searchs = Table3g.objects.filter(q_query)[0:20]
            if len(one_kq_searchs)>0:
                for tram in one_kq_searchs:
                    tram_dict = {}
                    try:
                        if fieldname =="site_id_3g":
                            thiet_bi = tram.Cabinet
                        elif fieldname =="site_ID_2G":
                            thiet_bi =tram.nha_san_xuat_2G
                        else:
                            thiet_bi = "2G&3G"
                    except Exception as e:
                            thiet_bi = 'error' + tram.site_name_1
                            #print e, tram
                    tram_dict['id'] = tram.id
                    tram_dict['sort_field'] = sort_fieldname
                    tram_dict['label'] =  getattr(tram,fieldname)
                    tram_dict['thiet_bi'] =  thiet_bi
                    tram_dict['site_name_1'] = tram.site_name_1
                    tram_dict['desc'] = description_for_search_tram_autocomplete(tram ,'site_name_1','site_name_2',)
                    tram_dict['desc2'] = description_for_search_tram_autocomplete(tram ,'site_id_3g','site_ID_2G')
                    results.append(tram_dict)
        to_json = {
                "key_for_list_of_item_dict": results,
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
def render_table_mll(request):
    table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/custom_table_template.html',{'table':table})
def render_table_mll_with_notification(request,notifcation):
    table = MllTable(Mll.objects.all().order_by('-id'),prefix="mlltable-")
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/table_and_notification.html',{'table':table,'notification':notifcation})
def delete_mll (request):
    id = request.GET['query']
    mll_instance  = Mll.objects.get(id=int(id))
    mll_instance.comments.all().delete()
    mll_instance.delete()
    return render_table_mll(request)

def update_trang_thai_cho_mll(mll_instance):
    last_comment_instance = mll_instance.comments.latest('id')
    mll_instance.trang_thai = last_comment_instance.trang_thai
    mll_instance.save()


from django.core.servers.basehttp import FileWrapper
#'/show_detail_tram/'
def show_detail_tram(request,no_return_httpresponse = False):
        print 'show_detail_tram '
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
                    print 'contain',contain
                    q_query = Q(**{"%s" % fieldname: contain})
                    tram = Table3g.objects.get(q_query)
            except Exception as e:
                print type(e),e
        table3g_form =Table3gForm (instance=tram)
        context_dict = {'table3g_form':table3g_form,}
        if no_return_httpresponse:
            return context_dict
        else:
            t = Template('''{% load crispy_forms_tags %}
    {% crispy table3g_form  %}''')
            c = RequestContext(request,context_dict)
            return HttpResponse(t.render(c))

def detail_tram_compact_with_search_table(request):
    context_dict = {}
    context_dict_detail_tram = show_detail_tram(request,no_return_httpresponse=True)
    context_dict.update(context_dict_detail_tram)
    context_dict_tram_table = tram_table(request,no_return_httpresponse=True)
    context_dict.update(context_dict_tram_table)
    return render(request, 'drivingtest/detail_tram_compact_with_search_table.html',context_dict)
#URL = /omckv2/tram_table/

def search_history(request):
    history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
    RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
    return render(request, 'drivingtest/custom_table_template_mll.html',{'table':history_search_table})

def edit_site(request):
    print request.POST
    site_id = request.POST['site_id']
    site_instance = Table3g.objects.get(id=site_id)
    form = Table3gForm(request.POST,instance=site_instance)
    form.save()
    context_dict = {'table3g_form':form,}
    t = Template('''{% load crispy_forms_tags %}{% crispy table3g_form  %}''')
    c = RequestContext(request,context_dict)
    return HttpResponse(t.render(c))
def save_history(query):
    if (SearchHistory.objects.all().count() > 200 ):
                oldest_instance= SearchHistory.objects.all().order_by('search_datetime')[0]
                oldest_instance.query_string = query
                oldest_instance.search_datetime = datetime.now()
                oldest_instance.save()
    else:
        instance = SearchHistory(query_string=query,search_datetime = datetime.now())
        instance.save()

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
    print request
    
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
            choices =  form.cleaned_data['sheetchoice']
            is_available_file =  form.cleaned_data['is_available_file']
            print 'is_available_file',is_available_file
            if not is_available_file: #must file upload
                if 'file' in request.FILES:
                    fcontain = request.FILES['file'].read()
                    workbook = xlrd.open_workbook(file_contents=fcontain)
                    import_database_4_cai_new(choices,workbook = workbook,is_available_file=False)
                else: # but not file upload so render invalid
                    result_handle_file = 'Invalid choices, please select file or tick into "is_available_file"'
                    return render_to_response('drivingtest/upload_excel_file.html', {'form': form,'result_handle_file':result_handle_file},context)
            else:
                import_database_4_cai_new(choices,workbook = None,is_available_file=is_available_file)
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

def download_script(request,file_names=None):
    """                                                                         
    Create a ZIP file on disk and transmit it in chunks of 8KB,                 
    without loading the whole file into memory. A similar approach can          
    be used for large dynamic PDF files.                                        
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    file_names = ['KG5733_IUB_W12_3.mo','KG5733_OAM_W12_1.xml','KG5733_SE-2carriers_2.xml']
    for file_name in  file_names:
        script_file = settings.MEDIA_ROOT + '/for_user_download_folder/' + file_name # Select your file here.                              
        archive.write(script_file, file_name)
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


from drivingtest.forms import UserForm, UserProfileForm

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        user_form.is_valid() 
        print '@@#$#',user_form.cleaned_data['email']
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
    
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
    
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
    
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            '''
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            '''
    
            # Now we save the UserProfile model instance.
            profile.save()
    
            # Update our variable to tell the template registration was successful.
            registered = True
    
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'drivingtest/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

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
            kq_searchs = Table3g.objects.filter(site_ID_2G__icontains=contain)
             
        context_dict = {'kq_searchs':kq_searchs}
        
        
        return render_to_response('drivingtest/kq_searchs.html', context_dict, context)


    





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
