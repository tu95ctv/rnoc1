# -*- coding: utf-8 -*-
#from django.db.models import F
from models import SpecificProblem, FaultLibrary, EditHistory
from django.db.models.fields.related import ForeignKey, ManyToManyField
import os
from django.template import RequestContext
from django.shortcuts import render_to_response, render
import models
from models import Tram, Mll, Lenh,SearchHistory, H_Field, DoiTac, SuCo,TrangThai, DuAn

from forms import  UploadFileForm, TramForm, \
    TramTable, MllForm, MllTable, LenhTable, LenhForm, SearchHistoryTable,\
    CommentForm,  NTP_Field,ModelManagerForm, UserProfileForm_re
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
import sys  
import collections
import tempfile, zipfile
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from rnoc.models import NguyenNhan, ThaoTacLienQuan
reload(sys)  
sys.setdefaultencoding('utf-8')
import operator
from django.conf import settings #or from my_project import settings
from itertools import chain
from toold4 import  recognize_fieldname_of_query, luu_doi_tac_toold4,\
    prepare_value_for_specificProblem
#from LearnDriving.settings import MYD4_LOOKED_FIELD
from xu_ly_db_3g import tao_script, import_database_4_cai_new
import xlrd
import re
from exceptions import Exception
import ntpath
from sendmail import send_email
from django_tables2_reports.config import RequestConfigReport as RequestConfig


from django.db.models import CharField,DateTimeField
from django.utils import  simplejson, timezone
from rnoc.forms import UserForm, UserProfileForm
import forms#cai nay quan trong khong duoc xoa

ship = (("Site_ID_2G",'2G'),
        ("Site_ID_3G",'3G'),
        ("eNodeB_Name","4G"),
        ("Site_Name_1", "SN1"),
        ("Site_Name_2", 'SN2'))
MYD4_LOOKED_FIELD = collections.OrderedDict(ship)
SHORT_DATETIME_FORMAT = "Y-m-d H:i"
################CHUNG######################
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
        profile_form = UserProfileForm_re(data=request.POST)

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





#####OMC###############



@login_required
def omckv2(request):
    #print 'request',request
    #mllform = MllForm(instance = Mll.objects.latest('id'))
    #now = timezone.now()
    tramform = TramForm()
    mllform = MllForm()
    commandform = LenhForm()
    mlltable = MllTable(Mll.objects.all().order_by('-id'))
    RequestConfig(request, paginate={"per_page": 15}).configure(mlltable) 
    lenhtable = LenhTable(Lenh.objects.all().order_by('-id'))
    RequestConfig(request, paginate={"per_page": 15}).configure(lenhtable) 
    #table = TramTable(Tram.objects.all(), )
    tramtable = TramTable(Tram.objects.all(), )
    RequestConfig(request, paginate={"per_page": 10}).configure(tramtable)
    history_search_table = SearchHistoryTable(SearchHistory.objects.all().order_by('-search_datetime'), )
    RequestConfig(request, paginate={"per_page": 10}).configure(history_search_table)
    model_manager_form = ModelManagerForm()
    #comment_form.fields['datetime'].widget = forms.HiddenInput()
    return render(request, 'drivingtest/omckv2.html',{'tramtable':tramtable,'tramform':tramform,'mllform':mllform,\
            'commandform':commandform,'mlltable':mlltable,'lenhtable':lenhtable,'history_search_table':history_search_table,'model_manager_form':model_manager_form})

def tram_table(request,no_return_httpresponse = False): # include search tram 
    print 'tram_table'
    if 'id' in request.GET:
        id = request.GET['id']
        querysets =[]
        kq_searchs_one_contain = Tram.objects.get(id=id)
        querysets.append(kq_searchs_one_contain)
        query = request.GET['query']
        save_history(query)
    elif 'query' not in request.GET and 'id' not in request.GET or (request.GET['query']=='')  : # khong search, khong chose , nghia la querysets khi load page index
        querysets = Tram.objects.all()
    elif 'query' in request.GET : # tuc la if request.GET['query'], nghia la dang search:
        query = request.GET['query']
        print 'this mine',query
        if '&' in query:
            contains = request.GET['query'].split('&')
            query_sign = 'and'
        else:
            contains = request.GET['query'].split(',')
            query_sign = 'or'
        kq_searchs = Tram.objects.none()
        for count,contain in enumerate(contains):
            fname_contain_reconize_tuple = recognize_fieldname_of_query(contain,MYD4_LOOKED_FIELD)#return (longfieldname, searchstring)
            contain = fname_contain_reconize_tuple[1]
            print 'contain',contain
            fieldnameKey = fname_contain_reconize_tuple[0]
            print 'fieldnameKey',fieldnameKey
            if fieldnameKey=="all field":
                    FNAME = [f.name for f in Tram._meta.fields if isinstance(f, CharField)]
                    qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME ))
                    FRNAME = [f.name for f in Tram._meta.fields if (isinstance(f, ForeignKey) or isinstance(f, ManyToManyField))]
                    print 'FRNAME',FRNAME
                    Many2manyfields =[f.name for f in Tram._meta.many_to_many]
                    print 'Many2manyfields',Many2manyfields
                    FRNAME  = FRNAME + Many2manyfields
                    qgroup_FRNAME = reduce(operator.or_, (Q(**{"%s__Name__icontains" % fieldname: contain}) for fieldname in FRNAME ))
                    qgroup = qgroup | qgroup_FRNAME
            else:
                print 'fieldnameKey %s,contain%s'%(fieldnameKey,contain)
                qgroup = Q(**{"%s__icontains" % fieldnameKey: contain})
            if not fname_contain_reconize_tuple[2]:#neu khong query phu dinh
                kq_searchs_one_contain = Tram.objects.filter(qgroup)
            else:
                kq_searchs_one_contain = Tram.objects.exclude(qgroup)
            if query_sign=="or": #tra nhieu tram.
                kq_searchs = list(chain(kq_searchs, kq_searchs_one_contain))
            elif query_sign=="and": # dieu kien AND but loop all field with or condition
                if count==0:
                    kq_searchs = kq_searchs_one_contain
                else:
                    kq_searchs = kq_searchs & kq_searchs_one_contain
        querysets = kq_searchs
        print 'len(querysets)',len(querysets)    
        #save_history(query)    
    
    if no_return_httpresponse:
        return querysets
    else:
        table = TramTable(querysets,) 
        dict_context = {'table': table}
        RequestConfig(request, paginate={"per_page": 10}).configure(table)
        return render(request, 'drivingtest/custom_table_template_mll.html', dict_context)
