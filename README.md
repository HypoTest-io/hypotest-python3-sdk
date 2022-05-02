# HypoTest Python3 SDK

[![PyPI version](https://badge.fury.io/py/optimizely-sdk.svg)](https://pypi.org/project/hypotest-python3-sdk)
[![Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

This repository houses the official Python3 SDK for use with HypoTest Hypergrowth Experimentation Platform

## Getting Started

### Installing the SDK

The SDK is available through [PyPi](https://pypi.python.org/pypi?hypotest-python3-sdk&:action=display).

To install:

    pip install hypotest-python3-sdk

## Quick Usage

```python
import hypotest

# you can configure the SDK's token by setting the environment variable "HT_TOKEN"
# or by code:
hypotest.config(token='JKV1QiLC29tIiwiZXhwIjox')

# reporting an event, just input the event_name and user or visitor associated with the event
hypotest.kpi_event(event_name='area/user_clicked_on_XXX', user_id='u123')

# add a calibration experiment, it's that easy:)
hypotest.experiment(experiment_name='area/feature/experiment_name', user_id='u123')


# add your first running experiment with 2 variants
if hypotest.experiment(experiment_name='area/feature/experiment_name', user_id='u123').is_control:
    # your current code
    pass
else:
    # the new code
    pass

# link between visitor and user for experiment that start before the user login and end after,
# so we can tell the full entity story, from visitor in the landing page until a user using the core product
hypotest.match_user_visitor(user_id='u123', visitor_id='123')
```

## SDK overview and principles
the SDK has a 2 way communication with Hypo's servers:
* the sdk pulls every "pull_interval" seconds experiments settings
* the sdk reports events back to Hypo's servers  

the SDK was design with safety in mind:
* the experiment function will return "control" for every error!, such as:  
Hypo's servers are down  
wrong parameters were used  
experiment or event don't exist
* the experiment function calculate variant locally, so no need to be afraid of delaying response time
* the SDK sends all events in a background thread

## Functions description and examples:

### config
```python
def config(token: str = None, pull_interval: int = None, pull_jitter: int = None,
           log_level: str = None, flush_events: bool = None, connect_to_server: bool = None)
```
you can configure the sdK in 2 ways:  
1. setting environment variables:  
   HT_TOKEN | HT_PULL_INTERVAL | HT_PULL_JITTER | HT_LOG_LEVEL | HT_FLUSH_EVENTS | HT_CONNECT_TO_SERVER
2. by calling this function with the below parameters  
[all are optional]
* **token**: the access token given by HypoTest for the SDK to be able to communicate with Hypo's servers 
* **pull_interval**: a background thread will pull the latest settings from the server each "poll_interval" seconds  
* **pull_jitter**: jitter number of seconds between each pull  
* **log_level**: the SDK log to stdout, possible options 'CRITICAL' | 'FATAL' | 'ERROR' | 'WARN' | 'WARNING' | 'INFO' | 'DEBUG'| 'NOTSET'
* **flush_events**: True|False if the SDK flushes the remaining events in the queue before the process ends  
* **connect_to_server**:  if False, the SDK doesn't connect to Hypo's servers. it uses dummy configuration and doesn't send events   

example:
```python
def config(token='kfds9werjkvjd', pull_interval=5, pull_jitter=1,
           log_level='DEBUG', flush_events=False, connect_to_server=False)
```

### experiment
```python
def experiment(experiment_name: str, user_id: str = None, visitor_id: str = None,
               tags: Dict[str, Union[str, int, float, bool, None]] = None, override: str = None, report_event=True)
```
this function is to warp your current and new code as an experiment,  
the function returns the chosen variant, and report the event back to Hypo's servers  
the function calculate for each user/visitor per test a variant locally,  
the function is deterministic, each user/visitor combined with an experiment will allways get the same variant
* **experiment_name**: the experiment key name as created in the platform   
* **user_id** | **visitor_id**: user_id or visitor_id string associated with the experiment,  
if the experiment starts before the user login/signup, use visitor_id (potential_id/anonymous_id),  
else use user_id

**optional**
* **tags**: a key value dictionary for "tagging" the user/visitor such as country, is_free, user_age, device_type, os, etc    
* **override**: override the variant chosen, a string with one of the variants in the experiment  
* **report_event**: if False, the function doesn't report an experiment exposure event to the servers

examples:
```python 
if experiment(experiment_name='signup/alternative-landingpage/difference-copywriting', visitor_id="v123",
               tags={"country": "usa", "is_free": False, "user_age": 4, "device_type": mobile},
               override="b", report_event=False).is_control:
    # your current code here
else:
    # the new code here
```
```python
# only for calibration experiment
experiment(experiment_name='signup/alternative-landingpage/difference-copywriting', visitor_id="v123",
               tags={"country": "usa", "is_free": False, "user_age": 4, "device_type": mobile},
               override="b", report_event=False)
```

### kpi_event
```python
def kpi_event(event_name: str, user_id=None, visitor_id=None, value=1.0,
              tags: Dict[str, Union[str, int, float, bool, None]] = None)
```
to report a kpi event back to Hypo's servers
* **event_name**: the kpi event name key name as created in the platform  
* **user_id** | **visitor_id**: user_id or visitor_id string associated with the event,  
if the event occurs before the user login/signup, use visitor_id (potential_id/anonymous_id),  
else use user_id   

**optional**  
* **value**: the value of the event, default to 1.0, used for events sush as reporting selected pricing package, etc  
* **tags**:  a key value dictionary for "tagging" the event such as chosen plan, login method, etc  

example:
```python
kpi_event(event_name="pricing/pricing-page/new-option", user_id="u456", value=39.9)
```

### match_user_visitor
```python
def match_user_visitor(user_id: str, visitor_id: str, context: str = None,
                       tags: Dict[str, Union[str, int, float, bool, None]] = None)
```
the purpose of this function is to be able to connect users and visitors.
* **user_id**: user_id string  
* **visitor_id**: user_id string  

**optional**  
* **context**: placeholder  
* **tags**:   a key value dictionary for "tagging" the event  

example:
```python
match_user_visitor(user_id="u456", visitor_id="v123", context="signup")
```