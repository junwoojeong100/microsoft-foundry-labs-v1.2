# 승인 후 차단 해소와 실제 결과 — 2026-09-27

[English](../../reference/approved-resume-20260927.md) | **한국어**

**승인된 권한·모델 선행 조건을 해결하고 이전에 막혔던 연동을 실제 Azure에서 실행했습니다.**
다만 **모든 품질 기준을 통과했다는 뜻은 아닙니다.** 영문 Hosted matrix는 최종 인용 검사 한 건으로 거절됐고,
국문 matrix는 native 결과 검토가 필요하며, Optimizer의 실제 근거 참조 연결은 무효였습니다.
점수를 좋게 만들려고 이 결과를 고치거나 재실행하지 않고 보존했습니다.

[새 근거·원본 해시·작업 기록](../../assets/approved-resume-20260927/results.json) ·
[62개 문서별 범위/상태](../../assets/approved-resume-20260927/guide-checks.json) ·
[앞선 9월 26일 기록](live-audit-20260926.md).
날짜는 한국 표준시이며 원래 서비스 타임스탬프는 UTC입니다. 이전 기록을 덮어쓰거나 새 근거로 바꾸지 않았습니다.

## 승인과 실제 변경

사용자가 남은 작업을 명시적으로 승인했습니다. Azure CLI·azd·열어 둔 브라우저에서 지정 계정을 확인했고,
기존 Sweden Central 프로젝트와 실습 Search 서비스를 재사용했습니다.
원래 주 응답 배포 `gpt-6-sol`, judge 배포, 기본 Azure 구독은 변경하지 않았습니다.
회사/Microsoft 365 데이터·API key·새 자격 증명·구독 전체 Owner 부여는 사용하지 않았습니다.

| 선행 조건 | 실제 변경 | 확인 |
|---|---|---|
| Native Toolbox → Search | **프로젝트** 관리 ID에 실습 Search 범위 **Search Service Contributor** 추가. Data Reader는 기존 역할 유지 | 실제 직접 도구 검색 후 모델·도구 답변 |
| 직접 OpenAPI → Search | **Foundry 계정** 관리 ID에 같은 서비스 범위 **Search Index Data Reader** 추가 | 두 언어의 `openapi_call`, 원문 문서와 실제 인자 확인 |
| IQ Chat 모델 | `gpt-5.6-luna` / `2026-07-09`, DataZoneStandard **30K TPM** 생성 | 정확한 모델·Search ID·별도 chat base·실제 계획과 합성 |
| Optimizer 모델 | `mfv2-live270927-opt-gpt55`: `gpt-5.5` / `2026-04-24`, DataZoneStandard **50K TPM** 생성 | 마법사에서 지원 모델 선택 및 제한된 실행 |
| Hosted Toolbox 호출자 | 실제 새 런타임 principal마다 프로젝트 범위 **Foundry User** | 원격 Skill 포함 Toolbox 실행과 근거 파일 다운로드 |
| Hosted matrix 호출자 | 실제 matrix 런타임마다 Search의 **Search Index Data Reader**, 계정의 **Cognitive Services OpenAI User** | 두 모델의 로컬·정확한 원격 버전 확인 |

새 모델은 `NoAutoUpgrade`·`Microsoft.DefaultV2`를 사용하며 spillover나 모델 fallback이 없습니다.
생성 전 할당량을 확인했습니다. 같은 계정의 하위 모델을 동시에 만들려던 첫 시도에서 `RequestConflict`가 발생해 보존했고,
부모 상태를 확인한 후 optimizer 모델을 순차 생성했습니다. 다른 모델·리전으로 바꾸지 않았습니다.
IQ Chat에 필요한 Search ID의 기존 **Cognitive Services User** 역할도 중복 생성하지 않았습니다.
새 역할의 정확한 assignment ID와 범위는 작업 기록에 있습니다.

