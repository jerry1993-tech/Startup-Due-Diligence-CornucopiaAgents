
"""
创建完整的配置文件用于定义三层架构中的所有 11 个智能体
一个包含代理所需全部内容的数据类：
1. 单一真实来源：一处更改配置，全局生效
2. 轻松对比：所有智能体一目了然
3. 可测试性：轻松切换配置进行测试
"""

from dataclasses import dataclass
from typing import List

@dataclass
class AgentConfig:
    name: str
    model: str
    tools: List[str]
    timeout_seconds: int
    system_prompt: str

# =============================================================================
# LAYER 1: RESEARCH AGENTS (5 agents)
# =============================================================================

COMPANY_PROFILER = AgentConfig(
    name="company_profiler",
    model="haiku",
    tools=["WebSearch", "WebFetch"],
    timeout_seconds=180,
    system_prompt = """你是一名专业的企业研究专家，负责对企业进行全面深入的调研，并返回关于企业业务、创立背景以及运营情况的结构化数据。"""
)

MARKET_RESEARCHER = AgentConfig(
    name="market_researcher",
    model="haiku",
    tools=["WebSearch", "WebFetch"],
    timeout_seconds=240,
    system_prompt = """你是一名专业的市场研究分析师，负责分析目标市场机会、TAM/SAM/SOM 市场规模、行业发展趋势以及竞争格局。"""
)

COMPETITOR_SCOUT = AgentConfig(
    name="competitor_scout",
    model="haiku",
    tools=["WebSearch", "WebFetch"],
    timeout_seconds=240,
    system_prompt = """你是一名专业的竞争情报分析专家，负责识别、研究和分析目标企业的竞争对手、竞争优势、竞争劣势以及市场定位。"""
)

TEAM_INVESTIGATOR = AgentConfig(
    name="team_investigator",
    model="haiku",
    tools=["WebSearch", "WebFetch"],
    timeout_seconds=180,
    system_prompt = """你是一名专业的团队研究专家，负责研究创业公司的创始人及核心团队成员，分析其教育与职业背景、行业经验以及历史业绩记录。"""
)

NEWS_MONITOR = AgentConfig(
    name="news_monitor",
    model="haiku",
    tools=["WebSearch", "WebFetch"],
    timeout_seconds=180,
    system_prompt = """你是一名专业的新闻分析专家，负责收集和分析企业近期新闻、官方新闻稿以及媒体报道信息。"""
)

# =============================================================================
# LAYER 2: ANALYSIS AGENTS (4 agents)
# =============================================================================

FINANCIAL_ANALYST = AgentConfig(
    name="financial_analyst",
    model="sonnet",
    tools=[],
    timeout_seconds=180,
    system_prompt = """你是一名专业的财务分析专家，负责分析企业财务数据、融资历史、资金消耗率以及财务健康状况指标。"""
)

RISK_ASSESSOR = AgentConfig(
    name="risk_assessor",
    model="haiku",
    tools=[],
    timeout_seconds=180,
    system_prompt = """你是一名专业的风险评估专家，负责识别、分析和评估企业面临的业务风险、市场风险、技术风险以及监管风险。"""
)

TECH_EVALUATOR = AgentConfig(
    name="tech_evaluator",
    model="sonnet",
    tools=[],
    timeout_seconds=180,
    system_prompt = """你是一名专业的技术评估专家，负责评估企业的技术架构、技术创新能力、技术壁垒（可防御性）以及技术规模化能力。"""
)

LEGAL_REVIEWER = AgentConfig(
    name="legal_reviewer",
    model="haiku",
    tools=[],
    timeout_seconds=180,
    system_prompt = """你是一名专业的法律分析专家，负责识别企业潜在法律风险、监管关注事项以及相关合规要求。"""
)

# =============================================================================
# LAYER 3: SYNTHESIS AGENTS (2 agents)
# =============================================================================

REPORT_GENERATOR = AgentConfig(
    name="report_generator",
    model="sonnet",
    tools=[],
    timeout_seconds=240,
    system_prompt = """你是一名专业的投资报告撰写专家，负责整合企业研究、市场分析及风险评估结果，生成全面、结构化的尽职调查报告。"""
)

DECISION_AGENT = AgentConfig(
    name="decision_agent",
    model="opus",
    tools=[],
    timeout_seconds=180,
    system_prompt = """你是一名专业的投资决策顾问，负责综合所有可获得的信息，生成投资建议，并提供决策置信度及支持投资判断的关键因素。"""
)

# =============================================================================
# AGENT GROUPS
# =============================================================================

RESEARCH_AGENTS = [
    COMPANY_PROFILER,
    MARKET_RESEARCHER,
    COMPETITOR_SCOUT,
    TEAM_INVESTIGATOR,
    NEWS_MONITOR,
]

ANALYSIS_AGENTS = [
    FINANCIAL_ANALYST,
    RISK_ASSESSOR,
    TECH_EVALUATOR,
    LEGAL_REVIEWER,
]

SYNTHESIS_AGENTS = [
    REPORT_GENERATOR,
    DECISION_AGENT,
]

ALL_AGENTS = RESEARCH_AGENTS + ANALYSIS_AGENTS + SYNTHESIS_AGENTS
