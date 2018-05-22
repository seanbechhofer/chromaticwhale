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
    parser.add_argument('-n', '--notweet', help='no actual tweeting', action="store_true")
    parser.add_argument('-d', '--debug', help='debug', action="store_true")
    parser.add_argument('-u', '--noauth', help='don\'t authenticate. Implies no tweeting.', action="store_true")
    parser.add_argument('-t', '--tweets', help='produce n tweets', default=1)

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

    api = None
    account_name = ""

    if args.noauth:
        print "Not authenticating"
    else:
        api = twitter.Api(consumer_key,
                              consumer_secret,
                              access_token_key,
                              access_token_secret)
        account_name = api.VerifyCredentials().screen_name
        print "Verified: {}".format((account_name))
        
    print "Grammar: {}, production: {}".format(grammar, production)

    for i in range(0,int(args.tweets)):
        tweetText = tweet(grammar=grammar,production=production)
        if tweetText == "":
            print "Unsuccesful Generation"
        else:
            diceRoll = randint(0,frequency-1)
            if args.debug or diceRoll == 0:
                if args.notweet or args.debug or args.noauth:
                    # We haven't authenticated or explicitly asked for no tweeting. 
                    print "Not tweeted"
                    print tweetText
                else:
                    status = api.PostUpdate(tweetText)
                    print "http://twitter.com/{}/status/{}".format(account_name, status.id)
                    print status.text
            else:
                print "No Tweet this time"
            
                

            
