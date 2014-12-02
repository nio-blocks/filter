Filter
===========

A block for filtering signal objects based on a list of plaintext conditions, evaluated as Python code.

Properties
--------------

-   **conditions**: List of queries.
-   **operator**: ALL or ANY. Determines whether all or any of the conditions must be satisfied for a signal to pass the filter.

Dependencies
----------------
None

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
A subset of the input list of signals but with only the signals that satisfy the *conditions*.
