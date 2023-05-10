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

product_details_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/dien-thoai-samsung-galaxy-m31-128gb-6gb-hang-chinh-hang-p58259141.html?src=category-page-1789&2hi=0',
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
}

product_details_params = {
    'platform' : 'web',
    'spid' : '74326215',
}

def get_products_details(json1):
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
    value['review_count'] = json1.get('review_count')
    value['seller_product_id'] = json1.get('seller_product_id')
    return value

products = []
count = 0
for i in range(1, 3):
    list_products_params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=list_products_headers, params=list_products_params)
    if response.status_code == 200:
        print('request success!!!')
        for product in response.json()['data']:
            value = get_products_details(product)
            products.append(value)
            count += 1
        print('     ' + str(count) + ' samples collected.')
    time.sleep(random.randrange(3, 5))

df_products = pd.DataFrame(products)
print(df_products)
df_products.to_csv('products.csv', index=False)