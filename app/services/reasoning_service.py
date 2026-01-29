from typing import Iterable, Tuple


class ReasoningService:
    @staticmethod
    async def answer(question: str, contexts: Iterable[str]) -> Tuple[str, float, float]:
        joined = "\n\n".join(contexts)
        if not joined:
            return "No relevant information found.", 0.0, 1.0
        snippet = joined[:1024]
        answer = f"Q: {question}\nA: {snippet}"
        confidence = min(0.99, max(0.1, len(snippet) / 1024.0))
        entropy = 1.0 - confidence
        return answer, confidence, entropy

