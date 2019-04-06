
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

def atoi(s):
	n, notnegative = 0, 1
	if s[0]=="-":
		notnegative = -1
		s = s[1:]
	for i in s:
		n = n*10 + ord(i)-ord("0")
	return notnegative*n

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

empty_package={
  "metadata": {
    "application"              : "ErixLogTenUpdater",
    "version"                  : "1.0",
    "dateFormat"               : "MM/dd/yy",
    "dateAndTimeFormat"        : "MM/dd/yy%20HH:mm:ss",
    "timesAreZulu"             : "true",
    "shouldApplyAutoFillTimes" : "true"
  },
  "entities": []
}
logtenline='logtenprox://v2/addEntities?package='

response = table.scan( )

entries=[]

def writeFlight(flight):
  
  try: 
    datum = flight['flightID'].split(' ')[0]
    [ mo, da, yr ] = datum.split('/')

    # Only consider flights after june 1 2018

    if ( 10000 * atoi(yr) + 100 * atoi(mo) + atoi(da) ) <= 180601:
       return

    if not 'icaoFrom' in flight:
      flight['icaoFrom']='ABCD'
    if not 'icaoTo' in flight:
      flight['icaoTo']='DCBA'
     
    printf ("%s/%02d/%02d: ", yr, int(mo), int(da))

    entry={

      "entity_name"                : "Flight",


      "flight_flightDate"          : datum,
      "flight_key"                 : flight['flightID'],
      "flight_from"                : flight['icaoFrom'],
      "flight_to"                  : flight['icaoTo'],
      "flight_distance"            : str(flight['Traveled']),
      "flight_actualDepartureTime" : datum+' '+flight['OffBlock'],
      "flight_actualArrivalTime"   : datum+' '+flight['OnBlocks'],
      "flight_takeoffTime"         : datum+' '+flight['TakeOff'],
      "flight_landingTime"         : datum+' '+flight['Landing'],

      "flight_totalTime"           : flight['PICTime'],

      # "flight_dayLandings"         : "1",
      # "flight_dayTakeoffs"         : "1",
      "flight_selectedAircraftType": "SR-20",
      "flight_selectedAircraftID"  : "N808KB",
      "flight_selectedCrewPIC"     : "Erik Meinders"
    }

    entries.append(entry)

    package=empty_package
    package['entities'] = [ entry ] 

    line=logtenline+json.dumps(package)

    printf ("<a href='%s'>Form %4s to %4s</a> Key: %s<br>\n",
     line,
     entry['flight_from'],
     entry['flight_to'],
     entry['flight_actualDepartureTime'])

  except Exception as e:
    printf ("Exception discovered %s\n", e)

# main 

for i in response[u'Items']:
    writeFlight(i)

# write sum

package=empty_package
package['entities']=entries

line=logtenline+json.dumps(package)

printf ("<br>Alle vluchten <a href='%s'>na 1 juni 2018</a>\n", line)

#### 

sample = {
  "lonEnd": "6.8838",
  "flightID": "4/9/17 09:26:47",
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
