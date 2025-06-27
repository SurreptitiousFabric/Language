"""Minimal SM-2 spaced repetition scheduler."""
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Card:
    """Represents a flashcard scheduled with SM-2."""
    id: int
    interval: int = 0           # days until next review
    repetition: int = 0         # number of successful reviews
    ef: float = 2.5             # easiness factor
    due: datetime = datetime.today()

def review(card: Card, quality: int) -> Card:
    """Update card scheduling based on review quality (0-5)."""
    if quality < 0 or quality > 5:
        raise ValueError("Quality must be between 0 and 5")

    if quality < 3:
        card.repetition = 0
        card.interval = 1
    else:
        card.repetition += 1
        if card.repetition == 1:
            card.interval = 1
        elif card.repetition == 2:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.ef)

    # Update easiness factor
    card.ef += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    if card.ef < 1.3:
        card.ef = 1.3

    card.due = datetime.today() + timedelta(days=card.interval)
    return card

if __name__ == "__main__":
    # Simple demonstration
    c = Card(id=1)
    for q in [5, 5, 5]:
        c = review(c, q)
        print(
            f"After quality {q}: interval={c.interval} days, "
            f"ef={c.ef:.2f}, due={c.due.date()}"
        )
