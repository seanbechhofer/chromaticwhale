#!/usr/local/bin/python
"""Generate a tracery grammar for fictitious travel reports"""
__author__ = "Sean Bechhofer"
__copyright__ = "Copyright 2016, Sean Bechhofer"
__credits__ = ["Sean Bechhofer"]
import json
import argparse

import tracery
from tracery.modifiers import base_english
import sparql


parser = argparse.ArgumentParser(description='Generate Tracery Grammar.')
parser.add_argument('-o', '--output', help='output file', default="grammar.json")

args = parser.parse_args()

# Get stuff from dbpedio

def dbpedia_things(query):
    things = []
    result = sparql.query('http://dbpedia.org/sparql', query)
    for row in result.fetchall():
        values = sparql.unpack_row(row)
        name = values[1]
        things.append(name)
    return things

# European Rodents
rodent_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Rodents_of_Europe.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
}
"""

# European Rodents
amphibian_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Amphibians_of_Europe.
?thing rdf:type dbo:Amphibian.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
}
"""

# Weather Conditions
weather_query="""
SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Weather_hazards.
?thing rdfs:label ?name.
{?thing rdf:type yago:NaturalPhenomenon111408559.}
      UNION
{?thing rdf:type yago:Danger114541044.}.
FILTER (lang(?name) = 'en')
}
"""

# Northern Rail Stations
station_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE 
{
?thing dbp:manager dbr:Northern_Rail.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
}
"""

# Grab stuff from dbpedia
rodents = dbpedia_things(rodent_query)
amphibians = dbpedia_things(amphibian_query)
#print rodents
weather = []
for w in dbpedia_things(weather_query):
    weather.append(w.lower())
#print weather
stations = []
for s in dbpedia_things(station_query):
    stations.append(s.replace(' railway station',''))

# Tracery Grammar
rules = {
    'origin': ['#issue.capitalize#. #consequence.capitalize#.',
               '#issue.capitalize#. #disruption.capitalize#.',
               '#issue.capitalize#. #disruption.capitalize#.',
               '#consequence.capitalize# due to #issue#.',
               '#disruption.capitalize# due to #issue#.',
               '#disruption.capitalize# due to #issue#.', 
               '#station# closed due to #infestation##animal.s#. Services will run via #station# for the next #duration#.'],
    'issue':  ['reports of #cause.s# #location#',
               '#problem.s# #location# caused by #cause.s#',
               '#modified_animal.a# #sighted# near #station#',
               'high volumes of #animal.s# reported at #station#'],
    'sighted': ['sighted', 'on the tracks', 'reported'],
    'modified_animal': '#animal_modifier##animal#',
    'infestation': ['', 'an infestation of '],
    'animal_modifier': ['', '', '', 'large ', 'aggressive ', 'rare ', 'sleeping ', 'bewildered ',
                        'drunk ', 'distressed ', 'unkempt ', 'weak ', 'curious ', 'migrating '], 
    'disruption': ['#service# #disrupted#'],
    'service': 'the #time# service from #station# to #station#',
    'disrupted': ['will terminate at #station#',
                  'is delayed', 'is cancelled',
                  'is running #duration# late',
                  'will be diverted via #station#'],
    'time': ['#hours#:#minutes#'],
    'hours': map(lambda x:("{:02d}".format(x)), range(0,24)),
    'minutes': map(lambda x:("{:02d}".format(x)), range(0,60)),
    'problem': ['technical issue',
                'staff shortage',
                'signal failure'],
    'location': ['in the #station# area',
                 'between #station# and #station#'],
    'animal': ['#rodent#', '#amphibian#'],
    'cause': ['#rodent#','#amphibian#', '#weather#'],
    'consequence': ['delays of #modifier##duration# #expectation#',
            'disruption #expectation# for the next #duration#',
            'limited catering on #service#',
            '#caution# advised'],
    'caution': ['caution', 'care'],
    'modifier': ['at least ', 'up to ', 'over '],
    'duration': '#number# #unit.s#',
    'number': ['two', 'five', 'ten', 'twenty'],
    'unit': ['minute', 'minute', 'hour'],
    'expectation': ['likely', 'expected', 'predicted'],
    'rodent': rodents,
    'amphibian': amphibians,
    'weather': weather,
    'station': stations
}

# Write the grammar out to json
with open(args.output,'w') as f:
    json.dump(rules,f,indent=4)
    
