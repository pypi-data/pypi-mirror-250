#!/usr/bin/env python

import logging
from time import sleep

from bidfx import Session, Subject
from bidfx.pricing.tenor import Tenor

"""
Example of streaming (RFS) firm spot rates direct from LPs.
"""

def on_price_event(event):
    if event.price:
        logging.info(
            "{} {} {} {} {} -> {}".format(
                event.subject[Subject.CURRENCY_PAIR],
                event.subject[Subject.LIQUIDITY_PROVIDER],
                event.subject[Subject.DEAL_TYPE],
                event.subject[Subject.CURRENCY],
                event.subject[Subject.QUANTITY],
                event.price,
            )
        )

def on_subscription_event(event):
    logging.info(f"Subscription to {event}")

def on_provider_event(event):
    logging.info(f"Provider {event}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(threadName)-12s %(message)s",
#       filename="api.log",
    )

    session = Session.create_from_ini_file("~/.bidfx/api/config_DEV.ini")
    pricing = session.pricing
    pricing.callbacks.price_event_fn = on_price_event
    pricing.callbacks.subscription_event_fn = on_subscription_event
    pricing.callbacks.provider_event_fn = on_provider_event
    pricing.start()

    xtx_pairs = ["EURUSD", "AUDUSD", "EURCHF", "EURGBP", "EURJPY", "EURNOK", "EURPLN", "EURSEK", "GBPUSD"]#"NOKSEK", "USDCAD", "USDCHF", "USDJPY", "USDMXN", "USDRUB", "USDTRY", "USDZAR"]
    tenors = [Tenor.IN_1_WEEK, Tenor.IN_2_WEEKS]

    for q in range(1000000, 1000001, 1000000):
        for pair in xtx_pairs:
            pricing.subscribe(
                pricing.build.fx.stream.spot.liquidity_provider("JPMCFX")
                .currency_pair(pair)
                .currency(pair[0:3])
                .quantity(q)
                .create_subject()
            )

            pricing.subscribe(
                pricing.build.fx.stream.forward.liquidity_provider("JPMCFX")
                .currency_pair(pair)
                .currency(pair[0:3])
                .quantity(q)
                .tenor(Tenor.IN_1_MONTH)
                .create_subject()
            )

#   for i in range(len(currencies)):
#       for j in range(i + 1, len(currencies)):
#           for q in quantities:
#               pricing.subscribe(
#                   pricing.build.fx.stream.spot.liquidity_provider("XTXFX")
#                   .currency_pair(currencies[i] + currencies[j])
#                   .currency(currencies[i])
#                   .quantity(q)
#                   .create_subject()
#               
#               for t in tenors:
#                   pricing.subscribe(
#                       pricing.build.fx.stream.forward.liquidity_provider("XTXFX")
#                       .currency_pair(currencies[i] + currencies[j])
#                       .currency(currencies[i])
#                       .tenor(t)
#                       .quantity(q)
#                       .create_subject()
#                   )
 
#   pricing.subscribe(
#       pricing.build.fx.stream.spot.liquidity_provider("HSBCFX")
#       .currency_pair("EURUSD")
#       .currency("USD")
#       .quantity(500000)
#       .create_subject()
#   )

    sleep(3600)
    pricing.stop()


if __name__ == "__main__":
    main()
