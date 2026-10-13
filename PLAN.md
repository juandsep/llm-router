# PLAN: llm-router

Goal: a personal LLM gateway that reads each prompt, decides with a fine-tuned Laya whether it is easy, mid or hard, and sends it to a cheap, middle or best model of the same family, so most traffic pays the cheap price and only hard prompts pay for the best model.

This file is the single source of truth for project status. The README links here instead of repeating it.

Each phase is one short-lived branch cut from `dev`, one pull request, one concern.

## Phases

- [x] **F0 · Foundations**: git repo, uv project pinned to Python 3.12, `laya` 0.4.6 as the only dependency. `scripts/zero_shot.py` asks the stock checkpoints one `score` question (easy / mid / hard) over 10 hand-labelled prompts (5 Spanish, 5 English). Scaffolded from `gh-project-standard` with the ML layer (`config/model_gate.json`, `docs/model_card.md`, drift check): CI, pre-commit, pytest with a coverage gate, and a `main`/`dev` branch model. The GCP layer is left out until F4.
  - **Baseline (2026-10-12, Apple Silicon, 74 s including the checkpoint download): 5/10.** Every mid prompt is right, but the model collapses toward mid: 2 of 3 easy prompts and all 3 hard prompts come out as mid (scores 0.24 to 1.46 on a 0 to 2 scale, confidence 0.05 to 0.47). This matches the README: the base checkpoints sit near chance on typed decisions until they are fine-tuned (0.36 base against 0.766 fine-tuned).
