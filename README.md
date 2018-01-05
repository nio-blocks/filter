Filter
======
The Filter block will evaluate an incoming signal against a conditional expression. If the condition is met, the signal will emit from the **true** terminal. If the condition is not met, the signal will emit from the **false** terminal.

Properties
----------
- **conditions**: A list of expressions to be evaluated as filter conditions.
- **operator**: Determines whether *all* or *any* of the conditions must be satisfied.

Inputs
------
- **default**: Signal to be filtered.

Outputs
-------
- **false**: Signals that evaluate to `False` will emit from this output.
- **true**: Signals that evaluate to `True` will emit from this output.

Commands
--------
None

Dependencies
------------
None

Input
-----
Any list of signals.

Output
------
Every signal is output to either `true` or `false`.
### true
If **operator** is `ALL` then signals are output here when all **conditions** are `true`.
If **operator** is `ANY` then signals are output here when any **conditions** are `true`.
### false
If **operator** is `ALL` then signals are output here when any **conditions** are `false`.
If **operator** is `ANY` then signals are output here when all **conditions** are `false`.

