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
import re

parser = argparse.ArgumentParser(description='Generate Tracery Grammar.')
parser.add_argument('-o', '--output', help='output file', default="whale.json")

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

# Folk Metal Bands
metal_query="""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
  {?thing dbo:genre dbr:Folk_metal.}
  UNION
  {?thing dbo:genre dbr:Doom_metal.}
}
?thing rdf:type dbo:Band.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
}
"""

# European Rodents
market_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Stock_exchanges_in_Europe.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""

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

godzilla_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Godzilla_characters.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
}
"""
# Pests. This is a bit hacky as the list includes some things we don't
# really want, like latin names. Also, tracery's plural modifier
# doesn't handle moths!
pests_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Household_pest_insects.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "tus", "i"))
FILTER (!regex(?name, "pes", "i"))
FILTER (!regex(?name, "mex", "i"))
FILTER (!regex(?name, "ella", "i"))
FILTER (!regex(?name, "dae", "i"))
FILTER (!regex(?name, "genus", "i"))
FILTER (!regex(?name, "entomology", "i"))
FILTER (!regex(?name, "moth", "i"))

}
"""

crime_organisation_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE
{
{
 {?thing rdf:type yago:WikicatDCComicsSupervillainTeams.}
 UNION
 {?thing dct:subject dbc:Fictional_organized_crime_groups.}
}
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name, "\\\\(", "i"))
FILTER (!regex(?name, "list", "i"))
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

# North American Primates
primate_query="""
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
?thing dct:subject dbc:Primates_of_Africa.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name,"\\\\(","i"))
FILTER (!regex(?name, "list", "i"))
}
"""

# Weather Conditions
weather_query="""
SELECT distinct ?thing ?name WHERE
{
 ?thing dct:subject dbc:Weather_hazards.
 ?thing rdfs:label ?name.
 {
  {?thing rdf:type yago:NaturalPhenomenon111408559.}
      UNION
  {?thing rdf:type yago:Danger114541044.}.
 }
FILTER (lang(?name) = 'en')
FILTER (!regex(?name,"\\\\(","i"))
}
"""

# Again, some hand pruning to get rid of chaff.
hazard_query="""
SELECT distinct ?thing ?name WHERE
{
?thing dct:subject dbc:Geological_hazards.
?thing rdfs:label ?name.
FILTER (lang(?name) = 'en')
FILTER (!regex(?name,"list","i"))
FILTER (!regex(?name,"large","i"))
FILTER (!regex(?name,"hazards","i"))
}
"""

# Northern Rail Stations. This one works well.

# All change! Now ?thing dbo:operator dbr:Northern_(train_operating_company).
station_query="""
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbp: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX yago-res: <http://yago-knowledge.org/resource/>

SELECT distinct ?thing ?name WHERE 
{
?thing dbo:operator <http://dbpedia.org/resource/Northern_(train_operating_company)>.
?thing rdfs:label ?name.
?thing rdf:type dbo:Station.
FILTER (lang(?name) = 'en')
}
ORDER BY ?name
"""
# ?thing dbp:manager dbr:Northern_Rail.

# Grab stuff from dbpedia
monster = dbpedia_things(godzilla_query)
rodents = dbpedia_things(rodent_query)
amphibians = dbpedia_things(amphibian_query)
pests = dbpedia_things(pests_query)
primates = dbpedia_things(primate_query)

crime_organisation = []
for c in dbpedia_things(crime_organisation_query):
    crime_organisation.append(re.sub('^The ', '', c))
weather = []
for w in dbpedia_things(weather_query):
    weather.append(w.lower())
hazard = []
for h in dbpedia_things(hazard_query):
    hazard.append(h.lower())
stations = []
for s in dbpedia_things(station_query):
    stations.append(s.replace(' railway station',''))
markets = dbpedia_things(market_query)
metal_band = dbpedia_things(metal_query)

