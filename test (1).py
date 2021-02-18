#!/usr/bin/env python
# coding: utf-8

# In[44]:


import requests
import datetime
import time

# Create your tests here.

IP = '193.61.36.66:8000'
URL = 'http://{}/'.format(IP)

TOKEN_DICT = {}


def register_payload(username, password):
    data = {
        'username': username,
        'password': password
    }
    return data


def test_TC1():
    """
    Olga, Nick and Mary register in the application and are ready to access the API
    """
    url = "authentication/register/"

    data = register_payload('olga', 'olga1234')

    res = requests.post(URL + url, data=data)
    TOKEN_DICT['olga'] = res.json()
   
    print("response:{}".format(res.json()))

    data = register_payload('nick', 'nick1234')

    res = requests.post(URL + url, data=data)
    TOKEN_DICT['nick'] = res.json()
   
    print("response:{}".format(res.json()))

    data = register_payload('mary', 'mary1234')

    res = requests.post(URL + url, data=data)
    TOKEN_DICT['mary'] = res.json()
   
    print("response:{}".format(res.json()))
    
    

def   test_TC2():
    """
    Olga, Nick and Mary will use the oAuth V2 authorisation service to get their tokens
    """
    
    
    url='authentication/token/refresh/'
    token = TOKEN_DICT['olga']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}
    data={'refresh_token':TOKEN_DICT['olga']['refresh_token']}
    
    res = requests.post(URL + url, headers=headers, data=data)
    #res = requests.post(URL + url, headers=headers)
    print(res.json())
    
    TOKEN_DICT['olga']= res.json()
    
    
    
    
def   test_TC3():
    """
    Olga makes a call to the API (any endpoint) without using a token. This call should be unsucessfull as the user is unauthorised. 
    """
    
    url='api/item/'
    
    
    res = requests.get(URL + url)
    #res = requests.post(URL + url)
    print(res.json())

    

def test_TC4():
    """
    Olga adds an item for auction with an expiration time using her token
    """
    url = "api/item/"
    token = TOKEN_DICT['olga']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    # set expire time to next day
    data={
    "expire_time": datetime.datetime.now() + datetime.timedelta(1),
    "title": "phone",
    "condition": "N",
    "price": 250,
    "description": "new Nokia phone"
    }
    res = requests.post(URL + url, headers=headers, data=data)
    #res = requests.post(URL + url, data=data)
    print(res.json())


def test_TC5():
    """
    Nick adds an item for auction with an expiration time using her token
    """
    url = "api/item/"
    token = TOKEN_DICT['nick']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    # set expire time to next day
    data={
    "expire_time": datetime.datetime.now() + datetime.timedelta(1),
    "title": "monitor",
    "condition": "N",
    "price": 500,
    "description": "new LG monitor"
    }
    res = requests.post(URL + url, headers=headers, data=data)
    #res = requests.post(URL + url, data=data)
    print(res.json())


def test_TC6():
    """
    Mary adds an item for auction with an expiration time using her token
    """
    url = "api/item/"
    token = TOKEN_DICT['mary']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    # set expire time to next hour
    data={
    "expire_time": datetime.datetime.now() + datetime.timedelta(0,60,0),
    "title": "laptop",
    "condition": "U",
    "price": 280,
    "description": "used HP laptop"
    }
    res = requests.post(URL + url, headers=headers, data=data)
    #res = requests.post(URL + url, data=data)
    print(res.json())


def test_TC7():
    """
    TC 7. Nick and Olga browse all the available items, there should be three items available
    """

    url = "api/item/"
    token = TOKEN_DICT['nick']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url, headers=headers)
    print(res.json())

    token = TOKEN_DICT['olga']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url, headers=headers)
    print(res.json())


def test_TC8():
    """
    TC 8. Nick and Olga get only the details of Mary’s item only.
    """
   
    url = "api/item/"
    token = TOKEN_DICT['nick']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url, headers=headers)

    item_id = None
    for item in res.json():
        if item['owner']  == 'mary':
            item_id = item['item_id']
            break

    token = TOKEN_DICT['nick']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url + str(item_id), headers=headers)
    print(res.json())

    token = TOKEN_DICT['olga']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url + str(item_id), headers=headers)
    print(res.json())


def test_TC9():
    """
    TC 9. Mary bids for her own item. This call should be unsuccessful, an owner cannot bid for own items.
    """

    url = "api/item/"
    token = TOKEN_DICT['mary']['access_token']
    headers = {'Authorization': 'Bearer '+str(token)}

    res = requests.get(URL + url, headers=headers)

    item_id = None
    for item in res.json():
        if item['owner']  == 'mary':
            item_id = item['item_id']
            break

    data={
     "item_id": item_id,
     "bidding_amount": 300
    }
    url = "api/bid/"
    res = requests.post(URL + url, headers=headers, data=data)
    #res = requests.post(URL + url, data=data)
    print(res.json())

def test_TC10():
    """
    TC 10. Nick and Olga bid for Mary’s item in a round robin fashion (one after the other).
    """

    url = "api/item/"
    token_nick = TOKEN_DICT['nick']['access_token']
    headers_nick = {'Authorization': 'Bearer '+str(token_nick)}

    res = requests.get(URL + url, headers=headers_nick)
    marry_item_id = None
    for item in res.json():
        if item['owner']  == 'mary':
            marry_item_id = item['item_id']
            break

    url_bid = "api/bid/"
    token_olga = TOKEN_DICT['olga']['access_token']
    headers_olga = {'Authorization': 'Bearer '+str(token_olga)}

    bidding_amount = 300
    for i in range(6):
        data={
         "item_id": marry_item_id,
         "bidding_amount": bidding_amount
        }
        bidding_amount += 50
        if i % 2 == 0:
            res = requests.post(URL + url_bid, headers=headers_nick, data=data)
            print(res.json())
        else:
            res = requests.post(URL + url_bid, headers=headers_olga, data=data)
            print(res.json())



def test_TC11():
    time.sleep(60)
    """
    TC 11. Nick or Olga wins the item after the end of the auction.
    """

    #wait for 1 hour then execute this TC

    url = "api/item/"
    token_nick = TOKEN_DICT['nick']['access_token']
    headers_nick = {'Authorization': 'Bearer '+str(token_nick)}

    res = requests.get(URL + url, headers=headers_nick)
    for item in res.json():
        if item['owner']  == 'mary':
            print(item) 


def test_TC12():
    """
    TC 12. Olga browses all the items sold
    """

    url = "api/item/"
    token_olga = TOKEN_DICT['olga']['access_token']
    headers_olga = {'Authorization': 'Bearer '+str(token_olga)}

    res = requests.get(URL + url, headers=headers_olga)
    for item in res.json():
        if item['auction_status']  == 'C':
            print(item)

test_TC1()
test_TC2()
test_TC3()
test_TC4()
test_TC5()
test_TC6()
test_TC7()
test_TC8()
test_TC9()
test_TC10()
test_TC11()
test_TC12()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




