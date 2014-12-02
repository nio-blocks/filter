from functools import reduce
from itertools import repeat
from enum import Enum
import operator
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.select import SelectProperty
from nio.metadata.properties.expression import ExpressionProperty
from nio.metadata.properties.holder import PropertyHolder


OPS = [operator.or_, operator.and_]


class BooleanOperator(Enum):
    ANY = 0
    ALL = 1


class Condition(PropertyHolder):
    expr = ExpressionProperty(title='Condition')




@Discoverable(DiscoverableType.block)
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

    conditions = ListProperty(Condition, title='Filter Conditions')
    operator = SelectProperty(
        BooleanOperator,
        default=BooleanOperator.ANY,
        title='Condition Operator')

    def configure(self, context):
        super().configure(context)
        self._expressions = tuple(c.expr for c in self.conditions)

    def process_signals(self, signals):
        result = signals
        if self.conditions:
            result = self._filter_signals(signals)

        if len(result):
            self.notify_signals(result)

    def _filter_signals(self, signals):
        """ Helper function to implement the any/all filtering

        """
        # bring them into local variables for speed
        eval_expr = self._eval_expr

        if self.operator is BooleanOperator.ANY:
            # let signal in if --           we find one True in the output
            result = [s for s in signals if next((True for n in map(eval_expr, self._expressions, repeat(s)) if n), False)]
        else:
            # Don't let signal in if --     there is a single False in the output
            result = [s for s in signals if next((False for n in map(eval_expr, self._expressions, repeat(s)) if not n), True)]

        return result

    def _eval_expr(self, expr, signal):
        try:
            return expr(signal)
        except Exception as e:
            self._logger.error(
                "Filter condition evaluation failed: {0}: {1}".format(
                    type(e).__name__, str(e))
            )
            return False
