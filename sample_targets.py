import json
import random
import re
from pathlib import Path

# Configuration
INPUT_JSON = Path("semdom.json")
OUTPUT_PSV = Path("data/04-target-concepts.psv")
SAMPLES_PER_CATEGORY = 200
RANDOM_SEED = 42  # Change or set to None for a different random draw each run

# Map SIL top-level and sub-level prefixes to c12 - c19
SIL_TO_CATEGORY = [
    # c12: matter (physical world, materials, elements, weather)
    (("1.1", "1.2", "1.3", "1.4", "1.7"), "c12"),
    # c13: biology (living organisms, anatomy, bodily functions)
    (("1.5", "1.6", "2.1", "2.2", "2.5", "2.6"), "c13"),
    # c14: motion (motion, mechanics, physical forces, actions)
    (("7.",), "c14"),
    # c15: artifact (artifacts, tools, technology, built spaces)
    (("5.", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8"), "c15"),
    # c16: sense (perception, sensory qualities, textures, evaluation)
    (("2.3", "8.3"), "c16"),
    # c17: mind (cognition, emotion, volition, internal states)
    (("2.4", "3.1", "3.2", "3.3", "3.4", "6.1"), "c17"),
    # c18: society (society, kinship, culture, communication, art)
    (("3.5", "3.6", "4."), "c18"),
    # c19: form (space, geometry, time, quantity, abstract relations)
    (("8.1", "8.2", "8.4", "8.5", "8.6"), "c19"),
]


def map_code_to_category(code: str) -> str | None:
    if not code:
        return None
    for prefixes, cat_id in SIL_TO_CATEGORY:
        if any(code == p.rstrip(".") or code.startswith(p) for p in prefixes):
            return cat_id
    return None


def clean_question(q_text: str) -> str:
    # Remove leading "(1) " and "What words refer to " / "What words describe "
    q = re.sub(r"^\(\d+\)\s*", "", q_text.strip())
    q = re.sub(
        r"^What\s+(words|phrases|verbs|nouns|adjectives)\s+(refer\s+to|describe|mean|indicate|are\s+used\s+for)\s+",
        "",
        q,
        flags=re.IGNORECASE,
    )
    q = q.rstrip("?.! ")
    return q.replace("|", "/")


def extract_headwords(example_words: str, max_words: int = 3) -> str:
    if not example_words:
        return ""
    parts = [w.strip() for w in example_words.split(",") if w.strip()]
    return ", ".join(parts[:max_words]).replace("|", "/")


def weighted_sample_without_replacement(items, k, rng):
    """Samples k items using item['weight'] without replacement."""
    if len(items) <= k:
        return list(items)
    # Efraimidis-Spirakis algorithm for weighted sampling without replacement
    scored = [(rng.random() ** (1.0 / item["weight"]), item) for item in items]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:k]]


def main():
    rng = random.Random(RANDOM_SEED)

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        domains = json.load(f)

    pools = {f"c{i}": [] for i in range(12, 20)}

    for dom in domains:
        code = dom.get("code", "")
        cat_id = map_code_to_category(code)
        if not cat_id:
            continue  # Skips root '1' and grammar '9.*'

        dom_name = dom.get("name", "").replace("|", "/").strip()
        questions = dom.get("questions", [])

        for idx, q_obj in enumerate(questions):
            raw_q = q_obj.get("question", "")
            raw_ex = q_obj.get("exampleWords", "")

            headwords = extract_headwords(raw_ex, max_words=3)
            cleaned_q = clean_question(raw_q)

            # Skip empty entries that have neither examples nor a valid question
            if not headwords and not cleaned_q:
                continue

            if headwords and cleaned_q:
                concept_str = f"{headwords} ({cleaned_q}) [{code}]"
            elif headwords:
                concept_str = f"{headwords} ({dom_name}) [{code}]"
            else:
                concept_str = f"{dom_name}: {cleaned_q} [{code}]"

            # Weight Question (1) 3x higher so core domain concepts are well-represented
            is_q1 = idx == 0 or raw_q.strip().startswith("(1)")
            weight = 2.0 if is_q1 else 1.0

            pools[cat_id].append(
                {
                    "code": code,
                    "concept": concept_str,
                    "weight": weight,
                }
            )

    OUTPUT_PSV.parent.mkdir(parents=True, exist_ok=True)

    rows = ["id|category|concept|word1|word2|word3"]
    t_counter = 1

    print("Sampling summary:")
    for cat_id in sorted(pools.keys()):
        candidates = pools[cat_id]
        sampled = weighted_sample_without_replacement(
            candidates, SAMPLES_PER_CATEGORY, rng
        )
        # Sort sampled items by SIL code so related concepts sit near each other
        sampled.sort(
            key=lambda x: [int(n) for n in x["code"].split(".") if n.isdigit()]
        )

        print(
            f"  {cat_id}: sampled {len(sampled)} / {len(candidates)} available questions"
        )

        for item in sampled:
            t_id = f"t{t_counter:04d}"
            rows.append(f"{t_id}|{cat_id}|{item['concept']}|||")
            t_counter += 1

    with open(OUTPUT_PSV, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")

    print(f"\nWrote {t_counter - 1} target concepts to {OUTPUT_PSV}")


if __name__ == "__main__":
    main()
