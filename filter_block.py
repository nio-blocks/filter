from functools import reduce
from itertools import repeat
from enum import Enum
import operator
from nio.common.block.base import Block
from nio.common.block.attribute import Output
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.select import SelectProperty
from nio.metadata.properties.expression import ExpressionProperty
from nio.metadata.properties.version import VersionProperty
from nio.metadata.properties.holder import PropertyHolder


class BooleanOperator(Enum):
    ANY = 0
    ALL = 1


class Condition(PropertyHolder):
    expr = ExpressionProperty(title='Condition')


@Discoverable(DiscoverableType.block)
@Output('false')
class Filter(Block):

    """ A block for filtering signal objects based on a list of
    plaintext conditions, evaluated as Python code.

    Parameters:
        conditions (list(str)): A list of strings to be evaluated
            as filter conditions.
        operator (select): Determines whether all or any of the
            conditions must be satisfied for a signal to pass the
            filter.
    """

    version = VersionProperty(version='0.1.0', min_version='0.1.0')
    conditions = ListProperty(Condition, title='Filter Conditions')
    operator = SelectProperty(
        BooleanOperator,
        default=BooleanOperator.ALL,
        title='Condition Operator')

    def configure(self, context):
        super().configure(context)
        self._expressions = tuple(c.expr for c in self.conditions)

    def process_signals(self, signals):
        self._logger.debug("Ready to process {} signals".format(len(signals)))
        true_result = signals
        false_result = []
        if self.conditions:
            true_result, false_result = self._filter_signals(signals)

        self._logger.debug("Emitting {} true signals".format(
            len(true_result)))
        if len(true_result):
            self.notify_signals(true_result, 'default')

        self._logger.debug("Emitting {} false signals".format(
            len(false_result)))
        if len(false_result):
            self.notify_signals(false_result, 'false')

    def _filter_signals(self, signals):
        """ Helper function to implement the any/all filtering """
        # bring them into local variables for speed
        eval_expr = self._eval_expr
        true_result = []
        false_result = []
        if self.operator is BooleanOperator.ANY:
            self._logger.debug("Filtering on an ANY condition")
            # let signal in if we find one True in the output
            for sig in signals:
                for expr in self._expressions:
                    if self._eval_expr(expr, sig):
                        self._logger.debug(
                            "Short circuiting ANY on Truthy condition")
                        true_result.append(sig)
                        break
                else:
                    false_result.append(sig)
        else:
            self._logger.debug("Filtering on an ALL condition")
            # Don't let signal in if there is a single False in the output
            for sig in signals:
                for expr in self._expressions:
                    if not self._eval_expr(expr, sig):
                        self._logger.debug(
                            "Short circuiting ALL on Falsy condition")
                        false_result.append(sig)
                        break
                else:
                    true_result.append(sig)

        return (true_result, false_result)

    def _eval_expr(self, expr, signal):
        try:
            return expr(signal)
        except Exception as e:
            self._logger.error("Filter condition evaluation failed")
            return False
