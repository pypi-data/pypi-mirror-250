import time

from typing import Optional
from driftpy.math.amm import calculate_bid_ask_price
from driftpy.math.oracles import calculate_live_oracle_twap
from driftpy.types import (
    OraclePriceData,
    PerpMarketAccount,
    is_variant,
)

from driftpy.constants.numeric_constants import (
    FUNDING_RATE_OFFSET_DENOMINATOR,
    PRICE_PRECISION as PRICE_PRECISION,
    # PEG_PRECISION,
    AMM_RESERVE_PRECISION,
    QUOTE_PRECISION,
    # FUNDING_PRECISION,
    # PRICE_TO_QUOTE_PRECISION,
    # AMM_TO_QUOTE_PRECISION_RATIO,
    # AMM_TIMES_PEG_TO_QUOTE_PRECISION_RATIO,
)


def calculate_long_short_funding(market: PerpMarketAccount):
    sym = calculate_symmetric_funding(market)
    capped = calculate_capped_funding(market)
    if market.base_asset_amount > 0:
        return [capped, sym]
    elif market.base_asset_amount < 0:
        return [sym, capped]
    else:
        return [sym, sym]


def calculate_live_mark_twap(
    market: PerpMarketAccount,
    oracle_price_data: OraclePriceData = None,
    mark_price: int = None,
    now: int = None,
    period: int = 3600,
) -> int:
    now = now or int(time.time())

    last_mark_twap_with_mantissa = market.amm.last_mark_price_twap
    last_mark_price_twap_ts = market.amm.last_mark_price_twap_ts

    time_since_last_mark_change = now - last_mark_price_twap_ts
    mark_twap_time_since_last_update = max(
        period, max(0, period - time_since_last_mark_change)
    )

    if not mark_price:
        bid, ask = calculate_bid_ask_price(market.amm, oracle_price_data)
        print(f"bid {bid}")
        print(f"ask {ask}")
        mark_price = (bid + ask) // 2

    mark_twap_with_mantissa = (
        mark_twap_time_since_last_update * last_mark_twap_with_mantissa
        + time_since_last_mark_change * mark_price
    ) // (time_since_last_mark_change + mark_twap_time_since_last_update)

    return mark_twap_with_mantissa


def shrink_stale_twaps(
    market: PerpMarketAccount,
    mark_twap_with_mantissa: int,
    oracle_twap_with_mantissa: int,
    now: int = None,
):
    now = now or int(time.time())
    new_mark_twap = mark_twap_with_mantissa
    new_oracle_twap = oracle_twap_with_mantissa

    if (
        market.amm.last_mark_price_twap_ts
        > market.amm.historical_oracle_data.last_oracle_price_twap_ts
    ):
        # Shrink oracle based on invalid intervals
        oracle_invalid_duration = max(
            0,
            market.amm.last_mark_price_twap_ts
            - market.amm.historical_oracle_data.last_oracle_price_twap_ts,
        )
        time_since_last_oracle_twap_update = (
            now - market.amm.historical_oracle_data.last_oracle_price_twap_ts
        )
        oracle_twap_time_since_last_update = max(
            1,
            min(
                market.amm.funding_period,
                max(1, market.amm.funding_period - time_since_last_oracle_twap_update),
            ),
        )
        new_oracle_twap = (
            oracle_twap_time_since_last_update * oracle_twap_with_mantissa
            + oracle_invalid_duration * mark_twap_with_mantissa
        ) // (oracle_twap_time_since_last_update + oracle_invalid_duration)
    elif (
        market.amm.last_mark_price_twap_ts
        < market.amm.historical_oracle_data.last_oracle_price_twap_ts
    ):
        # Shrink mark to oracle twap over tradeless intervals
        tradeless_duration = max(
            0,
            market.amm.historical_oracle_data.last_oracle_price_twap_ts
            - market.amm.last_mark_price_twap_ts,
        )
        time_since_last_mark_twap_update = now - market.amm.last_mark_price_twap_ts
        mark_twap_time_since_last_update = max(
            1,
            min(
                market.amm.funding_period,
                max(1, market.amm.funding_period - time_since_last_mark_twap_update),
            ),
        )
        new_mark_twap = (
            mark_twap_time_since_last_update * mark_twap_with_mantissa
            + tradeless_duration * oracle_twap_with_mantissa
        ) // (mark_twap_time_since_last_update + tradeless_duration)

    return (new_mark_twap, new_oracle_twap)


