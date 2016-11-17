#!/usr/local/bin/python
"""Generate reports from a tracery grammar"""
__author__ = "Sean Bechhofer"
__copyright__ = "Copyright 2016, Sean Bechhofer"
__credits__ = ["Sean Bechhofer"]
import json
import argparse

import tracery
from tracery.modifiers import base_english
import sparql

parser = argparse.ArgumentParser(description='Generate Tracery Grammar.')
parser.add_argument('-i', '--input', help='output file', default="grammar.json")
parser.add_argument('-n', '--number', help='output file', type=int, default=4)
parser.add_argument('-p', '--production', default="origin")
parser.add_argument('--html', action="store_true")

args = parser.parse_args()

with open(args.input) as f:
    rules = json.load(f)
    
grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

LIMIT = 140

# Should really do html via templates, but quick'n'dirty FTW!.
if args.html:
    print "<html>"
    print """
    <head>
    <style>
    body {font-family: 'Helvetica Neue', 'Open Sans'; background: #fff;}
    div.box {border: solid black; background: #eee; padding: 10px; margin: 20px}
    p {margin: 0px;font-size: large;}
    .right {text-align: right;}
    .red {color: red;}
    </style>
    </head>
    """
    print "<body>"
    
for i in range(0,args.number):
    stuff = grammar.flatten("#" + args.production + "#")
    style = ""
    if len(stuff) > LIMIT:
        style = " red"

    if args.html:
        print "<div class='box" + style + "'>"
    if args.html:
        print "<p>{}</p>".format(stuff)
    else:
        print "{}".format(stuff)
    print
    if args.html:
        print "<p class='right'>({})</p>".format(len(stuff))
        print "</div>"
    

if args.html:
    print "</body>"
    print "</html>"
    
