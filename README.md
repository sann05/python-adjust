## Welcome to the python-adjust
This is an unofficial Python wrapper for the Adjust.com REST API.
I am in no way affiliated with Adjust.com, use at your own risk.


### Regards
This project was inspired by [adjusty](https://github.com/techieashish/adjusty)


### Documentation
Please find official documentation by:
https://help.adjust.com/en/article/kpi-service


### QuickStart

Your access to the KPI Service is tied to your Adjust user account. Each user account has an associated user token, to allow you to individually control access to your KPIs.

You can find your own user token in the dashboard, under **Account Settings > Your Data > User Details**. This is the user token we’ll be referring to for your authentication below.
```
pip install python-adjust
```

Let's retrieve list of applications accessible to you
```python

from adjustapi.api import AdjustApi

api = AdjustApi('USER_TOKEN')

apps = api.list_apps()

print(apps[0].name, apps[0].token, apps[0].id)
# Prints something like: "MyTestApp ft5popkfebns com.mytest.app"
```

This is how KPI API works
```python
kpis_api = api.kpi_service(trackers=trackers,
                           start_date=start_date,
                           end_date=end_date,
                           countries=countries,
                           app_tokens=app_tokens,
                           kpis=kpis)
print(str(kpis_api.fetch_kpi()))
# prints: KpiResult(result_parameters=ResultParameters(kpis=['revenue'], start_date=datetime.date(2020, 4, 4), end_date=datetime.date(2020, 5, 4), sandbox=False, countries=['us'], events=None, trackers=[TrackerResultParameters(token='tsrdag', name='Facebook Installs::Expired Attributions', currency=None, has_subtrackers=False)], grouping=['trackers'], period=None, attribution_type='click', utc_offset='00:00', cohort_period_filter=None, day_def=None, attribution_source='dynamic'), result_set={'token': 'thomki', 'name': 'Facebook Installs', 'currency': 'USD', 'trackers': [{'token': 'tsodkg', 'kpi_values': [3627.54]}]})

print(str(kpis_api.fetch_events()))
# prints: KpiResult(result_parameters=ResultParameters(kpis=['revenue'], start_date=datetime.date(2020, 4, 4), end_date=datetime.date(2020, 5, 4), sandbox=False, countries=['us'], events=[EventParameter(name='com.test.subscription.name', token='s6p2ub'), EventParameter(name='event_name', token='eakvze'), EventParameter(name='event.name.2', token='5a6u7u'), EventParameter(name='event_name_3', token='e34v0e')], trackers=[TrackerResultParameters(token='6tcrta', name='Facebook Installs::Expired Attributions', currency=None, has_subtrackers=False)], grouping=['trackers', 'event_types'], period=None, attribution_type='click', utc_offset='00:00', cohort_period_filter=None, day_def=None, attribution_source='dynamic'), result_set={'token': 'thamsi', 'name': 'Facebook Installs', 'currency': 'USD', 'trackers': [{'token': 'tsrdta', 'events': [{'token': 'e6e2v1', 'kpi_values': [1149.77]}, {'token': 'ea3vpe', 'kpi_values': [95.88]}, {'token': 'e34v0e', 'kpi_values': [17.99]}, {'token': 'eovy8e', 'kpi_values': [147.63]}}]}]})

print(str(kpis_api.fetch_cohorts()))
# KpiResult(result_parameters=ResultParameters(kpis=['revenue'], start_date=datetime.date(2020, 4, 4), end_date=datetime.date(2020, 5, 4), sandbox=False, countries=['us'], events=None, trackers=[TrackerResultParameters(token='csodbh', name='Facebook Installs::Expired Attributions', currency=None, has_subtrackers=False)], grouping=['trackers', 'periods'], period='day', attribution_type='click', utc_offset='00:00', cohort_period_filter=None, day_def='24h', attribution_source='dynamic'), result_set={'token': 'chamsh', 'name': 'Facebook Installs', 'currency': 'USD', 'trackers': [{'token': 'cscoth', 'periods': [{'period': '0', 'kpi_values': [109.89]}}]}]})
```

But most of the time you need these data as table, so you can retrieve it as pandas Dataframe
```python
kpis_api = api.kpi_service(trackers=trackers,
                           start_date=start_date,
                           end_date=end_date,
                           countries=countries,
                           app_tokens=app_tokens,
                           kpis=kpis)
print(str(kpis_api.fetch_kpi(as_df=True)))

# '  tracker_token                             tracker_name  revenue
# 0        tsrdag  Facebook Installs::Expired Attributions  3627.54'
```

For more check out [the documentation](https://help.adjust.com/en/article/kpi-service).

If you have any questions feel free to add [issues]() or write to me. 

TODO: Add link to Airflow hook and operator for AdjustApi
