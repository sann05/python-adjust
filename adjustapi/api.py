import logging
from abc import ABC
from datetime import date
from io import StringIO

import pandas as pd
import requests

from adjustapi.model import parse_apps, parse_kpi


class _Api(ABC):
    """
    Class that implements HTTP requests
    """

    def _get(self, url, params=None, **kwargs):
        logging.info(f"Request url: {url}")
        logging.info(f"Request params: {params}")
        headers = {**self._default_header, **kwargs}
        logging.info(f"Request header: {headers}")
        logging.info(f"Request extras: {kwargs}")
        r = requests.get(url,
                         params=params,
                         headers=headers)
        r.raise_for_status()
        return r

    def _post(self, url, **kwargs):
        logging.info(f"Request url: {url}")
        logging.info(f"Request params: {kwargs.get('params')}")
        kwargs['headers'] = {**self._default_header,
                             **kwargs.get('headers', {})}
        logging.info(f"Request header: {kwargs['headers']}")
        logging.info(f"Request extras: {kwargs}")
        r = requests.post(url, **kwargs)
        r.raise_for_status()
        return r


class AdjustApi(_Api):
    """
    Object to query Adjust API
    """

    def __init__(self, user_token):
        self.user_token = user_token
        self._base_url = 'https://api.adjust.com'
        self._raw_export_settings_endpoint = "{}/dashboard/api/apps/".format(
            self._base_url) + "{}/settings/raw_export_settings"

        self._default_header = {
            'Authorization': f'Token token={self.user_token}'
        }

    def kpi_service(self,
                    trackers: list = None,
                    start_date: date = None,
                    end_date: date = None,
                    app_tokens: list = None,
                    kpis: list = None,
                    groups: list = None,
                    **kwargs):
        """
        Returns: instance of KpiAdjustApi service
        """
        return KpiAdjustApi(self,
                            trackers=trackers,
                            start_date=start_date,
                            end_date=end_date,
                            app_tokens=app_tokens,
                            kpis=kpis,
                            groups=groups,
                            **kwargs)

    def list_apps(self):
        """
        Returns: list of all applications found in your Adjust account
        """
        url = self._base_url + '/dashboard/api/apps'
        r = self._get(url)
        return parse_apps(r)

    def get_app(self, app_token):
        url = self._base_url + '/dashboard/api/apps/' + app_token
        r = self._get(url)
        return r.json()

    def get_raw_export_settings(self, app_token: str):
        """
        Retrieve raw export settings
        :param app_token:
        :return: dict object settings
        """
        url = self._raw_export_settings_endpoint.format(
            app_token
        )
        r = self._get(url)
        return r.json()

    def update_raw_export_settings(self, app_token: str, settings: dict):
        """
        Update raw export settings
        :param app_token:
        :param settings: dictionary retrieved from get_raw_export_settings
        method
        :return dict object
        """
        url = self._raw_export_settings_endpoint.format(
            app_token
        )
        if "raw_export_settings" not in settings:
            raise ValueError(
                "Settings should be retrieved from \"raw_export_settings\" "
                "function and contains \"raw_export_settings\"")
        settings["raw_export_settings"].pop('hash')
        cols = settings["raw_export_settings"].pop('columns')
        settings["raw_export_settings"]['csv_definition'] = ",".join(
            [x['value'] for x in cols])
        r = self._post(url, json=settings, headers={
            'content-type': "application/json",
        })
        return r.json()

    def list_callbacks(self, app_token: str):
        """
        Retrieve list of available callbacks
        :param app_token:
        :return: dict object settings
        """
        url = "{}/dashboard/api/apps/{}/callbacks".format(
            self._base_url,
            app_token
        )
        r = self._get(url)
        return r.json()


class KpiAdjustApi(_Api):
    """
    Documentation of KPI service:
        http://help.adjust.com/resources/kpi-service
    Example:
        https://api.adjust.com/kpis/v1/<app-token>/trackers/<tracker-token>?start_date=2020-05-01&end_date=2020-05-31&kpis=sessions,installs&countries=de,gb,us
        Header = Authorization:Token token=<ADJUST_TOKEN>
    """

    def __init__(self,
                 api: AdjustApi,
                 trackers: list = None,
                 start_date: date = None,
                 end_date: date = None,
                 app_tokens: list = None,
                 kpis: list = None,
                 groups: list = None,
                 **kwargs):
        for var in [kpis, groups, app_tokens]:
            if var is not None and not isinstance(var, list):
                raise TypeError("{} must be a list".format(var))
        for var in [start_date, end_date]:
            if var is not None and not isinstance(var, date):
                raise TypeError("{} must be a date".format(var))

        self.api = api
        self.app_tokens = app_tokens or []
        self.start_date = start_date
        self.end_date = end_date
        self.kpis = kpis or []
        self.group = groups or []
        self._default_header = dict(api._default_header)
        self._base_url = '{}/kpis/v1/{}'.format(self.api._base_url,
                                                ','.join(self.app_tokens))
        if trackers is not None:
            self._base_url = '{}/trackers/{}'.format(self._base_url.rstrip('/'),
                                                     ','.join(trackers))

        self.extras = kwargs

    def _get_params(self):

        params = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "kpis": ",".join(self.kpis),
            "grouping": ",".join(self.group)
        }
        if self.extras is not None:
            params.update(self.extras)
        return params

    def fetch_kpi(self, as_df=False):
        return self._fetch_kpis(self._base_url, as_df)

    def fetch_events(self, as_df=False):
        url = self._base_url + "/events"
        return self._fetch_kpis(url, as_df)

    def fetch_cohorts(self, as_df=False):
        url = self._base_url + "/cohorts"
        return self._fetch_kpis(url, as_df)

    def _fetch_kpis(self, url, as_df=False):
        if as_df:
            url += '.csv'
            response = self._get(url, self._get_params())
            response.raise_for_status()
            return pd.read_csv(StringIO(''.join(
                [i for i in response.text if ord(i) < 128]
            )))
        else:
            response = self._get(url, self._get_params())
            return parse_kpi(response)
