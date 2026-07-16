
"""
 Input - What the user provides (startup name, description)
 Research outputs - What research agents discover
 Analysis outputs - What analysis agents conclude
 Synthesis outputs - The final report and decision
 Metadata - Current stage, errors, retry count
"""

"""
State schema for the Startup Due Diligence workflow.
"""

from typing import TypedDict, List, Optional, Annotated
from operator import add
from .funding_stage_enums import normalize_funding_stage


class DueDiligenceState(TypedDict):
    """
    Central state object that flows through the LangGraph workflow.
    All agents read from and write to this state.
    """

    # INPUT
    startup_name: str
    startup_description: str
    funding_stage: Optional[str]

    # RESEARCH OUTPUTS (Layer 1)
    research_outputs: Annotated[List[dict], add]   # Annotated + reducers 实现并行安全的列表更新

    # ANALYSIS OUTPUTS (Layer 2)
    analysis_outputs: Annotated[List[dict], add]

    # SYNTHESIS OUTPUTS (Layer 3)
    full_report: Optional[str]
    investment_decision: Optional[dict]

    # WORKFLOW METADATA
    current_stage: str
    errors: Annotated[List[str], add]
    retry_count: int


def create_initial_state(
    startup_name: str,
    startup_description: str,
    funding_stage: Optional[str] = None
) -> DueDiligenceState:
    """Create an initial workflow state from user input."""
    return DueDiligenceState(
        startup_name=startup_name,
        startup_description=startup_description,
        funding_stage=normalize_funding_stage(funding_stage) if funding_stage else None,
        research_outputs=[],
        analysis_outputs=[],
        full_report=None,
        investment_decision=None,
        current_stage="init",
        errors=[],
        retry_count=0
    )
