
from ..base import run_agent, AgentResult, parse_json_from_output
from ...config.agent_configs import NEWS_MONITOR


async def run_news_monitor(
    startup_name: str
) -> AgentResult:
    """Find recent news and press coverage."""

    prompt = f"""请查找关于以下创业公司的近期新闻：

创业公司：{startup_name}

请调研并输出以下内容：
1. 近期官方新闻稿（Press Releases）
2. 新闻报道及媒体报道
3. 融资公告
4. 产品发布或重大更新
5. 存在的争议事件或潜在风险关注点

请以 JSON 格式输出结果：{{...}}
"""

    result = await run_agent(
        agent_name=NEWS_MONITOR.name,
        prompt=prompt,
        tools=NEWS_MONITOR.tools,
        model=NEWS_MONITOR.model,
        system_prompt=NEWS_MONITOR.system_prompt,
        timeout_seconds=NEWS_MONITOR.timeout_seconds
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result
