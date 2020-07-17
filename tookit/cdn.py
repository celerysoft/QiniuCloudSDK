# -*-coding:utf-8 -*-
from sdk.cdn import cdn_ssl_sdk, cdn_domain_sdk


class CDNToolkit:
    @staticmethod
    def create_ssl_cert_and_activate_on_domain(
            cert_name, cert_domain: str, private_key: str, full_chain: str,
            cdn_domain: str, force_https: bool = False, enable_http2: bool = True):
        """
        创建 SSL 证书并应用到指定 CDN 域名上

        :param cert_name: 证书名（在七牛控制台显示的名称）
        :param cert_domain: 证书域名
        :param private_key: 证书私钥字符串
        :param full_chain: 证书 full chain 字符串
        :param cdn_domain: CDN 域名
        :param force_https: 强制使用 HTTPS（开启后 HTTP 请求会强制跳转到 HTTPS 进行访问）
        :param enable_http2: 开启 HTTP/2 访问
        :return:
        """
        create_ssl_cert_ret, create_ssl_cert_info = cdn_ssl_sdk.create_ssl_cert(
            cert_name=cert_name, domain=cert_domain, private_key=private_key, full_chain=full_chain)

        if create_ssl_cert_ret is None:
            raise RuntimeError('创建证书失败：{}'.format(create_ssl_cert_info.text_body))

        if 'certID' not in create_ssl_cert_ret.keys():
            raise RuntimeError('创建证书异常：返回结果不包含 cert_id')

        cert_id = create_ssl_cert_ret['certID']

        modify_ssl_cert_ret, modify_ssl_cert_info = cdn_domain_sdk.modify_ssl_cert(
            domain=cdn_domain, cert_id=cert_id, force_https=force_https, enable_http2=enable_http2)

        return modify_ssl_cert_ret, modify_ssl_cert_info

    @classmethod
    def create_ssl_cert_and_activate_on_domain_from_local_file(
            cls, cert_name, cert_domain: str, private_key_file: str, full_chain_file: str,
            cdn_domain: str, force_https: bool = False, enable_http2: bool = True):
        """
        创建 SSL 证书并应用到指定 CDN 域名上

        :param cert_name: 证书名（在七牛控制台显示的名称）
        :param cert_domain: 证书域名字符串
        :param private_key_file: 证书私钥文件路径
        :param full_chain_file: 证书 full chain 文件路径
        :param cdn_domain: CDN 域名
        :param force_https: 强制使用 HTTPS（开启后 HTTP 请求会强制跳转到 HTTPS 进行访问）
        :param enable_http2: 开启 HTTP/2 访问
        :return:
        """
        with open(private_key_file, 'r') as f:
            private_key = f.read()
        with open(full_chain_file, 'r') as f:
            full_chain = f.read()

        return cls.create_ssl_cert_and_activate_on_domain(
            cert_name=cert_name, cert_domain=cert_domain, private_key=private_key, full_chain=full_chain,
            cdn_domain=cdn_domain, force_https=force_https, enable_http2=enable_http2
        )


cdn_toolkit = CDNToolkit()


if __name__ == '__main__':
    cert_name_ = '*.celerysoft.com20200717'
    domain_ = '*.celerysoft.com'
    full_chain_ = """
    -----BEGIN CERTIFICATE-----
    MIIFWjCCBEKgAwIBAgISBI+fM/q+w5e4e+0I0GVW76dvMA0GCSqGSIb3DQEBCwUA
    VBKmRMQt9QfNT7snGEt7nW/2EBwMtk6HsaQ4p4Q+
    -----END CERTIFICATE-----
    -----BEGIN CERTIFICATE-----
    MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/
    PfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6
    KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==
    -----END CERTIFICATE-----
        """
    private_key_ = """
    -----BEGIN PRIVATE KEY-----
    MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQCq0eUnDKoYlXf7
    fyeFHkZES9ywvSbLGnFQeb7QeKk=
    -----END PRIVATE KEY-----
        """

    cdn_domain_ = 'static.celerysoft.com'
    # ret, info = cdn_toolkit.create_ssl_cert_and_activate_on_domain(
    #     cert_name=cert_name_, cert_domain=domain_, private_key=private_key_, full_chain=full_chain_,
    #     cdn_domain=cdn_domain_, force_https=False, enable_http2=True)

    private_key_file_ = '../local/privkey.pem'
    full_chain_file_ = '../local/fullchain.pem'
    ret, info = cdn_toolkit.create_ssl_cert_and_activate_on_domain_from_local_file(
        cert_name=cert_name_, cert_domain=domain_, private_key_file=private_key_file_, full_chain_file=full_chain_file_,
        cdn_domain=cdn_domain_, force_https=False, enable_http2=True)

    print(info.text_body)
    print('=' * 100)
    print(ret)