async def calculate_all_estimated_funding_rate(
    market: PerpMarketAccount,
    oracle_price_data: Optional[OraclePriceData],
    mark_price: Optional[int],
    now: Optional[int],
):
    if is_variant(market.status, "INITIALIZED"):
        return (0, 0, 0, 0, 0)

    now = now if now else int(time.time())

    live_mark_twap = calculate_live_mark_twap(
        market, oracle_price_data, mark_price, now, market.amm.funding_period
    )

    live_oracle_twap = calculate_live_oracle_twap(
        market.amm.historical_oracle_data,
        oracle_price_data,
        now,
        market.amm.funding_period,
    )

    (mark_twap, oracle_twap) = shrink_stale_twaps(
        market, live_mark_twap, live_oracle_twap, now
    )

    twap_spread = mark_twap - oracle_twap
    twap_spread_with_offset = twap_spread + (
        abs(oracle_twap) // FUNDING_RATE_OFFSET_DENOMINATOR
    )

    twap_spread_pct = (twap_spread_with_offset * PRICE_PRECISION * 100) // oracle_twap

    seconds_in_hour = 3600
    hours_in_day = 24

    time_since_last_update = now - market.amm.last_funding_rate_ts

    lowerbound_est = (
        twap_spread_pct
        * market.amm.funding_period
        * min(seconds_in_hour, time_since_last_update)
        // seconds_in_hour
        // seconds_in_hour
        // hours_in_day
    )
    interp_est = twap_spread_pct // hours_in_day
    interp_rate_quote = (
        twap_spread_pct // hours_in_day // (PRICE_PRECISION // QUOTE_PRECISION)
    )

    fee_pool_size = calculate_funding_pool(market)
    if interp_rate_quote < 0:
        fee_pool_size *= -1

    if market.amm.base_asset_amount_long > abs(market.amm.base_asset_amount_short):
        larger_side = abs(market.amm.base_asset_amount_long)
        smaller_side = abs(market.amm.base_asset_amount_short)
        if twap_spread > 0:
            return mark_twap, oracle_twap, lowerbound_est, interp_est, interp_est
    elif market.amm.base_asset_amount_long < abs(market.amm.base_asset_amount_short):
        larger_side = abs(market.amm.base_asset_amount_short)
        smaller_side = abs(market.amm.base_asset_amount_long)
        if twap_spread < 0:
            return mark_twap, oracle_twap, lowerbound_est, interp_est, interp_est
    else:
        return mark_twap, oracle_twap, lowerbound_est, interp_est, interp_est

    if larger_side > 0:
        capped_alt_est = (smaller_side * twap_spread) // hours_in_day
        fee_pool_top_off = (
            fee_pool_size * (PRICE_PRECISION // QUOTE_PRECISION) * AMM_RESERVE_PRECISION
        )
        capped_alt_est = (capped_alt_est + fee_pool_top_off) // larger_side
        capped_alt_est = capped_alt_est * PRICE_PRECISION * 100 // oracle_twap

        if abs(capped_alt_est) >= abs(interp_est):
            capped_alt_est = interp_est
    else:
        capped_alt_est = interp_est

    return mark_twap, oracle_twap, lowerbound_est, capped_alt_est, interp_est


async def calculate_long_short_funding_and_live_twaps(
    market: PerpMarketAccount,
    oracle_price_data: OraclePriceData,
    mark_price: Optional[int],
    now: Optional[int],
):
    (
        mark_twap_live,
        oracle_twap_live,
        _,
        capped_alt_est,
        interp_est,
    ) = await calculate_all_estimated_funding_rate(
        market, oracle_price_data, mark_price, now
    )

    if market.amm.base_asset_amount_long > abs(market.amm.base_asset_amount_short):
        return mark_twap_live, oracle_twap_live, capped_alt_est, interp_est
    elif market.amm.base_asset_amount_long < abs(market.amm.base_asset_amount_short):
        return mark_twap_live, oracle_twap_live, interp_est, capped_alt_est
    else:
        return mark_twap_live, oracle_twap_live, interp_est, interp_est


def calculate_capped_funding(market: PerpMarketAccount):
    smaller_side = min(
        abs(market.amm.base_asset_amount_short), market.amm.base_asset_amount_long
    )
    larger_side = max(
        abs(market.amm.base_asset_amount_short), market.amm.base_asset_amount_long
    )

    next_funding = calculate_oracle_mark_spread_owed(market)
    funding_fee_pool = calculate_funding_fee_pool(market)

    if larger_side != 0:
        capped_funding = (
            smaller_side * next_funding
            + funding_fee_pool * PRICE_PRECISION * AMM_RESERVE_PRECISION
        ) / larger_side
    else:
        capped_funding = next_funding
    # estimated capped amount above estimated next amount, then not a cap
    if abs(capped_funding) >= abs(next_funding):
        capped_funding = next_funding

    capped_funding /= market.amm.last_oracle_price_twap * 100

    return capped_funding


def calculate_symmetric_funding(market: PerpMarketAccount):
    next_funding = calculate_oracle_mark_spread_owed(market)

    next_funding /= market.amm.last_oracle_price_twap * 100

    return next_funding


def calculate_oracle_mark_spread_owed(market: PerpMarketAccount):
    return (market.amm.last_mark_price_twap - market.amm.last_oracle_price_twap) / 24


def calculate_funding_fee_pool(market: PerpMarketAccount):
    fee_pool = (
        market.amm.total_fee_minus_distributions - market.amm.total_fee / 2
    ) / QUOTE_PRECISION
    funding_interval_fee_pool = fee_pool * 2 / 3
    return funding_interval_fee_pool


def calculate_funding_pool(market: PerpMarketAccount):
    total_fee_lb = market.amm.total_exchange_fee // 2
    fee_pool = max(0, (market.amm.total_fee_minus_distributions - total_fee_lb) // 3)
    return fee_pool
