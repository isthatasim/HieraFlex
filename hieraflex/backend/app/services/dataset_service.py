from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from data.loaders.deddiag_adapter import DEDDIAGAdapter, summarize_appliance_stats
from data.loaders.local_adapter import LocalAdapter
from data.preprocess.align import align_timeseries
from data.preprocess.clean import clean_trace
from data.preprocess.feature_builder import build_features
from data.preprocess.price_builder import build_price_series


@dataclass
class DatasetBundle:
    trace: pd.DataFrame
    features: pd.DataFrame
    prices: pd.DataFrame
    appliance_meta: pd.DataFrame


class DatasetService:
    def __init__(self) -> None:
        self.deddiag = DEDDIAGAdapter()
        self.local = LocalAdapter()

    def load_bundle(self, scenario_id: str = "demo_week") -> DatasetBundle:
        local = self.local.load_scenario(scenario_id)
        if local is not None and not local.empty:
            trace = clean_trace(local)
        else:
            trace = clean_trace(align_timeseries(self.deddiag.load()))
        features = build_features(trace)
        prices = build_price_series(sorted(trace["timestamp"].unique().tolist()))
        appliance_meta = summarize_appliance_stats(trace)
        return DatasetBundle(trace=trace, features=features, prices=prices, appliance_meta=appliance_meta)


dataset_service = DatasetService()
