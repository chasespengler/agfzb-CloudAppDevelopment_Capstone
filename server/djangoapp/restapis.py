import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error", e)
    print("Status ", {response.status_code})
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
   
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]            
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                    address=dealer_doc["address"], 
                    city=dealer_doc["city"], 
                    full_name=dealer_doc["full_name"],
                    id=dealer_doc["id"], 
                    lat=dealer_doc["lat"], 
                    long=dealer_doc["long"],
                    short_name=dealer_doc["short_name"],
                    st=dealer_doc["st"], 
                    zip=dealer_doc["zip"]
                )
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
    
    if "body" in json_result:
        reviews = json_result["body"]["data"]
        # For each review object
        for review in reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date= "" if review["purchase"] == False else review["purchase_date"],
                car_make="" if review["purchase"] == False else review["car_make"],
                car_model="" if review["purchase"] == False else review["car_model"],
                car_year="" if review["purchase"] == False else review["car_year"],
                sentiment=analyze_review_sentiments(review["review"]),
                id=""
                )
            results.append(review_obj)
    #print(results[0])
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    api_key="_El3bzzb6hEkwffJ5CjbeRkZG8VoKLgRcjmsWFS4yQhE"
    url='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b1082e97-f92e-4311-81f7-9748b52fc8e2/v1/analyze?version=2020-08-01'
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(
        url,
        data=params,
        headers={'Content-Type':'application/json'},
        auth=HTTPBasicAuth("apikey", api_key)
        )
    
    #print(response.json())
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"