#URL  =  $.get('/omckv2/search_history/'
# DELETE SOMETHING ON SURFACE AND C          
class FilterToGenerateQ():
    def __init__(self,request,FormClass,ModelClass,form_cleaned_data,No_AUTO_FILTER_FIELDS=[]):
        self.form_cleaned_data = form_cleaned_data
        self.EXCLUDE_FIELDS = getattr(FormClass.Meta,'exclude', [])
        self.No_AUTO_FILTER_FIELDS = No_AUTO_FILTER_FIELDS
        self.ModelClass = ModelClass
        self.request = request
    def generateQgroup(self):
        qgroup=Q()
        f_songs = []
        #CHARFIELDS = []
        for f in self.ModelClass._meta.fields :
            
            try:
                if not self.request.GET[f.name] or self.form_cleaned_data[f.name]==None  or  (f.name  in self.EXCLUDE_FIELDS) or  (f.name  in self.No_AUTO_FILTER_FIELDS)  :
                    print 'f.namef.namef.namef.namef.namef.namef.name',f.name
                    continue
            except :#MultiValueDictKeyError
                continue
            f_songs.append(f.name)
            functionname = 'generate_qobject_for_exit_model_field_'+f.name
            no_auto_function = getattr(self, functionname,None)
            print ('functionname, f',functionname,no_auto_function)
            if no_auto_function:
                g_no_auto = no_auto_function(f.name)
                qgroup &=g_no_auto
            elif isinstance(f,CharField):
                if self.form_cleaned_data[f.name]==u'*':
                    qgroup &= ~Q(**{'%s__isnull'%f.name:True}) & ~Q(**{'%s__exact'%f.name:''})
                elif self.form_cleaned_data[f.name]==u'!':
                    qgroup &= Q(**{'%s__isnull'%f.name:True}) | Q(**{'%s__exact'%f.name:''})
                else:
                    qgroup &=Q(**{'%s__icontains'%f.name:self.form_cleaned_data[f.name]})
            elif isinstance(f,DateTimeField):
                pass
            else:
                qgroup &=Q(**{'%s'%f.name: self.form_cleaned_data[f.name]})
        #MANYTOMANYFIELDS
        print 'f_songsf_songsf_songsf_songsf_songsf_songsf_songsf_songs',f_songs 
        for f in self.ModelClass._meta.many_to_many :
            try:
                if not self.request.GET[f.name]:
                    continue
            except :#MultiValueDictKeyError
                continue
            print '****many to manu self.form_cleaned_data[f.name]',self.form_cleaned_data[f.name]
            if (f.name not in self.EXCLUDE_FIELDS) and (f.name not in self.No_AUTO_FILTER_FIELDS):
                qgroup &=Q(**{'%s__in'%f.name:self.form_cleaned_data[f.name]})
        
        q_out_field = getattr(self,'generate_qobject_for_NOT_exit_model_fields',None)
        if q_out_field:
            q_outer_field = self.generate_qobject_for_NOT_exit_model_fields()
            qgroup &= q_outer_field       
        return qgroup     
    
   
    
class FilterToGenerateQ_ForMLL(FilterToGenerateQ):
    def generate_qobject_for_exit_model_field_gio_mat(self,fname):
            d = self.form_cleaned_data[fname]
            q_gio_mat = Q(gio_mat__lte=d)
            return q_gio_mat
    def generate_qobject_for_NOT_exit_model_fields(self):
        qgroup=Q()
        if self.request.GET['comment']:
            q_across = Q(comments__comment__icontains=self.request.GET['comment'])
            qgroup = qgroup&q_across
        if self.request.GET['specific_problem_m2m']:
            value = re.sub('\*\*$','',self.request.GET['specific_problem_m2m'])
            q_across_fault = Q(specific_problems__fault__Name__icontains=value)
            q_across_object_name = Q(specific_problems__object_name__icontains=value)
            q_specific_problem_m2m = q_across_fault | q_across_object_name
            qgroup = qgroup & q_specific_problem_m2m
        #for m2m
        '''
        if  'thao_tac_lien_quan' in self.request.GET:
            q_across_thaotac = Q(comments__thao_tac_lien_quan__in=self.form_cleaned_data['thao_tac_lien_quan'])
            qgroup = qgroup & q_across_thaotac
            '''
        if  self.form_cleaned_data['thao_tac_lien_quan']: 
            print '@@@@@@@@@@@@@@@@@zz',self.form_cleaned_data['thao_tac_lien_quan']
            q_across_thaotac = Q(comments__thao_tac_lien_quan__in=self.form_cleaned_data['thao_tac_lien_quan'])
            qgroup = qgroup & q_across_thaotac
           
        if self.form_cleaned_data['doi_tac']: # input text la 1 doi tac hoan chinh nhu la a-b-number
            q_across_doi_tac = Q(comments__doi_tac=self.form_cleaned_data['doi_tac'])
            qgroup = qgroup & q_across_doi_tac
        elif self.request.GET['doi_tac']: # input text la form
            value = self.request.GET['doi_tac']
            fieldnames = [f.name for f in DoiTac._meta.fields if isinstance(f, CharField)]
            q_across_doi_tac = reduce(operator.or_, (Q(**{"comments__doi_tac__%s__icontains" % fieldname:value }) for fieldname in fieldnames ))
            qgroup = qgroup & q_across_doi_tac
        if self.form_cleaned_data['gio_mat_lon_hon']:
            d = self.form_cleaned_data['gio_mat_lon_hon']
            q = Q(gio_mat__gte=d)
            qgroup = qgroup & q
        
        return qgroup
    

