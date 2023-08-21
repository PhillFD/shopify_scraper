import requests
from markdown import markdown 
from html2text import html2text 
from markdownify import markdownify
import pandas as pd

def get_json(url, page):

    try:
        response = requests.get(f'{url}/products.json?page={page}', timeout=5)
        products_json = response.json()
        response.raise_for_status()
        return products_json

    except requests.exceptions.HTTPError as error_http:
        print("HTTP Error:", error_http)

    except requests.exceptions.ConnectionError as error_connection:
        print("Connection Error:", error_connection)

    except requests.exceptions.Timeout as error_timeout:
        print("Timeout Error:", error_timeout)

    except requests.exceptions.RequestException as error:
        print("Error: ", error)

def get_products(url):
    product_list = []
    page = 1

    while True:
        products_json = get_json(url, page)

        if len(products_json['products']):
            for item in products_json['products']:
                imagesrc = []
                title = item['title']
                handle = item['handle']
                created = item['created_at']

                md = markdownify(item['body_html'])
                html2 = markdown(md)
                description = html2text(html2)
                
                for image in item['images']:
                    try:
                        imagesrc.append(image['src'])
                    except:
                        imagesrc.append('None')

                for variant in item['variants']:
                    if variant['compare_at_price'] == None:
                        original_price = variant['price']
                    else:
                        original_price = variant['compare_at_price']

                    size = variant['title']
                    current_price = variant['price']
                    sku = variant['sku']
                    available = variant['available']
                    weight = variant['grams']
                
                    product = {
                        'title': title,
                        'handle': handle,
                        'description': description,
                        'size': size,
                        'current price': current_price,
                        'original price': original_price,
                        'sku': sku,
                        'weight': weight,
                        'available': available,
                        'created': created,
                        'image': imagesrc
                    }

                    product_list.append(product)
            page += 1

        else: 
            df = pd.DataFrame(product_list)
            df.to_csv("test_1.csv")
            print("saved to file.")        
            break

product_list = get_products("https://www.iloveugly.co.nz")



