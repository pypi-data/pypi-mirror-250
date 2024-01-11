# Utils for creating swaptions

import numpy as np
from qablet_contracts.timetable import timetable_from_dicts


def simple_swap_period(
    ccy: str, start: float, end: float, fixed_rate: float, track: str = ""
) -> list:
    """Simple representation of a swap period, paying fixed, receiving floating rate.

    Args:
        ccy: the currency of the swap.
        start: the start of the period in years.
        end: the end of the period in years.
        fixed_rate: the fixed annual rate of the swap.
        track: an optional identifier for the contract.
    """
    return [
        {
            "track": track,
            "time": start,
            "op": "+",
            "quantity": 1,
            "unit": ccy,
        },
        {
            "track": track,
            "time": end,
            "op": "+",
            "quantity": -1 - fixed_rate * (end - start),
            "unit": ccy,
        },
    ]


def bermuda_swaption_timetable(
    ccy: str, times: list[float], strike_rate: float, track: str = ""
) -> dict:
    """Create timetable for a co-terminal bermuda swaption.

    Args:
        ccy: the currency of the swap.
        times: the period times of the underlying swap, including the inception and maturity.
        strike_rate: the strike rate of the swaption (in units, i.e. 0.02 means 200 bps).
        track: an optional identifier for the contract.
    """

    events = []
    for start, end in zip(times[0:-1], times[1:]):
        # option expiration event before each period
        events.append(
            {
                "track": track + ".opt",
                "time": start,
                "op": ">",
                "quantity": 1,
                "unit": track + ".swp",
            }
        )
        # payment event for the underlying swap
        events.extend(
            simple_swap_period(ccy, start, end, strike_rate, track + ".swp")
        )

    return timetable_from_dicts(events)


def swaption_timetable(
    ccy: str, times: list[float], strike_rate: float, track: str = ""
) -> dict:
    """Create timetable for a vanilla swaption.

    Args:
        ccy: the currency of the swap.
        times: the period times of the underlying swap, including the inception and maturity.
        strike_rate: the strike rate of the swaption (in units, i.e. 0.02 means 200 bps).
        track: an optional identifier for the contract.
    """

    # option expiration event at beginning of the swap
    events = [
        {
            "track": track + ".opt",
            "time": times[0],
            "op": ">",
            "quantity": 1,
            "unit": track + ".swp",
        }
    ]
    # payment events for the underlying swap
    for start, end in zip(times[0:-1], times[1:]):
        events.extend(
            simple_swap_period(ccy, start, end, strike_rate, track + ".swp")
        )

    return timetable_from_dicts(events)


if __name__ == "__main__":
    # Create the bermuda swaption
    times = np.linspace(
        1, 6, 6
    ).tolist()  # Start at 1 year, mature at 6 years.
    strike_rate = 0.03
    timetable = bermuda_swaption_timetable("USD", times, strike_rate)

    print(timetable["events"].to_pandas())
