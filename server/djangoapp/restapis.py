import requests
import json
# import related models here
from models import CarDealer, CarMake, CarModel, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, autho=HTTPBasicAuth('apikey', api_key))
       else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error", e)
    print("Status ", {response.status_code})
    json_data = json.loads(response.text)
    return 

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["body"]["data"]
        # For each review object
        for review in reviews:
            review_obj = DealerReview(
                name = review['name'],
                purchase = review['purchase'],
                review = review['review'],
                dealership = review['dealership'],
                purchase_date = review['purchase_date'] if review['purchase'] else 'na',
                car_make = review['car_make'] if review['purchase'] else 'na',
                car_model = review['car_model'] if review['purchase'] else 'na',
                car_year = review['car_year'] if review['purchase'] else 'na',
                sentiment = analyze_review_sentiments(review['review']),
                id = review['id']
                )
            results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    api_key="3bvJIGsWLzs8lDiK5ZVHr12IVUGToEC58ujJArcFN-9z"
    url='https://api.us-south.language-translator.watson.cloud.ibm.com/instances/f91e96b6-33a1-4432-85eb-d017c56aa405'
    params = {'text': kwargs['text'], 'version': kwargs['version'], 'features': kwargs['features'], 'return_analyzed_text': kwargs['return_analyzed_text']}
    response = requests.get(
        url,
        data=params,
        headers={'Content-Type':'application/json'},
        auth=HTTPBasicAuth("apikey", api_key)
        )
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"



