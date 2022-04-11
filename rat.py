import requests
import json
import time

contract = "0x14e0a1f310e2b7e321c91f58847e98b8c802f6ef"
timeNow = time.time()
etherscanAPI = ""
openseaAPI = ""

for index in range(100):
  limit = 200
  offset = index * limit

  
  url = "https://api.opensea.io/api/v1/events?asset_contract_address="+str(contract)+"&event_type=successful"

  if(cursor):
    url = url + "&cursor="+cursor

  print(url);

  headers = {
      "Accept": "application/json",
      "X-API-KEY": openseaAPI
  }
  try: 
    response = requests.request("GET", url, headers=headers)

    sales = json.loads(response.text)


    if("next" in sales):
      cursor = sales['next']

    if('asset_events' in sales):
      if(sales['asset_events']):
        for trans in sales["asset_events"]:
          buyer = trans["winner_account"]
          price = int(trans["total_price"])/1000000000000000000
          # print(buyer["address"])
          eth_url = "https://api.etherscan.io/api?module=account&action=txlist&address="+buyer["address"]+"&startblock=0&endblock=99999999&offset=0&sort=asc&apikey="+str(etherscanAPI)

          eth_res = requests.request("GET", eth_url)
          txn = json.loads(eth_res.text)
          # print(len(txn["result"]))
          cnt += 1;
          print(cnt);
          if('result' in txn):
            if not (txn['result'] is None):
              if(len(txn["result"]) < 6):
                print(buyer["address"],' ', price,flush=True)
  except Exception as ex:
    print("This request is bad")
    print(ex)
