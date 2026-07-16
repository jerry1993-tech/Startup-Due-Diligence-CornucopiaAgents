
"""
Risk Assessor Agent 
- it receives ALL research and analysis outputs to identify risks across all domains.
"""

import json
from typing import Optional, Dict, Any, List
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import RISK_ASSESSOR


async def run_risk_assessor(
    research_outputs: List[Dict[str, Any]],
    analysis_outputs: Optional[List[Dict[str, Any]]] = None,
    startup_name: str = ""
) -> AgentResult:
    """Perform comprehensive risk assessment using all available data."""
    # Compile all available data
    context_parts = []

    if startup_name:
        context_parts.append(f"Startup: {startup_name}\n")

    context_parts.append("## Research Findings:")
    for output in research_outputs:
        if output.get("success") and output.get("output"):
            agent_name = output.get("agent", "Unknown")
            context_parts.append(f"\n### {agent_name}:")
            context_parts.append(json.dumps(output.get("output"), indent=2, default=str))

    if analysis_outputs:
        context_parts.append("\n## Analysis Findings:")
        for output in analysis_outputs:
            if output.get("success") and output.get("output"):
                agent_name = output.get("agent", "Unknown")
                context_parts.append(f"\n### {agent_name}:")
                context_parts.append(json.dumps(output.get("output"), indent=2, default=str))

    context = "\n".join(context_parts)

    prompt = f"""请基于所有调研结果和分析内容，对该创业公司开展全面风险评估：

{context}

请识别并分析以下风险领域：

1. 市场风险（Market Risks）——市场规模、市场进入时机、市场采用情况
2. 竞争风险（Competitive Risks）——市场竞争、价格竞争压力
3. 执行风险（Execution Risks）——团队执行能力、业务规模化能力
4. 财务风险（Financial Risks）——资金可支撑运营周期（Runway）、盈利能力
5. 监管风险（Regulatory Risks）——合规要求、法律风险暴露

对于每一项风险，请提供以下内容：
- 风险类别
- 风险描述
- 风险严重程度（1-10 分）
- 风险发生可能性（1-10 分）
- 风险缓解措施

请将回答严格按照以下合法的 JSON 格式输出：

{{
    "market_risks": [
        {{
            "description": "...",
            "severity": 6,
            "likelihood": 4,
            "mitigation": "..."
        }}
    ],
    "competitive_risks": [...],
    "execution_risks": [...],
    "financial_risks": [...],
    "regulatory_risks": [...],
    "overall_risk_score": 6,
    "top_risks": [
        "风险 1",
        "风险 2",
        "风险 3"
    ],
    "mitigation_suggestions": [
        "建议 1",
        "建议 2"
    ]
}}
"""

    result = await run_agent(
        agent_name=RISK_ASSESSOR.name,
        prompt=prompt,
        tools=RISK_ASSESSOR.tools,
        model=RISK_ASSESSOR.model,
        system_prompt=RISK_ASSESSOR.system_prompt,
        timeout_seconds=RISK_ASSESSOR.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