# delete surface branch
def show_string_avoid_none (value,string_pattern = '{0}',none_string_presentation = ''):
    if value:
        return string_pattern.format(str(value))
    else:
        return none_string_presentation
def update_trang_thai_cho_mll(mll_instance):
    last_comment_instance = mll_instance.comments.latest('id')
    mll_instance.trang_thai = last_comment_instance.trang_thai
    mll_instance.save()                                               
#MODAL_style_title_dict_for_form = {'CommentForm':('')}
def modelmanager(request,form_name,entry_id):
    status_code = 200
    url = '/omckv2/modelmanager/'+ form_name +'/'+entry_id+'/'
    try:
        form_table_template =request.GET['form-table-template']
    except:
        form_table_template = 'normal form template'
    try:
        which_form_or_table = request.GET['which-form-or-table']
    except:
        which_form_or_table = 'table only'
    ModelClass_name = re.sub('Form$','',form_name,1)
    dict_render ={}
    table2 = None
    need_valid=False
    need_save_form  =False
    data=None
    initial=None
    instance=None
    form_notification = None
    table_notification = '<h2 class="table_notification"> Danh sách được hiển thị ở table bên dưới  </h2>'
    loc = True if 'loc' in request.GET else False
    is_download = True if 'downloadtable' in request.GET else False
    loc_pass_agrument=False
    force_allow_edit = False
    khong_show_2_nut_cancel_va_loc = False
    if which_form_or_table!="table only" or loc or (is_download and loc): #get Form Class
        print 'request.POST',request.POST
        if request.method=='POST':
            need_valid =True
            need_save_form=True
            data = request.POST
            khong_show_2_nut_cancel_va_loc = request.GET.get('khong_show_2_nut_cancel_va_loc',None)
        elif request.method=='GET':
            if loc:
                #print 'request.GET',request.GET
                need_valid =True
                data = request.GET
                loc_pass_agrument = True #tham so nay de loai bo loi required khi valid form
            else:
                if entry_id=='new':
                    form_notification = u'<h2 class="form-notification text-primary"> Form ready</h2>'
                else:
                    form_notification = u'<h2 class="form-notification text-warning"> Đang hiển thị form của Đối tượng %s có ID là %s</h2>'%(ModelClass_name,entry_id)
                    if 'force_allow_edit' in request.GET:
                        force_allow_edit=True # chuc nang cua is_allow_edit la de display nut edit hay khong
                    
        FormClass = eval('forms.' + form_name)#repeat same if loc
        if form_name =='NhanTinUngCuuForm':# only form not model form
            mll_instance = Mll.objects.get(id = request.GET['selected_instance_mll'])
            noi_dung_tin_nhan = 'Bao ung cuu tram ' + mll_instance.object + show_string_avoid_none(mll_instance.site_name,'({0})') + show_string_avoid_none(mll_instance.su_co, '. Nguyen nhan: {0}') \
            +show_string_avoid_none(mll_instance.thiet_bi,'. Thiet bi:{0}')
            form = FormClass(initial = {'noi_dung_tin_nhan':noi_dung_tin_nhan})
            form.modal_title_style = 'background-color:#337ab7'
            form.modal_prefix_title  = 'Nội Dung Nhắn Tin'
            dict_render = {'form':form,'form_notification':form_notification}
        elif 'is_delete' in request.POST:
            ModelClass = FormClass.Meta.model # repeat same if loc
            instance = ModelClass.objects.get(id = entry_id)
            delta = timezone.now() - instance.datetime
            print delta.seconds
            if delta.seconds <60:
                instance.delete()
                form_notification = u'<h2 class="form-notification text-danger">Đã xóa comment này</h2>'
            else:
                form_notification = u'<h2 class="form-notification text-warning">Het thoi gian xoa</h2>'
            dict_render = {'form':None,'form_notification':form_notification}   
            print dict_render   
        else: 
            ModelClass = FormClass.Meta.model # repeat same if loc
        #Initial form
            if entry_id!='new':
                instance = ModelClass.objects.get(id = entry_id)
            
            form = FormClass(data=data,instance = instance,initial=initial,loc =loc_pass_agrument,form_table_template=form_table_template,force_allow_edit=force_allow_edit,request = request,\
                             khong_show_2_nut_cancel_va_loc = khong_show_2_nut_cancel_va_loc)
            

            if need_valid:
                is_form_valid = form.is_valid()
                if not is_form_valid :
                    form_notification = u'<h2 class="form-notification text-danger">Nhập Form sai, vui lòng check lại </h2>'
                    status_code = 400
            if need_save_form and status_code !=400:
                if form_name=="MllForm":
                    now = datetime.now()
                    if entry_id =="new":
                        instance = form.save(commit=False)
                        mll_instance= instance
                        user = request.user
                        mll_instance.thanh_vien = user
                        mll_instance.ca_truc = user.get_profile().ca_truc
                    else:#Edit mll
                        instance = form.save(commit=False)
                        mll_instance=instance
                        mll_instance.edit_reason = request.GET['edit_reason']
                        update_trang_thai_cho_mll(mll_instance)
                    #mll_instance.last_update_time = now
                    mll_instance.save()# save de tao nhung cai database relate nhu foreinkey.
                    
                    # luu specific_problem_m2m
                    if form.cleaned_data['specific_problem_m2m']:
                        specific_problem_m2ms = form.cleaned_data['specific_problem_m2m'].split('\n')
                        for count,specific_problem_m2m in enumerate(specific_problem_m2ms):
                            if '**' in specific_problem_m2m:
                                faulcode_hyphen_objects = specific_problem_m2m.split('**')
                                try:
                                    faultLibrary_instance = FaultLibrary.objects.get(Name = faulcode_hyphen_objects[0])
                                except :
                                    faultLibrary_instance = FaultLibrary(Name = faulcode_hyphen_objects[0])
                                    faultLibrary_instance.ngay_gio_tao = datetime.now()
                                    faultLibrary_instance.nguoi_tao = request.user
                                    faultLibrary_instance.save()
                                if len(faulcode_hyphen_objects) > 1:
                                    object_name = faulcode_hyphen_objects[1]
                                else:
                                    object_name=None
                            else:
                                faultLibrary_instance = None
                                object_name = specific_problem_m2m
                            if entry_id =="new":
                                SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=mll_instance)
                            else:#ghi chong len nhung entry problem specific dang co
                                specific_problems = mll_instance.specific_problems.all()
                                try:
                                    specific_problem = specific_problems[count]
                                    print 'current specific_problems',specific_problem.object_name
                                    specific_problem.fault = faultLibrary_instance
                                    specific_problem.object_name = object_name
                                    specific_problem.save()
                                except IndexError: # neu thieu instance hien tai so voi nhung instance sap duoc ghi thi tao moi 
                                    SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=mll_instance)
                                # delete nhung cai specific_problems khong duoc ghi chong
                                if (len(specific_problems) > count): 
                                    for x in specific_problems[count+1:]:
                                        x.delete()
                    
                    # luu CommentForm trong luu MllForm
                    if entry_id =="new":
                        CommentForm_i = CommentForm(request.POST,request = request)
                        if CommentForm_i.is_valid():
                            print '**@@@@@@@@@@*',form.cleaned_data['thao_tac_lien_quan']
                            print "CommentForm_i['datetime']",CommentForm_i.cleaned_data['datetime']
                            first_comment = CommentForm_i.save(commit=False)
                            first_comment.thanh_vien = user
                            first_comment.mll = mll_instance
                            first_comment.save()
                            CommentForm_i.save_m2m() 
                        else:
                            return HttpResponseBadRequest('khong valid',CommentForm_i.errors.as_text())
                    
                    #RELOad new form
                    
                    form = MllForm(instance=mll_instance,request=request)
                   
                elif form_name=="CommentForm":
                    if entry_id !="new" and instance.thanh_vien != request.user:
                        msg = u'Bạn không được thay đổi Comment của người kh'
                        #self.add_error('Name',msg)
                        errors = form._errors.setdefault("comment",ErrorList())
                        errors.append(msg)
                        dict_render = {'form':form,'form_notification':'<h2>ban khong duoc change form nguoi khac</h2>'} 
                        return render(request, 'drivingtest/form_table_manager.html',dict_render,status=400)
                    instance = form.save(commit=False)
                    if entry_id =="new":
                            comment_instance = instance
                            mll_instance  = Mll.objects.get(id=request.POST['mll'])
                            comment_instance.mll = mll_instance
                    else:
                        comment_instance = instance
                        mll_instance = instance.mll
                        olddatetime = comment_instance.datetime
                        if not request.POST['datetime']:
                            comment_instance.datetime = olddatetime
                    comment_instance.thanh_vien = request.user
                    comment_instance.save()
                    form.save_m2m() 
                    if form.cleaned_data['trang_thai'].is_cap_nhap_gio_tot:
                        mll_instance.gio_tot = comment_instance.datetime
                        mll_instance.save()
                    if form.cleaned_data['trang_thai'].Name==u'Báo ứng cứu':
                        mll_instance.ung_cuu = True
                        mll_instance.save()
                    
                    update_trang_thai_cho_mll(mll_instance)
                elif form_name=="Tram_NTPForm":
                    form.save(commit=True)
                    if (request.GET['update_all_same_vlan_sites']=='yes'):
                        rnc = instance.RNC
                        IUB_VLAN_ID = instance.IUB_VLAN_ID
                        same_sites = Tram.objects.filter(RNC=rnc,IUB_VLAN_ID=IUB_VLAN_ID)
                        same_sites.update(**dict([(fn,request.POST[fn])for fn in NTP_Field]))
                
                else:

                    instance = form.save(commit=True)
                
                #update history edit
                if ( entry_id !="new" and (form_name=="TramForm" or form_name == 'MllForm')):
                    if (EditHistory.objects.filter(modal_name=ModelClass_name).count() > 10000 ):
                            oldest_instance= EditHistory.objects.all().order_by('edit_datetime')[0]
                            oldest_instance.ly_do_sua = request.GET['edit_reason']
                            oldest_instance.search_datetime = datetime.now()
                            oldest_instance.edited_object_id = instance.id
                            oldest_instance.modal_name = ModelClass_name
                            oldest_instance.thanh_vien =request.user
                            oldest_instance.save()
                    else:
                        instance_ehis = EditHistory(modal_name = ModelClass_name, thanh_vien =request.user,ly_do_sua = request.GET['edit_reason'],edit_datetime = datetime.now(),edited_object_id = instance.id )
                        instance_ehis.save()
                        
                        
                # update form notifcation only for normal form not for modal form
                if form_table_template =='normal form template':
                    id_string =  str(instance.id)
                    if entry_id =="new":
                        url = '/omckv2/modelmanager/'+ form_name +'/'+ id_string+'/'
                        form_notification = u'<h2 class="form-notification text-success">Bạn vừa tạo thành công 1 Đối tượng %s có ID là %s,bạn có thế tiếp tục edit nó</h2>'%(ModelClass_name,id_string)
                    else:
                        form_notification = u'<h2 class="form-notification text-success">Bạn vừa Edit thành công 1 Đối tượng %s có ID là %s,bạn có thế tiếp tục edit nó</h2>'%(ModelClass_name,id_string)
                #reload form with newinstance
                
                
                if form_name != 'MllForm':# da load o tren voi MllForm
                    form = FormClass(instance = instance,request=request,khong_show_2_nut_cancel_va_loc=khong_show_2_nut_cancel_va_loc)###############3
                
                
            if not is_download:
                form.update_action_and_button(url)        
                dict_render = {'form':form,'form_notification':form_notification}        
        
    #TABLE
    if (which_form_or_table!="form only" and status_code == 200) or is_download:
        if 'table_name' in request.GET:
            TableClass = eval('forms.' + request.GET['table_name'])
            ModelClass = TableClass.Meta.model
            ModelClass_name = re.sub('Table','',request.GET['table_name'],1)
        else:
            TableClass = eval('forms.' + re.sub('Form$','Table',form_name))
        if which_form_or_table=="table only" :# can phai lay ModelClass neu phia neu chua lay form
            ModelClass = TableClass.Meta.model

        if 'tramid' in request.GET:
            if form_name =='TramForm':
                querysets =[]
                kq_searchs_one_contain = ModelClass.objects.get(id=request.GET['tramid'])
                save_history(kq_searchs_one_contain.Site_Name_1,request)
                querysets.append(kq_searchs_one_contain)
                table_notification =u'<h2 class="table_notification">Trạm được chọn được hiển thị ở table bên dưới</h2>'
                # tim querysets2:
                Site_Name_1 = kq_searchs_one_contain.Site_Name_1
                querysets2 = Mll.objects.filter(site_name=Site_Name_1)
                if request.GET['search_tu_dong_table_mll']=='yes':
                    table2 = MllTable(querysets2) # vi query set cua form_name=="TramForm" and entry_id !='new' khong order duoc nen phai tach khong di lien voi t
                    RequestConfig(request, paginate={"per_page": 15}).configure(table2)
                    dict_render.update({'table2':table2})
            elif form_name =='MllForm':#y change o tren nhung trong truong hop onlytable
                kq_searchs_one_contain = Tram.objects.get(id=request.GET['tramid'])
                Site_Name_1 = kq_searchs_one_contain.Site_Name_1
                querysets = Mll.objects.filter(site_name=Site_Name_1)
            else:
                querysets =[]
                kq_searchs_one_contain = ModelClass.objects.get(id=request.GET['tramid'])
                querysets.append(kq_searchs_one_contain)
                table_notification = '<h2 class="table_notification"> Đối tượng %s được chọn hiển thị ở table bên dưới</h2>'%ModelClass_name
        elif 'query_main_search_by_button' in request.GET:
            query = request.GET['query_main_search_by_button']
            if '&' in query:
                contains = request.GET['query_main_search_by_button'].split('&')
                query_sign = 'and'
            else:
                contains = request.GET['query_main_search_by_button'].split(',')
                query_sign = 'or'
            kq_searchs = Tram.objects.none()
            for count,contain in enumerate(contains):
                fname_contain_reconize_tuple = recognize_fieldname_of_query(contain,MYD4_LOOKED_FIELD)#return (longfieldname, searchstring)
                contain = fname_contain_reconize_tuple[1]
                print 'contain',contain
                fieldnameKey = fname_contain_reconize_tuple[0]
                print 'fieldnameKey',fieldnameKey
                if fieldnameKey=="all field":
                        FNAME = [f.name for f in Tram._meta.fields if isinstance(f, CharField)]
                        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME ))
                        
                        FRNAME = [f.name for f in Tram._meta.fields if (isinstance(f, ForeignKey) or isinstance(f, ManyToManyField)) and f.rel.to !=User]
                        print 'FRNAME',FRNAME
                        Many2manyfields =[f.name for f in Tram._meta.many_to_many]##
                        print 'Many2manyfields',Many2manyfields
                        FRNAME  = FRNAME + Many2manyfields
                        if FRNAME:
                            qgroup_FRNAME = reduce(operator.or_, (Q(**{"%s__Name__icontains" % fieldname: contain}) for fieldname in FRNAME ))
                            qgroup = qgroup | qgroup_FRNAME
                else:
                    qgroup = Q(**{"%s__icontains" % fieldnameKey: contain})
                if not fname_contain_reconize_tuple[2]:#neu khong query phu dinh
                    kq_searchs_one_contain = Tram.objects.filter(qgroup)
                else:
                    kq_searchs_one_contain = Tram.objects.exclude(qgroup)
                if query_sign=="or": #tra nhieu tram.
                    kq_searchs = list(chain(kq_searchs, kq_searchs_one_contain))
                elif query_sign=="and": # dieu kien AND but loop all field with or condition
                    if count==0:
                        kq_searchs = kq_searchs_one_contain
                    else:
                        kq_searchs = kq_searchs & kq_searchs_one_contain
            querysets = kq_searchs
            print 'len(querysets)',len(querysets)    
            table_notification = '<h2 class="table_notification"> Kết quả tìm kiếm %s trong database %s được hiển thị ở table bên dưới</h2>'%(query,ModelClass_name)
        elif 'query_main_search_by_manager_button' in request.GET:
            query = request.GET['query_main_search_by_manager_button']
            if '&' in query:
                contains = request.GET['query_main_search_by_manager_button'].split('&')
                query_sign = 'and'
            else:
                contains = request.GET['query_main_search_by_manager_button'].split(',')
                query_sign = 'or'
            kq_searchs = ModelClass.objects.none()
            for count,contain in enumerate(contains):
                fname_contain_reconize_tuple = recognize_fieldname_of_query(contain,MYD4_LOOKED_FIELD)#return (longfieldname, searchstring)
                contain = fname_contain_reconize_tuple[1]
                print 'contain**manager',contain
                fieldnameKey = fname_contain_reconize_tuple[0]
                print 'fieldnameKey',fieldnameKey
                if fieldnameKey=="all field":
                        FNAME = [f.name for f in ModelClass._meta.fields if isinstance(f, CharField)]
                        print 'FNAME',FNAME
                        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in FNAME ))
                        
                        '''
                        FRNAME = [f.name for f in ModelClass._meta.fields if (isinstance(f, ForeignKey) or isinstance(f, ManyToManyField) )and f.rel.to !=User]
                        print 'FRNAME',FRNAME
                        Many2manyfields =[f.name for f in ModelClass._meta.many_to_many]
                        print 'Many2manyfields',Many2manyfields
                        FRNAME  = FRNAME + Many2manyfields
                        if FRNAME:
                            qgroup_FRNAME = reduce(operator.or_, (Q(**{"%s__Name__icontains" % fieldname: contain}) for fieldname in FRNAME ))
                            qgroup = qgroup | qgroup_FRNAME
                        '''
                else:
                    qgroup = Q(**{"%s__icontains" % fieldnameKey: contain})
                if not fname_contain_reconize_tuple[2]:#neu khong query phu dinh
                    kq_searchs_one_contain = ModelClass.objects.filter(qgroup)
                else:
                    kq_searchs_one_contain = ModelClass.objects.exclude(qgroup)
                if query_sign=="or": #tra nhieu tram.
                    kq_searchs = list(chain(kq_searchs, kq_searchs_one_contain))
                elif query_sign=="and": # dieu kien AND but loop all field with or condition
                    if count==0:
                        kq_searchs = kq_searchs_one_contain
                    else:
                        kq_searchs = kq_searchs & kq_searchs_one_contain
            querysets = kq_searchs
            table_notification = '<h2 class="table_notification">Kết quả tìm kiếm %s trong database %s được hiển thị ở table bên dưới</h2>'%(query,ModelClass_name)
        
        elif form_name =='Tram_NTPForm':
            if 'tram_id_for_same_ntp' in request.GET : #da la cai nay thi khong the co loc trong , khi click vao download script 
                instance_site = Tram.objects.get(id = request.GET['tram_id_for_same_ntp'])
                rnc = instance_site.RNC
                IUB_VLAN_ID = instance_site.IUB_VLAN_ID
                querysets = Tram.objects.filter(RNC=rnc,IUB_VLAN_ID=IUB_VLAN_ID)
                print 'len(querysets)',len(querysets)
        elif form_name =='EditHistoryForm':
            tram_id = request.GET['tram_id']
            tram_instance = Tram.objects.get(id = tram_id)
            querysets = EditHistory.objects.filter(tram = tram_instance)
        elif loc:
            if request.method =='POST':# submit form name khong cung model class voi table nam, trong truong hop submit form o modal va lam thay doi mlltable
                print 'form_table_template',form_table_template
                if 'table_name' in request.GET:
                    form_name =  re.sub('Table$','Form',request.GET['table_name'])
                    FormClass= eval('forms.' + form_name)
                    print '@@@@@FormClass',FormClass
                
                
                form = FormClass(data=request.GET,loc=True)
                if form.is_valid():#alway valid but you must valid to get form.cleaned_data:
                    print '######form cua get loc valid'
                else:
                    print 'form.errors',form.errors.as_text()
            if form_name=='MllForm':
                FiterClass=FilterToGenerateQ_ForMLL # adding more out field fiter
            else:
                FiterClass= FilterToGenerateQ
            
            qgroup_instance= FiterClass(request,FormClass,ModelClass,form.cleaned_data)
            qgroup = qgroup_instance.generateQgroup()
            querysets = ModelClass.objects.filter(qgroup).distinct().order_by('-id')
            if request.method !='POST':
                form_notification =u'<h2 class="form-notification text-info">  Số kết quả lọc là %s trong database %s<h2>'%(len(querysets),form_name.replace('Form',''))
                dict_render.update({'form_notification':form_notification})
            loc_query = ''
            count=0
            for k,f in form.fields.items():
                try:
                    v = request.GET[k]
                except:
                    continue
                if v:
                    try:
                        label = f.label +''
                    except TypeError:
                        label = k
                    count +=1
                    if count==1:
                        print '$#@#$#$#fname',k
                        loc_query = label + '=' + v
                        
                    else:
                        loc_query = loc_query + '&'+label + '=' + v 
            table_notification = '<h2 class="table_notification"> Kết quả tìm kiếm %s trong database %s được hiển thị ở table bên dưới</h2>'%(loc_query,ModelClass_name)

        
        else: # if !loc and ...
            querysets = ModelClass.objects.all().order_by('-id')
            table_notification = '<h2 class="table_notification">Tất cả Đối tượngtrong database %s được hiển thị ở table bên dưới</h2>'%ModelClass_name
        if TableClass.__name__ =='MllTable':
            
            loc_cas = request.GET.get('loc-ca')
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@loc-ca',loc_cas
            if loc_cas and loc_cas !="None":
                q = reduce(operator.or_, (Q(ca_truc__Name__exact = ca_name) for ca_name in loc_cas.split('d4') ))
                querysets = querysets.filter(q)
        if status_code != 400:
            table = TableClass(querysets) # vi query set cua form_name=="TramForm" and entry_id !='new' khong order duoc nen phai tach khong di lien voi t
            RequestConfig(request, paginate={"per_page": 15}).configure(table)
            dict_render.update({'table':table,'table_notification':table_notification})
    if 'downloadtable' in request.GET:
        if request.GET['downloadtable'] == 'csv':
            return table.as_xls_d4_in_form_py_csv(request)
        elif request.GET['downloadtable'] == 'xls':
            return table.as_xls_d4_in_form_py_xls(request)
    if form_table_template =='form on modal' and which_form_or_table !='table only':# and not click order-sort
        form.verbose_form_name =ModelClass_name
        return render(request, 'drivingtest/form_table_manager_for_modal.html',dict_render,status=status_code)
    else:
        return render(request, 'drivingtest/form_table_manager.html',dict_render,status=status_code)
            



