
#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

import sys
def printf(format, *args):
    sys.stdout.write(format % args)

# Helper class to convert a DynamoDB item to JSON.

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

table = dynamodb.Table('avidyneFlightLogs')


response = table.scan( )

entries=[]

def writeFlight(flight):
  
  try: 
    datum = flight['flightID'].split(' ')[0]
    [ mo, da, yr ] = datum.split('/')
    printf ("%s/%s/%s: ", yr, mo, da)

    # datum = '02/02/19'

    if not 'icaoFrom' in flight:
      flight['icaoFrom']='ABCD'
    if not 'icaoTo' in flight:
      flight['icaoTo']='DCBA'
     
    entry={

      "entity_name"                : "Flight",
      "flight_flightDate"          : datum,
      "flight_from"                : flight['icaoFrom'],
      "flight_to"                  : flight['icaoTo'],
      "flight_distance"            : str(flight['Traveled']),
      "flight_actualDepartureTime" : datum+' '+flight['OffBlock'],
      "flight_actualArrivalTime"   : datum+' '+flight['OnBlocks'],

      "flight_totalTime"           : flight['PICTime'],

      "flight_dayLandings"         : "1",
      "flight_dayTakeoffs"         : "1",
      "flight_selectedAircraftType": "SR-20",
      "flight_selectedAircraftID"  : "N808KB",
      "flight_selectedCrewPIC"     : "Erik Meinders"
    }

    if (yr == "19" ):
       entries.append(entry)

    package={
      "metadata": {
        "application"              : "ErixLogTenUpdater",
        "version"                  : "1.0",
        "dateFormat"               : "MM/dd/yy",
        "dateAndTimeFormat"        : "MM/dd/yy%20HH:mm:ss",
        "timesAreZulu"             : "true",
        "shouldApplyAutoFillTimes" : "true"
      },
      "entities": [ entry ]
    }

    line='logtenprox://v2/addEntities?package='+json.dumps(package)

    printf ("<a href='%s'> Form %4s to %4s %s</a><br>\n", line, entry['flight_from'], entry['flight_to'], entry['flight_actualDepartureTime'])

  except Exception as e:
    printf ("Exception discovered %s\n", e)

for i in response[u'Items']:
    writeFlight(i)


package={
  "metadata": {
    "application"              : "ErixLogTenUpdater",
    "version"                  : "1.0",
    "dateFormat"               : "MM/dd/yy",
    "dateAndTimeFormat"        : "MM/dd/yy%20HH:mm:ss",
    "timesAreZulu"             : "true",
    "shouldApplyAutoFillTimes" : "true"
  },
  "entities": entries
}

line='logtenprox://v2/addEntities?package='+json.dumps(package)

printf ("Totaal <a href='%s'>2019</a>\n", line)

sample = {
  "lonEnd": "6.8838",
  "flightID": "4/9/17 09:26:47\r\n",
  "lonStart": "5.5261",
  "AvgSpeed": "100.416255672",
  "Flying": "0:38:36",
  "latStart": "52.4580",
  "Landing": "10:10:42",
  "Traveled": "64.6011244822",
  "icaoTo": "EHTW",
  "gcDist": "50.9485443277",
  "OnBlocks": "10:11:36",
  "TakeOff": "09:32:06",
  "icaoFrom": "EHLE",
  "Ground": "0:05:06",
  "PICTime": "0:43:42",
  "OffBlock": "09:27:54",
  "latEnd": "52.2767"
}
