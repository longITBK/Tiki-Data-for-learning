import requests
import time
import random
import pandas as pd

list_products_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/thoi-trang-nam/c915',
    'x-guest-token': 'kMcejsRQZoN2nFUy4ub3rfIwgWTXzh9Y',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

list_products_params = {
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': '2c1a732c-db42-f41d-bdbb-8c6afd15912a',
    'category': '915',
    'page': '1',
    'urlKey': 'thoi-trang-nam',
    'sort' : 'default',
}

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

sort = ['default', 'top_seller', 'newest', 'price,asc', 'price,desc']

def get_products_details(json1, json2):
    try:
        value = dict()
        value['id'] = json1.get('id')
        value['name'] = json1.get('name')
        value['brand'] = json1.get('brand_name')
        value['original_price'] = json1.get('original_price')
        value['discount'] = json1.get('discount')
        value['price'] = json1.get('price')
        value['discount_rate'] = json1.get('discount_rate')
        value['quantity_sold'] = json1.get('quantity_sold').get('value')
        value['rating_average'] = json1.get('rating_average')
        value['seller_id'] = json1.get('seller_id')
        value['seller_name'] = json2.get('data').get('seller').get('name')
        value['days_since_joined'] = json2.get('data').get('seller').get('days_since_joined')
        value['seller_avg_rating'] = json2.get('data').get('seller').get('avg_rating_point')
        value['is_official'] = json2.get('data').get('seller').get('is_official')
        value['review_count'] = json2.get('data').get('seller').get('review_count')
        value['total_follower'] = json2.get('data').get('seller').get('total_follower')
    except Exception as e:
        print(e)
    return value

products = []
sample_size = 10000
count = 0
flag = False

for s in sort:
    list_products_params['sort'] = s
    for i in range(1, 51):
        list_products_params['page'] = i
        response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=list_products_headers, params=list_products_params)
        requests.adapters.DEFAULT_RETRIES = 10
        if response.status_code == 200:
            print('request success!!!')
            for product in response.json()['data']:
                # Call API of Seller
                seller_params['seller_id'] = product.get('seller_id')
                response_seller = requests.get('https://tiki.vn/api/shopping/v2/widgets/seller', headers=seller_headers,
                                        params=seller_params)
                if response_seller.status_code == 200:
                    value = get_products_details(product, response_seller.json())
                    products.append(value)
                    count += 1
                    if count == sample_size:
                        flag = True
                        break
            print('     ' + str(count) + ' samples collected.')
            if flag:
                break
        time.sleep(random.randrange(7, 10))

df_products = pd.DataFrame(products)
df_products.to_csv('BigDS.csv', index=False)