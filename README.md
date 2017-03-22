# getresponse-python

![Build Status](https://app.codeship.com/projects/4b47f1f0-ed08-0134-977a-7ab4e0ed4895/status?branch=master)
[![Coverage](https://codecov.io/github/pavelkalin/getresponse-python/coverage.svg?branch=master)](https://codecov.io/github/pavelkalin/getresponse-python)

Python wrapper for GetResponse API 3


## Introduction


This library provides a pure Python interface for the [GetResponse API 3](http://apidocs.getresponse.com/v3). 
It works with Python version 3. <br />
[GetResponse](http://getresponse.com) is a leading Email Marketing platform that is used by thousands of users arount the globe. <br />
_It is_ 
>All-in-one Online Marketing Platform to Grow Your Business


## Installing

```commandline
git@github.com:pavelkalin/getresponse-python.git
cd getresponse-python
pip install -Ur requirements/production.txt
```
For testing purposes install staging.txt instead of production:

```commandline
pip install -Ur requirements/staging.txt
```

Tests can be run via nose like this without coverage:

```commandline
nosetest
```

Tests can be run via nose like this with coverage:

```commandline
nosetest --with-coverage
```

## Usage

Obtain API_KEY, API_ENDPOINT and X_DOMAIN if GetResponse 360 is used. <br />
For GetResponse it's enough to have just API_KEY and API_ENDPOINT <br />

```python
from getresponse.getresponsev3 import Api

API_ENDPOINT = ''
API_KEY = ''
X_DOMAIN = ''

getresponse = Api(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

#to get list of all campagins within account
campaigns = getresponse.get_campaigns()
print(campaigns)

```

## Description

This API wrapper should mimic the original [documentation](http://apidocs.getresponse.com/v3/resources) <br />
However original documentaion is still evolving (new API methods are added) and this wrapper is still being builded, so feel free to fork this repo and change/update/add it however you like.  

At this stage please use it AS IS and consult with documentation [here](http://apidocs.getresponse.com/v3/resources)

## Todo

- [ ] readthedocs
- [ ] installing via pip 
- [ ] full mapping for original API calls
- [ ] more examples
- [ ] live cases

### Project tree

```commandline
|── LICENSE
├── README.md
├── examples
│   └── usage.py
├── getresponse
│   └── getresponsev3.py
├── requirements
│   ├── base.txt
│   ├── local.txt
│   ├── production.txt
│   └── staging.txt
├── testdata
│   ├── get_campaign_id.json
│   └── get_campaigns.json
│   └── post_campaign.json
│   └── ...
└── tests
    └── tests.py

```

### Author

Pavel Kalinichenko <br /> [pavel.kalinichenko@getresponse.ru](mailto:pavel.kalinichenko@getresponse.ru) <br />
 [pavel.kalinichenko@gmail.com](mailto:pavel.kalinichenko@gmail.com) 
