import requests
import time
import random
import pandas as pd
import json

seller_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    #'Referer': 'https://tiki.vn/ao-chong-nang-nam-cao-cap--thong-hoi--chong-nang--chong-tia-uv--chong-bam-bui---formen-shop---fmtht024-p79435123.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.124876_Y.1228710_Z.2878025_CN.Ad-group-124876&itm_medium=CPC&itm_source=tiki-ads&spid=79435137',
    'x-guest-token': 'kMcejsRQZoN2nFUy4ub3rfIwgWTXzh9Y',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

seller_params = {
    'seller_id': '17914',
    'mpid' : '79435123',
    'spid' : '79435137',
    'trackity_id' : '7dfb9fec-ef2f-4957-1848-61b44a86b2c0',
    'platform' : 'desktop'
}

products = []
count = 0
for i in range(1, 2):
    response = requests.get('https://tiki.vn/api/shopping/v2/widgets/seller', headers=seller_headers, params=seller_params)
    if response.status_code == 200:
        print('request success!!!')
        print(response.json())
        value = dict()
        value['seller_avg_rating'] = response.json().get('data').get('seller').get('avg_rating_point')
        value['is_official'] = response.json().get('data').get('seller').get('is_official')
        value['review_count'] = response.json().get('data').get('seller').get('review_count')
        value['total_follower'] = response.json().get('data').get('seller').get('total_follower')
        products.append(value)

        count += 1
        print('     ' + str(count) + ' samples collected.')
    time.sleep(random.randrange(3, 5))

df_products = pd.DataFrame(products)
print(df_products)
df_products.to_csv('products_abc.csv', index=False)