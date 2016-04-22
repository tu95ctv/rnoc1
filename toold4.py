# -*- coding: utf-8 -*- 
import re
import datetime
import os

'''
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

'''
from rnoc.models import DoiTac
#from LearnDriving.settings import MYD4_LOOKED_FIELD

def luu_doi_tac_toold4(doi_tac_inputext,user_tao=None,is_save_doitac_if_not_exit=False):
            if "-" not in doi_tac_inputext:
                dictx = {'Name':doi_tac_inputext}
            else: # if has - 
                fieldnames= ['Name','Don_vi','So_dien_thoai']
                doi_tac_inputexts = doi_tac_inputext.split('-')
                doi_tac_inputexts = [x.lstrip().rstrip() for x in doi_tac_inputexts ]
                sdt_fieldname = fieldnames.pop(2)
                p = re.compile('[\d\s]{3,}') #digit hoac space lon hon 3 kytu lien tiep
                kq= p.search(doi_tac_inputext)
                try:
                    phone_number_index_of_ = kq.start()
                    #Define the index of number phone in array, 0 or 1, or 2, or 3
                    index_of_sdt_in_list = len(re.findall('-',doi_tac_inputext[:phone_number_index_of_]))
                    fieldnames.insert(index_of_sdt_in_list, sdt_fieldname)
                except:
                    pass
                dictx = dict(zip(fieldnames,doi_tac_inputexts))
            doitacs = DoiTac.objects.filter(**dictx)
            if len(doitacs)==0:
                if is_save_doitac_if_not_exit:
                    dictx.update({'nguoi_tao':user_tao})
                    doitac = DoiTac(**dictx)
                    doitac.save()
                    return doitac
                else:
                    return None
            else:
                return doitacs[0]


def create_dict_d41(contains,fieldnames):
    dict ={}
    for contain in contains:
        contain = contain.lstrip().rstrip()
        for key in fieldnames:
            p = re.compile('^'+ key +'_',re.VERBOSE)
            kq = p.subn('',contain)
            #print kq[1]
            if kq[1]:
                #print key,contain.replace(key+'_','')
                #print key,p.subn('',contain)
                dict[fieldnames[key]] = kq[0]
                continue
        if kq[1]==0:
            dict["all field"] = contain
                
    print dict
    return dict
def recognize_fieldname_of_query(contain,fieldnames):
    #Chuc nang: nhận dạng search theo kiểu: 2g=hc1001 hoac site_Site_ID_2G = hc1001
    is_negative_query = False
    contain = contain.lstrip().rstrip()
    '''
    for longfield,sortfield in fieldnames.items():
        p = re.compile('^'+ sortfield +'=',re.IGNORECASE)
        kq = p.subn('',contain)
        #print kq[1]
        if kq[1]:
            contain = kq[0]
            fieldname = longfield
            return (fieldname,contain,is_negative_query)
    if kq[1]==0:
    '''
    p = re.compile('^'+ '(.*?)' +'=(.*?)$',re.IGNORECASE)
    kq = p.findall(contain)
    if kq:
        fieldname = kq[0][0].lstrip().rstrip().replace(" ","_")
        for longfield,sortfield in fieldnames.items():
            if fieldname.lower()==sortfield.lower():
                fieldname = longfield
                break
        contain = kq[0][1].lstrip().rstrip()
    else:
        fieldname = "all field"
    if contain[0]=='!':
        contain = contain[1:]
        is_negative_query = True
    else:
        is_negative_query = False
    return (fieldname,contain,is_negative_query)
def prepare_value_for_specificProblem(specific_problem_instance):
    return ((specific_problem_instance.fault.Name + '**') if specific_problem_instance.fault else '') + ((specific_problem_instance.object_name) if specific_problem_instance.object_name else '')
    
if __name__=="__main__":
    
    print datetime.datetime.now()
    
