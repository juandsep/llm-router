# Model card: llm-router

Keep this current. A model without a model card is not deployable.

## Intended use

- **What it decides:** <!-- e.g. probability that a customer churns in the next 30 days -->
- **Who consumes it:** <!-- batch scoring / API consumer -->
- **Out of scope:** <!-- populations, time windows or decisions it must not be used for -->

## Data

- **Source and license:**
- **Window:** <!-- training period, and what "today" means for feature freshness -->
- **Checksum:** <!-- hash of the exact training snapshot, recorded in the run tags -->
- **Excluded:** <!-- known leakage, PII handling, dropped columns and why -->

## Model

- **Type and version:**
- **Training command:** <!-- the exact command, reproducible from a clean clone -->
- **Selection metric and gate:** `config/model_gate.json` (`primary_metric`, `minimum_acceptable`)

## Evaluation

| Metric | Baseline | This model | Split |
|---|---|---|---|
|  |  |  |  |

- **Calibration:**
- **Subgroup results:** <!-- where it performs worse -->

## Limitations and biases

<!-- Be specific. Unknown is a valid answer; "none" is not. -->

## Monitoring

- **Drift:** PSI per feature, thresholds in `monitoring.psi` docstring.
- **Metric monitoring:** the primary metric re-evaluated on labelled data as it arrives.
- **Retraining trigger:** <!-- drift above threshold, metric below floor, or fixed cadence -->

## Retirement

- **How to take it out of service:** <!-- remove the model version from the serving config, keep the run -->
- **Owner and contact:**
