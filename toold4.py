import re
from LearnDriving.settings import MYD4_LOOKED_FIELD



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
    
    contain = contain.lstrip().rstrip()
    for longfield,sortfield in fieldnames.items():
        p = re.compile('^'+ sortfield +'=',re.IGNORECASE)
        kq = p.subn('',contain)
        #print kq[1]
        if kq[1]:
            contain = kq[0]
            fieldname = longfield
            return (fieldname,contain)
    if kq[1]==0:
        p = re.compile('^'+ '(.*?)' +'=(.*?)$',re.IGNORECASE)
        kq = p.findall(contain)
        if kq:
            fieldname = kq[0][0].replace(" ","_").lstrip().rstrip()
            contain = kq[0][1].lstrip().rstrip()
            #print 'fieldname',fieldname
        else:
            fieldname = "all field"
        if contain[0]=='!':
            contain = contain[1:]
            is_negative_query = True
        else:
            is_negative_query = False
        return (fieldname,contain,is_negative_query)
    

if __name__ =="__main__":
    contains = ['3G_AG4209_3G_','2G_HC1129','Tay-Khanh-5_AGG','Tay-Khdfdfedanh-5_AGG']
    fieldnames = {'3G': 'site_id_3g', '2G': 'site_id_2g_E', 'SN2': 'site_name_2', 'SN1': 'site_name_1'}
    for contain in contains:
        print recognize_fieldname_of_query(contain, MYD4_LOOKED_FIELD)