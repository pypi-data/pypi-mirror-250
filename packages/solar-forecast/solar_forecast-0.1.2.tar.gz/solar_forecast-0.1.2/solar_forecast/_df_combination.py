from dataclasses import dataclass
import pandas as pd


@dataclass
class DFCombination:
    def __merge_dataframes__(
        self,
        weather_df: pd.DataFrame,
        daily_snow_on_ground_df: pd.DataFrame,
        solar_position_df: pd.DataFrame,
        solar_energy_production_final_df: pd.DataFrame,
    ) -> pd.DataFrame:
        merge_df = pd.merge(weather_df, daily_snow_on_ground_df, on=("day", "interval"))
        merge_df = pd.merge(solar_position_df, merge_df, on=("day", "interval"))
        return pd.merge(
            solar_energy_production_final_df, merge_df, on=("day", "interval")
        )

    def __cast_date_format__(self, merge_df: pd.DataFrame) -> pd.DataFrame:
        merge_df["day"] = pd.to_datetime(merge_df["day"], format="%Y-%m-%d")
        return merge_df

    def __binary_representation_per_component__(
        self, merge_df: pd.DataFrame
    ) -> pd.DataFrame:
        merge_df["day_binary"] = merge_df["day"].dt.day.apply(
            lambda x: bin(x)[2:].zfill(5)
        )
        merge_df["month_binary"] = merge_df["day"].dt.month.apply(
            lambda x: bin(x)[2:].zfill(4)
        )
        merge_df["year_binary"] = merge_df["day"].dt.year.apply(
            lambda x: bin(x)[2:].zfill(14)
        )
        return merge_df

    def transform(
        self,
        weather_df: pd.DataFrame,
        daily_snow_on_ground_df: pd.DataFrame,
        solar_position_df: pd.DataFrame,
        solar_energy_production_final_df: pd.DataFrame,
    ) -> pd.DataFrame:
        merge_df: pd.DataFrame = self.__merge_dataframes__(
            weather_df=weather_df,
            daily_snow_on_ground_df=daily_snow_on_ground_df,
            solar_position_df=solar_position_df,
            solar_energy_production_final_df=solar_energy_production_final_df,
        )
        merge_df: pd.DataFrame = self.__cast_date_format__(
            merge_df=merge_df,
        )
        return self.__binary_representation_per_component__(merge_df=merge_df)
