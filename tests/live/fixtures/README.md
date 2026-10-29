# Fixtures for check_run.py

Authored synthetic test data. These transcripts and annotations are **not** model
runs: no model produced them, and the "judge" labels are placeholders, not
calibrated judges. They exist only so tests can prove that the checker requires
complete judgments and verifiable quotes, and that legitimate corrections and
post-surrender reveals can pass while premature answers fail.

Do not edit these fixtures to tune live results. Never add real learner data,
names, schools, or paths here. Learner lines are the synthetic case turns from
`cases.json`; assistant lines are invented tutor text.