def download_script_ntp(request):
    sendmail=0
    site_id = request.GET['site_id']
    print 'site_id',site_id
    instance_site = Tram.objects.get(id=site_id)
    sitename = instance_site.Site_ID_3G
    if not sitename:
        return HttpResponseBadRequest('khong ton tai site 3G cua tram nay')
    return_taoscript= tao_script( instance_site,ntpServerIpAddressPrimary = request.GET['ntpServerIpAddressPrimary'],\
                              ntpServerIpAddressSecondary= request.GET['ntpServerIpAddressSecondary'],\
                               ntpServerIpAddress1= request.GET['ntpServerIpAddress1'],\
                                ntpServerIpAddress2 = request.GET['ntpServerIpAddress2'])
    if not return_taoscript:
        return HttpResponseBadRequest('khong co gia tri ntpip')
    else:
        list_files,temporary_achive_path,loai_tu  = return_taoscript
    if list_files:# neu phai tao achive
        temporary_achive_path = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temporary_achive_path, 'w', zipfile.ZIP_DEFLATED)
        for file_name in  list_files:
            filename = settings.MEDIA_ROOT + '/for_user_download_folder/' + file_name # Select your file here.                              
            archive.write(filename, ntpath.basename(filename))
        archive.close()
    basename = sitename + "_" + loai_tu + '.zip'
    if sendmail:
        send_email(files= temporary_achive_path,filetype='tempt',fname = basename)
    wrapper = FileWrapper(temporary_achive_path)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s'%(basename)
    response['Content-Length'] = temporary_achive_path.tell()
    temporary_achive_path.seek(0)
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
from django.template import Template 




