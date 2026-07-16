
from enum import Enum
from typing import Optional


class FundingStage(str, Enum):
    """International standard startup funding stages."""

    BOOTSTRAPPED = "bootstrapped"
    FRIENDS_AND_FAMILY = "friends_and_family"

    PRE_SEED = "pre_seed"
    SEED = "seed"

    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D = "series_d"
    SERIES_E_PLUS = "series_e_plus"

    PRE_IPO = "pre_ipo"
    IPO = "ipo"
    POST_IPO = "post_ipo"


# ==========================================================
# 标准中文
# ==========================================================

STANDARD_ZH = {
    FundingStage.BOOTSTRAPPED: "自举创业",
    FundingStage.FRIENDS_AND_FAMILY: "亲友轮",

    FundingStage.PRE_SEED: "天使前轮",
    FundingStage.SEED: "种子轮",

    FundingStage.SERIES_A: "A轮融资",
    FundingStage.SERIES_B: "B轮融资",
    FundingStage.SERIES_C: "C轮融资",
    FundingStage.SERIES_D: "D轮融资",
    FundingStage.SERIES_E_PLUS: "E轮及以后",

    FundingStage.PRE_IPO: "上市前融资",
    FundingStage.IPO: "首次公开募股",
    FundingStage.POST_IPO: "上市后融资",
}


# ==========================================================
# 所有可能出现的别名
# key：用户输入
# value：标准Enum
# ==========================================================
# todo: 改为字符相似度匹配
NORMALIZATION_MAP = {

    # -----------------------------
    # Bootstrapped
    # -----------------------------
    "bootstrapped": FundingStage.BOOTSTRAPPED,
    "bootstrap": FundingStage.BOOTSTRAPPED,
    "self funded": FundingStage.BOOTSTRAPPED,
    "self-funded": FundingStage.BOOTSTRAPPED,
    "自举": FundingStage.BOOTSTRAPPED,
    "自举创业": FundingStage.BOOTSTRAPPED,
    "自筹资金": FundingStage.BOOTSTRAPPED,

    # -----------------------------
    # Friends & Family
    # -----------------------------
    "friends and family": FundingStage.FRIENDS_AND_FAMILY,
    "friends & family": FundingStage.FRIENDS_AND_FAMILY,
    "friends_family": FundingStage.FRIENDS_AND_FAMILY,
    "friends-family": FundingStage.FRIENDS_AND_FAMILY,
    "亲友轮": FundingStage.FRIENDS_AND_FAMILY,

    # -----------------------------
    # Pre Seed
    # -----------------------------
    "pre seed": FundingStage.PRE_SEED,
    "pre-seed": FundingStage.PRE_SEED,
    "pre_seed": FundingStage.PRE_SEED,
    "天使前轮": FundingStage.PRE_SEED,
    "种子前轮": FundingStage.PRE_SEED,

    # -----------------------------
    # Seed
    # -----------------------------
    "seed": FundingStage.SEED,
    "seed round": FundingStage.SEED,
    "种子轮": FundingStage.SEED,

    # -----------------------------
    # Series A
    # -----------------------------
    "series a": FundingStage.SERIES_A,
    "series_a": FundingStage.SERIES_A,
    "a轮": FundingStage.SERIES_A,
    "a轮融资": FundingStage.SERIES_A,

    # -----------------------------
    # Series B
    # -----------------------------
    "series b": FundingStage.SERIES_B,
    "series_b": FundingStage.SERIES_B,
    "b轮": FundingStage.SERIES_B,
    "b轮融资": FundingStage.SERIES_B,

    # -----------------------------
    # Series C
    # -----------------------------
    "series c": FundingStage.SERIES_C,
    "series_c": FundingStage.SERIES_C,
    "c轮": FundingStage.SERIES_C,
    "c轮融资": FundingStage.SERIES_C,

    # -----------------------------
    # Series D
    # -----------------------------
    "series d": FundingStage.SERIES_D,
    "series_d": FundingStage.SERIES_D,
    "d轮": FundingStage.SERIES_D,
    "d轮融资": FundingStage.SERIES_D,

    # -----------------------------
    # Series E+
    # -----------------------------
    "series e": FundingStage.SERIES_E_PLUS,
    "series_e": FundingStage.SERIES_E_PLUS,
    "series f": FundingStage.SERIES_E_PLUS,
    "series g": FundingStage.SERIES_E_PLUS,
    "series h": FundingStage.SERIES_E_PLUS,
    "series e+": FundingStage.SERIES_E_PLUS,
    "e轮": FundingStage.SERIES_E_PLUS,
    "f轮": FundingStage.SERIES_E_PLUS,
    "g轮": FundingStage.SERIES_E_PLUS,
    "e轮及以后": FundingStage.SERIES_E_PLUS,

    # -----------------------------
    # Pre IPO
    # -----------------------------
    "pre ipo": FundingStage.PRE_IPO,
    "pre-ipo": FundingStage.PRE_IPO,
    "pre_ipo": FundingStage.PRE_IPO,
    "上市前融资": FundingStage.PRE_IPO,

    # -----------------------------
    # IPO
    # -----------------------------
    "ipo": FundingStage.IPO,
    "首次公开募股": FundingStage.IPO,
    "上市": FundingStage.IPO,

    # -----------------------------
    # Post IPO
    # -----------------------------
    "post ipo": FundingStage.POST_IPO,
    "post-ipo": FundingStage.POST_IPO,
    "post_ipo": FundingStage.POST_IPO,
    "上市后融资": FundingStage.POST_IPO,
}


def normalize_funding_stage(
    funding_stage: Optional[str],
) -> Optional[str]:
    """
    将 funding_stage(中英文/大小写/别名)
    转换为标准中文

    Returns
    -------
    str | None

    Examples
    --------
    >>> normalize_funding_stage("Series A")
    'A轮融资'

    >>> normalize_funding_stage("A轮")
    'A轮融资'

    >>> normalize_funding_stage("series_b")
    'B轮融资'
    """

    if not funding_stage:
        return None

    key = (
        funding_stage
        .strip()
        .lower()
        .replace("_", " ")
    )

    stage = NORMALIZATION_MAP.get(key)

    if stage is None:
        return None

    return STANDARD_ZH[stage]
