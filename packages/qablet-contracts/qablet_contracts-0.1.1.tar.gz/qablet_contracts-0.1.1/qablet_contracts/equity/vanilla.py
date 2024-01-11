"""
Utils for creating vanilla options timetable
"""

from qablet_contracts.timetable import timetable_from_dicts


def option_timetable(
    ccy: str,
    asset_name: str,
    strike: float,
    maturity: float,
    is_call: bool,
    track: str = "",
) -> dict:
    """Create timetable for an equity vanilla call option.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike: the option strike.
        maturity: the maturity of the option in years.
        is_call: true if the option is a call.
        track: an optional identifier for the contract.
    """

    events = [
        {
            "track": track,
            "time": maturity,
            "op": ">",
            "quantity": 0,
            "unit": ccy,
        },
        {
            "track": track,
            "time": maturity,
            "op": "+",
            "quantity": -strike,
            "unit": ccy,
        },
        {
            "track": track,
            "time": maturity,
            "op": "+",
            "quantity": 1,
            "unit": asset_name,
        },
    ]
    return timetable_from_dicts(events)


if __name__ == "__main__":
    # Create the option
    timetable = option_timetable("USD", "SPX", 2900, 0.5, True)
    print(timetable["events"].to_pandas())
