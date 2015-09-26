# -*- coding: utf-8 -*-

import os
    
def insert_owncontact(owncontact_dict):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
    from drivingtest.models import OwnContact
    dia_chi = owncontact_dict['dia_chi']
    ten = owncontact_dict['ten']
    sodienthoai = owncontact_dict['sodienthoai']
    email = owncontact_dict['email']
    is_show_promote_product  = owncontact_dict['is_show_promote_product']
    is_best_sale_product  = owncontact_dict['is_best_sale_product']
    google_map  = owncontact_dict['google_map']
    slogan  = owncontact_dict['slogan']
    about_us  = owncontact_dict['about_us']
    base_title  = owncontact_dict['base_title']
    banner_url = owncontact_dict['banner_url']
    
    webpage= owncontact_dict['webpage']
    mainheader_color = owncontact_dict['mainheader_color']
    mainheader_type =owncontact_dict['mainheader_type']
    banner1_url =owncontact_dict['banner1_url']
    banner2_url =owncontact_dict['banner2_url']
    banner_height=owncontact_dict['banner_height']
    number_product_san_pham = owncontact_dict['number_product_san_pham']
    try:
        cn2_dia_chi=  owncontact_dict['cn2_dia_chi']
        cn2_sodienthoai=  owncontact_dict['cn2_sodienthoai']
        cn2_google_map=  owncontact_dict['cn2_google_map']
    except:
        cn2_dia_chi= ''
        cn2_sodienthoai=  ''
        cn2_google_map=  ''
    facebook_page=  owncontact_dict['facebook_page']
    script_google_analytics=  owncontact_dict['script_google_analytics']
    icon_path=  owncontact_dict['icon_path']
    footer_custom_color=  owncontact_dict['footer_custom_color']
    script_google_analytics_acc2 =  owncontact_dict['script_google_analytics_acc2']
    
    
    
    try:
        OwnContact.objects.latest('id').delete()
    except:
        pass
        
    OwnContact.objects.get_or_create(dia_chi=dia_chi,
        ten=ten,
        sodienthoai=sodienthoai,
        email=email,
        is_show_promote_product =is_show_promote_product ,
        is_best_sale_product =is_best_sale_product ,
        google_map =google_map ,
        slogan =slogan ,
        about_us =about_us ,
        base_title=base_title,
        banner_url = banner_url,
    
    webpage= webpage,
    mainheader_color = mainheader_color,
    mainheader_type = mainheader_type,
    banner1_url =banner1_url,
    banner2_url =banner2_url,
    banner_height=banner_height,
    number_product_san_pham=number_product_san_pham,
    cn2_dia_chi=cn2_dia_chi,
    cn2_sodienthoai=cn2_sodienthoai,
    cn2_google_map=cn2_google_map,
    facebook_page=facebook_page,
    script_google_analytics=script_google_analytics,
    icon_path = icon_path,
    footer_custom_color = footer_custom_color,
    script_google_analytics_acc2=script_google_analytics_acc2,
        )[0]
                
        
    return "Insert ok 1 ownContact"
