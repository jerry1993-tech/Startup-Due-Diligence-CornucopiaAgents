
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import TEAM_INVESTIGATOR


async def run_team_investigator(
    startup_name: str
) -> AgentResult:
    """Research the founding team and key personnel."""

    prompt = f"""请调研以下创业公司的团队情况：

创业公司：{startup_name}

请调研并输出以下内容：
1. 创始人：姓名、教育及职业背景、曾任职公司
2. 核心管理团队及其相关从业经验
3. 重要顾问或董事会成员
4. 团队的历史业绩记录以及专业能力与业务方向的匹配度

请以 JSON 格式输出结果：{{...}}
"""

    result = await run_agent(
        agent_name=TEAM_INVESTIGATOR.name,
        prompt=prompt,
        tools=TEAM_INVESTIGATOR.tools,
        model=TEAM_INVESTIGATOR.model,
        system_prompt=TEAM_INVESTIGATOR.system_prompt,
        timeout_seconds=TEAM_INVESTIGATOR.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