# Tracery Grammar
rules = {
    'origin': ['#issue.capitalize#. #consequence.capitalize#.',
               '#issue.capitalize#. #disruption.capitalize#.',
               '#issue.capitalize#. #disruption.capitalize#.',
               '#consequence.capitalize# due to #issue#.',
               '#disruption.capitalize# due to #issue#.',
               '#disruption.capitalize# due to #issue#.',
               '#disruption.capitalize# due to #market_issue#.',
               '#infestation#'],
    'issue':  ['reports of #cause.s# #location#',
               'reports of #cause.s# #location#',
               '#problem.s# #location# caused by #cause.s#',
               '#problem.s# #location# caused by #cause.s#',
               '#modified_animal.a# #sighted# #station#',
               '#monster# #sighted# #station#',
               '#metal_band# #sighted# #station#',
               '#metal_band# #sighted# #station#',
               '#modified_monster.a# #sighted# #station#',
               '#quantity##animal.s# reported at #station#',
               '#quantity##animal.s# reported at #station#',
#               '#crime#',
               '#quantity##animal.s# expected #location#',
               '#quantity##animal.s# expected #location#'
               ],
    'crime': ['#crime_organisation# #crime_activity# #suspected# #location#'],
    'crime_activity': ['activity', 'operations'],
    'suspected': ['suspected', 'observed'], 
    "market_issue": [
        "early closure of the #market#", 
        "falling values on the #market#", 
        "heavy trading on the #market#", 
        "suspicious trades on the #market#"
        ], 
    'quantity': ['high volumes of ', 'several ', 'numerous ', 'unprecedented levels of ', 'groups of ', '', '', '#number# '],
    'number': ['two', 'three', 'eight', 'a dozen', 'twelve', 'seventeen', 'forty-seven', 'fifty'],
    'infestation': '#station# closed due to #infestation_type##animal_or_pest.s#. #infestation_disruption.capitalize#',
    'infestation_type': ['', 'an infestation of '],
    'infestation_disruption': ['delays expected', 'services will run via #station# for the next #duration#.', 'replacement bus service from #station#.'],
    'sighted': ['sighted near', 'on the tracks near', 'reported near', 'approaching'],
    'modified_animal': '#animal_modifier##animal#',
    'modified_monster': '#animal_modifier##monster#',
    'animal_modifier': ['', '', '', 'large ', 'aggressive ', 'rare ', 'sleeping ', 'bewildered ',
                        'drunk ', 'distressed ', 'unkempt ', 'weak ', 'curious ', 'migrating '], 
    'disruption': ['#service# #disrupted#'],
#    'service': 'the #time# service from #station# to #station#',
    'service': 'the #time# from #station# to #station#',
    'disrupted': ['will terminate at #station#',
                  'is delayed', 'is cancelled',
                  'is running #duration# late',
                  'will be diverted via #station#',
                  'will #maybe_call# call at #station#'],
    'maybe_call': ['no longer', 'additionally'],
    'time': ['#hours#:#minutes#'],
    'hours': map(lambda x:("{:02d}".format(x)), range(0,24)),
    'minutes': map(lambda x:("{:02d}".format(x)), range(0,60)),
    'problem': ['technical issue',
                'staff shortage',
                'signal failure'],
    'location': ['in the #station# area',
                 'between #station# and #station#',
                 'outside #station#',
                 'on the #station# line'],
    'animal_or_pest': ['#animal#','#pest#'],
    'animal': ['#rodent#', '#amphibian#', '#primate#'],
    'cause': ['#rodent#','#amphibian#', '#primate#'], # Removed #weather# and #hazard#
    'consequence': ['delays of #modifier##duration# #expectation#',
            'disruption #expectation# for the next #duration#',
            'limited catering on #service#',
            '#caution# advised',
            'replacement bus service between #station# and #station#',
            'tickets will be accepted on services via #station#'],
    'caution': ['caution', 'care'],
    'modifier': ['at least ', 'up to ', 'over '],
    'duration': '#number# #unit.s#',
    'number': ['two', 'five', 'ten', 'twenty'],
    'unit': ['minute', 'minute', 'hour'],
    'expectation': ['likely', 'expected', 'predicted'],
    'pest': pests,
    'rodent': rodents,
    'amphibian': amphibians,
    'weather': weather,
    'hazard': hazard,
    'station': stations,
    'market': markets,
    'monster': monster,
    'primate': primates,
    'crime_organisation': crime_organisation,
    'metal_band': metal_band
}

# Write the grammar out to json
with open(args.output,'w') as f:
    json.dump(rules,f,indent=4)
    
