***REMOVED*** Lambda function using Yelp API

***REMOVED******REMOVED******REMOVED*** Requirements

- Python 3.6
- AWS cli
- Serverless Framework

***REMOVED******REMOVED******REMOVED*** Setup

Create virtualenv and activate

```sh
$ virtualenv -p python3 env
$ source env/bin/activate
```

Install packages

```sh
$ pip install -r requirements
```

***REMOVED******REMOVED******REMOVED*** Run

```sh
$ sls invoke local -f main --data '{"search_term": "kfc", "latitude": "19.610760", "longitude": "-99.017310"}'
```

You can use an optional parameter `radius`

```sh
$ sls invoke local -f main --data '{"search_term": "kfc", "latitude": "19.610760", "longitude": "-99.017310", "radius": "2000"}'
```
