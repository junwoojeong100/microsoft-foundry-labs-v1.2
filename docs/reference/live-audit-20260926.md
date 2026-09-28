# Live deployment and guide audit — September 26, 2026

**English** | [한국어](../ko/reference/live-audit-20260926.md)

**Real Azure deployment and the core A/B paths were checked independently in English and Korean.**
All 29 lab/extension pages and two advanced workbooks per language have an explicit review status.
**This is not a claim that all optional features ran successfully.** Required permissions, unsupported features and design-only boundaries remain visible.

Evidence: [62-entry guide matrix](../assets/live-guide-audit-20260926/guide-checks.json) ·
[Responses, evaluations, deployment/cleanup records and source hashes](../assets/live-guide-audit-20260926/results.json).
The audit was performed by an AI assistant using the requested account, not by an independent beginner or a human business approver.
No new video was recorded.

## Scope and environment

The requested account was verified separately in Azure CLI, azd and the browser.
The current `gpt-6-sol` / `2026-09-22` deployment, separate `gpt-6-sol-judge`, existing Search service and Application Insights
were used in the Sweden Central training project `mfv2-g6luna-20260923`.
The old resource name does not mean the model was switched to Luna.

Source commit: `a48c3a633e1e1a6ccbc529a1b9ebcdde652558f5`.
English and Korean used independent source copies, `.env` files, run folders and ownership ledgers.
The source repository's historical `.env` and `azure.yaml` were not repointed, and the default Azure subscription was not changed.
No role was assigned. No company/Microsoft 365 data, external web search, new model deployment or infrastructure provisioning was used.
The user completed the browser authentication; SDK and browser authentication were not assumed to be interchangeable.

| Deployed target | Version | Actual execution |
|---|---|---|
| `mfv2-live260926-en-hosted` | `1` | English single-agent local Responses smoke, direct code deployment, remote response |
| `mfv2-live260926-ko-hosted` | `1` | Independent Korean local smoke, direct code deployment, remote response |
| `mfv2-live260926-en-workflow` | `1` | Sequential workflow-as-agent local smoke, direct code deployment, remote response with three actual model-call records |

Each deployment used its own standalone azd directory, an existing-project binding, Python 3.13 and `1 CPU / 2Gi`.
`show` confirmed the new version was active before the remote invocation.
No Docker build, model substitution or deployment of the source repository's historical services was needed.
The package manifests still say `cloud_deployed: false`: that is their original packaging claim, not a field to rewrite after deployment.

## Results and what they establish

| Check | English | Korean | Boundary |
|---|---|---|---|
| Offline v1/v2 rehearsal | 0/6 → 6/6, errors 0 | 0/6 → 6/6, errors 0 | Fixed fixtures, not prompt-quality improvement |
| B dev baseline / candidate | 6/6 / 6/6, errors 0 | 6/6 / 6/6, errors 0 | Same frozen local-retrieval experiment; equal scores do not establish superiority |
| B final holdout | 4/4, errors 0 | 4/4, errors 0 | Collected once per language only after its own dev gate; public teaching data, not unseen validation |
| B acceptance | `ready-for-human-review` | `ready-for-human-review` | `deployment_approved: false`; no human production approval |
| A saved inline agent | Version 2, four smoke checks, six new assessment answers | Separate version 2, four smoke checks, six new assessment answers | Actual saved instructions matched the respective learner file; AI-assisted rubric review, not a learner pilot |
| Native candidate | Groundedness 6/6, relevance 5/6 | Groundedness 6/6, relevance 5/6 | Low scores retained separately from business checks |
| MAF function-tool evaluation | Tool accuracy 6/6, relevance 6/6, errors 0 | Tool accuracy 6/6, relevance 6/6, errors 0 | Actual tool transcripts from these new evaluations; SDK reports evaluator versions were not pinned |
| Portal dataset evaluation | Relevance 6/6, coherence 6/6, TaskAdherence 0/6 | Relevance 5/6, coherence 6/6, TaskAdherence 0/6 | Exact browser-agent v2 and questions-only dataset; all original evaluator rows retained |
| Custom business evaluator | Baseline/candidate agreement 6/6 each; groundedness 6/6 and relevance 5/6 each | Not repeated | Same evaluation group and pinned custom rubric; not a Korean result |
| Conversation evaluation | Turn: 6/6 for both metrics; conversation: 2/2 for both | Independent same counts | Six actual turns / two histories; groundedness and coherence have different evaluation units |

Both languages also completed the no-tool/function/MCP paths, all three MAF patterns, owned ordinary Search and GA IQ retrieval,
and a fresh IQ-grounded answer. Search and IQ returned different evidence sets; the audit did not pretend they were identical.
The separate English hybrid branch used a new owned index and actual 3072-dimensional embeddings, then retrieved and answered.
It did not change the original text index or become a fallback for a failed IQ call.

### Trace correlation

