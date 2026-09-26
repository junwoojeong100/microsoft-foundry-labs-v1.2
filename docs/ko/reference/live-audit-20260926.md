# 실제 배포와 가이드 점검 — 2026-09-26

[English](../../reference/live-audit-20260926.md) | **한국어**

**영어·한국어를 독립적으로 실행해 실제 Azure 배포와 기본 A/B 경로를 확인했습니다.**
언어별 Lab·확장 문서 29개와 심화 워크북 2개에 각각 점검 상태를 남겼습니다.
**모든 선택 기능을 성공적으로 실행했다는 뜻은 아닙니다.** 필요한 권한, 지원되지 않는 기능, 설계 전용 범위를 그대로 표시합니다.

근거: [62개 문서별 점검표](../../assets/live-guide-audit-20260926/guide-checks.json) ·
[응답·평가·배포/정리 기록과 원본 해시](../../assets/live-guide-audit-20260926/results.json).
지정 계정으로 AI 도우미가 수행한 점검이며, 독립적인 초보자 시범 운영이나 사람의 업무 승인이 아닙니다.
새 영상은 녹화하지 않았습니다.

## 범위와 환경

Azure CLI·azd·브라우저에서 지정 계정을 각각 확인했습니다.
Sweden Central 실습 프로젝트 `mfv2-g6luna-20260923`의 현재 `gpt-6-sol` / `2026-09-22`,
별도 `gpt-6-sol-judge`, 기존 Search와 Application Insights를 사용했습니다.
리소스의 과거 이름이 남아 있다고 모델을 Luna로 바꾼 것은 아닙니다.

기준 소스 커밋은 `a48c3a633e1e1a6ccbc529a1b9ebcdde652558f5`입니다.
영문·국문은 서로 다른 소스 복사본·`.env`·실행 폴더·소유권 기록을 사용했습니다.
원래 저장소의 과거 `.env`·`azure.yaml`을 다른 대상으로 바꾸거나 기본 Azure 구독을 변경하지 않았습니다.
역할을 추가하지 않았고 회사/Microsoft 365 데이터·외부 웹 검색·새 모델 배포·인프라 프로비저닝도 사용하지 않았습니다.
브라우저 인증은 사용자가 완료했으며 SDK 인증과 브라우저 인증을 같다고 가정하지 않았습니다.

| 배포 대상 | 버전 | 실제 실행 |
|---|---|---|
| `mfv2-live260926-en-hosted` | `1` | 영어 단일 agent 로컬 Responses 확인 → 코드 직접 배포 → 원격 응답 |
| `mfv2-live260926-ko-hosted` | `1` | 독립적인 한국어 로컬 확인 → 코드 직접 배포 → 원격 응답 |
| `mfv2-live260926-en-workflow` | `1` | 순차 workflow-as-agent 로컬 확인 → 코드 직접 배포 → 모델 호출 3건을 포함한 원격 응답 |

각 배포는 독립 azd 폴더, 기존 프로젝트 연결, Python 3.13, `1 CPU / 2Gi`를 사용했습니다.
원격 호출 전에 `show`로 새 버전의 active 상태를 확인했습니다.
Docker 빌드·다른 모델로 대체·소스 저장소의 과거 서비스 배포는 필요하지 않았습니다.
패키지 manifest의 `cloud_deployed: false`는 원래 패키징 시점의 기록이므로 배포 후에도 바꾸지 않았습니다.

## 결과와 확인 범위

| 확인 | 영어 | 한국어 | 해석의 한계 |
|---|---|---|---|
| 오프라인 v1/v2 체험 | 0/6 → 6/6, 오류 0 | 0/6 → 6/6, 오류 0 | 고정 fixture이며 프롬프트 품질 개선이 아님 |
| B dev baseline / candidate | 6/6 / 6/6, 오류 0 | 6/6 / 6/6, 오류 0 | 고정된 로컬 검색 실험. 같은 점수로 우월성 주장 금지 |
| B 최종 holdout | 4/4, 오류 0 | 4/4, 오류 0 | 각 언어의 dev 조건 확인 후 한 번만 수집. 미공개 검증이 아닌 공개 교육 데이터 |
| B 인수 | `ready-for-human-review` | `ready-for-human-review` | `deployment_approved: false`. 사람의 운영 승인 아님 |
| A 저장된 인라인 agent | 버전 2, 사전 확인 4건·새 평가 답변 6개 | 별도 버전 2, 사전 확인 4건·새 평가 답변 6개 | 실제 저장 지침과 각 언어 학습자 파일 일치. AI 보조 기준 검토이며 학습자 시범 운영 아님 |
| Native candidate | Groundedness 6/6, relevance 5/6 | Groundedness 6/6, relevance 5/6 | 낮은 점수도 업무 검사와 별도로 보존 |
| MAF 함수 도구 평가 | 도구 정확도 6/6, relevance 6/6, 오류 0 | 도구 정확도 6/6, relevance 6/6, 오류 0 | 새 평가의 실제 도구 호출 기록. SDK는 평가자 버전이 고정되지 않았다고 보고 |
| 포털 데이터 세트 평가 | Relevance 6/6, coherence 6/6, TaskAdherence 0/6 | Relevance 5/6, coherence 6/6, TaskAdherence 0/6 | 정확한 브라우저 agent v2와 질문 전용 자료. 평가자 원본 행 전부 보존 |
| 사용자 정의 업무 평가자 | Baseline/candidate 일치 6/6씩. Groundedness 6/6·relevance 5/6씩 | 반복하지 않음 | 같은 평가 그룹과 고정된 업무 rubric이며 국문 결과가 아님 |
| 대화 평가 | 턴: 두 지표 각각 6/6, 대화: 각각 2/2 | 독립적으로 같은 수치 | 실제 6턴·이력 2개. Groundedness/coherence의 평가 단위가 다름 |

