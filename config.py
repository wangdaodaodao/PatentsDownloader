# -*- coding: utf-8 -*-

"""
    作者:     王导导
    版本:     1.0
    日期:     2019/02/11
    项目名称： 专利下载

"""

verify_url = 'http://www2.drugfuture.com/cnpat/verify.aspx'
verifycode_url = 'http://www2.drugfuture.com/cnpat/verifyCode.aspx'
search_url = 'http://www2.drugfuture.com/cnpat/search.aspx'
securepdf_url = 'http://{host_name}/cnpat/SecurePdf.aspx'

headers_verify = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www2.drugfuture.com',
    'Origin': 'http://www.drugfuture.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.drugfuture.com/cnpat/cn_patent.asp',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4399.400 QQBrowser/9.7.12777.400',
}

headers_search = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '51',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www2.drugfuture.com',
    'Origin': 'http://www2.drugfuture.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www2.drugfuture.com/cnpat/verify.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4399.400 QQBrowser/9.7.12777.400',
}

headers_verifycode = {
    'Referer': 'http://www2.drugfuture.com/cnpat/verify.aspx',
    'Host': 'www2.drugfuture.com',
    'Accept': 'image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Language': 'en-us',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4(KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
}

headers_securepdf = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '415',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www2.drugfuture.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www2.drugfuture.com/cnpat/search.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4399.400 QQBrowser/9.7.12777.400'
}


headers_p_info = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;,',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
    'Content-Type': 'application/grpc-web+proto',
}