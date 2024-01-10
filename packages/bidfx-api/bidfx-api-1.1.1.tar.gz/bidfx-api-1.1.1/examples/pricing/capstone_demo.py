from time import sleep

from bidfx import Session

 

import logging

import sys

event_test = None

output_file = None

 

def on_price_event(event):

    global event_test

    #global output_file
    #output_file = open('bidfx.csv', 'a')

    print("Got update")

    print_str = ''

    try:

        #for key in event.price.keys():

        #    print_str += key + '='  + str (event.price[key]) + ','

        #print_str = str(event.subject) + "," + print_str + "\n"
        print(f"Price update to {event}")

        #output_file.write(print_str)

    except Exception as e:

        print(e)

        pass
        
    #output_file.close()

 

def main():

 

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(

        #"%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"

        "%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s (%(filename)s:%(lineno)d)", "%Y-%m-%d %H:%M:%S"

    )

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    #output_file = open('bidfx.csv', 'w')
 
    print("creating session")
    session = Session.create_from_ini_file("~/.bidfx/api/config_UAT.ini")

    print("creating pricing")
    pricing = session.pricing

    print("registering callback")
    pricing.callbacks.price_event_fn = on_price_event

 
    print("starting pricing")
    pricing.start()

 

    for lp in ["GSFX", "DBFX", "UBSFX", "JPMCFX", "BNPFX", "BARCFX", "BOFAFX", "CACIBFX","CITIFX", "HSBCFX", "NOMURAFX", "RBSFX", "SGFX", "SSFX", "SCBFX"]:
    #for lp in ["JPMCFX"]:

        for ccy_pair in ["USDBRL","USDCOP","USDCLP","USDPEN","USDKRW","USDPHP","USDTWD","USDIDR","USDINR", "USDCNY"]: #["EURUSD", "GBPUSD", "USDJPY"]:
        #for ccy_pair in ["USDCNY"]: #["EURUSD", "GBPUSD", "USDJPY"]:

            ccy = ccy_pair[:3]

            print("Building price subject")
            pricing.subscribe(

                #pricing.build.fx.stream.spot.liquidity_provider(lp)

                pricing.build.fx.stream.ndf.liquidity_provider(lp)

                .currency_pair(ccy_pair)

                .tenor("1M")

                .currency("USD")

                .quantity(1000000)

                .create_subject()

            )

 
    print("Subscribed to all prices")

    sleep(60)

    pricing.stop()

    #output_file.close()

 

if __name__ == "__main__":

    main()
