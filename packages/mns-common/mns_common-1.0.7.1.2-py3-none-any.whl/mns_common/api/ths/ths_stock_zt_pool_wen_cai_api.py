import requests
import pandas as pd

cookies = {
    'spversion': '20130314',
    'Hm_lvt_722143063e4892925903024537075d0d': '1703751194',
    'Hm_lvt_929f8b362150b1f77b477230541dbbc2': '1703751194',
    'searchGuide': 'sg',
    'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1703751194,1704203019,1704296114,1704354142',
    'historystock': '600895%7C*%7C870199%7C*%7C002178%7C*%7C002255',
    'other_uid': 'Ths_iwencai_Xuangu_2ks4gxsl2y0m0mvrwnpzva0fkfysrtu0',
    'ta_random_userid': '9fxbvh9fz0',
    'cid': '6dceddb033111d3d626f5bc653aec43a1704862184',
    'v': 'A7SYqkofbXmQDPm1lAGiUXrthXkjjdqxGrNsqE4VQOnDM1qndp2oB2rBPFid',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'spversion=20130314; Hm_lvt_722143063e4892925903024537075d0d=1703751194; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1703751194; searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1703751194,1704203019,1704296114,1704354142; historystock=600895%7C*%7C870199%7C*%7C002178%7C*%7C002255; other_uid=Ths_iwencai_Xuangu_2ks4gxsl2y0m0mvrwnpzva0fkfysrtu0; ta_random_userid=9fxbvh9fz0; cid=6dceddb033111d3d626f5bc653aec43a1704862184; v=A7SYqkofbXmQDPm1lAGiUXrthXkjjdqxGrNsqE4VQOnDM1qndp2oB2rBPFid',
    'Origin': 'https://search.10jqka.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://search.10jqka.com.cn/unifiedwap/result?w=%E6%B6%A8%E5%81%9C',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'hexin-v': 'A7SYqkofbXmQDPm1lAGiUXrthXkjjdqxGrNsqE4VQOnDM1qndp2oB2rBPFid',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def wen_cai_web_api(page):
    data = {
        'query': '涨停',
        'urp_sort_way': 'desc',
        'page': page,
        'perpage': '100',
        'addheaderindexes': '',
        'codelist': '',
        'indexnamelimit': '',
        'logid': '8b5deaca32921b07f1f3cadfd5ed3fe0',
        'ret': 'json_all',
        'sessionid': '8b5deaca32921b07f1f3cadfd5ed3fe0',
        'source': 'Ths_iwencai_Xuangu',
        'date_range[0]': '20240110',
        'iwc_token': '0ac9664b17048806202472416',
        'urp_use_sort': '1',
        'user_id': 'Ths_iwencai_Xuangu_2ks4gxsl2y0m0mvrwnpzva0fkfysrtu0',
        'uuids[0]': '24087',
        'query_type': 'stock',
        'comp_id': '6836372',
        'business_cat': 'soniu',
        'uuid': '24087',
    }

    response = requests.post(
        'http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    data_json = response.json()

    datas = data_json['answer']['components'][0]['data']['datas']
    data_stock_df = pd.DataFrame(datas)
    return data_stock_df


def get_today_zt():
    flag = True
    page = 1
    result = None
    while flag:
        zt_df = wen_cai_web_api(page)
        if zt_df.shape[0] < 100:
            flag = False
        else:
            page = page + 1
        result = pd.concat([result, zt_df])
    return result


if __name__ == '__main__':
    zt_df_today = get_today_zt()
    print(zt_df_today)
