import json
import requests

# Walmart API constants
WLMT_STORE_ID_STR = "storeId"
WLMT_PURCH_DATE_STR = 'purchaseDate'
WLMT_CARD_TYPE_STR = "cardType"
WLMT_TOTAL_STR = 'total'
WLMT_LAST_FOUR_STR = "lastFourDigits"

# Make a POST request to walmart's receipt API to get json data back with the
#   receipt information requested.
def api_call(store_id, purch_date, card_type, total, last_four):
    data = {
        WLMT_STORE_ID_STR : str(store_id),
        WLMT_PURCH_DATE_STR : str(purch_date),
        WLMT_CARD_TYPE_STR : str(card_type),
        WLMT_TOTAL_STR : str(total),
        WLMT_LAST_FOUR_STR : str(last_four)
    }

    response = requests.post('https://www.walmart.com/chcwebapp/api/receipts', \
                            json=data)
    receipt_json = response.json()

    # Delete the image of the barcode. Did this at the time because the URL is
    #   really long
    if (response.status_code == 200):

        for i in receipt_json['receipts'][0]:
            if (i == 'image'):
                del receipt_json['receipts'][0]['image']
                break
    else:
        print('No good status code')
    return json.dumps(receipt_json)
