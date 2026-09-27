# Approved blocker resolution — September 27, 2026

**English** | [한국어](../ko/reference/approved-resume-20260927.md)

**The approved permission and model prerequisites were resolved and the previously blocked integrations ran on real Azure.**
That does **not** mean every quality gate passed. The English Hosted matrix was rejected on one final citation check;
the Korean matrix requires review of native findings; the Optimizer's actual grounding references were invalid.
Those outcomes remain in the evidence rather than being repaired or retried for better scores.

[New evidence, original hashes and operation receipts](../assets/approved-resume-20260927/results.json) ·
[62-entry scope/status matrix](../assets/approved-resume-20260927/guide-checks.json) ·
[Earlier September 26 record](live-audit-20260926.md).
The date is Korea Standard Time; original service timestamps are UTC.
The previous record was not overwritten or relabeled.

## What was approved and changed

The user explicitly approved the remaining work. Azure CLI, azd and the opened browser were checked against the requested account.
The existing Sweden Central project and training Search service were reused.
The original main `gpt-6-sol` answer deployment, judge deployment and default Azure subscription remained unchanged.
No company/Microsoft 365 data, API keys, new credentials or subscription-wide Owner grants were used.

| Prerequisite | Actual change | Verification |
|---|---|---|
| Native Toolbox → Search | Add **Search Service Contributor** to the **project** managed identity at the training Search service; its Data Reader role already existed | Actual direct tool query, then model/tool answer |
| Direct OpenAPI → Search | Add **Search Index Data Reader** to the **Foundry account** managed identity at that same service | English and Korean `openapi_call` results, original document content and returned arguments |
| IQ Chat model | Create `gpt-5.6-luna`, version `2026-07-09`, DataZoneStandard **30K TPM** | Exact model, Search identity, separate chat-base configuration, actual planning and synthesis |
| Optimizer model | Create `mfv2-live270927-opt-gpt55` using `gpt-5.5` `2026-04-24`, DataZoneStandard **50K TPM** | Supported model appeared in the wizard; a bounded run executed |
| Hosted Toolbox callers | Project-scoped **Foundry User** on each actual newly deployed runtime principal | Real remote Skill-bearing Toolbox request and downloaded evidence |
| Hosted matrix callers | **Search Index Data Reader** on Search and **Cognitive Services OpenAI User** on the account for each actual matrix runtime | Both models passed local and exact-version remote smoke requests |

New models use `NoAutoUpgrade` and `Microsoft.DefaultV2`, with no spillover or model fallback.
Quota was checked before creation. Two simultaneous account-child writes initially produced a retained `RequestConflict`;
the parent state was inspected and the optimizer deployment was then serialized, not moved to another model or region.
The Search identity's existing **Cognitive Services User** grant for IQ Chat was reused, not duplicated.
Exact new assignment IDs and scopes are in the operation records.

**The identity distinction is important:** correcting the Toolbox's project identity did not fix OpenAPI.
The direct OpenAPI contract uses the Foundry **account** identity. Granting more permissions to the wrong principal is not recovery.

## Recovered integrations

| Integration | English | Korean | Boundary |
|---|---|---|---|
| Ordinary native Toolbox | Real query and MAF answer | Independent real query and MAF answer | Only the owned six-document index; no API key |
| Tool Search and versioned Skill | Toolbox v3, Skill v1 | Toolbox v2, Skill v1 | Upload/download bytes matched; actual `load_skill`, discovery and policy calls retained |
| Hosted Toolbox | `mfv2-live260926-en-tb-r27:1` | `mfv2-live260926-ko-tb-r27:1` | Local and remote execution, immutable package/response verification and all eight session evidence files downloaded |
| OpenAPI | Real successful read-only search | Real successful read-only search after required-argument fix | Not substituted with native Search, IQ or a Python tool |
| IQ Chat | Separate owned English chat base | Separate owned Korean chat base | Search system identity, `low`, `answerSynthesis`, `2026-08-01-preview`; real `modelQueryPlanning` and `modelAnswerSynthesis` |
| Direct model comparison | Six dev rows for each model, 6/6 and 6/6 | Independent six dev rows per model, 6/6 and 6/6 | Same code/prompt/local retrieval; original model setting restored, no migration or holdout use |

