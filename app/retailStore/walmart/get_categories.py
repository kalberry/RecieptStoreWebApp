import requests
from lxml import html
from app import db
from app.models import Item

# Make a request to the walmart website to get an item's top 3 categories
# This needs to be fixed. Get the first item in the search list and get those
#   categories
def get_walmart_categories(item):
    i = Item.query.filter_by(name=item.name, upc=item.upc).first()

    if i != item:
        search_string = "https://www.walmart.com/search/?query="+item.name
        request = requests.get(search_string)
        root = html.fromstring(request.content)
        first_item = root.xpath('//*[@id="searchProductResult"]/ul/li[1]/div/div[2]/div[2]/a/@href')
        if not first_item:
            first_item = root.xpath('//*[@id="searchProductResult"]/div/div[1]/div/div/div[2]/div[1]/a/@href')

        if first_item:
            item_request = requests.get('https://www.walmart.com' + first_item[0])
            item_root = html.fromstring(item_request.content)
            category_list = item_root.xpath('//*[@class="breadcrumb-list"]/li/a/span/span/text()')

            return category_list
        else:
            # If its a fee, dont get this far!
            return [None, None, None]
    elif i == item:
        print('Already in DB')
        return [i.category1, i.category2, i.category3]
