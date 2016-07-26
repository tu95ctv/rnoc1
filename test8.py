from random import randint
import collections
xac_suat = {3:0.00462962962962963,4:0.0138888888888889,5:0.0277777777777778,6:0.0462962962962963,7:0.0694444444444444,8:0.0972222222222222,9:0.115740740740741,10:0.125,11:0.125,12:0.115740740740741,13:0.0972222222222222,14:0.0694444444444444,15:0.0462962962962963,16:0.0277777777777778,17:0.0138888888888889,18:0.00462962962962963}
rs_lists = []
mau_thu = 100000
tai = 0
xiu = 0
TAI = 1
XIU = 0
tai_xiu_list = []
for i in range(1,mau_thu+1):
    tx_rs = randint(1,6) + randint(1,6) + randint(1,6)
    rs_lists.append(tx_rs)
    if tx_rs <11:
        xiu +=1
        tai_xiu_list.append(XIU)
    else:
        tai +=1
        tai_xiu_list.append(TAI)
    
print rs_lists
arrange_dict  = {}
for i in range(3,19):
    rs_percent = rs_lists.count(i)/float(mau_thu)
    sai_so = (rs_percent -xac_suat[i])*100/float(xac_suat[i])
    arrange_dict[rs_percent ] = i
    print i,rs_percent,"%.2f%%" %sai_so
#arrange_dict1 = collections.OrderedDict(sorted(arrange_dict.items()))
#print arrange_dict1
xen_ke_or_giong_nhau_lists= []

GIONG_NHAU=0
XEN_KE=1
tai_tich_luy = 0
xiu_tich_luy = 0
chot_tai_hoac_xiu = 0
tai_tich_luy_list = []
xiu_tich_luy_list = []
for c,current_i in enumerate(tai_xiu_list):
    if current_i==XIU:
        xiu_tich_luy += 1
    else:
        tai_tich_luy +=1
    if c ==0:
        bf_i = current_i
    else:
        if current_i !=bf_i:
            xen_ke_or_giong_nhau_lists.append(XEN_KE)
            if current_i==XIU:
                chot_tai = tai_tich_luy
                tai_tich_luy_list.append(chot_tai)
                tai_tich_luy =0
            else:#chot tai
                chot_xiu = xiu_tich_luy
                xiu_tich_luy_list.append(chot_xiu)
                xiu_tich_luy= 0
        else:
            xen_ke_or_giong_nhau_lists.append(GIONG_NHAU)
        bf_i = current_i
    
print tai_xiu_list,tai,xiu
print 'tai_tich_luy_list',tai_tich_luy_list
print 'xiu_tich_luy_list',xiu_tich_luy_list
len_tai_tich_luy_list = len(tai_tich_luy_list)
len_xiu_tich_luy_list = len(xiu_tich_luy_list)
print 'tai,xiu,len_tai_tich_luy_list,len_xiu_tich_luy_list',tai,xiu,len_tai_tich_luy_list,len_xiu_tich_luy_list



print 'XEN_KE',xen_ke_or_giong_nhau_lists.count(XEN_KE)
print 'GIONG_NHAU',xen_ke_or_giong_nhau_lists.count(GIONG_NHAU)  
for i in range(1,20):
    tai_tich_luy_list_count = tai_tich_luy_list.count(i)
    xiu_tich_luy_list_count =  xiu_tich_luy_list.count(i)
    rs_percent_t = tai_tich_luy_list_count*100/float(mau_thu)
    rs_percent_x =  xiu_tich_luy_list_count*100/float(mau_thu)
    print 'so lan lap lai,cua tai, cua xiu',i,"%s (%.2f%%)"%(tai_tich_luy_list_count,rs_percent_t),"%s (%.2f%%)"%(xiu_tich_luy_list_count,rs_percent_x)