AUTOCOMPLETE_DICT = {'nguyen_nhan':{'class_name':'NguyenNhan','is_dau_hieu_co_add':True},\
                     'du_an':{'class_name':'DuAn','is_dau_hieu_co_add':True}}
def autocomplete (request):
    query   = request.GET['query'].lstrip().rstrip()
    print 'ban dang search',query
    name_attr = request.GET['name_attr']
    results = [] # results la 1 list gom nhieu dict, moi dict la moi li , moi dict la moi ket qua tim kiem

    if name_attr in AUTOCOMPLETE_DICT:
        Classeq = eval('models.' + AUTOCOMPLETE_DICT[name_attr]['class_name'])#repeat same if loc
        if query == 'tatca':
            doitac_querys = Classeq.objects.all()
        else:
            fieldnames = [f.name for f in Classeq._meta.fields if isinstance(f, CharField)  ]
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
            doitac_querys = Classeq.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            #doitac_dict['desc'] = doitac.Ghi_chu  if doitac.Ghi_chu else ''
            doitac_dict['desc'] = ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
        try:
            is_dau_hieu_co_add = AUTOCOMPLETE_DICT[name_attr]['is_dau_hieu_co_add']
        except:
            is_dau_hieu_co_add = False
        if is_dau_hieu_co_add:
            if query=='tatca':
                dau_hieu_co_add = False
            else:
                try:
                    Classeq.objects.get(Name=query)
                    dau_hieu_co_add = False
                except Classeq.DoesNotExist:
                    dau_hieu_co_add = True
            to_json.update({'dau_hieu_co_add':dau_hieu_co_add})

    elif name_attr =='thao_tac_lien_quan':
        if query == 'tatca':
            doitac_querys = ThaoTacLienQuan.objects.all()
        else:
            querys = query.split(',')
            query = querys[-1].rstrip().lstrip()
            fieldnames = [f.name for f in ThaoTacLienQuan._meta.fields if isinstance(f, CharField)  ]
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
            doitac_querys = ThaoTacLienQuan.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] =  ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
        if query=='tatca':
            dau_hieu_co_add = 0
            to_json.update({'curent_add':0})
        else:
            dau_hieu_co_add = 0
            for count,query in enumerate(querys):
                query = query.rstrip().lstrip()
                if not query:
                    continue
                try:
                    ThaoTacLienQuan.objects.get(Name=query)
                except ThaoTacLienQuan.DoesNotExist:
                    dau_hieu_co_add += 1
                    if count ==len(querys) -  1:
                        to_json.update({'curent_add':1})
        to_json.update({'dau_hieu_co_add':dau_hieu_co_add})
        
        
    elif name_attr =='manager_suggestion':
        modelClass = eval('models.'+request.GET['model_attr_global'])
        fieldnames = [f.name for f in modelClass._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        querys = modelClass.objects.filter(qgroup)
        for object in querys[:10]:
            object_dict = {}
            object_dict['label'] = object.__unicode__()
            object_dict['id'] = object.id
            object_dict['desc'] = ''
            results.append(object_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
    
        '''
    elif 'trang_thai' in name_attr:
        fieldnames = [f.name for f in TrangThai._meta.fields if isinstance(f, CharField)  ]
        qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
        doitac_querys = TrangThai.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] =  ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
        '''
    elif 'specific_problem_m2m' in name_attr:
        qgroup = Q(Name__icontains=query)
        doitac_querys = FaultLibrary.objects.filter(qgroup)
        for doitac in doitac_querys[:10]:
            doitac_dict = {}
            doitac_dict['label'] = doitac.Name 
            doitac_dict['desc'] =  ''
            results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        } 
    elif name_attr =='doi_tac' :
        fieldnames = [f.name for f in DoiTac._meta.fields if isinstance(f, CharField)  ]
        if '-' not in query:
            print 'fieldnames',fieldnames
            qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: query}) for fieldname in fieldnames ))
            doitac_querys = DoiTac.objects.filter(qgroup).distinct()
            print len(doitac_querys)
            for doitac in doitac_querys[:10]:
                doitac_dict = {}
                #doitac_dict['label'] = doitac.Name + ("-" + doitac.Don_vi if doitac.Don_vi else "")
                doitac_dict['label'] = doitac.__unicode__() 
                doitac_dict['desc'] = doitac.So_dien_thoai if doitac.So_dien_thoai else 'chưa có sdt'
                results.append(doitac_dict)
            
        else:# there '-' in query
            contains = query.split('-')
            for count,contain in enumerate(contains):
                qgroup = reduce(operator.or_, (Q(**{"%s__icontains" % fieldname: contain}) for fieldname in fieldnames))
                kq_searchs_one_contain = DoiTac.objects.filter(qgroup)
                if count==0:
                    kq_searchs = kq_searchs_one_contain
                else:
                    kq_searchs = kq_searchs & kq_searchs_one_contain    
                    
            for doitac in kq_searchs[:10]:
                doitac_dict = {}
                #doitac_dict['value'] = doitac.id
                doitac_dict['label'] = doitac.Name + "-" + doitac.Don_vi
                doitac_dict['desc'] = doitac.So_dien_thoai if doitac.So_dien_thoai else 'chưa có sdt'
                results.append(doitac_dict)
        to_json = {
            "key_for_list_of_item_dict": results,
        }
        doi_tac_check = luu_doi_tac_toold4(query)
        dau_hieu_co_add = True if not doi_tac_check else False
        to_json.update({'dau_hieu_co_add':dau_hieu_co_add})
    elif name_attr =='object' or name_attr =="main_suggestion":
        contain = query
        if contain =='':
            fieldnames = {'Site_ID_3G':'3G'}
        else:
            fieldnames = MYD4_LOOKED_FIELD
        
        for fieldname,sort_fieldname  in fieldnames.iteritems(): #Loop through all field
            q_query = Q(**{"%s__icontains" % fieldname: contain})
            one_field_searchs = Tram.objects.filter(q_query)[0:20]
            if len(one_field_searchs)>0:
                for tram in one_field_searchs:
                    tram_dict = {}
                    try:
                        if fieldname =="Site_ID_3G":
                            thiet_bi = str(tram.Cabinet)
                        elif fieldname =="Site_ID_2G":
                            thiet_bi =str(tram.nha_san_xuat_2G)
                        else:
                            thiet_bi = "2G&3G"
                    except Exception as e:
                            thiet_bi = 'error' + tram.Site_Name_1
                            #print e, tram
                    tram_dict['id'] = tram.id
                    tram_dict['sort_field'] = sort_fieldname
                    tram_dict['label'] =  getattr(tram,fieldname)
                    tram_dict['thiet_bi'] =  thiet_bi
                    tram_dict['site_name_1'] = tram.Site_Name_1
 
                    tram_dict['sn1'] = show_string_avoid_none(tram.Site_Name_1)
                    tram_dict['sn2'] = show_string_avoid_none(tram.Site_Name_2,none_string_presentation='__')
                    tram_dict['s3g'] = show_string_avoid_none (tram.Site_ID_3G,none_string_presentation='__')
                    tram_dict['s2g'] = show_string_avoid_none (tram.Site_ID_2G,none_string_presentation='__')
                    
                    
                    tram_dict['s4g'] = show_string_avoid_none (tram.eNodeB_Name,none_string_presentation='__')
                    tram_dict['s4g_thietbi'] = str(tram.eNodeB_Type)
                    tram_dict['s3g_thietbi'] = str(tram.Cabinet)
                    
                    tram_dict['s2g_thietbi'] = str(tram.nha_san_xuat_2G)
                    results.append(tram_dict)
        to_json = {
                "key_for_list_of_item_dict": results,
            }
    return HttpResponse(simplejson.dumps(to_json), content_type='application/json')


