from openai import OpenAI

from backend.app.config import settings


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt_type: str, params: dict) -> str:
        if not self.is_available():
            return "OpenAI service is not configured. Please set OPENAI_API_KEY in backend/.env"

        prompt_builders = {
            "kpop_us_analysis": self._build_kpop_prompt,
            "football_pathway": self._build_football_prompt,
            "travel_itinerary": self._build_travel_prompt,
            "perception_report": self._build_perception_prompt,
        }

        builder = prompt_builders.get(prompt_type)
        if not builder:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

        prompt = builder(params)

        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
        )

        return response.output_text

    def _build_kpop_prompt(self, params: dict) -> str:
        return f"""
You are a K-pop global market analyst.

Analyse the US market potential of the following K-pop group.

Group: {params.get("group_name", "Unknown")}
US Potential Score: {params.get("us_score", 0)}/10

User-rated factors:
- English Accessibility: {params.get("english", 0)}/10
- Performance Impact: {params.get("performance", 0)}/10
- Social Media Power: {params.get("social_media", 0)}/10
- Western Market Compatibility: {params.get("western_fit", 0)}/10
- Global Fanbase Strength: {params.get("fanbase", 0)}/10

Context:
Japan and China are already established K-pop markets.
This analysis focuses on the US because it represents mainstream Western penetration,
Billboard visibility, Spotify conversion, TikTok virality, and global brand value.

Return a concise report with:
- US market potential level
- main strengths
- main risks
- recommended strategy
- final judgement
"""

    def _build_football_prompt(self, params: dict) -> str:
        return f"""
You are a football pathway analyst.

Analyse whether the following Korean player is closer to:
1. Park Ji-sung pathway
2. Son Heung-min pathway
3. or a different pathway

Player profile:
- Name: {params.get("player_name", "Unknown")}
- Age: {params.get("age", 0)}
- Position: {params.get("position", "Unknown")}
- Current club: {params.get("current_club", "Unknown")}
- Speed: {params.get("speed", 0)}/10
- Finishing: {params.get("finishing", 0)}/10
- Work rate: {params.get("work_rate", 0)}/10
- Tactical discipline: {params.get("tactical_discipline", 0)}/10
- Physicality: {params.get("physicality", 0)}/10
- Marketability: {params.get("marketability", 0)}/10
- European readiness: {params.get("european_readiness", 0)}/10

Park Ji-sung model:
- tactical discipline
- work rate
- big-club adaptability
- team-first role
- Champions League-level system player

Son Heung-min model:
- elite attacking output
- speed
- finishing
- Premier League suitability
- global star power

Return a concise analysis with:
- closest pathway
- EPL potential score
- UCL potential score
- strengths
- risks
- final recommendation
"""

    def _build_travel_prompt(self, params: dict) -> str:
        language = params.get("language", "English")
        route_text = params.get("route_text", "")
        interests_text = params.get("interests_text", "")
        budget_text = params.get("budget_text", "")
        style_text = params.get("style_text", "")

        if language == "中文":
            output_rule = """
非常重要：
请全部使用简体中文输出。
不要使用英文标题。
除非是必要的英文地名或品牌名，否则不要混入英文。
请用中文标题，例如：基本信息、每日路线、交通建议、美食建议、预算说明、文化提示。
"""
        else:
            output_rule = """
IMPORTANT:
Please write the whole output in English.
Use clear English headings.
"""

        return f"""
You are a Korea travel intelligence planner.

Please generate a practical Korea multi-city travel itinerary.

Customer name: {params.get("customer_name", "Customer")}
Travel route: {route_text}
Trip days: {params.get("days", 5)}
Budget level: {budget_text}
Interests: {interests_text}
Travel style: {style_text}
Output language: {language}

Requirements:
1. Create a day-by-day itinerary.
2. Each day should include morning, afternoon, and evening.
3. If the route includes multiple cities, include transportation between cities.
4. Include KTX / bus / flight recommendation where suitable.
5. Include hotel transition advice.
6. Include food suggestions.
7. Include budget notes.
8. Include one local cultural insight.
9. If K-pop is among interests, include K-pop related areas or activities.
10. If sports is among interests, include K League, baseball, or sports viewing ideas.
11. Keep it practical and suitable for a travel product demo.

{output_rule}
"""

    def _build_perception_prompt(self, params: dict) -> str:
        return f"""
You are an analyst writing a concise strategic report on Korea.

User perception:
- Technology: {params.get("q1", 0)}/10
- Culture: {params.get("q2", 0)}/10
- Social Pressure: {params.get("q3", 0)}/10
- Global Influence: {params.get("q4", 0)}/10
- Overall Perception Score: {params.get("score", 0)}/10

System module scores:
{params.get("module_scores", {})}

Return ONLY valid JSON with this structure:

{{
  "executive_summary": "...",
  "system_strengths": ["...", "...", "..."],
  "structural_risks": ["...", "..."],
  "comparative_position": "...",
  "strategic_insight": "...",
  "system_interaction": "..."
}}

Keep it concise, analytical, and suitable for a portfolio project.
"""


openai_service = OpenAIService()
