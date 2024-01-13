import pandas as pd


def std_norm(v, sd=None, m=None):
    v = pd.to_numeric(v)
    m = v.mean() if m is None else m
    sd = v.std() if sd is None else sd

    return (v - m) / sd


def extract_sample(df, sample_size, date_col="date", end_date=None):
    if date_col not in df.columns:
        df[date_col] = df.index
    end_date = df[date_col].max() if end_date is None else end_date
    # Filter dataframe based on sample size
    # convert sample size to timedelta in days
    sample_size_in_days = {"1W": 7, "1M": 30, "3M": 90, "6M": 180, "1Y": 365}
    start_date = (
        df[date_col].min()
        if sample_size == "MAX"
        else end_date - pd.Timedelta(sample_size_in_days[sample_size], unit="d")
    )

    return df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]


def split_sample_in_two(
    df, base_sample_period, compare_sample_period, include_compare_sample_in_base
):
    """
    split sample into 2 sample last compare_sample_period and base_sample_period.
    If include_compare_sample_in_base is True, then include compare_sample_period in base_sample_period as well otherwise exclude it
    return 2 samples: base_sample_period, compare_sample_period
    """
    base_sample_end_date = (
        df.index.max() - pd.Timedelta(compare_sample_period)
        if include_compare_sample_in_base
        else df.index.max()
    )
    base_sample = extract_sample(df, base_sample_period, end_date=base_sample_end_date)
    compare_sample = extract_sample(df, compare_sample_period)
    return [base_sample, compare_sample]


def split_sample_into_n_samples(df, size_of_each_sample):
    """split sample into n samples of size size_of_each_sample"""
    n_samples = len(df) // size_of_each_sample
    samples = []
    for i in range(n_samples):
        start_index = i * size_of_each_sample
        end_index = start_index + size_of_each_sample
        samples.append(df.iloc[start_index:end_index])
    return samples


def split_data_into_samples_by_break(df, gap_days_gt=10):
    """
    Split the data into samples by looking at the gaps in the data.
    """
    samples = []
    start_index = 0
    for i in range(1, len(df)):
        if (df.index[i] - df.index[i - 1]).days > gap_days_gt:
            samples.append(df.iloc[start_index:i])
            start_index = i
    samples.append(df.iloc[start_index:])
    return samples
