import oss2
import sys
from rmbserver import config
from rmbserver.log import log
from urllib.parse import urlparse, unquote

# 用于存储生成的文件的OSS
try:
    oss_auth = oss2.Auth(config.oss_access_key_id, config.oss_access_key_secret)
    oss_bucket = oss2.Bucket(oss_auth, config.oss_endpoint, config.oss_bucket_name)
except:
    log.error("OSS 配置错误，请检查！")
    sys.exit(1)


try:
    oss_ugc_auth = oss2.Auth(
        config.oss_ugc_access_key_id,
        config.oss_ugc_access_key_secret
    )
    oss_ugc_bucket = oss2.Bucket(
        oss_ugc_auth,
        config.oss_ugc_endpoint,
        config.oss_ugc_bucket_name
    )
except:
    log.warning("OSS UGC 配置错误，自动忽略。")
    oss_ugc_auth = None
    oss_ugc_bucket = None


def get_object_name_from_oss_url(url, bucket_obj=oss_ugc_bucket):
    # 判断提供的URL，是否是上述bucket_obj的URL
    # 返回False 或者 对应的object_name
    if not bucket_obj:
        return None

    # 解析URL
    parsed_url = urlparse(url)

    # 从URL解析主机名
    url_hostname = parsed_url.netloc

    url_bucket_name, url_base_hostname = url_hostname.split('.', 1)

    # 判断主机名是否是 bucket_obj 的主机名
    if ((bucket_obj.bucket_name, urlparse(bucket_obj.endpoint).netloc)
            == (url_bucket_name, url_base_hostname)):
        # 从URL解析对象名
        object_name = unquote(parsed_url.path[1:])
        # log.info(f"URL {url} 是 {bucket_obj.bucket_name} 的 URL, "
        #          f"对象名为 {object_name}")
        return object_name
    else:
        return None

