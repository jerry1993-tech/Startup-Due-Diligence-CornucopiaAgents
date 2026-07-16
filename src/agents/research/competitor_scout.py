
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import COMPETITOR_SCOUT


async def run_competitor_scout(
    startup_name: str,
    startup_description: str
) -> AgentResult:
    """Research competitors for the startup."""

    prompt = f"""请识别并分析以下创业公司的竞争对手：

创业公司：{startup_name}
公司描述：{startup_description}

请调研并报告以下内容：
1. 直接竞争对手（提供相同解决方案，面向相同市场）
2. 间接竞争对手（采用不同解决方案，但解决相同问题）
3. 每个竞争对手的优势与劣势
4. 市场定位对比分析

请以 JSON 格式输出结果：{{...}}
"""

    result = await run_agent(
        agent_name=COMPETITOR_SCOUT.name,
        prompt=prompt,
        tools=COMPETITOR_SCOUT.tools,
        model=COMPETITOR_SCOUT.model,
        system_prompt=COMPETITOR_SCOUT.system_prompt,
        timeout_seconds=COMPETITOR_SCOUT.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
