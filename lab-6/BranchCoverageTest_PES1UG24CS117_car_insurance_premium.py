
import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout

# Example test cases:
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600

def test_no_bonus():
    assert no_claim_bonus(0) == 0

# Annual premium test cases
def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)

def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)

def test_young_driver():
    assert annual_premium("hatchback", 20, 1, False) == 12000

def test_senior_driver():
    assert annual_premium("suv", 60, 1, False) == 17000

def test_more_than_two_claims():
    assert annual_premium("hatchback", 30, 3, False) == 16000

def test_anti_theft_discount():
    assert annual_premium("sedan", 30, 1, True) == 11500

# No claim bonus test cases
def test_negative_claim_free_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)

def test_one_claim_free_year():
    assert no_claim_bonus(1) == 20

def test_three_claim_free_years():
    assert no_claim_bonus(3) == 35

def test_five_claim_free_years():
    assert no_claim_bonus(5) == 50

# Claim payout test cases
def test_negative_damage_cost():
    with pytest.raises(ValueError):
        claim_payout(-100, 5000, 500, False)

def test_negative_deductible():
    with pytest.raises(ValueError):
        claim_payout(1000, 5000, -100, False)

def test_total_loss():
    assert claim_payout(10000, 8000, 500, True) == 8000

def test_damage_below_deductible():
    assert claim_payout(400, 5000, 500, False) == 0

def test_damage_equal_to_deductible():
    assert claim_payout(500, 5000, 500, False) == 0

def test_normal_payout():
    assert claim_payout(3000, 5000, 500, False) == 2500

def test_payout_capped_at_insured_value():
    assert claim_payout(10000, 5000, 500, False) == 5000
