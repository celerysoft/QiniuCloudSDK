"""
持久化处理（pfop）
https://developer.qiniu.com/dora/api/3686/pfop-directions-for-use
"""
from qiniu import http

from sdk.base import BaseQiniuMacSDK


class DoraPropSDK(BaseQiniuMacSDK):
    BASE_URL = 'https://api.qiniu.com'

    def get_prop_status(self, persistent_id: str):
        """
        查询持久化处理状态
        https://developer.qiniu.com/dora/api/1294/persistent-processing-status-query-prefop

        :param persistent_id:
        :return:
        """
        url = self.BASE_URL + '/status/get/prefop?id=' + persistent_id

        ret, info = http._get(url=url, params=None, auth=None)

        return ret, info


sdk = DoraPropSDK()
dora_prop_sdk = sdk

if __name__ == '__main__':
    pass
