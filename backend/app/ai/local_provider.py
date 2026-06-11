from ..schemas import AIReportRequest, AIReportResponse


def _score_gap_text(scores: dict, baseline: dict | None) -> str:
    if not baseline:
        return "No Korea baseline was provided, so this report focuses on your own score pattern."

    labels = {
        "economy": "Economy",
        "technology": "Technology",
        "education": "Education",
        "culture": "Culture",
        "global_influence": "Global Influence",
        "quality_of_life": "Quality of Life",
    }
    gaps = []
    for key, label in labels.items():
        if key in scores and label in baseline:
            gaps.append((label, scores[key] - baseline[label]))
    if not gaps:
        return "Your scores were compared with the Korea baseline where matching categories were available."

    closest = min(gaps, key=lambda item: abs(item[1]))
    widest = max(gaps, key=lambda item: abs(item[1]))
    direction = "above" if widest[1] > 0 else "below"
    return (
        f"Your perception is closest to the Korea baseline in {closest[0]}. "
        f"The largest gap is {widest[0]}, where your score is {abs(round(widest[1], 1))} points {direction} baseline."
    )


class LocalReportProvider:
    provider_name = "local"

    def generate(self, request: AIReportRequest) -> AIReportResponse:
        scores = request.scores.model_dump()
        profile_label = self._profile_label(scores)
        strongest = self._strongest_associations(scores)
        concerns = self._concerns_or_gaps(scores)

        if request.total_submissions is None or request.total_submissions <= 1:
            community_text = "You are among the first respondents. Community comparison is still forming."
        elif request.community_average:
            community_text = self._community_comparison(scores, request.community_average)
        else:
            community_text = "Community averages were not available for this report."

        return AIReportResponse(
            provider=self.provider_name,
            profile_label=profile_label,
            perception_summary=self._summary(request.display_name, profile_label, scores),
            strongest_associations=strongest,
            concerns_or_gaps=concerns,
            korea_baseline_comparison=_score_gap_text(scores, request.korea_baseline),
            community_average_comparison=community_text,
            interpretation_profile=self._interpretation(profile_label),
            suggested_next_question=self._next_question(profile_label),
        )

    def _profile_label(self, scores: dict) -> str:
        economy = scores.get("economy", 0)
        technology = scores.get("technology", 0)
        culture = scores.get("culture", 0)
        global_influence = scores.get("global_influence", 0)
        quality_of_life = scores.get("quality_of_life", 0)

        if economy >= 8 and technology >= 8:
            return "Market-Driven Pragmatist"
        if culture >= 8 and global_influence >= 8:
            return "Soft Power Enthusiast"
        if technology >= 8:
            return "Technology-Focused Analyst"
        if culture >= 8:
            return "Culture-Driven Korea Optimist"
        if quality_of_life <= 4:
            return "Quality-of-Life Skeptic"
        return "Balanced Regional Observer"

    def _strongest_associations(self, scores: dict) -> list[str]:
        labels = {
            "economy": "economic competitiveness",
            "technology": "technology and digital industry",
            "education": "education and human capital",
            "culture": "culture and entertainment exports",
            "global_influence": "global influence and soft power",
            "quality_of_life": "quality of life",
        }
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [labels[key] for key, _ in ranked[:3]]

    def _concerns_or_gaps(self, scores: dict) -> list[str]:
        labels = {
            "economy": "Economic confidence is comparatively lower.",
            "technology": "Technology strength is not strongly associated yet.",
            "education": "Education is not a major perception driver.",
            "culture": "Culture is not the primary association in this response.",
            "global_influence": "Global influence may be perceived as limited.",
            "quality_of_life": "Quality of life appears to be a concern.",
        }
        low = [labels[key] for key, value in scores.items() if value <= 5]
        return low[:3] or ["No major concern stands out; the response is broadly positive."]

    def _summary(self, display_name: str | None, profile_label: str, scores: dict) -> str:
        name = display_name or "This respondent"
        average = round(sum(scores.values()) / len(scores), 1)
        return (
            f"{name} has a {profile_label.lower()} perception pattern, with an overall average of {average}/10. "
            "The response suggests a practical view of Korea shaped by the strongest score categories."
        )

    def _community_comparison(self, scores: dict, community_average: dict) -> str:
        comparable = []
        key_map = {
            "economy": "Economy",
            "technology": "Technology",
            "education": "Education",
            "culture": "Culture",
            "global_influence": "Global Influence",
            "quality_of_life": "Quality of Life",
        }
        for key, label in key_map.items():
            if label in community_average:
                comparable.append((label, scores[key] - community_average[label]))
        if not comparable:
            return "Community averages were available but did not match the report categories."

        strongest_gap = max(comparable, key=lambda item: abs(item[1]))
        direction = "higher than" if strongest_gap[1] > 0 else "lower than"
        return (
            f"Compared with the community average, the clearest difference is {strongest_gap[0]}, "
            f"where this response is {abs(round(strongest_gap[1], 1))} points {direction} the group."
        )

    def _interpretation(self, profile_label: str) -> str:
        profiles = {
            "Market-Driven Pragmatist": "You read Korea through economic and technology capability first, making this profile useful for business, investment, or market-entry thinking.",
            "Soft Power Enthusiast": "You associate Korea strongly with culture and global visibility, suggesting a perception shaped by soft power and media reach.",
            "Technology-Focused Analyst": "You primarily see Korea as a technology and innovation system.",
            "Culture-Driven Korea Optimist": "Your perception is led by cultural appeal, but may need more economic and social context.",
            "Quality-of-Life Skeptic": "Your response suggests interest in Korea, but concern about everyday life, pressure, or wellbeing.",
            "Balanced Regional Observer": "Your perception is moderate and multi-dimensional, with no single category dominating the interpretation.",
        }
        return profiles[profile_label]

    def _next_question(self, profile_label: str) -> str:
        if profile_label == "Quality-of-Life Skeptic":
            return "Which quality-of-life factor most affects your view of Korea: work pressure, cost, housing, education, or social expectations?"
        if profile_label == "Market-Driven Pragmatist":
            return "Which Korean industry would you trust most as a market-entry signal?"
        if "Culture" in profile_label or profile_label == "Soft Power Enthusiast":
            return "Which cultural signal most shaped your perception: K-pop, drama, food, fashion, travel, or social media?"
        return "What would most change your perception of Korea over the next year?"