두 언어 모두 무도구·함수·MCP, MAF 세 패턴, 본인 일반 Search·GA IQ 검색, 새 IQ 기반 답변을 실행했습니다.
Search와 IQ가 반환한 문서 집합은 달랐으며 같다고 기록하지 않았습니다.
별도 영어 hybrid 분기는 새 소유 인덱스와 실제 3072차원 임베딩으로 검색·답변까지 실행했습니다.
원래 텍스트 인덱스를 바꾸거나 실패한 IQ를 대신하는 경로로 쓰지 않았습니다.

### 추적 연결

| 대상 | 확인된 trace | 확인 내용 |
|---|---|---|
| 영어 브라우저 agent v2 | `9daaa842155e46c3917f64cfca2dce74` | 저장한 D01 응답, `invoke_agent`와 하위 `chat` |
| 한국어 브라우저 agent v2 | `70e9ed12aa634bb28e32bf45aad34082` | 독립 국문 D01 응답·버전 일치 |
| 영어 SDK agent v1 | `298b0d8974008b864e19c5e52c603d25` | 정확한 `response_id`, 입력 1124 / 출력 108 토큰 |
| 한국어 SDK agent v1 | `aa499b28e352f15af558819a9d5df794` | 정확한 `response_id`, 입력 1290 / 출력 135 토큰 |
| 영문 / 국문 Hosted 단일 agent | `c58c700677a171e1947cc90ba6fae7ac` / `6c6038ab79b14ae2bf5643ef9f336a96` | 원격 호출이 반환한 ID. 새 포털 상관 분석까지 주장하지 않음 |
| 영어 Hosted workflow | `1a521ecc076e15306ce8f50d178477e7` | 원격 trace context와 실제 모델 호출 3건. Export 상태는 원래 보고값 유지 |

Trace 화면을 채우려고 모델을 다시 호출하지 않았습니다.
직접 호출·로컬 MAF 응답 기록을 서버 측 trace로 바꾸어 표시하지 않았습니다.

<a id="advanced-modules-preserve-successes-and-blockers"></a>

## 심화 모듈: 성공과 차단을 함께 보존

**두 언어에서 확인:** A2A 대상·카드·keyless 연결·relay와 실제 1.0 위임,
관리형 Memory 생성·저장·검색·변경·삭제·정리,
원래 정책 ID·제목 6행이 정확히 들어 있는 Code Interpreter 다운로드 CSV,
그리고 routine 수동 실행 한 번과 비활성화·삭제입니다.
Routine은 전달이 확인됐지만 **저장된 답변과 미래 timer 실행은 미확인**입니다. 취소된 timer 시도도 기록에 남깁니다.

**영어에서만 추가 확인:** 배포한 Responses workflow, hybrid RAG, 사용자 정의 업무 평가 비교, SDK Insights 한 번입니다.
Insights는 trace 17개를 분석해 judge 토큰 158,439개를 사용했고 발견 사항 2개를 반환했습니다.
Monitor는 계속 비활성 상태였으며 결과 저장 후 삭제했습니다.
로컬 SDK 승인 gate 연습도 완료했지만 고정 영어 D03 작업이며 **Azure·모델 호출이 없고** `human_authorization: not-granted`입니다.
국문 복구 가이드도 같은 고정 영어 시뮬레이션을 설명하며 별도 국문 모델 실험은 아닙니다.

