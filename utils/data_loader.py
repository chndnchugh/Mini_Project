import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from typing import Dict

class SampleDataLoader:
    """Generate sample economic data for testing"""
    
    @staticmethod
    def generate_gdp_data(periods: int = 12) -> pd.DataFrame:
        """Generate sample GDP growth data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='Q')
        # India's GDP typically ranges 5-8%
        base = 6.5
        values = base + np.random.normal(0, 0.8, periods)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_inflation_data(periods: int = 24) -> pd.DataFrame:
        """Generate sample CPI inflation data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        # India's inflation typically ranges 4-7%
        base = 5.5
        values = base + np.random.normal(0, 1.0, periods)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_wpi_data(periods: int = 24) -> pd.DataFrame:
        """Generate sample WPI inflation data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        base = 4.5
        values = base + np.random.normal(0, 1.2, periods)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_repo_rate_data(periods: int = 24) -> pd.DataFrame:
        """Generate sample repo rate data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        # Repo rate changes slowly
        base = 6.5
        values = np.full(periods, base)
        # Add some step changes
        values[periods//3:] += 0.25
        values[2*periods//3:] += 0.25
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_usd_inr_data(periods: int = 90) -> pd.DataFrame:
        """Generate sample USD-INR exchange rate data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='D')
        base = 83.0
        # Random walk
        changes = np.random.normal(0, 0.2, periods)
        values = base + np.cumsum(changes)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_crude_oil_data(periods: int = 90) -> pd.DataFrame:
        """Generate sample crude oil price data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='D')
        base = 85.0
        changes = np.random.normal(0, 2.0, periods)
        values = base + np.cumsum(changes)
        values = np.clip(values, 60, 110)  # Keep in reasonable range
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_iip_data(periods: int = 12) -> pd.DataFrame:
        """Generate sample Industrial Production Index data"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        base = 4.5
        values = base + np.random.normal(0, 1.5, periods)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def generate_fiscal_deficit_data(periods: int = 5) -> pd.DataFrame:
        """Generate sample fiscal deficit data (yearly)"""
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='Y')
        # Fiscal deficit as % of GDP
        base = 6.4
        values = base + np.random.normal(0, 0.3, periods)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @staticmethod
    def load_all_indicators() -> Dict[str, pd.DataFrame]:
        """Load all sample economic indicators"""
        return {
            "gdp_growth": SampleDataLoader.generate_gdp_data(),
            "inflation_cpi": SampleDataLoader.generate_inflation_data(),
            "inflation_wpi": SampleDataLoader.generate_wpi_data(),
            "repo_rate": SampleDataLoader.generate_repo_rate_data(),
            "usd_inr": SampleDataLoader.generate_usd_inr_data(),
            "crude_oil": SampleDataLoader.generate_crude_oil_data(),
            "industrial_production": SampleDataLoader.generate_iip_data(),
            "fiscal_deficit": SampleDataLoader.generate_fiscal_deficit_data()
        }
    
    @staticmethod
    def save_to_csv(data: Dict[str, pd.DataFrame], directory: str = "./data/economic_data"):
        """Save all indicators to CSV files"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        for indicator, df in data.items():
            filepath = f"{directory}/{indicator}.csv"
            df.to_csv(filepath, index=False)
            print(f"✓ Saved {indicator} to {filepath}")
    
    @staticmethod
    def load_from_csv(directory: str = "./data/economic_data") -> Dict[str, pd.DataFrame]:
        """Load indicators from CSV files"""
        import os
        import glob
        
        data = {}
        csv_files = glob.glob(f"{directory}/*.csv")
        
        for filepath in csv_files:
            indicator = os.path.basename(filepath).replace('.csv', '')
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            data[indicator] = df
            print(f"✓ Loaded {indicator} from {filepath}")
        
        return data