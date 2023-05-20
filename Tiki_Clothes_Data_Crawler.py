import requests
import time
import random
import pandas as pd
import os
import csv
from retrying import retry

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
    'trackity_id': '7dfb9fec-ef2f-4957-1848-61b44a86b2c0',
    'category': '915',
    'page': '1',
    'urlKey': 'thoi-trang-nam',
    'sort' : 'top_seller'
}

seller_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
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

urlKey_category = {
    'thoi-trang-nam' : '915',
    # 'giay-dep-nam' : '1686'
    'ao-thun-nam' : '917',
    'ao-so-mi-nam' : '918',
    'ao-vest-ao-khoac-nam' : '925',
    'quan-nam' : '27562',
    'tui-thoi-trang-nam' : '27616',
    'do-ngu-do-mac-nha-nam' : '27570'

}

sort = ['default', 'top_seller']

def get_products_details(json1, json2):
    try:
        value = dict()
        value['id'] = json1.get('id')
        value['name'] = json1.get('name')
        value['brand'] = json1.get('brand_name')
        value['original_price'] = json1.get('original_price')
        value['discount'] = json1.get('discount')
        value['current_price'] = json1.get('price')
        value['discount_rate'] = json1.get('discount_rate')
        value['quantity_sold'] = json1.get('quantity_sold').get('value')
        value['rating_average'] = json1.get('rating_average')
        value['product_review_count'] = json1.get('review_count')
        value['seller_id'] = json1.get('seller_id')
        value['seller_name'] = json2.get('data').get('seller').get('name')
        value['days_since_joined'] = json2.get('data').get('seller').get('days_since_joined')
        value['seller_rating_average'] = json2.get('data').get('seller').get('avg_rating_point')
        value['is_official'] = json2.get('data').get('seller').get('is_official')
        value['seller_review_count'] = json2.get('data').get('seller').get('review_count')
        value['total_follower'] = json2.get('data').get('seller').get('total_follower')
    except Exception as e:
        value = None
        print(e)
    return value

csv_file = "HugeDS.csv"
header = ['id', 'name', 'brand', 'original_price', 'discount', 'current_price', 'discount_rate', 
          'quantity_sold', 'rating_average', 'product_review_count', 'seller_id', 'seller_name', 
          'days_since_joined', 'seller_rating_average', 'is_official', 'seller_review_count', 'total_follower']
products = []
sample_size = 5000
count = 0
flag = False

# Khởi tạo session để sử dụng cho tất cả các request
session = requests.Session()
# Đặt số lần retry mặc định là 10
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=10))

@retry(wait_random_min=5000, wait_random_max=10000)
def get_response(url, headers, params):
    response = session.get(url, headers=headers, params=params)
    # Kiểm tra trạng thái của response
    if response.status_code == 200:
        return response
    else:
        # Nếu response lỗi, raise một exception để retry lại
        raise ValueError(f"Request failed with error {response.status_code}. Retrying...")


    # for s in sort:
    #     list_products_params['sort'] = s
for i in range(1, 51):
    list_products_params['page'] = i
    for key, category in urlKey_category.items():
        list_products_params['urlKey'] = key
        list_products_params['category'] = category
        print('Page: ', i, ' - ', 'urlKey: ', key, ' - ', 'Category: ', category)
        response = get_response('https://tiki.vn/api/personalish/v1/blocks/listings', headers=list_products_headers, params=list_products_params)        
        if response.status_code == 200:
            print('request success!!!')
            for product in response.json()['data']:
                # Call API of Seller
                seller_params['seller_id'] = product.get('seller_id')
                response_seller = get_response('https://tiki.vn/api/shopping/v2/widgets/seller', headers=seller_headers,
                                        params=seller_params)
                if response_seller.status_code == 200:
                    # Lấy các dữ liệu từ file json khi respond trả về
                    value = get_products_details(product, response_seller.json())
                    if value != None:
                        products.append(value)
                        count += 1
                        if not os.path.isfile(csv_file):
                            # Nếu không tồn tại, tạo tệp mới và ghi tiêu đề vào tệp
                            with open(csv_file, mode="w", newline="") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(header)
                        else:
                            # Nếu đã tồn tại, mở tệp và ghi tiếp dữ liệu vào tệp
                            with open(csv_file, mode="a", newline="", encoding="utf-8") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(list(value.values()))
                    if count == sample_size:
                        flag = True
                        break
            print('     ' + str(count) + ' samples collected.')
            if flag:
                break            
        time.sleep(random.randrange(7, 10))
        if flag:
            break
    if flag:
        break

print("Done crawling !!!")
# df_products = pd.DataFrame(products)
# print(df_products)
# df_products.to_csv('HugeDS.csv', index=False)