# Flash‑Card Repo

A **tiny, GitHub‑only flash‑card system** that you can study from any Mac, iPhone, or browser using ChatGPT‑Codex.  No extra apps or installs — everything lives in plain **YAML files** so you always own your data.

---

## 1 · Repo Layout

```
flashcards/
├─ decks/
│  ├─ italian.yaml      # 🇮🇹   Italian vocabulary
│  ├─ german.yaml       # 🇩🇪   German vocabulary
│  ├─ russian.yaml      # 🇷🇺   Russian vocabulary
│  └─ pegs.yaml         # 0‑999 number‑peg words (memory system)
└─ tools/
   └─ scheduler.py      # <optional> helper script (see §5)
```

*Feel free to rename or add more decks — each deck is just another YAML file in **decks/**.*

---

## 2 · YAML Card Format

```yaml
- id: 1                # unique within the deck (integer or string)
  front: ciao          # question / prompt
  back: hello          # answer
  stats:
    reps: 0            # how many times you have reviewed it
    ease: 250          # ease factor ×100 (starts at 250 → 2.5)
    interval: 0        # days until next review (0 = learn queue)
    due: 2025‑06‑27    # next review date (YYYY‑MM‑DD)
```

Only **`front`** and **`back`** are required when you first add a card; the `stats` block is added/updated automatically after you study.

---

## 3 · Studying with ChatGPT‑Codex

1. **Get the raw link** to a deck: open the file on GitHub → **Raw** → copy URL.
2. In ChatGPT (or ChatGPT‑Codex in VS Code), paste a prompt like:

   ```
   Load this YAML deck
   https://raw.githubusercontent.com/your‑user/flashcards/main/decks/italian.yaml
   and quiz me on all cards that are *due today*.
   ```
3. ChatGPT will:

   * parse the YAML,
   * pick cards whose `due` ≤ *today*,
   * show the **front** text and wait for your answer,
   * reveal the **back** and ask how you did — type `again`, `hard`, `good`, or `easy`.
4. When you finish, ask ChatGPT to **output the updated YAML**, then
   *copy‑paste* the new text back into GitHub (Replace → Commit).

That’s the entire loop!  Your phone, Mac, or any browser works the same way.

> **Tip:** Bookmark a prompt like the one above so future study sessions are one click.

---

## 4 · Number‑Peg Deck (pegs.yaml)

The file `pegs.yaml` contains ready‑made mnemonic “peg” words for **0‑999** so you can attach vivid images to numbers when you study.  Use it like any other deck:

```yaml
- id: 23
  front: 23
  back: Name    # the peg word for 23
```

Feel free to edit or localise the words — they’re just YAML.

---

## 5 · (Optional) scheduler.py

If you prefer a one‑click script instead of manual copy‑paste, run:

```bash
python tools/scheduler.py italian.yaml
```

The script will:

1. fetch the deck from GitHub,
2. quiz you in the terminal,
3. update `stats`, and
4. push the file back (you’ll need a personal‑access token set in the `GITHUB_TOKEN` env var).

The algorithm is a minimal variant of the SM‑2 spaced‑repetition model:

```
if rating < 3:          # again / hard
    reps = 0
    interval = 1
else:
    ease += (‑0.8 + 0.28*rating + 0.02*rating^2)
    ease  = max(ease, 130)
    reps += 1
    interval = 1 if reps == 1 else round(interval * ease/100)

due = today + interval days
```

*You don’t need to understand the maths; the script (or ChatGPT) updates these numbers for you.*

---

## 6 · Adding New Cards

1. Open a deck on GitHub → **Edit**.
2. Append new items — keep the same YAML structure.
3. Commit.  Next study session will include them automatically.

---

## 7 · FAQ

**Q · Do I have to use the script?**  No.  Manual copy‑paste via ChatGPT is enough for light use.

**Q · Can I mix media (images, audio)?**  Yes — add extra keys (e.g. `image: url`) and tell ChatGPT to render them when quizzing.

**Q · What happens if two devices edit at once?**  GitHub will show a merge conflict; resolve by keeping the newest `stats` block.

---

Happy learning — and enjoy owning your flash‑card data!
