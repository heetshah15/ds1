"""
utils.py
--------
Helper module for fetching & shaping CoinGecko data into a clean pandas DataFrame.
- Calls exactly one endpoint per refresh to avoid rate limits
- Uses Demo API with proper authentication
- Includes a 15-min @lru_cache wrapper
"""

from __future__ import annotations
from typing import Tuple, Optional, Dict, List
import time
from functools import lru_cache

import requests
import pandas as pd

# ----- Basic coin list (CoinGecko ids) -----
COIN_OPTIONS: List[Dict[str, str]] = [
    {"label": "Bitcoin (BTC)", "value": "bitcoin"},
    {"label": "Ethereum (ETH)", "value": "ethereum"},
    {"label": "Solana (SOL)", "value": "solana"},
    {"label": "Tether (USDT)", "value": "tether"},
]
CG_IDS_TO_SYMBOL: Dict[str, str] = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "tether": "USDT",
}

# --- API Configuration ---
COINGECKO_API_KEY = "CG-EF8xyCXSkgg9x2fgdUHkVnoi"
BASE = "https://api.coingecko.com/api/v3"

HEADERS = {
    "User-Agent": "ResumeCryptoTicker/1.0 (Dash; pandas; plotly)",
    "Accept": "application/json",
    "x-cg-demo-api-key": COINGECKO_API_KEY,
}


def _get_json(path: str, params: dict, retries: int = 3, timeout: int = 15) -> Optional[dict]:
    """
    Polite GET with minimal retry/backoff. Returns:
      - dict (JSON) on success
      - dict with "_error" on HTTP failure
      - None on silent/unexpected failure
    """
    url = f"{BASE}{path}"
    backoff = 1.0
    
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            
            if r.status_code == 429:
                # Rate limited - wait and retry
                wait_time = backoff * (attempt + 1)
                time.sleep(wait_time)
                continue
                
            if r.status_code == 404:
                return {"_error": f"Coin not found: {path}"}
                
            if not r.ok:
                try:
                    error_detail = r.json()
                    return {"_error": f"HTTP {r.status_code}: {error_detail}"}
                except:
                    return {"_error": f"HTTP {r.status_code}: {r.text[:200]}"}
                    
            return r.json()
            
        except requests.Timeout:
            if attempt < retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 5.0)
            else:
                return {"_error": "Request timeout after retries"}
                
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 5.0)
            else:
                return {"_error": f"Network error: {str(e)}"}
                
    return {"_error": "Network failure after retries"}


def fetch_market_chart_df(coin_id: str, days: int = 1) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Fetch market chart (USD) for the given coin and days range.
    Returns (DataFrame, error_message). DataFrame columns: ['time', 'price'].
    
    CoinGecko automatically determines granularity:
    - 1 day: 5-minute intervals
    - 2-90 days: hourly intervals
    - 90+ days: daily intervals
    """
    params = {
        "vs_currency": "usd",
        "days": str(days),
        "precision": "full"  # Get full precision for prices
    }
    
    js = _get_json(f"/coins/{coin_id}/market_chart", params)

    if not js:
        return None, "No response from API"
        
    if "_error" in js:
        return None, js["_error"]
        
    if "prices" not in js:
        return None, "Missing 'prices' data in API response"

    try:
        prices_data = js["prices"]
        
        if not prices_data or len(prices_data) == 0:
            return None, "No price data available for this timeframe"
        
        # 'prices' is [[timestamp_ms, price], ...]
        df = pd.DataFrame(prices_data, columns=["ms", "price"])
        
        # Convert timestamp to datetime
        df["time"] = pd.to_datetime(df["ms"], unit="ms", utc=True)
        
        # Clean up data
        df = df.dropna(subset=["price"])
        df = df[df["price"] > 0]  # Remove any zero prices
        df = df.sort_values("time")
        df = df[["time", "price"]].reset_index(drop=True)
        
        if df.empty:
            return None, "No valid price data after filtering"
            
        return df, None
        
    except KeyError as e:
        return None, f"Data format error: missing key {e}"
    except Exception as e:
        return None, f"Parse error: {str(e)}"


# ---------- 15-minute cache ----------
@lru_cache(maxsize=64)
def fetch_market_chart_df_cached(
    coin_id: str, 
    days: int, 
    bucket: int
) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Cached wrapper around fetch_market_chart_df. 'bucket' is an integer time bucket
    (e.g., floor(now/900)) so results are reused for up to 15 minutes.
    
    The bucket parameter ensures cache invalidation every 15 minutes while allowing
    multiple requests within that window to reuse the same data.
    """
    return fetch_market_chart_df(coin_id, days)