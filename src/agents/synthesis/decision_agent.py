
"""
Decision Agent 
- makes final investment recommendation using the best LLM. It outputs structured JSON.
"""

import json
from typing import Optional, Dict, Any, List
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import DECISION_AGENT


async def run_decision_agent(
    startup_name: str,
    full_report: str,
    risk_assessment: Optional[Dict[str, Any]] = None,
    research_outputs: Optional[List[Dict[str, Any]]] = None,
    analysis_outputs: Optional[List[Dict[str, Any]]] = None
) -> AgentResult:
    """Make final investment recommendation."""
    # Build context
    context_parts = []
    context_parts.append(f"# Investment Decision: {startup_name}\n")
    context_parts.append("## Due Diligence Report\n")
    context_parts.append(full_report)

    if risk_assessment:
        context_parts.append("\n## Risk Assessment Summary\n")
        context_parts.append(json.dumps(risk_assessment, indent=2, default=str))

    context = "\n".join(context_parts)

    prompt = f"""作为一名资深投资决策者，请基于以下信息提供投资建议：

{context}

请综合考虑以下因素：
1. 市场机会及市场进入时机
2. 竞争定位
3. 团队能力
4. 财务健康状况
5. 技术可防御性
6. 风险特征

投资建议选项：
- strong_invest：强烈投资建议，具有高度吸引力，应优先考虑投资
- invest：投资机会良好，按照标准投资条款推进
- hold：具有投资价值，但需等待更多市场验证或增长数据
- pass：未达到投资标准，建议放弃投资
- strong_pass：存在重大风险或关键问题，应避免投资

请将回答严格按照以下合法的 JSON 格式输出：

{{
    "recommendation": "invest",
    "confidence": 0.75,
    "key_factors_for": [
        "市场规模较大",
        "团队实力较强"
    ],
    "key_factors_against": [
        "资金消耗速度较高"
    ],
    "conditions": [
        "希望看到未来 3 个月更多业务数据"
    ],
    "summary_rationale": "尽管存在一定风险，但该项目仍具有较强投资价值……"
}}

请保持分析结果的平衡性和客观性。
"""

    result = await run_agent(
        agent_name=DECISION_AGENT.name,
        prompt=prompt,
        tools=DECISION_AGENT.tools,
        model=DECISION_AGENT.model,
        system_prompt=DECISION_AGENT.system_prompt,
        timeout_seconds=DECISION_AGENT.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
