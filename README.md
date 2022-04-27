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