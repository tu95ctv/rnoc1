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
    Doitac_objects = DoiTac.objects
    if doi_tac_inputext:
                fieldnames= ['Full_name','Don_vi','So_dien_thoai']
                if "-" not in doi_tac_inputext:
                    if is_save_doitac_if_not_exit:
                        taodoitac = Doitac_objects.get_or_create(Full_name = doi_tac_inputext,nguoi_tao = user_tao )
                        return taodoitac[0]
                    else:#only get doitac not save new doitac if doitac not exit
                        try:
                            doitac = Doitac_objects.get(Full_name = doi_tac_inputext)
                        except DoiTac.DoesNotExist:
                            return None  #return None de generate_qobject_for_NOT_exit_model_fields trong view xu ly
                        return doitac
       
      
                else: # if has - 
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
                    if is_save_doitac_if_not_exit:
                        dictx.update({'nguoi_tao':user_tao})
                        doitac = Doitac_objects.get_or_create(**dictx)[0]
                    else:
                        try:
                            print '@@@@@@@@@Tu@@@@@@@@@@',dictx
                            doitac = Doitac_objects.get(**dictx)
                        except DoiTac.DoesNotExist:
                            return None 
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
    
