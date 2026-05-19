# Spark Handoffs

This directory stores portable handoff packets when a Spark session reaches a
stop-line before finishing a bounded scenario.

Use `open/` for active handoffs and `closed/` for resolved or superseded
packets that remain useful as examples.

Ordinary closeout belongs in the conversation or pull request. Commit a
handoff packet only when it helps a later session resume without absorbing
neighboring owner truth.
