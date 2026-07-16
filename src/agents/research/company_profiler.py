
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import COMPANY_PROFILER


async def run_company_profiler(
    startup_name: str,
    startup_description: str
) -> AgentResult:
    prompt = f"""请对以下创业公司进行调研：

{startup_name}

要求：
1. 基于公开信息进行调研。
2. 严格输出合法的 JSON。
3. 不要输出任何解释、分析过程、Markdown 或代码块。
4. 对于无法确定的信息，使用 null。

输出格式如下：

{{
    "name": "{startup_name}",
    "founded": "成立年份，如果未知则为 null",
    ...
}}
"""

    result = await run_agent(
        agent_name=COMPANY_PROFILER.name,
        prompt=prompt,
        tools=COMPANY_PROFILER.tools,
        model=COMPANY_PROFILER.model,
        system_prompt=COMPANY_PROFILER.system_prompt,
        timeout_seconds=COMPANY_PROFILER.timeout_seconds
        )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result

