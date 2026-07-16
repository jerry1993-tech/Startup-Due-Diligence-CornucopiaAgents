
"""
Financial Analyst Agent: Analyzes financial health and sustainability based on research data.
"""

from typing import Optional, Dict, Any
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import FINANCIAL_ANALYST


async def run_financial_analyst(
    company_profile: Optional[Dict[str, Any]] = None,
    market_analysis: Optional[Dict[str, Any]] = None,
    startup_name: str = "",
    startup_description: str = ""
) -> AgentResult:
    """Analyze financial health based on research data."""
    # Build context from available data
    context_parts = []

    if startup_name:
        context_parts.append(f"Startup Name: {startup_name}")
    if startup_description:
        context_parts.append(f"Description: {startup_description}")
    if company_profile:
        context_parts.append(f"\n## Company Profile Data:\n{_format_dict(company_profile)}")
    if market_analysis:
        context_parts.append(f"\n## Market Analysis Data:\n{_format_dict(market_analysis)}")

    context = "\n".join(context_parts)

    prompt = f"""请分析以下创业公司的财务健康状况及可持续发展能力：

{context}

请提供以下分析内容：
1. 累计融资总额（根据融资历史汇总计算）
2. 基于当前融资阶段估算的资金可支撑运营周期（Runway）
3. 收入模式评估
4. 财务健康评分（1-10 分）
5. 主要财务风险或关注点

请将回答严格按照以下合法的 JSON 格式输出：

{{
    "total_funding": {{"amount": 50000000, "currency": "USD"}},
    "estimated_runway": "18-24 个月",
    "revenue_model": "SaaS 订阅模式",
    "financial_health_score": 7,
    "concerns": ["资金消耗速度较高", "需要建立清晰的盈利路径"]
}}

请基于可获得的数据进行分析；如果相关数据缺失，请明确说明。
"""

    result = await run_agent(
        agent_name=FINANCIAL_ANALYST.name,
        prompt=prompt,
        tools=FINANCIAL_ANALYST.tools,
        model=FINANCIAL_ANALYST.model,
        system_prompt=FINANCIAL_ANALYST.system_prompt,
        timeout_seconds=FINANCIAL_ANALYST.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result


def _format_dict(d: Dict[str, Any], indent: int = 0) -> str:
    """Format a dictionary for readable output."""
    lines = []
    prefix = "  " * indent
    for key, value in d.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(_format_dict(value, indent + 1))
        else:
            lines.append(f"{prefix}{key}: {value}")
    return "\n".join(lines)
