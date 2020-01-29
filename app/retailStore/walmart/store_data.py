import json
from datetime import datetime
from app import db
from app.models import Item, Receipt, Image
from app.retailStore.add_image import add_image_to_folder
from app.retailStore.walmart.get_categories import get_walmart_categories
from concurrent import futures

# Stores the walmart data gathered from the api call to the database
def store_walmart_data(receipt_json, user_id):
    receipt_data = json.loads(receipt_json)

    date = receipt_data['receipts'][0]['dateTime'].split()[0]
    store = receipt_data['receipts'][0]['store']['displayName']
    sales_tax = receipt_data['receipts'][0]['total']['taxTotal']
    subtotal = receipt_data['receipts'][0]['total']['subtotal']

    queried_receipt = Receipt.query.filter_by(date=date, store=store, sales_tax=sales_tax, subtotal=subtotal, user_id=user_id).first()
    receipt = Receipt(date=date, store=store, sales_tax=sales_tax, subtotal=subtotal, user_id=user_id)

    #ERROR: SAME RECEIPT
    if queried_receipt == None or queried_receipt != receipt:
        db.session.add(receipt)
        db.session.commit()

        items = receipt_data['receipts'][0]['items']

        item_list = []
        with futures.ThreadPoolExecutor() as executor:
            futures_list = {}
            category_list = {}
            for item in items:
                name = item['description']
                price = item['price']
                upc = item['upc']
                image_url = item['imageUrl']

                i = Item(
                        name=name,
                        price=price,
                        upc=upc,
                        receipt_id=receipt.id
                        )
                item_list.append(i)

                category_list[executor.submit(get_walmart_categories, i)] = name
                futures_list[executor.submit(add_image_to_folder, image_url, upc)] = name

            for future in futures.as_completed(category_list):
                item_name = category_list[future]
                for item in item_list:
                    if item.name == item_name:
                        categoryList = future.result()
                        item.category1 = categoryList[0]
                        item.category2 = categoryList[1]
                        item.category3 = categoryList[2]

            for future in futures.as_completed(futures_list):
                item_name = futures_list[future]
                for item in item_list:
                    if item.name == item_name:
                        item.image_id = future.result()
                        db.session.add(item)
                        db.session.commit()
    else:
        #Do more with "same reciept" error
        print('Same Receipt')
