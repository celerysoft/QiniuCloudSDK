# -*-coding:utf-8 -*-
import json

from qiniu import http

from sdk.base import BaseQiniuMacSDK


class CDNSslSDK(BaseQiniuMacSDK):
    def get_ssl_cert_list(self, marker: str = '', limit: int = 10):
        url = 'https://api.qiniu.com/sslcert?marker={}&limit={}'.format(marker, limit)
        # content_type = 'application/json'

        # headers = {'Content-Type': content_type}
        # ret, info = http._post_with_qiniu_mac_and_headers(url, data, self._qiniu_mac_auth, headers)
        ret, info = http._get_with_qiniu_mac(url, params=None, auth=self._qiniu_mac_auth)
        return ret, info

    def get_ssl_cert(self, cert_id: str = ''):
        url = 'https://api.qiniu.com/sslcert/{}'.format(cert_id)

        ret, info = http._get_with_qiniu_mac(url=url, params=None, auth=self._qiniu_mac_auth)
        return ret, info

    def create_ssl_cert(self, cert_name: str, domain: str, private_key: str, full_chain: str):
        url = 'https://api.qiniu.com/sslcert'
        content_type = 'application/json'

        data = {
            'name': cert_name,
            'common_name': domain,
            'pri': private_key,
            'ca': full_chain
        }
        data = json.dumps(data)

        headers = {'Content-Type': content_type}
        ret, info = http._post_with_qiniu_mac_and_headers(
            url=url, data=data, auth=self._qiniu_mac_auth, headers=headers)
        return ret, info

    def delete_ssl_cert(self, cert_id: str = ''):
        url = 'https://api.qiniu.com/sslcert/{}'.format(cert_id)

        ret, info = http._delete_with_qiniu_mac(url=url, params=None, auth=self._qiniu_mac_auth)
        return ret, info

    def delete_all_expired_certs(self):
        expired_cert_id_list = []

        marker = ''
        while True:
            cert_list_ret, info = self.get_ssl_cert_list(marker=marker, limit=10)  # type: (dict, any)
            if cert_list_ret is not None:
                cert_list = cert_list_ret['certs']
                marker = cert_list_ret['marker']

                if cert_list is None or len(cert_list) == 0:
                    break

                for cert in cert_list:  # type: dict
                    if not cert['enable']:
                        expired_cert_id_list.append(cert['certid'])

        for expired_cert_id in expired_cert_id_list:
            self.delete_ssl_cert(expired_cert_id)


class CDNDomainSDK(BaseQiniuMacSDK):
    def modify_ssl_cert(self, domain: str, cert_id: str, force_https: bool = False, enable_http2: bool = False):
        url = 'https://api.qiniu.com/domain/{}/httpsconf'.format(domain)
        content_type = 'application/json'

        data = {
            'certId': cert_id,
            'forceHttps': force_https,
            'http2Enable': enable_http2
        }
        data = json.dumps(data)

        headers = {'Content-Type': content_type}
        ret, info = http._put_with_qiniu_mac_and_headers(
            url=url, data=data, auth=self._qiniu_mac_auth, headers=headers)
        return ret, info


cdn_ssl_sdk = CDNSslSDK()
cdn_domain_sdk = CDNDomainSDK()


if __name__ == '__main__':
    pass

    # ret, info = cdn_ssl_sdk.get_ssl_cert_list('', 10)
    # print(ret)

    # ret, info = cdn_ssl_sdk.get_ssl_cert('5f11ad8e3405977d37000562')
    # print(ret)

    # cert_name_ = '*.celerysoft.com20200717'
    # domain_ = '*.celerysoft.com'
    # full_chain_ = """
    #     -----BEGIN CERTIFICATE-----
    #     MIIFWjCCBEKgAwIBAgISBI+fM/q+w5e4e+0I0GVW76dvMA0GCSqGSIb3DQEBCwUA
    #     VBKmRMQt9QfNT7snGEt7nW/2EBwMtk6HsaQ4p4Q+
    #     -----END CERTIFICATE-----
    #     -----BEGIN CERTIFICATE-----
    #     MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/
    #     KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==
    #     -----END CERTIFICATE-----
    # """
    # private_key_ = """
    #     -----BEGIN PRIVATE KEY-----
    #     MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQCq0eUnDKoYlXf7
    #     fyeFHkZES9ywvSbLGnFQeb7QeKk=
    #     -----END PRIVATE KEY-----
    # """
    # ret, info = cdn_ssl_sdk.create_ssl_cert(cert_name_, domain_, private_key_, full_chain_)
    # print(ret)

    # cert_id = '5f11ad8e3405977d37000562'
    # ret, info = cdn_ssl_sdk.delete_ssl_cert(cert_id=cert_id)
    # print(ret)

    # cdn_ssl_sdk.delete_all_expired_certs()

    # cdn_domain_sdk.modify_ssl_cert()