| Target | Verified trace | Check |
|---|---|---|
| English browser agent v2 | `9daaa842155e46c3917f64cfca2dce74` | Matching saved D01 reply, `invoke_agent` and child `chat` |
| Korean browser agent v2 | `70e9ed12aa634bb28e32bf45aad34082` | Matching independent Korean D01 reply and version |
| English SDK agent v1 | `298b0d8974008b864e19c5e52c603d25` | Exact `response_id`, 1124 input / 108 output tokens |
| Korean SDK agent v1 | `aa499b28e352f15af558819a9d5df794` | Exact `response_id`, 1290 input / 135 output tokens |
| English / Korean Hosted single-agent smoke | `c58c700677a171e1947cc90ba6fae7ac` / `6c6038ab79b14ae2bf5643ef9f336a96` | Trace IDs returned by remote invocation; not a new portal correlation claim |
| English Hosted workflow smoke | `1a521ecc076e15306ce8f50d178477e7` | Remote trace context plus actual three-call lineage; export status kept as reported |

No new request was sent solely to populate a trace screenshot.
Direct/local MAF response records were not relabeled as server-side traces.

## Advanced modules: preserve successes and blockers

**Verified in both languages:** A2A target/card/keyless connection/relay and matching 1.0 delegation; managed-memory create/put/recall/update/forget/cleanup;
Code Interpreter's downloaded CSV with exactly the original six policy IDs/titles; and one manual routine dispatch followed by disabling/deletion.
Routine delivery is verified, **stored answer and future timer firing are not**. Cancelled timer attempts remain in the records.

**English-only additions:** the deployed Responses workflow, hybrid RAG, custom business-rubric comparison, and one SDK Insights scan.
Insights analyzed 17 traces, used 158,439 judge tokens and returned two findings. Its monitor stayed disabled and was deleted after its results were saved.
The local SDK approval-gate exercise also completed; it used fixed English D03 work, **no Azure/model calls**, and retained `human_authorization: not-granted`.
The Korean recovery guide describes that same fixed-English simulation, not a separate Korean model experiment.

| Blocked or not run | Actual reason |
|---|---|
| File Search | `Upload files` disabled for `gpt-6-sol`; English tooltip explicitly says temporarily unavailable |
| Native Toolbox → Search | Owned Toolbox creation/discovery succeeded; direct query returned Access denied. Project identity had Search Index Data Reader only. Additional scoped role approval was requested but unavailable; no role was granted |
| Tool Search/Skills and Hosted Toolbox | Depend on that successful native tool query; not bypassed with a different provider |
| OpenAPI | Outer HTTP 400 `tool_user_error` contained a downstream Search HTTP 403; original error retained, no replacement request |
| IQ Chat | Required separate supported `gpt-5.6-luna` deployment and outbound identity preparation were absent in the selected account |
| Hosted IQ/Invocations matrix | Separate runtime Search permission and matrix prerequisites were not approved/prepared; core Responses scores were not transferred |
| Agent Optimizer / model migration / Router | No supported optimizer or separately approved second answer model/Router prepared; portal confirmed the optimizer blocker |
| RAI attachment / generated red teaming | No approved dedicated RAI policy or separate generated-attack scope; an instruction-following refusal is not a platform block |
| Recurring monitoring / CI release | No extra recurring-budget/pause agreement or role-changing release dispatch approval; exact-commit CI passed, but a new CI deployment was not run |
| Fabric, Work IQ, private networking, specialist features | Design/prerequisite review only; no missing external assets or company data invented |
| Additional optional UI/SDK alternatives | Not every alternative command or editor UI was repeated; use the per-guide matrix, not a blanket claim |

## Improvements made during the actual run

1. **Unambiguous workflow price:** A's hotel price now says **per person per night** in both languages.
   The original model correctly made its answer conditional; that response remains, and the clarified question was re-run successfully in both languages.
2. **Stable evaluator selection:** the portal now auto-selects five Quality evaluators, including **OutputQuality**.
   Labs 07 and 09 now say to keep **only Relevance and Coherence** before the optional TaskAdherence addition. Both portal evaluations used this corrected selection.
3. **Read the real OpenAPI error:** the guide now explains nested HTTP 400/403 permission failures and preserves the service error before considering another paid attempt.

Insights also exposed limitations beyond the small rubric: an English historical answer omitted the receipt condition,
and a D06 price without explicit nightly units was interpreted as nightly.
These are retained **review findings**, not reasons to edit frozen questions, scores, prompts or an exposed holdout retroactively.
No automatic prompt promotion or claimed universal correctness follows from the 6/6 rubric result.

## Cleanup and handoff

All three CLI-tested remote Hosted sessions were stopped and their state read back as **idle**.
Both owned memory stores, Code Interpreter resources, one-shot routines, the blocked English Toolbox and the disabled Insights monitor were cleaned up.
Original response/error/ownership records remain. Local test servers were stopped.

Hosted agent versions, browser/SDK/A2A agents, A2A connections, evaluation datasets/results and owned Search objects are retained for review.
The requested-account resource owner remains responsible for eventual removal and residual costs.
Shared Foundry/Search/Application Insights resources were not deleted; idle sessions can retain storage costs.
This is not a zero-cost or permanent-erasure claim.

The two independent local handoffs preserve all core JSON files, assessment CSVs, saved instructions, run labels, acceptance decisions and these limitations.
The original source commit's [three GitHub check jobs passed](https://github.com/junwoojeong100/microsoft-foundry-labs-v1.2/actions/runs/36237749226);
that does not prove CI has run for the later local documentation fixes. Local tests must be run on the corrected working tree.
No new commit, push, role assignment or publishing action was performed as part of this audit.

Return to [coverage](../coverage.md), [validation](validation.md), or [your learning route](../paths.md).
