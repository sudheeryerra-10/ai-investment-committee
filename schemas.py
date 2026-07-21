from pydantic import BaseModel, Field
from typing import List, Optional

# --- AGENT A OUTPUT SCHEMA ---
class QuantReport(BaseModel):
    ticker: str = Field(description="Ticker symbol of the company")
    rule_of_40_score: float = Field(description="Revenue Growth Rate + Free Cash Flow Margin (%)")
    fcf_yield_pct: float = Field(description="Free Cash Flow / Market Cap (%)")
    pe_ratio: Optional[float] = Field(description="Trailing P/E ratio")
    ps_ratio: Optional[float] = Field(description="Price to Sales ratio")
    fundamental_score: float = Field(description="Overall fundamental health score from 0 to 100 based on quantitative math")
    quant_summary: str = Field(description="Executive summary of the quantitative health and growth efficiency")

# --- AGENT B OUTPUT SCHEMA ---
class RiskFactor(BaseModel):
    category: str = Field(description="Category of risk (e.g., Supply Chain, Geopolitical, Regulatory, Currency)")
    severity: str = Field(description="Severity rating: LOW, MEDIUM, or HIGH")
    description: str = Field(description="Specific detail of the risk and how it impacts corporate margins")

class RiskReport(BaseModel):
    ticker: str = Field(description="Ticker symbol")
    identified_risks: List[RiskFactor] = Field(description="List of specific macro/geopolitical risks identified")
    macro_headwind_score: float = Field(description="Macro risk impact score from 0 (no risk) to 100 (extreme risk)")
    bear_case_thesis: str = Field(description="Detailed narrative attacking Agent A's growth assumptions")

# --- AGENT C OUTPUT SCHEMA ---
class InvestmentMemo(BaseModel):
    ticker: str = Field(description="Ticker symbol")
    conviction_score: float = Field(description="Final consensus conviction rating from 0 to 100")
    recommended_allocation_pct: float = Field(description="Suggested portfolio allocation percentage (0.0% to 10.0%)")
    quant_vs_risk_synthesis: str = Field(description="Key reasoning resolving the debate between Agent A and Agent B")
    human_in_the_loop_flag: bool = Field(description="True if human override/manual audit is required prior to execution")
    final_decision: str = Field(description="Final rating: STRONG BUY, BUY, HOLD, or AVOID")