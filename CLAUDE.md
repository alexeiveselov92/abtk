# ABTK - A/B Testing Toolkit

Python library for statistical analysis of A/B tests. Will be available on PyPi for analysts.

**Language:** All code, comments, and documentation in English.

## Core Principles

- **Unified API:** All tests return same `TestResult` format
- **Main method:** `.compare(samples: List[SampleData]) -> List[TestResult]`
- **Pairwise comparisons:** Compare all pairs when multiple samples provided

## Project Structure

```
abtk/
├── core/
│   ├── data_types.py          # SampleData, ProportionData, TestResult
│   ├── base_test_processor.py # Abstract base class for all tests
│   └── quantile_test_result.py
├── tests/                     # Statistical tests (domain logic)
│   ├── parametric/            # TTest, PairedTTest, CupedTTest, ZTest, AncovaTest
│   └── nonparametric/         # BootstrapTest, PairedBootstrapTest, PostNormedBootstrapTest
├── utils/                     # Reusable utilities
│   ├── corrections.py         # Multiple comparisons correction (Bonferroni, Holm, BH, etc.)
│   ├── quantile_analysis.py   # QuantileAnalyzer for QTE
│   ├── dataframe_helpers.py   # Convert pandas DataFrame to SampleData/ProportionData
│   └── visualization.py
├── unit_tests/                # Pytest tests (NOT statistical tests)
├── examples/                  # Usage examples
└── docs/                      # Comprehensive documentation (5000+ lines)
```

## Key Data Types

**SampleData** (continuous metrics):
```python
SampleData(
    data=np.array,          # Required: metric values
    covariates=np.array,    # Optional: for CUPED/ANCOVA (1D or 2D)
    strata=np.array,        # Optional: for stratified bootstrap
    paired_ids=np.array,    # Optional: for paired tests
    cluster_ids=np.array,   # Optional: for cluster-randomized (future, 1D or 2D)
    name=str                # Optional: label
)
```

**ProportionData** (binary metrics):
```python
ProportionData(
    successes=int,  # Number of successes
    trials=int,     # Total trials
    name=str        # Optional: label
)
```

**TestResult:**
- `effect` - treatment effect (relative or absolute)
- `pvalue` - statistical significance
- `reject` - bool (reject null hypothesis?)
- `left_bound`, `right_bound` - confidence interval
- `ci_length` - CI width

## Available Tests (8 total)

**Parametric (5):**
1. `TTest` - Standard two-sample t-test
2. `PairedTTest` - For matched pairs
3. `CupedTTest` - Variance reduction with 1 covariate
4. `ZTest` - For proportions (binary metrics)
5. `AncovaTest` - Multiple covariates + diagnostics (VIF, normality, etc.)

**Nonparametric (3):**
1. `BootstrapTest` - No assumptions, custom statistics
2. `PairedBootstrapTest` - Bootstrap for paired data
3. `PostNormedBootstrapTest` - Bootstrap + variance reduction

## Key Utilities

**corrections.py:**
- `adjust_pvalues(results, method="bonferroni")` - 5 correction methods

**quantile_analysis.py:**
- `QuantileAnalyzer(test, quantiles)` - Analyze effects across distribution

**dataframe_helpers.py:**
- `sample_data_from_dataframe(df, group_col, metric_col, ...)` - For continuous metrics
- `proportion_data_from_dataframe(df, group_col, ...)` - For proportions (2 formats)

**sample_size_calculator.py:**
- `calculate_mde_ttest()` - MDE for t-test
- `calculate_sample_size_ttest()` - Sample size for t-test
- `calculate_mde_cuped()` - MDE with variance reduction (accounts for correlation!)
- `calculate_sample_size_cuped()` - Sample size with CUPED (need fewer users!)
- `calculate_mde_proportions()` - MDE for proportions (CTR, CVR)
- `calculate_sample_size_proportions()` - Sample size for proportions
- All functions accept **either SampleData/ProportionData OR parameters** (hybrid approach)

## Important Conventions

1. **All tests inherit from `BaseTestProcessor`** and implement:
   - `compare(samples)` - main entry point
   - `compare_samples(sample1, sample2)` - pairwise comparison

2. **Test types:** `test_type="relative"` (default, %) or `"absolute"` (raw units)

3. **Alpha level:** `alpha=0.05` (default significance level)

4. **Minimum pandas usage:** Prefer numpy for internal calculations

5. **Documentation:** Comprehensive guides in `docs/` (avoid duplication, use cross-references)

## Testing

- **Unit tests:** `pytest unit_tests/`
- **Statistical tests:** Live in `tests/` directory (domain logic, not pytest)

## Documentation Structure

- `docs/getting-started.md` - Tutorial for beginners
- `docs/faq.md` - Common questions
- `docs/user-guide/` - 7 comprehensive guides:
  - `test-selection.md` - Decision tree
  - `parametric-tests.md` - T-Test, CUPED, etc.
  - `nonparametric-tests.md` - Bootstrap tests
  - `variance-reduction.md` - Overview of CUPED/ANCOVA
  - `ancova-guide.md` - Detailed ANCOVA with diagnostics
  - `multiple-comparisons.md` - P-value corrections
  - `quantile-analysis.md` - QTE analysis

**Total: 5000+ lines of documentation**

## Common Patterns

**Basic usage:**
```python
from core.data_types import SampleData
from tests.parametric import TTest

control = SampleData(data=[100, 110, 95], name="Control")
treatment = SampleData(data=[105, 115, 100], name="Treatment")

test = TTest(alpha=0.05, test_type="relative")
results = test.compare([control, treatment])
```

**With DataFrame:**
```python
from utils.dataframe_helpers import sample_data_from_dataframe

samples = sample_data_from_dataframe(df, group_col='variant', metric_col='revenue')
results = test.compare(samples)
```

**Multiple comparisons:**
```python
from utils.corrections import adjust_pvalues

results = test.compare([control, treatment_a, treatment_b, treatment_c])
adjusted = adjust_pvalues(results, method="bonferroni")
```

**Experiment planning (sample size / MDE):**
```python
from utils.sample_size_calculator import calculate_mde_cuped, calculate_sample_size_ttest

# Option 1: Use historical data
historical = SampleData(data=last_month_revenue)
mde = calculate_mde_cuped(sample=historical, n=1000, correlation=0.7)

# Option 2: Plan from parameters
n_needed = calculate_sample_size_ttest(mean=100, std=20, mde=0.05)
```