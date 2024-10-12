import pandas as pd

class YTCalculation:
    def __init__(self, df_merged, df_combined, maturity, points, underlying_amount, pendle_yt_multiplier):
        """
        Initializes the YTCalculation class to compute various metrics like hours to maturity,
        yt/underling, long_yield_apy, weighted points, and the fair value curve.
        
        :param df_merged: The merged DataFrame containing transaction and APY data.
        :param df_combined: The combined DataFrame with OHLCV and other data.
        :param maturity: The asset maturity date in string format (e.g., '2023-01-01 00:00:00').
        :param points: Points earned per hour per underlying asset.
        :param underlying_amount: The amount of underlying assets.
        :param pendle_yt_multiplier: Multiplier for Pendle YT.
        """
        self.df_merged = df_merged
        self.df_combined = df_combined
        self.maturity = pd.to_datetime(maturity, format='%Y-%m-%d %H:%M:%S', utc=True)
        self.points = points
        self.underlying_amount = underlying_amount
        self.pendle_yt_multiplier = pendle_yt_multiplier

    def calculate_hours_to_maturity(self):
        """
        Calculate the hours to maturity for each timestamp in the DataFrame.
        """
        self.df_merged['timestamp'] = pd.to_datetime(self.df_merged['timestamp'], utc=True)
        self.df_merged['hours_to_maturity'] = (self.maturity - self.df_merged['timestamp']).dt.total_seconds() / 3600

    def calculate_yt_and_long_yield(self):
        """
        Calculate yt/underling and long_yield_apy based on APYs and time to maturity.
        """
        self.df_merged['yt/underling'] = (self.df_merged['impliedApy'] + 1) ** (self.df_merged['hours_to_maturity'] / 8760) - 1
        self.df_merged['long_yield_apy'] = (1 + (self.df_merged['underlyingApy'] - self.df_merged['impliedApy']) / self.df_merged['impliedApy']) ** (8760 / self.df_merged['hours_to_maturity']) - 1

    def calculate_price_and_weighted_points(self):
        """
        Calculate the price, weighted points, and the total points per underlying asset.
        """
        price = self.df_merged['yt/underling']
        time_diff_hours = (self.maturity - self.df_merged['timestamp']).dt.total_seconds() / 3600
        self.df_merged['points'] = 1 / price * time_diff_hours * self.points * self.underlying_amount * self.pendle_yt_multiplier

    def generate_hourly_date_range(self):
        """
        Generate a date range in hourly intervals from the first timestamp to maturity.
        
        :return: A Pandas date range from the first timestamp in df_merged to maturity.
        """
        return pd.date_range(start=self.df_merged['timestamp'].iloc[0], end=self.maturity, freq='H')

    def calculate_average_implied_apy(self):
        """
        Calculate the average implied APY weighted by volume.
        
        :return: Weighted average of implied APY.
        """
        return (self.df_merged['impliedApy'] * self.df_merged['valuation_usd'] / self.df_merged['valuation_usd'].sum()).sum()

    def calculate_fair_value_curve(self):
        """
        Calculate the fair value curve based on the average implied APY.
        
        :return: Fair value curve for each hourly interval.
        """
        self.h_range = self.generate_hourly_date_range()
        implied_apy_average = self.calculate_average_implied_apy()
        fair_value_curve = 1 - 1 / (1 + implied_apy_average) ** (((self.maturity - self.h_range).total_seconds() / 3600) / 8760)
        return fair_value_curve

    def calculate_weighted_points_per_underlying(self):
        """
        Calculate weighted points for each row and sum the weighted points per underlying asset.
        
        :return: Total weighted points per underlying asset.
        """
        self.df_merged['weighted_points'] = self.df_merged['points'] * self.df_merged['valuation_usd'] / self.df_merged['valuation_usd'].sum()
        return self.df_merged['weighted_points'].sum()

    def add_fair_value_to_combined(self, fair_value_curve):
        """
        Add fair value curve to the df_combined DataFrame.
        """
        self.df_combined['fair'] = fair_value_curve[:len(self.df_combined)]

    def run_calculations(self):
        """
        Run all calculations in sequence and return the merged and combined DataFrames with calculated values.
        """
        self.calculate_hours_to_maturity()
        self.calculate_yt_and_long_yield()
        self.calculate_price_and_weighted_points()
        fair_value_curve = self.calculate_fair_value_curve()
        weighted_points = self.calculate_weighted_points_per_underlying()
        self.add_fair_value_to_combined(fair_value_curve)
        return self.df_merged, self.df_combined, self.h_range,fair_value_curve, weighted_points
