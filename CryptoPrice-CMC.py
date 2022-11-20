# -------------------------------------
# Program Starts from here
# ------------------------------------- 
import os
import configparser
from requests import Session
import time
from numerize import numerize



# -------------------------------------------------------
# Extracting info
# -------------------------------------------------------


def getInfo( key ) :

    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = config['cmc']['api_url'] # Coinmarketcap API url

    parameters = { 'slug': key, 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    api_key = config['cmc']['api_key']

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    } # Replace 'YOUR_API_KEY' with the API key you have recieved

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    if response:

        info = response.json()
    
    else:

        init_loop = True

        while init_loop:

            time.sleep(1)
            print( "Requesting Response......" )
            response = session.get(url, params=parameters)

            if response :

                info = response.json()
                init_loop = False

            else:
                init_loop = True

    return info



# -------------------------------------------------------
# Generating Status
# -------------------------------------------------------


def getStatus( name, symbol, price, m_cap, change_1h , change_24h, volume_24h ):

    status = f"{name} #{symbol} Statistics 📊 \n\n Current price is : {price} USD with marketcap of : {m_cap} USD. \n In last 1H, price change in percentage is {change_1h}%. \n In 24H time frame, {change_24h}% was change with volume of : {volume_24h} USD. \n\n #{symbol}Price"

    return status


def main():

    query = {
        "bitcoin" : '1',
        "ethereum" : '1027',
        "bnb" : '1839',
        "solana" : '5426',
        "cardano" : '2010',
        "polygon" : '3890',
        "polkadot" : '6636',
        "dogecoin" : '74',
        "xrp" : '52',
        "tron" : '1958'
    }

    for key, value in query.items():

        print(">>>>>> Init Requesting Response. <<<<<<")

        info = getInfo( key )
        data = info['data'][value]

        name = data['name']
        symbol = data['symbol']
        price = round( data['quote']['USD']['price'], 5 )
        m_cap = numerize.numerize( data['quote']['USD']['market_cap'], 2 )
        change_1h = round( data['quote']['USD']['percent_change_1h'], 2 )
        change_24h = round( data['quote']['USD']['percent_change_24h'], 2 )
        volume_24h = numerize.numerize( data['quote']['USD']['volume_24h'], 2 )

        print("------ Writing {} price. ------".format(key))

        with open(r"CryptoPrice-CMC.txt", "a") as cp:

            cp.write( f"{name} #{symbol} Statistics \n\n Current price is : {price} USD with marketcap of : {m_cap} USD. \n In last 1H, price change in percentage is {change_1h}%. \n In 24H time frame, {change_24h}% was change with volume of : {volume_24h} USD. \n\n #{symbol}Price" )

            cp.write( "\n\n -------------------------------------" )
            cp.write( "------------------------------------- \n\n" )

        print("****** Done writing {} price. ******\n".format(key))
        cp.close()
        time.sleep(1)



# -------------------------------------------------------
# Run Program
# -------------------------------------------------------


if __name__ == '__main__':

    if os.path.isfile(r"CryptoPrice-CMC.txt"):

        print("Removing existing price file.")
        time.sleep(1)
        os.remove(r"CryptoPrice-CMC.txt")
        print("Removed price file. \n")
        time.sleep(1)
        
    main()











    


	                        




