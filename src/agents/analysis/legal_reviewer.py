
"""Legal Reviewer Agent - checks for lawsuits, regulatory concerns, and compliance requirements."""

from typing import Optional, Dict, Any
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import LEGAL_REVIEWER


async def run_legal_reviewer(
    startup_name: str,
    market_analysis: Optional[Dict[str, Any]] = None
) -> AgentResult:
    """Conduct legal due diligence review."""
    market_context = ""
    if market_analysis:
        market_def = market_analysis.get("market_definition", "")
        if market_def:
            market_context = f"\nMarket: {market_def}"

    prompt = f"""请对以下创业公司开展法律尽职调查：

创业公司名称：{startup_name}{market_context}

请搜索并分析以下内容：
1. 已知的诉讼或法律纠纷
2. 所属行业的监管环境
3. 知识产权相关风险（专利纠纷、商标争议等）
4. 关键合规要求
5. 整体法律风险评分（1-10 分）

请将回答严格按照以下合法的 JSON 格式输出：

{{
    "known_legal_issues": ["存在一项尚未结案的专利侵权诉求"],
    "regulatory_environment": "受监管的金融服务行业",
    "ip_concerns": ["核心技术可能与现有专利存在重叠"],
    "compliance_requirements": ["SOC 2", "GDPR"],
    "legal_risk_score": 5
}}

如果未发现任何法律问题，请明确说明。
"""

    result = await run_agent(
        agent_name=LEGAL_REVIEWER.name,
        prompt=prompt,
        tools=LEGAL_REVIEWER.tools,
        model=LEGAL_REVIEWER.model,
        system_prompt=LEGAL_REVIEWER.system_prompt,
        timeout_seconds=LEGAL_REVIEWER.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
