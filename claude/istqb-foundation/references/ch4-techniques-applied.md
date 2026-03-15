# Chapter 4 — Test Techniques Applied to Python/pytest

## Equivalence Partitioning → pytest parametrize

**Scenario**: Function `calculate_discount(age)` — under 18: 20%, 18-65: 10%, over 65: 25%

### Step 1: Identify Partitions
| Partition | Range | Valid? | Expected |
|-----------|-------|--------|----------|
| EP1 | age < 0 | Invalid | Raise ValueError |
| EP2 | 0 ≤ age < 18 | Valid | 20% discount |
| EP3 | 18 ≤ age ≤ 65 | Valid | 10% discount |
| EP4 | age > 65 | Valid | 25% discount |

### Step 2: Pick one value per partition (minimum test set)
- EP1: -1 → ValueError
- EP2: 10 → 20%
- EP3: 30 → 10%
- EP4: 70 → 25%

### pytest Code
```python
import pytest

@pytest.mark.parametrize("age, expected_discount", [
    # Valid partitions — one value each
    (10, 0.20),   # EP2: under 18
    (30, 0.10),   # EP3: adult 18-65
    (70, 0.25),   # EP4: senior over 65
])
def test_discount_valid_partitions(age, expected_discount):
    assert calculate_discount(age) == expected_discount

@pytest.mark.parametrize("invalid_age", [-1, -100])  # EP1: invalid
def test_discount_invalid_age_raises(invalid_age):
    with pytest.raises(ValueError):
        calculate_discount(invalid_age)
```

---

## Boundary Value Analysis → pytest parametrize

**Same scenario**: 0-17 → 20%, 18-65 → 10%, 66+ → 25%

### BVA 2-value (test at boundary itself + just outside)
| Boundary | Values to test | Expected |
|----------|---------------|----------|
| Lower bound age 0 | -1 (invalid), 0 (valid) | Error, 20% |
| Transition 17→18 | 17 (20%), 18 (10%) | 20%, 10% |
| Transition 65→66 | 65 (10%), 66 (25%) | 10%, 25% |

### pytest Code
```python
@pytest.mark.parametrize("age, expected", [
    (-1, "error"),   # BVA: below min
    (0,  0.20),      # BVA: min boundary
    (17, 0.20),      # BVA: just below transition
    (18, 0.10),      # BVA: transition point
    (65, 0.10),      # BVA: just before upper transition
    (66, 0.25),      # BVA: upper transition
])
def test_discount_boundaries(age, expected):
    if expected == "error":
        with pytest.raises(ValueError):
            calculate_discount(age)
    else:
        assert calculate_discount(age) == expected
```

---

## Decision Table Testing → pytest

**Scenario**: Login system — Username exists AND Password correct

| Rule | Username exists | Password correct | Expected |
|------|----------------|-----------------|---------|
| R1 | T | T | Login success |
| R2 | T | F | "Wrong password" |
| R3 | F | T | "User not found" |
| R4 | F | F | "User not found" |

*(R3 and R4 same outcome — can collapse to 3 tests if desired)*

```python
@pytest.mark.parametrize("username, password, expected_message", [
    ("alice", "correct_pass", "Login success"),   # R1: T+T
    ("alice", "wrong_pass",   "Wrong password"),   # R2: T+F
    ("unknown", "any_pass",   "User not found"),   # R3/R4: F+T or F+F
])
def test_login_decision_table(username, password, expected_message):
    result = login(username, password)
    assert result.message == expected_message
```

---

## State Transition Testing → pytest

**Scenario**: Traffic light — Red → Green → Yellow → Red

### States & Transitions
```
[Red] --timer--> [Green] --timer--> [Yellow] --timer--> [Red]
```

### 0-switch coverage (every transition once)
| Test | Start State | Event | End State |
|------|-------------|-------|-----------|
| T1 | Red | timer | Green |
| T2 | Green | timer | Yellow |
| T3 | Yellow | timer | Red |

```python
def test_red_to_green():
    light = TrafficLight(initial_state="Red")
    light.timer_event()
    assert light.state == "Green"

def test_green_to_yellow():
    light = TrafficLight(initial_state="Green")
    light.timer_event()
    assert light.state == "Yellow"

def test_yellow_to_red():
    light = TrafficLight(initial_state="Yellow")
    light.timer_event()
    assert light.state == "Red"
```

---

## Combining Techniques (Real-world approach)

For any feature, apply in order:
1. **EP** → define partitions → minimum test set
2. **BVA** → add boundary tests to each partition boundary
3. **DT** → if ≥2 conditions interact, add combination tests
4. **ST** → if stateful, add transition tests
5. **Error guessing** → null, empty string, 0, max int, Unicode, SQL injection strings
