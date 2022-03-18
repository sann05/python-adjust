import logging
from datetime import date
from typing import Optional, List, Any

from marshmallow_dataclass import dataclass

VALUE_FIELD = 'kpi_values'


@dataclass
class Currency:
    name: str
    symbol: str
    iso_code: str


@dataclass
class Permissions:
    generate_report: Optional[bool]
    read_statistics: Optional[bool]
    create_tracker: Optional[bool]
    update_settings: Optional[bool]
    update_custom_twitter_permissions: Optional[bool]


@dataclass
class EventParameter:
    name: str
    token: str


@dataclass
class TrackerResultParameters:
    token: Optional[str]
    name: Optional[str]
    currency: Optional[str]
    has_subtrackers: bool


@dataclass
class ResultParameters:
    kpis: List[str]
    start_date: date
    end_date: date
    sandbox: bool
    countries: Optional[List[str]]
    events: Optional[List[EventParameter]]
    trackers: Optional[List[TrackerResultParameters]]
    grouping: List[str]
    period: Optional[str]
    attribution_type: str
    utc_offset: str
    cohort_period_filter: Optional[Any]
    day_def: Optional[str]
    attribution_source: str


@dataclass
class KpiResult:
    result_parameters: ResultParameters
    result_set: dict


@dataclass
class App:
    id: int
    name: str
    token: Optional[str]
    start_date: date
    default_store_app_id: Optional[str]
    integration_dates: Optional[dict]
    default_attribution_platform: str
    app_token: str
    platforms: dict
    permissions: Permissions
    currency: Currency
    is_ctv: Optional[bool]


@dataclass
class AppsResponse:
    apps: List[App]
    urls: Optional[dict]
    page: Optional[dict]

def parse_apps(resp):
    apps = AppsResponse.Schema().load(resp.json()).apps
    if len(apps) > 0:
        logging.info(f'Found {len(apps)} applications in your account')
        return apps
    else:
        logging.info(f'Didn\'t find applications in your account')
        return []


def get_grouping(result_set):
    grouping = []

    def iterate_for_grouping(obj):
        for key in obj:
            if isinstance(obj[key], list):
                grouping.append(key)
                if VALUE_FIELD in obj[key][0]:
                    return grouping
                else:
                    iterate_for_grouping(obj[key][0])

    iterate_for_grouping(result_set)
    return grouping


def get_meta(result_set):
    meta = []

    def iterate_for_meta(obj, current_path=None):
        current_path = current_path or []
        for key in obj.keys():
            if isinstance(obj[key], list):
                if VALUE_FIELD not in obj[key][0].keys():
                    current_path.append(key)
                    iterate_for_meta(obj[key][0], current_path)

            else:
                meta.append(current_path + [key])

    iterate_for_meta(result_set)
    return meta


def parse_kpi(resp):
    resp.raise_for_status()
    kpis = KpiResult.Schema().load(resp.json())
    return kpis
