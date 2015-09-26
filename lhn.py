# -*- coding: utf-8 -*-
import os

def populate():
    python_cat = add_cat('sạc')

    add_linhkien(cat=python_cat,
        name="Pin dự phòng Moigus Moijuice 8100 mAh (2.4A)",
        price=30,
        old_price=20,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/7136246101_pin-du-phong-moigus-moijuice-8100-mah--2-4a-.jpg",
        description ='''ản phẩm chính hãng Moigus (Singapore), giá đã bao gồm 10% VATNguyên hộp gồm : Pin Moijuice 8100 mAh, cáp micro USB, tài liệu hướng dẫn
* Pin dự phòng công suất 8100 mAh
* Cung cấp nguồn điện lý tưởng cho các sản phẩm điện tử bất cứ đâu, bất cứ lúc nào
* Hỗ trợ truyền tải dữ liệu trực tiếp từ USB OTG 
* Có thể sử dụng sạc nhiểu thiết bị cùng mốt lúc
* Dung lượng lớn, phù hợp với tất cả các sản phẩm Smartphone, Tablet
* Đèn Led thông minh hiển thị dung lượng pin
* Sản phẩm chính hãng Moigus (Singapore)
Thông số kỹ thuật:
- Dung lượng 8100mAh
- Loại pin: Li-Polymer
- Trọng lượng : 260g
- Kích thước : 125 x 73 x 15mm
- Đầu vào : DC5V/1.5A
- Đầu ra 1: DC5V/2.4A(Max) 
-Đầu ra 2: DC5V/1A 
- Đầu ra 3: DC5V/1A
- Pin chỉ số: 4Led ( 25% cho mỗi nấc hiển thị) 
- Thời gian sạc : ≈ 6.5h''',
        )

    add_linhkien(cat=python_cat,
        name="Tai nghe Hoco EPV02 (có mic)",
        price=40,
        old_price=50,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/4821575135_tai-nghe-hoco-epv02--co-mic-.jpg",
        description ="",
        )
    add_linhkien(cat=python_cat,
        name="Nắp sau Viva Convertir Flex iPhone 6",
        price=50,
        old_price=60,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/3371603824_nap-sau-viva-convertir-flex-iphone-6-.jpg",
        description ='''Hàng cao cấp hiệu VIVA (Singapore)
Nguyên hộp: 1 nắp sau cao cấp

* Bao ốp lưng dành cho iPhone 6
* Sử dụng chất liệu nhựa dẻo bọc bởi lớp da chất lượng cao
* Thiết kế gọn, ôm sát vào iPhone
* Bảo vệ chiếc iPhone 6 của bạn khỏi va chạm mạnh và an toàn khi sử dụng
* Mặt sau được thiết kế cho chiếc iPhone có thể đứng được
* Nhiều màu sắc cho bạn lựa chọn
* Sản phẩm thương hiệu Viva (Singapore) nổi tiếng''',
        )
    
    python_cat = add_cat("cáp")
    add_linhkien(cat=python_cat,
        name="Gậy chụp hình tự sướng Mono Pod (có remote)",
        price=67,
        old_price=87,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/4826504253_gay-chup-hinh-tu-suong-mono-pod--co-remote-.jpg",
        description ='''* Gậy chụp hình thế hệ mới dành cho các sản phẩm smartphone sử dụng hệ điều hành Android hoặc iOS. 
* Tay cầm gồm 7 đoạn có khả năng thu ngắn gọn gàng hoặc kéo dài trong khoảng 235-1100 mm.
* Khung kẹp chắc chắn, chịu được trọng lượng tối đa 500gr, có thể điều chỉnh độ rộng linh hoạt và xoay nhiều góc độ.
* Giúp người sử dụng có thể chụp ảnh theo nhóm hoặc tạo những góc chụp mà bình thường không hỗ trợ 
* Tương thích với các thiết bị hỗ trợ hệ điều hành Android & iOS
* Có hỗ trợ thêm remote kết nối blutooth rất tiện dụng
* Cho chất lượng ảnh đẹp; không rung, nhòe như khi chụp bằng tay''',
        )
    add_linhkien(cat=python_cat,
        name="Nắp sau Hoco Defender iPhone 6 Plus",
        price=50000,
        old_price=60000,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/1456983885_nap-sau-hoco-defender-iphone-6-.jpg",
        description ='''Hàng cao cấp hiệu Hoco nổi tiếng
Nguyên hộp: 1 nắp sau cao cấp

* Nắp sau thương hiệu cao cấp dành cho iPhone 6 Plus
* Thiết kế siêu mỏng với độ bền cao
* Sử dụng chất liệu nhựa cứng cao cấp trong suốt
* Giúp bảo vệ chiếc iPhone 6 Plus khỏi va chạm mạnh và an toàn khi sử dụng
* Dễ dàng truy cập các cổng kết nối, các nút điều khiển mà không cần tháo ra
* Nhiều màu sắc cho bạn lựa chọn
* Thương hiệu Hoco nổi tiếng của Hong Kong''',
        )
    add_linhkien(cat=python_cat,
        name="cap iphone 6",
        price=60,
        old_price=89,
        description ='''Hàng chính hãng Moigus (Singapore)
Nguyên hộp bao gồm : Loa bluetooth Moigus Blue S,jack kết nối


* Loa di động dành cho điện thoại di động, máy tính bảng
* Tích hợp mic với chất lượng đàm thoại tốt
* Thiết kế với những biểu tượng độc lạ và thời trang
* Sử dụng công nghệ kết nối Bluetooth v4.0 + EDR cho khả năng kết nối nhanh và ổn định
* Di động với 6 giờ chơi nhạc liên tục bạn có thể nghe nhạc mọi lúc mọi nơi
* Sản phẩm thương hiệu Moigus (Singapore)''',
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/9227315765_loa-bluetooth-moigus-blue-s-prism-painting.jpg"
        )
    
    
    
    python_cat = add_cat('Phụ kiện khác')

    add_linhkien(cat=python_cat,
        name="Pin dự phòng Moigus Moijuice 8100 mAh (2.4A)1",
        price=30,
        old_price=20,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/7136246101_pin-du-phong-moigus-moijuice-8100-mah--2-4a-.jpg",
        description ='''ản phẩm chính hãng Moigus (Singapore), giá đã bao gồm 10% VATNguyên hộp gồm : Pin Moijuice 8100 mAh, cáp micro USB, tài liệu hướng dẫn
* Pin dự phòng công suất 8100 mAh
* Cung cấp nguồn điện lý tưởng cho các sản phẩm điện tử bất cứ đâu, bất cứ lúc nào
* Hỗ trợ truyền tải dữ liệu trực tiếp từ USB OTG 
* Có thể sử dụng sạc nhiểu thiết bị cùng mốt lúc
* Dung lượng lớn, phù hợp với tất cả các sản phẩm Smartphone, Tablet
* Đèn Led thông minh hiển thị dung lượng pin
* Sản phẩm chính hãng Moigus (Singapore)
Thông số kỹ thuật:
- Dung lượng 8100mAh
- Loại pin: Li-Polymer
- Trọng lượng : 260g
- Kích thước : 125 x 73 x 15mm
- Đầu vào : DC5V/1.5A
- Đầu ra 1: DC5V/2.4A(Max) 
-Đầu ra 2: DC5V/1A 
- Đầu ra 3: DC5V/1A
- Pin chỉ số: 4Led ( 25% cho mỗi nấc hiển thị) 
- Thời gian sạc : ≈ 6.5h''',
        )

    add_linhkien(cat=python_cat,
        name="Tai nghe Hoco EPV02 (có mic)2",
        price=40,
        old_price=50,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/4821575135_tai-nghe-hoco-epv02--co-mic-.jpg",
        description ="",
        )
    add_linhkien(cat=python_cat,
        name="Nắp sau Viva Convertir Flex iPhone 6 3",
        price=50,
        old_price=60,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/3371603824_nap-sau-viva-convertir-flex-iphone-6-.jpg",
        description ='''Hàng cao cấp hiệu VIVA (Singapore)
Nguyên hộp: 1 nắp sau cao cấp

* Bao ốp lưng dành cho iPhone 6
* Sử dụng chất liệu nhựa dẻo bọc bởi lớp da chất lượng cao
* Thiết kế gọn, ôm sát vào iPhone
* Bảo vệ chiếc iPhone 6 của bạn khỏi va chạm mạnh và an toàn khi sử dụng
* Mặt sau được thiết kế cho chiếc iPhone có thể đứng được
* Nhiều màu sắc cho bạn lựa chọn
* Sản phẩm thương hiệu Viva (Singapore) nổi tiếng''',
        )
    
    
    
    python_cat = add_cat("ốp l")
    add_linhkien(cat=python_cat,
        name="Gậy chụp hình tự sướng Mono Pod (có remote)1",
        price=67,
        old_price=87,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/4826504253_gay-chup-hinh-tu-suong-mono-pod--co-remote-.jpg",
        description ='''* Gậy chụp hình thế hệ mới dành cho các sản phẩm smartphone sử dụng hệ điều hành Android hoặc iOS. 
* Tay cầm gồm 7 đoạn có khả năng thu ngắn gọn gàng hoặc kéo dài trong khoảng 235-1100 mm.
* Khung kẹp chắc chắn, chịu được trọng lượng tối đa 500gr, có thể điều chỉnh độ rộng linh hoạt và xoay nhiều góc độ.
* Giúp người sử dụng có thể chụp ảnh theo nhóm hoặc tạo những góc chụp mà bình thường không hỗ trợ 
* Tương thích với các thiết bị hỗ trợ hệ điều hành Android & iOS
* Có hỗ trợ thêm remote kết nối blutooth rất tiện dụng
* Cho chất lượng ảnh đẹp; không rung, nhòe như khi chụp bằng tay''',
        )
    add_linhkien(cat=python_cat,
        name="Nắp sau Hoco Defender iPhone 6 Plus1",
        price=50000,
        old_price=60000,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/1456983885_nap-sau-hoco-defender-iphone-6-.jpg",
        description ='''Hàng cao cấp hiệu Hoco nổi tiếng
Nguyên hộp: 1 nắp sau cao cấp

* Nắp sau thương hiệu cao cấp dành cho iPhone 6 Plus
* Thiết kế siêu mỏng với độ bền cao
* Sử dụng chất liệu nhựa cứng cao cấp trong suốt
* Giúp bảo vệ chiếc iPhone 6 Plus khỏi va chạm mạnh và an toàn khi sử dụng
* Dễ dàng truy cập các cổng kết nối, các nút điều khiển mà không cần tháo ra
* Nhiều màu sắc cho bạn lựa chọn
* Thương hiệu Hoco nổi tiếng của Hong Kong''',
        )
    add_linhkien(cat=python_cat,
        name="cap iphone 62",
        price=60,
        old_price=89,
        description ='''Hàng chính hãng Moigus (Singapore)
Nguyên hộp bao gồm : Loa bluetooth Moigus Blue S,jack kết nối


* Loa di động dành cho điện thoại di động, máy tính bảng
* Tích hợp mic với chất lượng đàm thoại tốt
* Thiết kế với những biểu tượng độc lạ và thời trang
* Sử dụng công nghệ kết nối Bluetooth v4.0 + EDR cho khả năng kết nối nhanh và ổn định
* Di động với 6 giờ chơi nhạc liên tục bạn có thể nghe nhạc mọi lúc mọi nơi
* Sản phẩm thương hiệu Moigus (Singapore)''',
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/9227315765_loa-bluetooth-moigus-blue-s-prism-painting.jpg"
        )
    
    
    
    
    python_cat = add_cat("pin dự ph")
    add_linhkien(cat=python_cat,
        name="Gậy chụp hình tự sướng Mono òngPod (có remote)2",
        price=67,
        old_price=87,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/4826504253_gay-chup-hinh-tu-suong-mono-pod--co-remote-.jpg",
        description ='''* Gậy chụp hình thế hệ mới dành cho các sản phẩm smartphone sử dụng hệ điều hành Android hoặc iOS. 
* Tay cầm gồm 7 đoạn có khả năng thu ngắn gọn gàng hoặc kéo dài trong khoảng 235-1100 mm.
* Khung kẹp chắc chắn, chịu được trọng lượng tối đa 500gr, có thể điều chỉnh độ rộng linh hoạt và xoay nhiều góc độ.
* Giúp người sử dụng có thể chụp ảnh theo nhóm hoặc tạo những góc chụp mà bình thường không hỗ trợ 
* Tương thích với các thiết bị hỗ trợ hệ điều hành Android & iOS
* Có hỗ trợ thêm remote kết nối blutooth rất tiện dụng
* Cho chất lượng ảnh đẹp; không rung, nhòe như khi chụp bằng tay''',
        )
    add_linhkien(cat=python_cat,
        name="Nắp sau Hoco Defender iPhone 6 Plus2",
        price=50000,
        old_price=60000,
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/1456983885_nap-sau-hoco-defender-iphone-6-.jpg",
        description ='''Hàng cao cấp hiệu Hoco nổi tiếng
Nguyên hộp: 1 nắp sau cao cấp

* Nắp sau thương hiệu cao cấp dành cho iPhone 6 Plus
* Thiết kế siêu mỏng với độ bền cao
* Sử dụng chất liệu nhựa cứng cao cấp trong suốt
* Giúp bảo vệ chiếc iPhone 6 Plus khỏi va chạm mạnh và an toàn khi sử dụng
* Dễ dàng truy cập các cổng kết nối, các nút điều khiển mà không cần tháo ra
* Nhiều màu sắc cho bạn lựa chọn
* Thương hiệu Hoco nổi tiếng của Hong Kong''',
        )
    add_linhkien(cat=python_cat,
        name="cap iphone 63",
        price=60,
        old_price=89,
        description ='''Hàng chính hãng Moigus (Singapore)
Nguyên hộp bao gồm : Loa bluetooth Moigus Blue S,jack kết nối


* Loa di động dành cho điện thoại di động, máy tính bảng
* Tích hợp mic với chất lượng đàm thoại tốt
* Thiết kế với những biểu tượng độc lạ và thời trang
* Sử dụng công nghệ kết nối Bluetooth v4.0 + EDR cho khả năng kết nối nhanh và ổn định
* Di động với 6 giờ chơi nhạc liên tục bạn có thể nghe nhạc mọi lúc mọi nơi
* Sản phẩm thương hiệu Moigus (Singapore)''',
        borrowed_picture="http://stcv4.hnammobile.com/uploads/accesories/details/9227315765_loa-bluetooth-moigus-blue-s-prism-painting.jpg"
        )

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Linhkien.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_linhkien(cat, name, price, old_price,borrowed_picture,description):
    p = Linhkien.objects.get_or_create(category=cat, name=name, price=price,old_price=old_price,description=description,borrowed_picture = borrowed_picture)[0]

    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
    from drivingtest.models import Category, Linhkien
    populate()