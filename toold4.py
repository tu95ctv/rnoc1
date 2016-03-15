import re
import os
import datetime
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from django.core.exceptions import MultipleObjectsReturned
from rnoc.models import DoiTac
#from LearnDriving.settings import MYD4_LOOKED_FIELD

def luu_doi_tac_toold4(model,doi_tac_inputext,user_tao,is_save_doitac_if_not_exit=True):
    Doitac_objects = model.objects
    if doi_tac_inputext:
                fieldnames= ['Full_name','Don_vi','So_dien_thoai']
                if "-" not in doi_tac_inputext:
                    try:
                        if is_save_doitac_if_not_exit:
                            print 'nguyen duc tu@@@@@@@@@@@@@@'
                            taodoitac = Doitac_objects.get_or_create(Full_name = doi_tac_inputext,nguoi_tao = user_tao )
                            return taodoitac[0]
                        else:#only get doitac not save new doitac if doitac not exit
                            doitac = Doitac_objects.get(Full_name = doi_tac_inputext)
                            return doitac
                    except :
                        return None
      
                else: # if has - 
                    doi_tac_inputexts = doi_tac_inputext.split('-')
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
                    print 'dictxdictxdictxdictxdictxdictxdictx',dictx
                    dictx.update({'nguoi_tao':user_tao})
                    print 'dictxdictxdictxdictxdictxdictxdictx222222',dictx
                    if is_save_doitac_if_not_exit:
                        doitac = Doitac_objects.get_or_create(**dictx)[0]
                    else:
                        doitac = Doitac_objects.get(**dictx)
                return doitac
    else:
        return None

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
    is_negative_query = False
    contain = contain.lstrip().rstrip()
    for longfield,sortfield in fieldnames.items():
        p = re.compile('^'+ sortfield +'=',re.IGNORECASE)
        kq = p.subn('',contain)
        #print kq[1]
        if kq[1]:
            contain = kq[0]
            fieldname = longfield
            return (fieldname,contain,is_negative_query)
    if kq[1]==0:
        p = re.compile('^'+ '(.*?)' +'=(.*?)$',re.IGNORECASE)
        kq = p.findall(contain)
        if kq:
            fieldname = kq[0][0].lstrip().rstrip().replace(" ","_")
            contain = kq[0][1].lstrip().rstrip()
            print 'fieldname',fieldname
        else:
            fieldname = "all field"
        if contain[0]=='!':
            contain = contain[1:]
            is_negative_query = True
        else:
            is_negative_query = False
        return (fieldname,contain,is_negative_query)
    
if __name__=="__main__":
    
    print datetime.datetime.now()
    
