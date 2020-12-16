"""
多文件压缩（mkzip）
https://developer.qiniu.com/dora/api/1667/mkzip
"""
from qiniu import urlsafe_base64_encode, PersistentFop

from sdk.base import BaseQiniuSDK


class DoraMkZipSDK(BaseQiniuSDK):
    def pack_files(self, bucket_name: str, key: str, mk_zip_args: dict, encoding: str = 'utf-8',
                   save_as_bucket_name: str = None, save_as_key: str = None, delete_after_days: int = None,
                   pipeline: str = None):
        """
        少量文件压缩（mode=2）

        :param bucket_name: 文件储存空间名
        :param key: 文件储存空间某个文件的文件名（存储空间内指定资源的文件名字。此处的key所指的资源内容对 mkzip 操作本身没有影响，必填是由于
                    pfop 接口规格要求请求 body 中参数必须包含 bucket 和 key，因此即使未对空间特定资源进行操作，在执行 mkzip 操作时仍然
                    需要指定账号下的特定空间和该空间的已有资源。）
        :param mk_zip_args: 文件压缩参数，dict类型，key为文件url，value为文件alias
        :param encoding: 压缩包内资源命名的编码，目前支持 gbk 和 utf-8，默认 utf-8
        :param save_as_bucket_name: 储存压缩好的文件的空间名
        :param save_as_key: 压缩文件另存为的名称
        :param delete_after_days: 将在多少天之后删除此压缩好的文件，不填则不会自动删除
        :param pipeline: 管道名称，不填则使用默认管道
        :return:
        """

        fops = 'mkzip/2/encoding/' + urlsafe_base64_encode(encoding)
        for url, alias in mk_zip_args.items():
            a = '/url/' + urlsafe_base64_encode(url) + '/alias/' + urlsafe_base64_encode(alias)
            fops += '/url/' + urlsafe_base64_encode(url) + '/alias/' + urlsafe_base64_encode(alias)

        if save_as_bucket_name is not None and save_as_key is not None:
            save_as = urlsafe_base64_encode(save_as_bucket_name + ':' + save_as_key)
            fops = fops + '|saveas/' + save_as

            if delete_after_days is not None:
                fops += '/deleteAfterDays/' + str(delete_after_days)

        ops = []
        pfop = PersistentFop(self._qiniu_auth, bucket_name, pipeline)

        ops.append(fops)
        ret, info = pfop.execute(key, ops, 1)

        return ret, info

    def pack_large_number_of_files(self, bucket_name: str, index_file_key: str, encoding: str = 'utf-8',
                                   save_as_bucket_name: str = None, save_as_key: str = None,
                                   delete_after_days: int = None, pipeline: str = None):
        """
        大量文件压缩（mode=4）
        为了将大量文件压缩，可以将待压缩文件URL写入一个索引文件，上传至bucket，再对该索引文件进行的mkzip操作。
        索引文件格式为：<br>
        /url/<Base64EncodedURL1>[/alias/<Base64EncodedAlias1>]
        /url/<Base64EncodedURL2>[/alias/<Base64EncodedAlias2>]
        ... ...
        /url/<Base64EncodedURLN>[/alias/<Base64EncodedAliasN>]

        :param bucket_name: 索引文件储存空间名
        :param index_file_key: 索引文件名
        :param encoding: 压缩包内资源命名的编码，目前支持 gbk 和 utf-8，默认 utf-8
        :param save_as_bucket_name: 储存压缩文件的空间名
        :param save_as_key: 压缩文件另存为的名称
        :param delete_after_days: 将在多少天之后删除此压缩好的文件，不填则不会自动删除
        :param pipeline: 管道名称，不填则使用默认管道
        :return:
        """
        fops = 'mkzip/4/encoding/' + urlsafe_base64_encode(encoding)

        if save_as_bucket_name is not None and save_as_key is not None:
            save_as = urlsafe_base64_encode(save_as_bucket_name + ':' + save_as_key)
            fops = fops + '|saveas/' + save_as

            if delete_after_days is not None:
                fops += '/deleteAfterDays/' + str(delete_after_days)

        ops = []
        pfop = PersistentFop(self._qiniu_auth, bucket_name, pipeline)

        ops.append(fops)
        ret, info = pfop.execute(index_file_key, ops, 1)

        return ret, info


sdk = DoraMkZipSDK()
dora_mk_zip_sdk = sdk

if __name__ == '__main__':
    pass
