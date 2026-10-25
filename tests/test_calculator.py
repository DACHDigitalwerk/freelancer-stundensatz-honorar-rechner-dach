# -*- coding: utf-8 -*-
import pytest
from stundensatz_dach import (
    RateInput,
    calculate_freelancer_rate,
    calculate_project_fixed_price,
)


def test_default_de_calculation():
    res = calculate_freelancer_rate(RateInput())
    assert res.country == "DE"
    assert res.currency == "EUR"
    assert res.working_days == 209
    assert res.billable_days == 146.3
    assert res.billable_hours == 1170.4
    assert res.recommended_hourly_net > res.min_hourly_rate_net > 0
    assert res.recommended_daily_net == round(res.recommended_hourly_net * 8, 2)


def test_at_svs_calculation():
    res = calculate_freelancer_rate(RateInput(country="AT", vat_rate_pct=20.0, social_security_costs=15800.0))
    assert res.country == "AT"
    assert res.currency == "EUR"
    assert res.recommended_hourly_gross == round(res.recommended_hourly_net * 1.20, 2)


def test_ch_ahv_calculation():
    res = calculate_freelancer_rate(RateInput(country="CH", vat_rate_pct=8.1, target_net_income=110000.0))
    assert res.country == "CH"
    assert res.currency == "CHF"
    assert res.recommended_hourly_gross == round(res.recommended_hourly_net * 1.081, 2)


def test_unbillable_impact():
    low_unbill = calculate_freelancer_rate(RateInput(unbillable_pct=20.0))
    high_unbill = calculate_freelancer_rate(RateInput(unbillable_pct=45.0))
    assert high_unbill.billable_hours < low_unbill.billable_hours
    assert high_unbill.recommended_hourly_net > low_unbill.recommended_hourly_net


def test_profit_margin_scaling():
    zero_margin = calculate_freelancer_rate(RateInput(profit_margin_pct=0.0))
    with_margin = calculate_freelancer_rate(RateInput(profit_margin_pct=15.0))
    assert zero_margin.recommended_hourly_net == zero_margin.min_hourly_rate_net
    assert with_margin.recommended_hourly_net > zero_margin.recommended_hourly_net


def test_project_fixed_price():
    proj = calculate_project_fixed_price(100.0, 110.0, risk_buffer_pct=20.0, vat_rate_pct=19.0)
    assert proj["buffered_hours"] == 120.0
    assert proj["net_price"] == 13200.0
    assert proj["gross_price"] == 15708.0


def test_invalid_country_raises():
    with pytest.raises(ValueError):
        calculate_freelancer_rate(RateInput(country="US"))


def test_invalid_tax_rate_raises():
    with pytest.raises(ValueError):
        calculate_freelancer_rate(RateInput(income_tax_rate_pct=90.0))


def test_invalid_project_params():
    with pytest.raises(ValueError):
        calculate_project_fixed_price(0.0, 100.0)
