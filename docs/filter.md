Filter
======
The Filter block will evaluate an incoming signal against a conditional expression. If the condition is met, the signal will emit from the **true** terminal. If the condition is not met, the signal will emit from the **false** terminal. The Filter block does not alter the incoming signal, it only redirects it to the true or false terminal based on the evaluation fo the conditional expression.

Properties
---
- **Filter Conditions**: A list of expressions to be evaluated as filter conditions.
- **Condition Operator**: Determines whether *ALL* or *ANY* of the conditions must be satisfied.

Examples
---
Every incoming signal is output to either `true` or `false`.
### true
If **Condition Operator** is `ALL` then signals are output here when ALL **Filter Conditions** are `true`.
If **Condition Operator** is `ANY` then signals are output here when ANY **Filter Conditions** are `true`.
### false
If **Condition Operator** is `ALL` then signals are output here when ANY **Filter Conditions** are `false`.
If **Condition Operator** is `ANY` then signals are output here when ALL **Filter Conditions** are `false`.
