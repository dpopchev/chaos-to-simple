"""The October dataset: the totals the finance frame prints, pinned."""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import pytest

CSV = Path(__file__).parents[1] / "data" / "october.csv"
MEMO = Path(__file__).parents[1] / "data" / "incident.txt"
FIRST_MONDAY = date(2026, 7, 27)
PRICE = 5


@pytest.fixture(name="rows")
def fixture_rows() -> list[dict[str, str]]:
    with CSV.open(newline="") as handle:
        return list(csv.DictReader(handle))


class TestOctober:
    def test_free_shipping_orders_sum_to_1214(self, rows: list[dict[str, str]]) -> None:
        assert sum(int(r["got_free_shipping"]) for r in rows) == 1214

    def test_free_with_coupon_sums_to_1214(self, rows: list[dict[str, str]]) -> None:
        assert sum(int(r["free_with_coupon"]) for r in rows) == 1214

    def test_free_without_coupon_sums_to_0(self, rows: list[dict[str, str]]) -> None:
        assert sum(int(r["free_without_coupon"]) for r in rows) == 0

    def test_shortfall_sums_to_6070(self, rows: list[dict[str, str]]) -> None:
        assert sum(int(r["expected_eur"]) - int(r["received_eur"]) for r in rows) == 6070

    def test_expected_is_should_pay_times_5(self, rows: list[dict[str, str]]) -> None:
        assert all(int(r["expected_eur"]) == int(r["should_pay_shipping"]) * PRICE for r in rows)

    def test_received_is_paid_orders_times_5(self, rows: list[dict[str, str]]) -> None:
        assert all(
            int(r["received_eur"])
            == (int(r["should_pay_shipping"]) - int(r["got_free_shipping"])) * PRICE
            for r in rows
        )

    def test_cart_before_coupon_sums_to_1214(self, rows: list[dict[str, str]]) -> None:
        assert sum(int(r["cart_50_before_coupon"]) for r in rows) == 1214

    def test_memo_quotes_the_sheet(self) -> None:
        memo = MEMO.read_text()
        assert all(figure in memo for figure in ("2,315", "1,101", "5,505", "6,070"))

    def test_monday_follows_the_week_calendar(self, rows: list[dict[str, str]]) -> None:
        assert all(
            date.fromisoformat(r["monday"])
            == FIRST_MONDAY + timedelta(days=7 * (int(r["week"]) - 1))
            for r in rows
        )
