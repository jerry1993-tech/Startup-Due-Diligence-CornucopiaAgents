
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import MARKET_RESEARCHER


async def run_market_researcher(
    startup_name: str,
    startup_description: str
) -> AgentResult:
    """Research market opportunity for the startup."""

    prompt = f"""请分析以下创业公司的市场机会：

创业公司：{startup_name}
公司描述：{startup_description}

请调研并报告以下内容：
1. 目标市场定义
2. TAM（总体可服务市场）、SAM（可服务目标市场）、SOM（可获取市场）
3. 市场增长率及发展趋势
4. 市场进入时机

请以 JSON 格式输出结果：{{...}}
"""

    result = await run_agent(
        agent_name=MARKET_RESEARCHER.name,
        prompt=prompt,
        tools=MARKET_RESEARCHER.tools,
        model=MARKET_RESEARCHER.model,
        system_prompt=MARKET_RESEARCHER.system_prompt,
        timeout_seconds=MARKET_RESEARCHER.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