| 차단 또는 미실행 | 실제 이유 |
|---|---|
| File Search | `gpt-6-sol`의 파일 업로드 비활성화. 영문 tooltip에 일시적으로 사용할 수 없다고 명시 |
| Native Toolbox → Search | 본인 Toolbox 생성·탐색 성공, 직접 검색은 Access denied. 프로젝트 identity에 Search Index Data Reader만 있음. 추가 범위 역할 승인을 요청했으나 받지 못해 권한 변경하지 않음 |
| Tool Search/Skills·Hosted Toolbox | 성공한 native 도구 검색이 선행 조건. 다른 provider로 우회하지 않음 |
| OpenAPI | HTTP 400 `tool_user_error` 내부에 실제 Search HTTP 403. 오류 원본 보존, 대체 응답 없음 |
| IQ Chat | 해당 계정에 별도 지원 모델 `gpt-5.6-luna`와 Search outbound identity 준비가 없음 |
| Hosted IQ/Invocations matrix | 별도 런타임 Search 권한과 matrix 선행 조건이 승인·준비되지 않음. 기본 Responses 점수 전용 금지 |
| Agent Optimizer·모델 교체·Router | 지원 optimizer나 별도로 승인된 두 번째 응답 모델/Router가 없음. 포털에서 optimizer 차단 확인 |
| RAI 연결·생성형 red teaming | 승인된 전용 RAI 정책이나 별도 생성 공격 범위가 없음. 지침을 따른 거절은 플랫폼 차단과 다름 |
| 되풀이 관측·CI 릴리스 | 추가 반복 비용·중지 시각 합의나 역할을 부여하는 릴리스 실행 승인이 없음. 기준 커밋 CI는 통과했지만 새 CI 배포는 실행하지 않음 |
| Fabric·Work IQ·사설망·전문 기능 | 설계·선행 조건 검토만 수행. 없는 외부 자산이나 회사 데이터 생성 금지 |
| 추가 선택 UI/SDK 방식 | 모든 대안 명령·편집기 UI를 반복한 것은 아님. 일괄 성공 대신 문서별 점검표 사용 |

## 실제 실행 중 개선한 내용

1. **명확한 workflow 가격 단위:** A의 호텔 가격을 두 언어 모두 **1인 1박**으로 고쳤습니다.
   원래 모델이 타당하게 조건부 답변한 결과는 보존하고, 명확해진 질문을 두 언어로 재실행했습니다.
2. **안정적인 평가자 선택:** 포털이 **OutputQuality**를 포함한 품질 평가자 다섯 개를 자동 선택합니다.
   Lab 07·09는 선택 TaskAdherence를 추가하기 전에 **Relevance·Coherence만** 남기도록 고쳤고 두 포털 평가에 적용했습니다.
3. **실제 OpenAPI 오류 읽기:** 중첩된 HTTP 400/403 권한 오류를 설명하고 다시 유료 요청하기 전에 원본 서비스 오류를 보존하도록 했습니다.

Insights는 작은 rubric 밖의 한계도 찾았습니다. 영어 과거 숙박 답변의 영수증 조건 누락,
명시적인 1박 단위가 없는 D06 가격을 1박 가격으로 해석한 문제입니다.
이는 보존할 **검토 사항**이며 고정 질문·점수·지침·이미 공개된 holdout을 소급 수정할 이유가 아닙니다.
Rubric 6/6만으로 자동 지침 승격이나 보편적인 정확성을 주장하지 않습니다.

## 정리와 인계

CLI로 확인한 원격 Hosted 세션 세 개를 모두 중지하고 **idle** 상태를 다시 읽었습니다.
본인 Memory store 두 개, Code Interpreter 자원, 일회성 routine, 차단된 영어 Toolbox, 비활성 Insights monitor를 정리했습니다.
원래 응답·오류·소유권 기록은 보존했고 로컬 테스트 서버는 종료했습니다.

검토를 위해 Hosted 버전, 브라우저·SDK·A2A agent, A2A 연결, 평가 자료·결과, 본인 Search 객체는 남겼습니다.
최종 삭제와 남은 비용은 지정 계정의 리소스 소유자가 관리합니다.
공유 Foundry·Search·Application Insights를 지우지 않았으며 idle 세션에는 저장 비용이 남을 수 있습니다.
비용 0이나 영구적인 모든 데이터 삭제를 주장하지 않습니다.

각 언어의 독립 인계 자료에는 기본 JSON 전체, 평가 CSV, 저장 지침, label, 인수 결과와 이 한계가 들어 있습니다.
기준 커밋의 [GitHub 검사 job 세 개는 통과](https://github.com/junwoojeong100/microsoft-foundry-v2-labs/actions/runs/36237749226)했지만,
그 후 로컬에서 고친 문서까지 CI가 실행됐다는 뜻은 아닙니다. 수정한 작업 트리의 로컬 검사는 별도로 해야 합니다.
이번 점검에서 새 커밋·push·역할 부여·게시를 수행하지 않았습니다.

[기능 범위](../coverage.md), [검증](validation.md), [학습 경로](../paths.md)로 돌아갑니다.
