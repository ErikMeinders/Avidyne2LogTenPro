# cirrus

Application for processing avidyne logfiles for cirrus aircraft
resulting in a flights.html file
that contains click-able lines of LogTenProX API calls

This allows for direct import into LogTenPro X from logs taken from your Avidyne MFD

## Prerequisites

This application assumes you have the AWS infrastructure in place to process the logfiles
It connects to a dynamoDB database containing your flights

## Usage

```
python ./generateLogTenX.sh
```

This will create create

