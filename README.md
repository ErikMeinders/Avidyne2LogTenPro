# Avidyne2LogTenPro

Application for processing avidyne logfiles for cirrus aircraft
resulting in a flights.html file
that contains click-able lines of LogTenProX API calls

This allows for direct import into LogTen Pro from logs taken from your Avidyne MFD

## Prerequisites

This application assumes you have the AWS infrastructure in place to process the logfiles
It connects to a dynamoDB database containing your flights

## Usage

```
python ./bin/generateLogTenX.sh > flights.html
```

This will create create an html file with links that upload your flights in LogTen Pro by means of the LogTen API:

http://help.coradine.com/kb/customizing-logten/logten-pro-api-for-directly-importing-data


