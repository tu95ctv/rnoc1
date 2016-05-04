
import re
url= '/omckv2/modelmanager/EditHistoryForm/new/?tramid=54&sort=-thanh_vien&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53&tramid=54'
url2= '/omckv2/modelmanager/EditHistoryForm/new/?sort=-thanh_vien&tramid=54&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53&tramid=54'
urls = [url,url2]
for url in urls:
    url = re.sub(u'&?tramid=[^&]*(&|$)', "",url)
    print url

#javascript
'''
url = '/omckv2/modelmanager/EditHistoryForm/new/?tramid=54&sort=-thanh_vien&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53'
url = '/omckv2/modelmanager/EditHistoryForm/new/?sort=-thanh_vien&tramid=54&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53'
//url = '/omckv2/modelmanager/EditHistoryForm/new/?sort=-thanh_vien&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53&tramid=54'


url = url.replace(/&tramid=([^&]*$|[^&]*?&)/i, "")
console.log('###########url new', url)


import re
url= 'd?s'
#url= '/omckv2/modelmanager/EditHistoryForm/new/?sort=-thanh_vien&tramid=54&sort=-thanh_vien&is_form=false&search_tu_dong_table_mll=yes&is_table=true&form-table-template=normal+form+template&edited_object_id=53'

url = re.sub(u'&?', "",url)
print url'''