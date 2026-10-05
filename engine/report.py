"""After-action report generator. Placeholder: built in Hard Stop 4 (task T8).

Will turn a score result into gaps, recommended NIST controls, and
implementation timelines (immediate, short-term, long-term).
"""


def build_report(scenario, score_result):
    """Build the after-action report for one scored session.

    scenario:     a scenario dict returned by engine.content.load_all()
    score_result: the dict returned by engine.scoring.score_session()
    returns:      a report dict rendered by templates/report.html (planned)
    """
    raise NotImplementedError("AAR generator is scheduled for Hard Stop 4 (task T8).")