
base_id = {
    'BTC': '5b71fc48-3dd3-540c-809b-f8c94d0e68b5',
    'ETH': 'd85dce9b-5b73-5c3c-8978-522ce1d1c1b4',
    'LTC': 'c9c24c6e-c045-5fde-98a2-00ea7f520437',
    'MKR': '5553e486-7a85-5433-a5c1-aaeb18a154dd',
    'API3': '4e181288-ccce-562d-8c4f-787afa655204'
} # base_id dictionary from web scraping observation in coinbase.com


#Set this values by your own
currency_code = 'EUR' # USD, CAD, EUR
crypto_coin = 'ETH' # BTC, ETH, LTC, MKR, API3
time_range = 'year' # day, week, month, year



url= 'https://www.coinbase.com/api/v2/assets/prices/'+base_id[crypto_coin]+ '?base=' + currency_code
filename = 'data_from'+crypto_coin+ 'to'+currency_code+'.json'

import shlex, subprocess, json
import pandas as pd
import matplotlib.pyplot as plt
import os

def curl_scrapping(url): # curl method to get the json data
    cmd = '''curl ''' + url
    args = shlex.split(cmd)
    process = subprocess.Popen( args, 
                                shell=False, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    json_out = json.loads(stdout)
    return json_out['data']['prices'] # curl response to json


class Coinbase:
    def __init__(self, url, filename, time_range='day'):
        self.url = url
        self.filename = filename
        self.time_range = time_range

    def gen_json(self): # generate json file from the url
        json_out = curl_scrapping(self.url)

        with open(self.filename, 'w') as outfile:
            json.dump(json_out, outfile)
        print(self.filename + ' successfully created')

    def showdata(self): # show the data from the json file
        df = pd.read_json(self.filename)

        df_price=pd.DataFrame(df.loc['prices', self.time_range])
        df_price.columns=[currency_code, self.time_range]
        df_price[currency_code]=df_price[currency_code].astype(float)
        df_price[self.time_range]=pd.to_datetime(df_price[self.time_range], unit='s')
        df_price.plot(x=self.time_range, y=currency_code)
        plt.grid(True)
        plt.show()

def main():
    # if file does not exist, create it
    coinbase = Coinbase(url, filename, time_range)
    if not os.path.isfile(filename):coinbase.gen_json()
    coinbase.showdata()

if __name__ == '__main__':
    main()