- [ ] **F1 · Dataset**: one `train.jsonl` and one `eval.jsonl` in Laya's row format (`{"state", "questions", "gold"}`, gold as a probability per level, so disagreement between labels is kept rather than forced into one level).
  - **Label definition, by outcome rather than by opinion.** A prompt is *easy* when the cheap tier answers it correctly, *mid* when the cheap tier fails and the mid tier answers it, and *hard* when only the best tier, or no tier, answers it.
  - **Sources.**
    - [RouterBench](https://huggingface.co/datasets/withmartian/routerbench): about 30k prompts from MMLU, GSM8K, MBPP, MT-Bench and others, each with the answers of 11 models and a correctness score per model. This lets the outcome labels be computed with no new LLM calls. The code repo is MIT, but the dataset card names no license, so confirm before redistributing.
    - [lmarena-ai/arena-human-preference-140k](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k) (CC-BY-4.0): real chat prompts with human votes between two models. A strong model beating a weak one implies the prompt is not easy, and a tie implies it is.
    - The same idea as [RouteLLM](https://huggingface.co/datasets/routellm/gpt4_dataset) (Apache-2.0).
  - **Spanish prompts and the owner's own prompts** (Juani, the RAG, coding) have no public labels. Answer them with the three tiers, then have DeepSeek grade each answer as the judge. The RAG project already uses this pattern in `scripts/compare.py`. Estimated cost is under $1 for 2k prompts at flash prices.
  - **Size and split.** About 6k training rows (2k per level, balanced) and 600 held-out rows. The held-out set is stratified by source and language and never used for calibration.
- [ ] **F2 · Fine-tune**: `laya-train --data train.jsonl --eval-data eval.jsonl --base convaiinnovations/laya-multilingual --loss rlcd`. The base is the multilingual checkpoint because prompts are mixed Spanish and English, and it is twice as fast. The run fits one temperature per question type on calibration items and saves a checkpoint.
  - **Where it runs.** First try locally on Apple Silicon (MPS, `--micro-batch 1 --grad-accum 32`, as the upstream `laya_finetune_typed_decisions_mps.py` does). If one epoch takes more than about 2 h, move to the Kaggle 2xT4 notebook (free, about 4 to 5 h for 4 epochs over 30k questions upstream).
  - Push the checkpoint to a private Hugging Face repo. Log the run, the data hash and the metrics to the shared MLflow.
- [ ] **F3 · Evaluation**: on the held-out set, measure:
  - accuracy and the confusion matrix per level, and calibration (ECE);
  - the cost of routing against always calling the best tier, at real token counts;
  - quality loss: the share of routed answers the DeepSeek judge rates worse than the best tier's answer.
  - **Gate:** promote only if the cost saved is at least 50% and the quality loss is at most 5%.
  - Also try `--freeze-encoder` (heads only) as a cheaper variant.
- [ ] **F4 · Router service**: FastAPI with an OpenAI-compatible `POST /v1/chat/completions` (streaming) and `GET /health`.
  - Laya scores the last user message, then the request goes to the tier's model. `model: "auto"` routes, and any concrete model name passes straight through.
  - The tier-to-model map lives in one YAML file. On a provider error the request falls back one tier up.
  - The client key comes from the `Authorization` header. Every request writes one JSON log line: tier, score, model, tokens, cost and latency.
  - Serve Laya with the ONNX backend (`laya.load(..., backend="onnx")`) so the image ships no torch.
- [ ] **F5 · Kubernetes**: Helm chart for the router, ArgoCD watching this repo (GitOps), and External Secrets Operator reading the provider keys from Google Secret Manager. Access is through Tailscale only, with no public IP.
  - **Cluster.** Start on local `kind` (free). Move to k3s on one GCP spot `e2-medium` VM (about $7 to $10 a month, stopped when not in use), with the budget guard from `portfolio-infra`.
  - Terraform state goes in the shared GCS state bucket.
- [ ] **F6 · Monitoring**: Prometheus `/metrics` (requests, cost and latency per tier), with a dashboard in the central Grafana of `portfolio-infra`. An alert fires when the hard share or the daily cost jumps.

## Decisions

- **Laya as the classifier, not an LLM.** One forward pass of about 33 ms on a T4, with no generated text to parse and a calibrated probability per level. An LLM classifier would cost tokens and latency on every request.
- **Labels come from outcomes, not opinions.** "Hard" means the cheap models failed, which is what the router has to predict. Opinions about difficulty drift from what actually costs quality.
- **Soft gold labels.** Laya trains on probability distributions (RLCD, proper scoring rules). Where models or judges disagree, the label keeps that uncertainty instead of picking one level.
- **One family per tier map.** Each tier map uses one provider family (Claude: Haiku, Sonnet, Opus), so style and tool calling stay the same across tiers. DeepSeek is the cheap alternative map.
- **Local first, cloud when a caller needs it.** The router runs in Docker on the laptop: provider latency dominates, the keys stay local and idle cost is $0. Deploy only when a cloud service (for example the Telegram assistant) must call it; then add the `gh-project-standard` GCP layer (Cloud Run scales to zero, cheaper than an idle VM).
- **Cost first.** The model is fine-tuned on a laptop or free Kaggle GPUs, the cluster runs locally until there is a reason to pay, and the VM is spot and stopped when idle.

## Tier map (prices per 1M tokens, input / output, checked 2026-10-12)

| Tier | Claude map | DeepSeek map |
|---|---|---|
| easy | `claude-haiku-5-5`: $0.10 / $0.50 | `deepseek-flash`: $0.30 / $1.20 peak, half off-peak |
| mid | `claude-sonnet-5-5`: $2 / $10 | `deepseek-v4-pro`: $1.32 / $3.96 peak, half off-peak |
| hard | `claude-opus-5-5`: $4 / $20 | `claude-opus-5-5` (DeepSeek has no stronger tier) |

Prices were verified on platform.claude.com/docs pricing and api-docs.deepseek.com on 2026-10-12. Check them again before F3's cost numbers. Claude Fable 5.1 ($10 / $50) is left out of the map as too expensive for personal use, but it can be passed through by name.

## Success metrics

- Held-out accuracy of at least 0.75, with fewer than 5% of hard prompts sent to the easy tier (the costly mistake).
- At least 50% cost saved against always calling the best tier, with at most 5% quality loss as rated by the judge.
- Router overhead under 50 ms p95 on CPU (ONNX).
- Idle cost of $0 locally and under $10 a month on GCP.
