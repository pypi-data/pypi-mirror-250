import logging

import numpy as np

log = logging.getLogger(__name__)


def validate(df):
    # Check for invalid values (nans, infs)
    count_cells = df.size
    count_invalid_cells = 0
    for col in df.columns:
        # Look for infs/nans as cell values
        count_invalid_cells += df[col].isin([np.inf, -np.inf, np.nan]).sum()
        # Look for infs/nans inside ndarrays
        count_invalid_cells += df[col].apply(lambda a: isinstance(a, np.ndarray) and (not np.isfinite(a).any())).sum()

    if count_invalid_cells > 0:
        log.error(
            f"{count_invalid_cells} ({count_invalid_cells / count_cells * 100:.0f}%) not-finite values (nans/infs)"
        )

    if len(set(df.columns)) != len(df.columns):
        log.error("Duplicate column names")

    if len(df.columns) == 0:
        log.error("No columns")

    if len(df) == 0:
        log.error("No rows")