**ID 구분이 핵심입니다.** Toolbox의 프로젝트 ID를 고쳐도 OpenAPI는 해결되지 않았습니다.
직접 OpenAPI 계약은 Foundry **계정** ID를 사용합니다. 잘못된 주체에 권한을 더 주는 것은 복구가 아닙니다.

## 재개한 연동

| 연동 | 영어 | 한국어 | 경계 |
|---|---|---|---|
| 일반 native Toolbox | 실제 검색·MAF 답변 | 독립 실제 검색·MAF 답변 | 본인 합성 문서 6개 인덱스만, key 없음 |
| Tool Search·버전 Skill | Toolbox v3, Skill v1 | Toolbox v2, Skill v1 | 업로드/다운로드 바이트 일치, 실제 `load_skill`·탐색·정책 호출 보존 |
| Hosted Toolbox | `mfv2-live260926-en-tb-r27:1` | `mfv2-live260926-ko-tb-r27:1` | 로컬·원격 실행, 패키지/응답 불변값 검사, 세션 근거 파일 8개씩 다운로드 |
| OpenAPI | 실제 읽기 전용 검색 성공 | 필수 인자 보완 후 실제 검색 성공 | native Search·IQ·Python 도구로 대체하지 않음 |
| IQ Chat | 별도 소유 영어 chat base | 별도 소유 국문 chat base | Search system identity, `low`, `answerSynthesis`, `2026-08-01-preview`; 실제 `modelQueryPlanning`·`modelAnswerSynthesis` |
| 직접 모델 비교 | 모델별 dev 6행, 6/6·6/6 | 독립 모델별 dev 6행, 6/6·6/6 | 같은 코드·prompt·local 검색, 원래 설정 복원, 모델 교체·holdout 사용 없음 |

IQ Chat은 150,000원 한도를 답하고 숫자 인용을 실제 정책 원문에 연결했습니다.
이 선택 지원 모델은 기존 GPT-6 주 응답 모델과 분리한 구성이지 오류 처리 중 바꾸는 fallback이 아닙니다.
원래 모델 없는 GA base를 chat base로 변환하지 않았습니다.

### OpenAPI 보완

국문 시도에서 별도의 오류 `Missing required query parameter: api-version`이 나타났습니다.
스키마는 이미 필수 인자로 선언했지만 기본값만으로 모델이 이를 보내지는 않았습니다.
Helper가 **`api-version=2024-07-01`**, `top=6`, 고정 select 필드를 명시하도록 보완하고 두 언어를 새 label로 확인했습니다.
실패한 원래 응답은 보존했습니다. 로컬 계획에도 계정 ID의 역할과 필요한 읽기 권한을 표시합니다.

지침·스키마 설명을 명확히 한 것이며 모든 모델이 영원히 인자를 빠뜨리지 않는다는 보장은 아닙니다.
서버의 검증과 명시적인 실패는 유지하며 오류 뒤 대체 응답을 만들지 않습니다.

## 실제 2-model Hosted matrix

각 언어는 독립 소스·소유 Search 객체·azd 폴더를 사용했습니다.
런타임은 **MAF 순차 workflow + GA IQ + 계정 Chat Completions + Invocations**입니다.
모델 key는 사전에 `a = gpt-6-sol`, `b = gpt-5.6-luna`로 고정했습니다.
Reranker filter `0`, concurrency `1`, 출력 한도 `2048`도 수집 전 고정했고,
baseline과 candidate 사이에는 prompt와 그에 대응하는 불변 agent 버전만 바뀌었습니다.

