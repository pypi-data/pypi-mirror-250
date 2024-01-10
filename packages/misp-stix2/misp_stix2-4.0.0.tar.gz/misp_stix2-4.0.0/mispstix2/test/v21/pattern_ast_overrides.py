"""
AST node class overrides for testing the pattern AST builder.
"""
from mispstix2.patterns import (
    EqualityComparisonExpression, StartStopQualifier, StringConstant,
)


class EqualityComparisonExpressionForTesting(EqualityComparisonExpression):
    pass


class StringConstantForTesting(StringConstant):
    pass


class StartStopQualifierForTesting(StartStopQualifier):
    pass
