
"""Report Generator Agent - it outputs Markdown text, not JSON. It compiles findings into comprehensive report."""

import json
from typing import Dict, Any, List
from ..base import run_agent, AgentResult
from ...config.agent_configs import REPORT_GENERATOR


async def run_report_generator(
    startup_name: str,
    startup_description: str,
    research_outputs: List[Dict[str, Any]],
    analysis_outputs: List[Dict[str, Any]]
) -> AgentResult:
    """Generate comprehensive due diligence report."""
    # Compile all findings into context
    context = _compile_findings(
        startup_name, startup_description,
        research_outputs, analysis_outputs
    )

    prompt = f"""生成一份全面的尽职调查报告：

{context}

请创建一份专业的 Markdown 格式报告，并包含以下章节：

# 尽职调查报告：{startup_name}

## 执行摘要（Executive Summary）
用 2-3 段文字概述该投资机会

## 公司概况（Company Overview）
介绍公司基本情况、产品以及融资历史

## 市场机会（Market Opportunity）
分析 TAM/SAM/SOM、市场增长趋势以及市场进入时机

## 竞争格局（Competitive Landscape）
分析竞争对手、市场定位以及竞争优势

## 团队评估（Team Assessment）
评估创始人、核心管理团队以及专业能力

## 财务分析（Financial Analysis）
分析融资情况、资金可支撑运营周期（Runway）以及收入模式

## 技术评估（Technical Evaluation）
分析技术栈、技术护城河以及专利情况

## 风险评估（Risk Assessment）
分析主要风险，包括风险严重程度及风险缓解措施

## 结论（Conclusion）
总结核心发现与关键判断

请确保报告具有专业性，并基于数据和事实进行分析。
"""

    result = await run_agent(
        agent_name=REPORT_GENERATOR.name,
        prompt=prompt,
        tools=REPORT_GENERATOR.tools,
        model=REPORT_GENERATOR.model,
        system_prompt=REPORT_GENERATOR.system_prompt,
        timeout_seconds=REPORT_GENERATOR.timeout_seconds
    )

    # For report generator, output IS the raw text
    if result.success:
        result.output = result.raw_output

    return result


def _compile_findings(
    startup_name: str,
    startup_description: str,
    research_outputs: List[Dict[str, Any]],
    analysis_outputs: List[Dict[str, Any]]
) -> str:
    """Compile all findings into structured context."""
    sections = []
    sections.append(f"# Startup: {startup_name}")
    sections.append(f"Description: {startup_description}\n")

    sections.append("## RESEARCH FINDINGS\n")
    for output in research_outputs:
        agent = output.get("agent", "Unknown")
        success = output.get("success", False)
        data = output.get("output")
        sections.append(f"### {agent.replace('_', ' ').title()}")
        if success and data:
            sections.append(json.dumps(data, indent=2, default=str)[:1500])
        else:
            sections.append("*Data not available*")
        sections.append("")

    sections.append("## ANALYSIS FINDINGS\n")
    for output in analysis_outputs:
        agent = output.get("agent", "Unknown")
        success = output.get("success", False)
        data = output.get("output")
        sections.append(f"### {agent.replace('_', ' ').title()}")
        if success and data:
            sections.append(json.dumps(data, indent=2, default=str)[:1500])
        else:
            sections.append("*Data not available*")
        sections.append("")

    return "\n".join(sections)
