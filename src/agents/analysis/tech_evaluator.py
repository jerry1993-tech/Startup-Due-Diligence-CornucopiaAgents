
"""Tech Evaluator Agent - assesses technology and technical defensibility."""

from typing import Optional, Dict, Any
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import TECH_EVALUATOR


async def run_tech_evaluator(
    startup_name: str,
    startup_description: str,
    team_analysis: Optional[Dict[str, Any]] = None
) -> AgentResult:
    """Evaluate technology and technical defensibility."""
    team_context = ""
    if team_analysis:
        team_context = f"\n## Team Technical Background:\n{_format_team_tech(team_analysis)}"

    prompt = f"""请对以下创业公司的技术能力及技术壁垒开展评估：

创业公司名称：{startup_name}
公司描述：{startup_description}
{team_context}

请调研并分析以下内容：
1. 技术栈（编程语言、开发框架、基础设施等）
2. 技术可防御性——哪些因素使其技术难以被复制？
3. 专利或知识产权情况（检索是否已申请或已公开的专利）
4. 技术护城河强度（强 / 中等 / 弱 / 无）
5. 技术风险
6. 综合技术评分（1-10 分）

请将回答严格按照以下合法的 JSON 格式输出：

{{
    "technology_stack": ["Python", "TensorFlow", "AWS"],
    "defensibility_assessment": "专有机器学习模型构成了较高的市场进入壁垒。",
    "patents_identified": 3,
    "technical_moat": "moderate",
    "technical_risks": [
        "关键人员依赖",
        "系统规模化挑战"
    ],
    "tech_score": 7
}}
"""

    result = await run_agent(
        agent_name=TECH_EVALUATOR.name,
        prompt=prompt,
        tools=TECH_EVALUATOR.tools,
        model=TECH_EVALUATOR.model,
        system_prompt=TECH_EVALUATOR.system_prompt,
        timeout_seconds=TECH_EVALUATOR.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result


def _format_team_tech(team_analysis: Dict[str, Any]) -> str:
    """Extract technical team information."""
    lines = []
    founders = team_analysis.get("founders", [])
    for founder in founders:
        if isinstance(founder, dict):
            name = founder.get("name", "Unknown")
            role = founder.get("role", "")
            if "tech" in role.lower() or "cto" in role.lower():
                lines.append(f"- {name} ({role})")
    return "\n".join(lines) if lines else "No technical team details available"
