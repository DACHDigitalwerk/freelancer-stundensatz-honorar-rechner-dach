# -*- coding: utf-8 -*-
import argparse
import json
from dataclasses import asdict
from .calculator import RateInput, calculate_freelancer_rate


def main():
    parser = argparse.ArgumentParser(description="DACH Freelancer Hourly & Daily Rate Calculator 2026")
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"])
    parser.add_argument("--net", type=float, default=72000.0)
    parser.add_argument("--office", type=float, default=14400.0)
    parser.add_argument("--social", type=float, default=13200.0)
    parser.add_argument("--tax", type=float, default=32.0)
    parser.add_argument("--margin", type=float, default=12.0)
    parser.add_argument("--unbillable", type=float, default=30.0)
    args = parser.parse_args()

    vat = 19.0 if args.country == "DE" else (20.0 if args.country == "AT" else 8.1)
    res = calculate_freelancer_rate(
        RateInput(
            country=args.country,
            target_net_income=args.net,
            office_fixed_costs=args.office,
            social_security_costs=args.social,
            income_tax_rate_pct=args.tax,
            profit_margin_pct=args.margin,
            vat_rate_pct=vat,
            unbillable_pct=args.unbillable,
        )
    )
    print(json.dumps(asdict(res), indent=2))


if __name__ == "__main__":
    main()
