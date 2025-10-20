"""
Parametric statistical tests.

This module contains parametric hypothesis tests that assume specific
distributional properties (typically normality). These tests are generally
more powerful than nonparametric tests when their assumptions are met.

Available tests:
- TTest: Independent samples t-test for means
- PairedTTest: Paired samples t-test for matched pairs
- CupedTTest: T-test with CUPED variance reduction
- ZTest: Z-test for proportions
- AncovaTest: ANCOVA / Regression Adjustment with multiple covariates
"""

from .ttest import TTest
from .paired_ttest import PairedTTest
from .cuped_ttest import CupedTTest
from .ztest import ZTest
from .ancova_test import AncovaTest

__all__ = [
    'TTest',
    'PairedTTest',
    'CupedTTest',
    'ZTest',
    'AncovaTest',
]
