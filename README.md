# 七牛云SDK

基于[七牛云官方SDK](https://github.com/qiniu/python-sdk)，新增了部分官方未实现的方法

## 现有方法

### [CDN](https://developer.qiniu.com/fusion)
    
- [x] 上传证书
- [x] 删除证书
- [x] 获取证书
- [x] 获取证书列表
- [x] 修改证书


## 需求

 * 七牛的密钥
 * Python 3

## 配置

### 安装Python依赖

```
pip install -r requirements.txt
```

### 修改配置

修改`configs.py`文件中的`ACCESS_KEY`和`SECRET_KEY`为你自己的，可以在七牛官网个人中心的[密钥管理](https://portal.qiniu.com/user/key)查看

## 举个例子

### 上传新的SSL证书并让域名绑定该证书

使用下面这段代码，上传了一个域名为`*.celerysoft.com`的SSL证书，并将该证书绑定到了CDN域名`static.celerysoft.com`下

```python
from toolkit.cdn import cdn_toolkit

# 证书名称
cert_name_ = '*.celerysoft.com20200717'
# 证书域名
domain_ = '*.celerysoft.com'
# 证书 private key 文件路径
private_key_file_ = '../local/privkey.pem'
# 证书 full chain 文件路径
full_chain_file_ = '../local/fullchain.pem'
# CDN 域名
cdn_domain_ = 'static.celerysoft.com'

ret, info = cdn_toolkit.create_ssl_cert_and_activate_on_domain_from_local_file(
    cert_name=cert_name_, cert_domain=domain_, private_key_file=private_key_file_, full_chain_file=full_chain_file_,
    cdn_domain=cdn_domain_, force_https=False, enable_http2=True)

# 打印结果看看
print(info.text_body)
print('=' * 100)
print(ret)
```

如果真有那么巧，你服务器是阿里云的，SSL证书是通过Certbot申请的通配符证书，那么推荐另一个小脚本[CertbotHooks](https://github.com/celerysoft/CertbotHooks)，可以定时更新证书

再结合上面这个例子，更新完证书后，同步更新到七牛

## License

[Apache License 2.0](./LICENSE)