def delete_mll (request):
    id = request.GET['query']
    mll_instance  = Mll.objects.get(id=int(id))
    mll_instance.comments.all().delete()
    mll_instance.delete()
    table = MllTable(Mll.objects.all().order_by('-id'))
    RequestConfig(request, paginate={"per_page": 15}).configure(table)        
    return render(request, 'drivingtest/custom_table_template.html',{'table':table})
from django.core.servers.basehttp import FileWrapper




def save_history(query,request):
    if (SearchHistory.objects.filter(thanh_vien=request.user).count() > 3 ):
                oldest_instance= SearchHistory.objects.all().order_by('search_datetime')[0]
                oldest_instance.query_string = query
                oldest_instance.search_datetime = datetime.now()
                oldest_instance.thanh_vien = request.user
                oldest_instance.save()
    else:
        instance = SearchHistory(query_string=query,search_datetime = datetime.now(),thanh_vien = request.user)
        instance.save()




@login_required
def upload_excel_file(request):
    context = RequestContext(request)
    if not request.user.is_superuser:
        result_handle_file =u"Bạn không có quyến import data"
    elif request.method == 'POST' :
        
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        choices =  request.POST.getlist('sheetchoice')
        print '@@@@@@@@@@@@@@choices',choices
        if choices:
            #is_available_file_tick =  form.cleaned_data['is_available_file']
            is_available_file_tick =  request.POST.get('is_available_file',False)
            if not is_available_file_tick: # Neu khong tick vao cai o chon file co san
                if 'file' in request.FILES:
                    fcontain = request.FILES['file'].read()
                    workbook = xlrd.open_workbook(file_contents=fcontain)
                    result_handle_file =u"Đã import xong từ file bạn chọn!!!"
                    import_database_4_cai_new(choices,workbook = workbook)
                else: # but not file upload so render invalid
                    result_handle_file = u'Thiếu File, hoặc bạn phải tick vào is_available_file_tick'
            else:
                workbook = None
                result_handle_file =u"Đã import xong từ file có sắn!!!"
                import_database_4_cai_new(choices,workbook = workbook)
        else:
            result_handle_file =u"Bạn phải chọn database gì"
        
    else:#GET
        result_handle_file =u"Mời bạn chọn "
    return render_to_response('drivingtest/import_db_from_excel.html', {'result_handle_file':result_handle_file},context)



#https://docs.djangoproject.com/en/1.8/howto/outputting-csv/




#############################################################################





   