| 기준 | 영어 | 한국어 |
|---|---|---|
| Agent | `mfv2-r27-mx-en-agent`, v1 → v2 | `mfv2-r27-mx-ko-agent`, v1 → v2 |
| Dev baseline | 12/12, 오류 0 | 12/12, 오류 0 |
| Dev candidate | 12/12, 오류 0 | 12/12, 오류 0 |
| 근거 비교 | `changed_context_rows: []`, prompt만의 비교 | 독립적으로 같은 조건 확인 |
| Judge calibration | 올바른 분류 2/2 | 올바른 분류 2/2 |
| 최종 holdout 한 번 | **7/8**, 오류 0: `a` 3/4, `b` 4/4 | **8/8**, 오류 0: 둘 다 4/4 |
| 실제 root trace | 12/12 + 12/12 + 8/8 | 12/12 + 12/12 + 8/8 |
| 실행 gate | `true` | `true` |
| 전체 gate / 권고 | **`false` / `reject`** | **`true` / `review-native-findings`** |
| Native 품질 / 운영 승인 | `false` / `false` | `false` / `false` |

영문 `a-H04`는 사전 정의된 인용 관련성 검사에 실패했습니다. 이를 빼거나 회귀 개발 사례로 바꾸지 않았고,
holdout을 본 뒤 모델을 다시 고르지 않았습니다. 결과를 통과시키려 prompt·corpus·정답·기준도 바꾸지 않았습니다.
국문 native 결과에는 `b-H03`의 낮은 groundedness와 두 H04의 낮은 relevance가 남아 있습니다.
업무 검사가 통과했어도 검토해야 할 사항입니다.

인수 정책은 모든 native 점수 통과가 아니라 **완전하고 유효한 native 실행·trace 계보**를 요구하도록 사전에 정했습니다.
점수를 본 뒤 정책을 바꾼 것이 아닙니다. Calibration 두 건은 절차 확인이지 judge의 일반적인 정확성 보장이 아니며,
공개 holdout은 최종 인수 방식 교육용이지 보지 못한 운영 데이터 검증이 아닙니다.

## Optimizer: 실행 가능하지만 승격 승인 아님

전용 `mfv2-live260926-en-opt-r27:1`은 검증된 영어 브라우저 agent 정의를 정확히 복사했습니다.
원래 baseline은 고치지 않았습니다. **Instruction만**, 후보 최대 **2개**, 새 GPT-5.5 optimizer,
기존 GPT-6 target과 별도 GPT-6 judge를 선택했고 파생 dev 6행만 업로드했습니다.
운영 trace 자동 생성 자료나 holdout은 사용하지 않았습니다.

`opt_3fc7b69370214a46b549f112b6d07197`은 약 4분에 완료됐습니다.

- **Baseline만** 반환했고 점수는 **0.958**, 최적화 후보는 없었습니다.
- Target 35,900·judge 96,413·reflection 9,583 토큰을 보고했습니다.
- “No improvement”와 일반적인 만점 조기 중단 안내를 동시에 표시했습니다.
- 실제 baseline 평가는 6행이며 D05 relevance가 3점으로 설정 임계값 4에 실패했습니다.

`eval_f27db2883fde4d56818d9b3fd15b7a42` / `evalrun_44faa0f83cdf48e89797707930881df0`에서
실제 `results[].sample.input`을 내보냈습니다.
**Groundedness context 6개 모두 원래 corpus가 아니라 생성한 답변 자체였습니다.**
따라서 그 점수는 원문 grounding을 입증하지 못합니다.
`grounding_binding_valid: false`로 남기고 승격하지 않았습니다.
국문 전용 target은 준비했지만 공통 참조 연결 결함을 확인한 뒤 유리한 결과를 찾기 위한 두 번째 유료 실행은 하지 않았습니다.

