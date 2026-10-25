# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict


@dataclass
class RateInput:
    country: str = "DE"  # DE, AT, CH
    target_net_income: float = 72000.0
    office_fixed_costs: float = 14400.0
    social_security_costs: float = 13200.0
    income_tax_rate_pct: float = 32.0
    profit_margin_pct: float = 12.0
    vat_rate_pct: float = 19.0
    vacation_days: int = 30
    holiday_days: int = 10
    sick_training_days: int = 12
    hours_per_day: float = 8.0
    unbillable_pct: float = 30.0


@dataclass
class RateResult:
    country: str
    currency: str
    working_days: int
    billable_days: float
    billable_hours: float
    pre_tax_profit_needed: float
    base_revenue_needed: float
    target_annual_revenue: float
    target_monthly_revenue: float
    min_hourly_rate_net: float
    recommended_hourly_net: float
    recommended_hourly_gross: float
    recommended_daily_net: float
    recommended_daily_gross: float
    employee_gross_equivalent: float


def calculate_freelancer_rate(inp: RateInput) -> RateResult:
    country = inp.country.upper().strip()
    if country not in ("DE", "AT", "CH"):
        raise ValueError(f"Unsupported country: {country}")
    if inp.target_net_income < 0 or inp.office_fixed_costs < 0 or inp.social_security_costs < 0:
        raise ValueError("Costs and target net income must be non-negative")
    if not (0.0 <= inp.income_tax_rate_pct < 85.0):
        raise ValueError("income_tax_rate_pct must be between 0 and 85")
    if not (0.0 <= inp.unbillable_pct < 95.0):
        raise ValueError("unbillable_pct must be between 0 and 95")
    if inp.hours_per_day <= 0:
        raise ValueError("hours_per_day must be positive")

    currency = "CHF" if country == "CH" else "EUR"
    working_days = max(1, 365 - 104 - inp.vacation_days - inp.holiday_days - inp.sick_training_days)
    billable_days = max(1.0, working_days * (1.0 - inp.unbillable_pct / 100.0))
    billable_hours = max(1.0, billable_days * inp.hours_per_day)

    tax_factor = max(0.15, 1.0 - (inp.income_tax_rate_pct / 100.0))
    pre_tax_profit = inp.target_net_income / tax_factor
    base_revenue = pre_tax_profit + inp.social_security_costs + inp.office_fixed_costs
    target_revenue = base_revenue * (1.0 + inp.profit_margin_pct / 100.0)

    min_hourly = round(base_revenue / billable_hours, 2)
    hourly_net = round(target_revenue / billable_hours, 2)
    vat_mult = 1.0 + (inp.vat_rate_pct / 100.0)
    hourly_gross = round(hourly_net * vat_mult, 2)
    daily_net = round(hourly_net * inp.hours_per_day, 2)
    daily_gross = round(daily_net * vat_mult, 2)
    emp_equiv = round(inp.target_net_income / 0.61, 2)

    return RateResult(
        country=country,
        currency=currency,
        working_days=working_days,
        billable_days=round(billable_days, 2),
        billable_hours=round(billable_hours, 2),
        pre_tax_profit_needed=round(pre_tax_profit, 2),
        base_revenue_needed=round(base_revenue, 2),
        target_annual_revenue=round(target_revenue, 2),
        target_monthly_revenue=round(target_revenue / 12.0, 2),
        min_hourly_rate_net=min_hourly,
        recommended_hourly_net=hourly_net,
        recommended_hourly_gross=hourly_gross,
        recommended_daily_net=daily_net,
        recommended_daily_gross=daily_gross,
        employee_gross_equivalent=emp_equiv,
    )


def calculate_project_fixed_price(
    estimated_hours: float,
    hourly_rate_net: float,
    risk_buffer_pct: float = 20.0,
    vat_rate_pct: float = 19.0,
) -> Dict[str, float]:
    if estimated_hours <= 0 or hourly_rate_net < 0 or risk_buffer_pct < 0:
        raise ValueError("Invalid project parameters")
    buffered_hours = round(estimated_hours * (1.0 + risk_buffer_pct / 100.0), 2)
    net_price = round(buffered_hours * hourly_rate_net, 2)
    gross_price = round(net_price * (1.0 + vat_rate_pct / 100.0), 2)
    return {
        "estimated_hours": estimated_hours,
        "buffered_hours": buffered_hours,
        "net_price": net_price,
        "gross_price": gross_price,
    }
