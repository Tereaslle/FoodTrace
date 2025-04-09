from django.test import TestCase
from segno import make_qr
# Create your tests here.
if __name__ == '__main__':
    with open('./static/img/qrcode.png', 'wb') as f:
        message = "Hello!"
        qr = make_qr(message)
        qr.designator
        qr.save(f, scale=40)  # 保存二维码 每个像素点为40像素大小