The IQ Chat answers identified the KRW 150,000 limit and linked their numeric citations to actual policy records.
This optional supported model binding is separate from the unchanged GPT-6 answer model, not an exception-handler fallback.
The original model-free GA bases were not converted into chat bases.

### OpenAPI correction

A Korean attempt surfaced a second, different failure: `Missing required query parameter: api-version`.
The OpenAPI schema already required the parameter, but a schema default did not cause the model to send it.
The helper now explicitly requests **`api-version=2024-07-01`**, `top=6` and the fixed selected fields;
both languages completed fresh requests after that change. The original failed response remains.
The offline plan also identifies the account identity and required read role.

This is an instruction/schema-clarity improvement, not a guarantee that a model can never omit an argument.
Server validation and visible failures remain; the code does not insert a replacement response after an error.

## Actual two-model Hosted matrix

Each language used an independent source copy, owned Search objects and azd directories.
The runtime was **MAF sequential workflow + GA IQ + account Chat Completions + Invocations**.
Model keys were fixed beforehand: `a = gpt-6-sol`, `b = gpt-5.6-luna`.
The reranker filter was fixed at `0`, concurrency at `1`, and output limit at `2048` before collection.
Only the prompt and corresponding immutable agent version changed between baseline and candidate.

| Gate | English | Korean |
|---|---|---|
| Agent | `mfv2-r27-mx-en-agent`, v1 → v2 | `mfv2-r27-mx-ko-agent`, v1 → v2 |
| Dev baseline | 12/12, errors 0 | 12/12, errors 0 |
| Dev candidate | 12/12, errors 0 | 12/12, errors 0 |
| Evidence comparison | `changed_context_rows: []`, isolated prompt comparison | Same, independently checked |
| Judge calibration | 2/2 correct classifications | 2/2 correct classifications |
| Final holdout, once only | **7/8**, errors 0: `a` 3/4, `b` 4/4 | **8/8**, errors 0: both 4/4 |
| Actual root traces | 12/12 + 12/12 + 8/8 | 12/12 + 12/12 + 8/8 |
| Execution gate | `true` | `true` |
| Overall gate / recommendation | **`false` / `reject`** | **`true` / `review-native-findings`** |
| Native quality / production approval | `false` / `false` | `false` / `false` |

English `a-H04` failed the predeclared citation-relevance check. It was not removed or turned into a regression-development case.
The models were not reselected after seeing holdout. No prompt, corpus, reference answer or threshold was changed to recover the result.
The Korean native results still contain a low groundedness score on `b-H03` and low relevance on the two H04 responses.
Those are review findings, even though its business contract passed.

The acceptance policy required complete, valid native execution and trace lineage, **not every native score to pass**.
That policy was selected before the runs, not after seeing scores.
The two-case calibration checks the judge procedure; it is not a general accuracy certificate.
The public holdout demonstrates final acceptance mechanics, not unseen production generalization.

## Optimizer: executable, but not approved for promotion

The dedicated `mfv2-live260926-en-opt-r27:1` copied the exact verified English browser-agent definition.
The original browser baseline was not edited. The run selected **Instruction only**, maximum **2** candidates,
the new GPT-5.5 optimizer, existing GPT-6 target and separate GPT-6 judge.
Only the six derived dev records were uploaded; no generated production dataset or holdout was used.

Run `opt_3fc7b69370214a46b549f112b6d07197` completed in about four minutes:

- Returned **only the baseline**, score **0.958**, and no optimized candidate.
- Reported 35,900 target tokens, 96,413 judge tokens and 9,583 reflection tokens.
- Displayed both “No improvement” and a generic perfect-score early-stop message.
- The actual baseline evaluation had six rows; D05 relevance scored 3 and failed the configured threshold 4.

