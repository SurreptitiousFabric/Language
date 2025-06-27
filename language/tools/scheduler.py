#!/usr/bin/env python3
"""
Minimal command-line scheduler for YAML decks (SM-2 variant).

Usage:
    python tools/scheduler.py italian.yaml
"""
import sys, random, datetime as dt, yaml

RATINGS = {'again': 0, 'hard': 2, 'good': 3, 'easy': 5}

def sm2(card, q):
    stats = card.setdefault('stats', {})
    reps = stats.get('reps', 0)
    ease = stats.get('ease', 250)
    interval = stats.get('interval', 0)

    if q < 3:                  # again / hard
        reps, interval = 0, 1
    else:
        ease = max(130, ease + int((-0.8 + 0.28*q + 0.02*q*q)*100))
        reps += 1
        interval = 1 if reps == 1 else round(interval * ease / 100)

    stats.update(
        reps=reps,
        ease=ease,
        interval=interval,
        due=(dt.date.today() + dt.timedelta(days=interval)).isoformat(),
    )

def main(path):
    with open(path, "r", encoding="utf-8") as f:
        cards = yaml.safe_load(f)

    today = dt.date.today().isoformat()
    due = [c for c in cards if c.get("stats", {}).get("due", today) <= today]
    random.shuffle(due)

    print(f"{len(due)} cards due\n")
    for c in due:
        input(f"\nQ: {c['front']}  ▸ press Enter to show answer…")
        print(f"A: {c['back']}")
        if 'mnemonic' in c:
            print(f"Mnemonic: {c['mnemonic']}")
        r = ''
        while r not in RATINGS:
            r = input("again | hard | good | easy : ").strip().lower()
        sm2(c, RATINGS[r])

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(cards, f, allow_unicode=True, sort_keys=False)
    print("\n✓ Deck updated — commit & push when ready.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: scheduler.py <deck.yaml>")
    main(sys.argv[1])
