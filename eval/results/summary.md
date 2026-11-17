# Results

Model: `openai/gpt-oss-120b`, temperature 0.7, 3 runs per design and condition.

## Primary: detection of the planted flaw (10 flawed designs)

- Detection rate, baseline: 0.97
- Detection rate, with skill: 1.00
- Difference (skill minus baseline), averaged over designs: +0.03 (95% bootstrap interval over designs: +0.00 to +0.10)
- Designs where the skill did better / worse / the same: 1 / 0 / 9 (exact sign test p = 1.000)

## Secondary

Share of detected flaws labelled BLOCKING:

| condition   |   as_blocking |
|:------------|--------------:|
| baseline    |           0.9 |
| skill       |           1   |

Over-flagging on the 2 clean designs (share of reviews):

| condition   |   overflag |
|:------------|-----------:|
| baseline    |          1 |
| skill       |          1 |

Verdicts:

| designs / condition   |   not ready |   ready with conditions |
|:----------------------|------------:|------------------------:|
| clean / baseline      |           4 |                       2 |
| clean / skill         |           5 |                       1 |
| flawed / baseline     |          27 |                       3 |
| flawed / skill        |          29 |                       1 |

Median review length (words) and failed-run share by condition:

| condition   |   median_words |   failed_share |
|:------------|---------------:|---------------:|
| baseline    |          750.5 |              0 |
| skill       |          817   |              0 |

## Per design

| design_id   |   baseline |   skill |   diff |
|:------------|-----------:|--------:|-------:|
| D01         |       1    |       1 |   0    |
| D02         |       1    |       1 |   0    |
| D03         |       1    |       1 |   0    |
| D04         |       0.67 |       1 |   0.33 |
| D05         |       1    |       1 |   0    |
| D06         |       1    |       1 |   0    |
| D07         |       1    |       1 |   0    |
| D08         |       1    |       1 |   0    |
| D09         |       1    |       1 |   0    |
| D10         |       1    |       1 |   0    |

Interpretation rules are in PLAN.md. The 10 designs were written for this test, so the result describes these flaws, not experimental designs in general.