The actual `results[].sample.input` was exported from
`eval_f27db2883fde4d56818d9b3fd15b7a42` / `evalrun_44faa0f83cdf48e89797707930881df0`.
**All six Groundedness contexts were the generated answer itself, not the original corpus.**
Its reported grounding scores therefore do not establish source grounding.
The binding review says `grounding_binding_valid: false`; nothing was promoted.
A separate Korean target was prepared, but no second paid run was used after this shared reference-binding defect was confirmed.

The new [`export_evaluation.py`](../../scripts/export_evaluation.py) was unit-tested and exercised against that completed evaluation.
It reads every output page, preserves failed scores, checks expected/unique rows and optionally requires actual judge inputs.
It never calls the target again, changes criteria or grants quality approval.
The [optimizer guide](../labs/extensions/agent-optimizer.md#raw-judge-export) now includes this working review procedure.
This makes the defect observable; it does not claim to repair the service's internal optimization.

## Approved safety and CI lanes

**Applied guardrail:** created and read back the dedicated `mfv2-r27-default-guardrail` policy with the observed default controls and Blocking mode.
The shared default policy definition remained byte-for-byte unchanged.
English and Korean Hosted Toolbox v2 definitions reference the actual full policy ARM ID.
The same D01 and D06 requests were recorded on v1 and v2. All completed; D06 still refused invented approval.
**No platform block was observed.** Policy attachment, an unblocked request and a correct model refusal are different evidence.
The new policy remains attached to these owned versions for reproducibility.

**CI release:** the existing OIDC identity and protected environment ran two deliberately isolated releases:
[English](https://github.com/junwoojeong100/microsoft-foundry-v1.2-labs/actions/runs/36272575801) and
[Korean](https://github.com/junwoojeong100/microsoft-foundry-v1.2-labs/actions/runs/36272833299).
They deployed `mfv2-r27-ci-hosted` v1/v2 and each retained **6/6 actual dev rows, errors 0**, plus runtime-role and idle-session cleanup records.
Only the environment's prefix/agent-name values were changed temporarily; their originals were restored and read back.
No branch protection, federation, client secret, default local subscription or other team's agent was changed.

CI used the already published, checked commit **`a48c3a633e1e1a6ccbc529a1b9ebcdde652558f5`**.
It is separate evidence, not a CI claim for uncommitted local OpenAPI/exporter fixes.
The selected release lane was CI; a new recurring paid monitoring schedule was not enabled.

## Cleanup, retained resources and limits

The final readback verified **20 local-audit Hosted sessions idle**: five for each language's Toolbox and matrix.
Both CI sessions also have idle cleanup evidence.
Runtime model/tool/Skill evidence was downloaded before stopping the main Toolbox sessions; local servers were stopped.

The explicitly approved scoped roles, two new model deployments, owned chat bases, Skills/Toolboxes, agent versions,
evaluation records and dedicated policy are retained so the owner can reproduce the guide.
Shared Foundry/Search/Insights resources were not deleted. Stored session files and shared resources can still incur costs.
This is not a zero-cost or permanent-data-erasure claim.

File Search on the fixed GPT-6 deployment, Router, private networking, Fabric/Work IQ, generated red teaming and optional editor installation
are not relabeled as successful execution. Company/Microsoft 365 access remains outside the workshop even with broad task approval.
The 62-entry matrix explicitly distinguishes newly checked scopes from earlier evidence.

Source runtime: the original commit plus the recorded OpenAPI instruction/identity-plan correction;
runtime hash `e786feac35b03e10e1e57e06bac40b3c5c9fa235f074e7a0977a7c1f0d9ce2fa`.
Frozen prompts, corpora, dev/holdout, dependency pins and the source repository's historical Azure configuration were not rewritten.
No working-tree commit or push was performed.

Return to [validation](validation.md), [coverage](../coverage.md), or [your route](../paths.md).
