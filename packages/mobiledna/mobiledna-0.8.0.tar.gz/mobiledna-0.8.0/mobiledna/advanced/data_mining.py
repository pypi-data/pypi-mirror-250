# -*- coding: utf-8 -*-

"""
    __  ___      __    _ __     ____  _   _____
   /  |/  /___  / /_  (_) /__  / __ \/ | / /   |
  / /|_/ / __ \/ __ \/ / / _ \/ / / /  |/ / /| |
 / /  / / /_/ / /_/ / / /  __/ /_/ / /|  / ___ |
/_/  /_/\____/_.___/_/_/\___/_____/_/ |_/_/  |_|

Machine learning & data mining functions

-- Coded by Simon Perneel
-- mailto:Simon.Perneel@UGent.be
"""
import pandas as pd
from apyori import apriori

from mobiledna.core.appevents import Appevents
import mobiledna.core.help as hlp


def get_association_rules(apps: Appevents, min_confidence=.5, min_support_tresh=0.005, min_lift=1, min_length=None):
    """
    Look for association rules to find apps that are frequently occuring together in a phone session.
    Apriori algorithm is used
    :param apps: Appevents object
    :param min_confidence: minimal confidence of the association rule (confidence A=>B = prob(B|A))
    :param min_support_tresh: minimum support treshold of the rule (= support count / # sessions)
    :param min_lift: minimum lift for the rule (lift A=>B = prob(B|A)/prob(B)
    :param min_length: minimum number of apps in the rule
    """
    # todo: option do this on person-level instead of all sessions together
    # group all sessions and get applications
    transactions = list(apps.get_data().groupby('session')['application'].apply(list))

    # Find association rules
    results = list(apriori(transactions,
                           min_support=min_support_tresh,
                           min_confidence=min_confidence,
                           min_lift=min_lift)
                   )

    if min_length:
        results = list(filter(lambda x: len(x.items) >= min_length, results))

    return results

def estimate_phone_health(apps: Appevents):
    ## todo, under construction
    apps_df = apps.get_data()
    apps_df['battery_shifted'] = apps_df.battery.shift(1)
    apps_df['battery_diff'] = apps_df['battery'] - apps_df['battery_shifted']

    charging_df = apps_df.groupby(['id', 'startDate'])['battery_diff'].agg([('discharged', lambda x: x[x < 0].sum()), ('charged', lambda x: x[x > 0].sum())])
    screentime = apps_df.groupby(['id', 'startDate'])['duration'].sum().div(60)
    charging_df = charging_df.merge(screentime, on=['id', 'startDate'], how='outer')

    # get average battery drain (% drain/min. screentime)
    charging_df['avg_drain'] = charging_df['discharged'] / abs(charging_df['duration'])
    print(charging_df.tail(10))


if __name__ == '__main__':
    hlp.hi()
    hlp.set_param(log_level=3, data_dir='../../data/')
    data = Appevents.load_data('../../data/total_sample_dec_2022/0baeabb1-27a1-4caf-9f64-212bba194677_appevents.parquet')
    estimate_phone_health(data)