새 [`export_evaluation.py`](../../../scripts/export_evaluation.py)는 단위 검사 후 실제 완료 평가에서도 실행했습니다.
전체 페이지와 실패 점수를 보존하고 예상·고유 행 수 및 선택적으로 실제 judge 입력을 검사합니다.
Target 재호출·기준 변경·품질 승인을 하지 않습니다.
[Optimizer 가이드](../labs/extensions/agent-optimizer.md#raw-judge-export)에 이제 실행 가능한 검토 절차가 있습니다.
이 도구는 결함을 확인하게 해 주며 서비스 내부 최적화를 수리했다고 주장하지 않습니다.

## 승인된 안전 제어와 CI 경로

**가드레일 적용:** 관찰한 기본 제어와 Blocking 모드로 전용 `mfv2-r27-default-guardrail` 정책을 만들고 다시 읽었습니다.
공유 기본 정책 정의는 바이트 단위로 동일했습니다.
영문·국문 Hosted Toolbox v2는 실제 정책의 전체 ARM ID를 참조합니다.
같은 D01·D06을 v1과 v2에서 실행했고 모두 완료됐으며 D06은 허위 승인을 계속 거절했습니다.
**플랫폼 차단은 관찰하지 못했습니다.** 정책 연결·차단되지 않은 요청·모델의 올바른 거절은 각각 다른 근거입니다.
재현을 위해 새 정책을 소유한 버전에 연결한 채 보관합니다.

**CI 릴리스:** 기존 OIDC identity와 보호된 environment로 분리된 릴리스 두 건을 실행했습니다.
[영어](https://github.com/junwoojeong100/microsoft-foundry-labs-v1.2/actions/runs/36272575801)와
[한국어](https://github.com/junwoojeong100/microsoft-foundry-labs-v1.2/actions/runs/36272833299)는
`mfv2-r27-ci-hosted` v1/v2를 배포하고 각각 **실제 dev 6/6·오류 0**, 런타임 역할과 idle 정리 근거를 보존했습니다.
Environment의 prefix·agent 이름만 임시 변경했고 원래 값을 복원·재확인했습니다.
Branch 보호·federation·client secret·로컬 기본 구독·다른 팀 agent는 변경하지 않았습니다.

CI는 이미 게시되고 검사된 **`a48c3a633e1e1a6ccbc529a1b9ebcdde652558f5`** 커밋을 사용했습니다.
이는 별도 근거이며 아직 커밋하지 않은 OpenAPI/exporter 수정까지 CI로 확인했다는 뜻이 아닙니다.
선택한 release 경로는 CI이며 새 반복 유료 관측 스케줄은 활성화하지 않았습니다.

## 정리·남긴 자원·한계

마지막 조회에서 **로컬 점검으로 만든 Hosted 세션 20개가 idle**임을 확인했습니다.
언어별 Toolbox·matrix에 각각 다섯 개이며 CI 세션 두 개도 idle 정리 근거가 있습니다.
주 Toolbox 세션은 중지 전 모델·도구·Skill 근거를 다운로드했고 로컬 서버는 종료했습니다.

명시적으로 승인된 범위 역할, 새 모델 두 개, 소유 chat base·Skill·Toolbox·agent 버전·평가 기록·전용 정책은
소유자가 가이드를 재현할 수 있게 남겼습니다.
공유 Foundry·Search·Insights를 삭제하지 않았으며 저장된 세션 파일과 공유 자원에는 비용이 남을 수 있습니다.
비용 0이나 영구적인 전체 데이터 삭제를 뜻하지 않습니다.

고정 GPT-6의 File Search, Router, 사설망, Fabric/Work IQ, 생성형 red teaming, 선택 편집기 설치를
성공한 실행으로 바꾸어 표시하지 않았습니다. 포괄적인 작업 승인도 회사/Microsoft 365 접근까지 실습 범위로 바꾸지 않습니다.
62개 문서별 표는 새로 확인한 범위와 이전 근거를 구분합니다.

런타임 소스는 기준 커밋과 기록한 OpenAPI 인자·ID 계획 보완이며, 해시는
`e786feac35b03e10e1e57e06bac40b3c5c9fa235f074e7a0977a7c1f0d9ce2fa`입니다.
고정 prompt·corpus·dev/holdout·의존성·원래 저장소의 과거 Azure 설정은 다시 쓰지 않았습니다.
작업 트리를 커밋하거나 push하지 않았습니다.

[검증](validation.md), [기능 범위](../coverage.md), [학습 경로](../paths.md)로 돌아갑니다.
