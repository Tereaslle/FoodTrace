from django.conf import settings    # 引入django 的随机数作为盐
import hashlib

# 定义md5 加密函数
def md5(data_string):
    # 加盐是django自动生产的随机数
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
