# Lambda function using Yelp API

### Requirements

- Python 3.6
- AWS cli
- Serverless Framework

### Setup

Create virtualenv and activate

```sh
$ virtualenv -p python3 env
$ source env/bin/activate
```

Install packages

```sh
$ pip install -r requirements.txt
```

### Run

```sh
$ sls invoke local -f main --data '{"search_term": "kfc", "latitude": "19.610760", "longitude": "-99.017310"}'
```

You can use an optional parameter `radius`

```sh
$ sls invoke local -f main --data '{"search_term": "kfc", "latitude": "19.610760", "longitude": "-99.017310", "radius": "2000"}'
```
