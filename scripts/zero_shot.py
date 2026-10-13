"""Zero-shot baseline: can stock Laya tell an easy prompt from a hard one?

Runs one `score` question over hand-labelled prompts and prints Laya's
expected level next to the label. The result is the F0 baseline in PLAN.md.

    uv run python scripts/zero_shot.py
"""

from laya import Router

TIERS = ["easy", "mid", "hard"]

QUESTION = {
    "difficulty": {
        "type": "score",
        "instructions": "How capable must a language model be to answer this prompt well?",
        "criteria": [
            "easy: a small cheap model answers it (lookup, rewrite, short translation, chit-chat)",
            "mid: needs solid reasoning or several steps (summaries, ordinary code, explanations)",
            "hard: needs the strongest model (multi-step proofs, system design, subtle debugging)",
        ],
    }
}

# (prompt, label) written by hand; half Spanish, half English.
PROMPTS = [
    ("¿Cuál es la capital de Francia?", "easy"),
    ("Translate 'good morning' to Portuguese.", "easy"),
    ("Corrige la ortografía: 'aver si mañana bamos al sine'.", "easy"),
    (
        "Write a Python function that removes duplicates from a list while keeping order.",
        "mid",
    ),
    ("Resume en tres viñetas las ventajas de Cloud Run frente a una VM.", "mid"),
    (
        "Explain the difference between a T-learner and an S-learner in uplift modeling.",
        "mid",
    ),
    (
        "Explica por qué mi consulta SQL con LEFT JOIN devuelve filas duplicadas y cómo arreglarlo sin subconsultas.",
        "mid",
    ),
    ("Prove that there are infinitely many primes of the form 4k+3.", "hard"),
    (
        "Diseña la arquitectura de un gateway LLM multi-tenant en Kubernetes con presupuestos por clave, fallbacks y trazas, y justifica cada decisión.",
        "hard",
    ),
    (
        "This Rust async code deadlocks only under load with tokio multi-thread runtime; here is the Mutex usage across .await points. Find the root cause and the minimal fix.",
        "hard",
    ),
]


def tier(score: float) -> str:
    return TIERS[min(len(TIERS) - 1, max(0, round(score)))]


def main() -> None:
    router = Router()
    hits = 0
    for text, label in PROMPTS:
        r = router.predict(text, QUESTION)
        ans = r["answers"]["difficulty"]
        got = tier(ans["score"])
        hits += got == label
        print(
            f"{ans['score']:.2f} {got:<4} gold={label:<4} conf={ans.get('confidence', 0):.2f} "
            f"[{r['routing']['model']}] {text[:60]}"
        )
    print(f"accuracy {hits}/{len(PROMPTS)}")


if __name__ == "__main__":
    assert [tier(s) for s in (0.0, 0.49, 0.5001, 1.4, 1.6, 2.0)] == [
        "easy",
        "easy",
        "mid",
        "mid",
        "hard",
        "hard",
    ]
    main()