def auto_create_owncontact_f ():
    txt_databases_bom ={
                        
        'dia_chi':'Kiot B45-Hùng Vương Square -100 Đường Hùng Vương Q5',
        'ten':'THANHTAMshop',
        'sodienthoai': '01635167567',
        'email':'giaythanhtam2@gmail.com',
        'is_show_promote_product':True,
        'is_best_sale_product' : True,
        'google_map' : '''<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.684274983023!2d106.670469!3d10.758797999999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752ee3581e6c4d%3A0x5607e93186c99468!2zMTAwIEjDuW5nIFbGsMahbmcsIHBoxrDhu51uZyA5LCBRdeG6rW4gNSwgSOG7kyBDaMOtIE1pbmgsIFZpZXRuYW0!5e0!3m2!1sen!2s!4v1434479168579" width="800" height="600" frameborder="0" style="border:0"></iframe>''' ,
        'slogan':'''Dẫn đầu về giá cả
Lấy chất lượng làm nền tảng
chế độ chăm sóc khách hàng và hậu mãi tốt nhất ....''',
        'about_us' : '''ThanhTamShop
        Thời Trang
        Giày Dép''',
        'number_product_san_pham':15,
        'base_title':'ThanhTamShop.vn Dẫn đầu về giá cả',
        'banner_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/banner5.png',
        'banner1_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/bannerb1.png',
        'banner2_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/bannerb3.png',
        'webpage':'ThanhTamShop.VN',
        'mainheader_color':'#6666CC',
        'footer_custom_color':'#337AB7',
        'mainheader_type':'main-header1', 
        'banner_height':200,
        'facebook_page':'https://www.facebook.com/thanhtamshop.vn',
        'script_google_analytics':'''<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-64710821-1', 'auto');
  ga('send', 'pageview');

</script>''',
        'icon_path':'/media/img/icon/bom.ico',
        'script_google_analytics_acc2':''' '''
        
                    }
    txt_databases_thien ={
        'dia_chi':'73 Nguyễn Hoàng, TP. Huế',
        'ten':'A.Thiện',
        'sodienthoai': '0907-975-603',
        'email':'trangphukien75@gmail.com',
        'is_show_promote_product':True,
        'is_best_sale_product' : False,
        'google_map' : '''<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3826.2432132558765!2d107.554793!3d16.463217999999994!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3141a6c0952c872f%3A0x78af503580db2f80!2zNzMgTmd1eeG7hW4gSG_DoG5nIFRow7RuIEFuIE5pbmggSOG6oSwgSMawxqFuZyBMb25nLCB0cC4gSHXhur8sIFRo4burYSBUaGnDqm4gSHXhur8sIFZpZXRuYW0!5e0!3m2!1sen!2s!4v1434985493546" width="800" height="600" frameborder="0" style="border:0"></iframe>''' ,
        'slogan':'''Với mong muốn mang đến cho khách hàng các sản phẩm điện tử và phụ kiện với giá cả cạnh tranh, cùng dịch vụ tốt nhất, hãy cùng trải nghiệm mua hàng tại Trangphukien - dễ dàng hơn, thuận tiện hơn và tiết kiệm hơn.''',
        'about_us' : 'Chuyên cung cấp các linh kiện điện thoại, sạc, cáp, bao da, ốp lưng.. giá tốt cho mọi người. Ship hàng tận nơi!',
        'base_title':'Phụ kiến tốt giá rẻ',
        'banner_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/logo.png',
        #'banner_url':'http://i1045.photobucket.com/albums/b460/trangphukien75/images2_zpsmtmdgqse.jpg',
        'banner1_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/bannerb1.png',
        'banner2_url':'http://i248.photobucket.com/albums/gg173/tu95ctv/bannerb3.png',
        'number_product_san_pham':15,
        'webpage':'TrangPhuKien.COM',
        'mainheader_color':'#6666CC',
        'footer_custom_color':'#337AB7',
        'mainheader_type':'main-header',
        'banner_height':200,
        'cn2_dia_chi':'53 Đặng Huy Trứ, TP. Huế',
        'cn2_ten':'',
        'cn2_email':'',
        'cn2_sodienthoai':'0945658081',
        'cn2_google_map' :'''<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7653.109893445818!2d107.58570803164491!3d16.447414393700697!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3141a14552814b4d%3A0xcb08c85ac5027cf1!2zNTMgxJDhurduZyBIdXkgVHLhu6kgdOG7lSAyMCwgVHLGsOG7nW5nIEFuLCB0cC4gSHXhur8sIFRo4burYSBUaGnDqm4gSHXhur8sIFZpZXRuYW0!5e0!3m2!1sen!2s!4v1435555521825" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>''',
        'facebook_page':'https://www.facebook.com/pages/trangphukiencom/748983948552898',
        'script_google_analytics':'''<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-64709012-1', 'auto');
  ga('send', 'pageview');

</script>''',

    'icon_path':'/media/img/icon/thien.ico',
    'script_google_analytics_acc2':''' <script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-64573338-1', 'auto');
ga('send', 'pageview');
</script>'''
                    }
    insert_owncontact(txt_databases_bom)
    return 'insert own contact to database ok'
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    print auto_create_owncontact_f()