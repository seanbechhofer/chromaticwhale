#!/usr/local/bin/python
"""Generate reports from a tracery grammar"""
__author__ = "Sean Bechhofer"
__copyright__ = "Copyright 2016, Sean Bechhofer"
__credits__ = ["Sean Bechhofer"]
import json
import argparse
import twitter
import tracery
from tracery.modifiers import base_english
import twitter
import os
from random import randint

# Twitter character limit
LIMIT = 140

# Max number of attempts
ATTEMPTS = 10

def tweet(grammar, production):
    stuff = ""
    with open(grammar) as f:
        rules = json.load(f)
    
        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)

        stuff = grammar.flatten("#" + production + "#")
        count = 0
        while len(stuff) > LIMIT and count < ATTEMPTS:
            print "Re-rolling..."
            stuff = grammar.flatten("#" + production + "#")
            count += 1
    if len(stuff) > LIMIT:
        stuff = ""
    return stuff

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Generate Tracery Grammar.')
    parser.add_argument('-c', '--config', help='configuration file', default="config.json")
    parser.add_argument('-n', '--notweet', help='no tweeting', action="store_true")

    args = parser.parse_args()

    config = json.load(open(args.config))

    consumer_key=os.environ['API_KEY']
    consumer_secret=os.environ['API_SECRET']
    access_token_key=os.environ['ACCESS_TOKEN']
    access_token_secret=os.environ['ACCESS_SECRET']

#    consumer_key=config['api.key']
#    consumer_secret=config['api.secret']
#    access_token_key=config['access.token']
#    access_token_secret=config['access.secret']

    grammar = config['grammar']
    production = config['production']
    frequency = config['frequency']

    print "Grammar: {}, production: {}".format(grammar, production)

    tweetText = tweet(grammar=grammar,production=production)
    if tweetText == "":
        print "Unsuccesful Generation"
    else:
        diceRoll = randint(0,frequency-1)
        if diceRoll == 0:
            api = twitter.Api(consumer_key,
                            consumer_secret,
                            access_token_key,
                            access_token_secret)
            account_name = api.VerifyCredentials().screen_name
            print "Verified: {}".format((account_name))
            if args.notweet:
                print "Not tweeted"
                print tweetText
            else:
                status = api.PostUpdate(tweetText)
                print "http://twitter.com/{}/status/{}".format(account_name, status.id)
                print status.text
        else:
            print "No Tweet this time"
            
                

            
