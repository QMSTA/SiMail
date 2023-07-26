import base64


def base64_encode_filename(filename) -> str:
    """
    该方法解决部分邮箱客户端在接收携带附件的邮件时, 附件中文名不能正常显示的问题

    经测试, 部分邮箱客户端不支持附件文件使用中文名, 该方法将文件名进行base64编码并配置, 现可正常显示
    """
    encode_filename = base64.b64encode(filename.encode('utf-8')).decode('ascii')
    return f"=?UTF-8?B?{encode_filename}?="
