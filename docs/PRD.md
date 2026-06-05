# UnitConverter PRD

**프로젝트:** UnitConverter_27  
**연계:** [`README.md`](../README.md) · [`TRACEABILITY.md`](../TRACEABILITY.md) · [`ARCHITECTURE.md`](../ARCHITECTURE.md)  
**근거:** Mom Test · [`Report/01.REPORT.md`](../Report/01.REPORT.md)

---

## §1 배경 & 목적

### 진짜 문제 (한 문장)

meter로 된 거리를 feet로 쓸 때마다 **환산 상수를 다시 찾고**, **어느 숫자가 맞는지 스스로 판단한 뒤** 계산기로 곱해 문서에 넣는 과정이 **귀찮아** **변환을 포기하고 대충 넘긴 적**도 있으며, 변환을 할 때는 **회당 약 1분**이 들고 **한 달에 약 20번** 반복된다.

### 해결하려는 pain point

| Pain | Mom Test 증거 | 제품 목표 |
|------|---------------|-----------|
| 비율 **매번 구글링** | “지난번에 meter를 feet로 바꿀 때 비율을 매번 구글링했다.” | 입력 한 번으로 변환 결과 확보 |
| **3.28084 vs 3.281** 재판단 | “1미터가 몇 feet인지 정확한 숫자가 헷갈렸다.” | 비율 **단일 출처(SSOT)** — 코드·설정·TC만 신뢰 |
| **시간 소모** (회당 ~1분, 월 ~20회) | “20번 정도, 검색 포함 1분 정도 걸렸다.” | 구글·계산기 없이 **1회 1분 미만** |
| **귀찮아서 포기·대충 넘김** | “아예 변환을 포기하고 대충 넘긴 적이 있다.” | `단위:값` → 출력 → 문서 복사 **단순 워크플로** |

> **표면 문제가 아닌 것:** “단위 변환 프로그램을 만든다” 자체가 목적이 아니다. **상수 재검색·판단·수동 곱셈·문서 반복**에 쓰이는 시간·불확실성을 줄이는 것이 목적이다.

---

## §2 사용자 & 페르소나

### 대상 사용자

**길이 단위 변환을 반복적으로 다루는 개발자** — 회의록 등 **문서**에 meter 기반 거리를 feet(및 yard)로 기록해야 하는 사람.

### 사용 시나리오

1. 회의록에 `2.5 meter`로 기록된 거리를 feet로 바꿔 동일 문서에 붙여 넣어야 한다.
2. 터미널에서 `meter:2.5` 형식으로 입력한다.
3. 프로그램이 **지원 단위 전부**에 대한 변환 결과를 출력한다.
4. 출력 문자열을 **그대로 복사**해 문서에 붙인다.
5. (P1) 필요 시 `units.json`에서 비율을 관리하거나, `cubit` 같은 단위를 **동적으로 등록**한다.
6. (P1) `--format json|csv|table`로 출력 형식을 선택한다.

**현재 지원 단위 (P0):** `meter` (기준), `feet`, `yard`

---

## §3 기능 요구사항 (FR)

**우선순위: P0** — 기본 기능·입력 검증

### FR-01 — `unit:value` 파싱

| 항목 | 내용 |
|------|------|
| **입력** | 유효 문자열 `"meter:2.5"` |
| **출력** | `unit = "meter"`, `value = 2.5` (float) |
| **검증** | 콜론(`:`)으로 단위명과 숫자 분리 |

### FR-02 — 전 단위 변환 출력

| 항목 | 내용 |
|------|------|
| **입력** | `unit = "meter"`, `value = 2.5` |
| **출력** | 등록된 **모든 단위**에 대한 변환 결과 (예: feet ≈ `8.20210`, yard ≈ `2.7340`) |
| **형식** | `{value} {source_unit} = {converted} {target_unit}` (table 기본) |
| **예시** | `2.5 meter = 8.20210 feet` · `2.5 meter = 2.73403 yard` |

### FR-03 — 미지 단위 거부

| 항목 | 내용 |
|------|------|
| **입력** | `"cubit:1"` (미등록 단위) |
| **출력** | **명확한 오류 메시지** (예: `Unknown unit: cubit`); 변환 결과 없음 |
| **조건** | registry에 등록되지 않은 단위명 |

### FR-04 — 음수 거부

| 항목 | 내용 |
|------|------|
| **입력** | `"meter:-1"` |
| **출력** | 거부 / 예외 (`ParseError` 등); 변환 결과 없음 |

### FR-05 — 잘못된 형식 거부

| 항목 | 내용 |
|------|------|
| **입력** | `""` (빈 입력), `"meter"` (콜론 없음), `"abc"` (비정상 형식) |
| **출력** | **형식 오류 메시지** (예: `Invalid format. Use unit:value (ex: meter:2.5)`); 변환 결과 없음 |

---

## §4 비기능 요구사항 (NFR)

**우선순위: P0** — 설계 품질

### NFR-01 — OCP (Open-Closed Principle)

| 항목 | 내용 |
|------|------|
| **요구** | 새 단위 추가 시 기존 **`Converter` · `ConvertUseCase` 코드 수정 없음** |
| **방법** | `LengthUnit` 구현 + `UnitRegistry.register()` |
| **검증** | `inch` 등 신규 단위 추가 후 기존 TC 비파괴 (D-REG-01) |

### NFR-02 — SRP (Single Responsibility Principle)

| 항목 | 내용 |
|------|------|
| **요구** | **Entity · Control · Boundary · Infrastructure** 4축 분리 |
| **축** | Entity(변환·등록) · Control(유스케이스 조율) · Boundary(파싱·포맷) · Infrastructure(설정 로드) |
| **검증** | [`ARCHITECTURE.md`](../ARCHITECTURE.md) ECB 구조 대조 |

---

## §5 추가 요구사항 (P1)

**우선순위: P1** — 설정·확장·출력

### EXT-01 — 설정 파일 로드

| 항목 | 내용 |
|------|------|
| **요구** | 변환 비율을 **`units.json` 또는 YAML**에서 로드 |
| **입력** | 설정 파일 경로 |
| **출력** | 파싱된 비율 dict; 깨진 JSON → `ConfigError` |
| **Test ID** | D-CFG-01 |

### EXT-02 — 동적 단위 등록

| 항목 | 내용 |
|------|------|
| **요구** | `1 cubit = 0.4572 meter` 등 **런타임 등록** 후 즉시 변환 가능 |
| **입력** | `unit_name`, `meters_per_unit` (예: `"cubit"`, `0.4572`) |
| **출력** | `convert_all("cubit", 1)["meter"] ≈ 0.4572` |
| **Test ID** | D-REG-01 |

### EXT-03 — 출력 포맷 선택

| 항목 | 내용 |
|------|------|
| **요구** | CLI `--format json \| csv \| table` |
| **입력** | 변환 결과 dict + format 옵션 |
| **출력** | 포맷별 직렬화 문자열 (json / csv / table) |
| **Test ID** | (GREEN 이후 확장) |

---

## §6 변환 비율 (단일 출처 SSOT)

모든 변환·TC·설정은 아래 상수 **한 곳**에서만 정의한다. `3.281`, `3.28` 등 **근사값 혼용 금지**.

| 관계 | 값 |
|------|-----|
| meter → feet | **1 meter = 3.28084 feet** |
| meter → yard | **1 meter = 1.09361 yard** |
| feet ↔ yard | **meter 경유만** (`feet → meter → yard`); feet↔yard **직접 비율 하드코딩 금지** |

**참조 계산 (TC 고정값):**

| 변환 | 계산 | TC 기대값 |
|------|------|-----------|
| 1 feet → meter | `1 / 3.28084` | `0.3048` (ε = 1e-4) |
| 2.5 m → feet | `2.5 × 3.28084` | `"8.20210"` (5자리) |

**저장 위치:** `units.json` / YAML (EXT-01) 또는 Entity `LengthUnit` 정의.

---

## §7 입력 검증 규칙

| 규칙 | 설명 | 관련 FR | Test ID |
|------|------|---------|---------|
| **형식** | `unit:value` — 콜론(`:`)으로 단위명·숫자 구분 | FR-01, FR-05 | U-IN-01, U-IN-02 |
| **빈 입력** | `""` → 형식 오류 | FR-05 | U-IN-01 |
| **콜론 없음** | `"meter"` → 형식 오류 | FR-05 | U-IN-02 |
| **음수 거부** | `value < 0` → 거부 | FR-04 | U-IN-03 |
| **미지 단위** | registry 미등록 단위 → 명확한 오류 | FR-03 | (GREEN 확장) |
| **잘못된 숫자** | `meter:abc` → 숫자 파싱 오류 | FR-05 | (GREEN 확장) |

**검증 책임:** Boundary `input_parser.py` (ECB — I/O 검증은 Boundary만).

---

## §8 C2C 추적표

Concept → Code → Test ID 매핑 ([`TRACEABILITY.md`](../TRACEABILITY.md) 기반, ECB 경로 반영)

### FR / NFR / EXT → Test ID

| ID | 요구 (Given → Then) | P | Test ID | 테스트 파일 |
|----|---------------------|---|---------|-------------|
| **FR-01** | `"meter:2.5"` → `unit=meter`, `value=2.5` | P0 | U-OUT-01 | `tests/boundary/test_u_out_01.py` |
| **FR-02** | `meter` 2.5 → feet ≈ `8.20210`, yard ≈ `2.7340` | P0 | D-CNV-01, D-CNV-02, D-CNV-03, U-OUT-01 | `tests/entity/test_d_cnv_*.py`, `tests/boundary/test_u_out_01.py` |
| **FR-03** | `cubit:1` (미등록) → 명확한 오류 | P0 | *(GREEN 확장)* | — |
| **FR-04** | `meter:-1` → 거부 | P0 | U-IN-03 | `tests/boundary/test_u_in_03.py` |
| **FR-05** | `""` / `meter` / `abc` → 형식 오류 | P0 | U-IN-01, U-IN-02 | `tests/boundary/test_u_in_01.py`, `test_u_in_02.py` |
| **NFR-01** | `inch` 추가 → Converter 비수정 | P0 | D-REG-01, D-CNV-* | `tests/entity/test_d_reg_01.py` 등 |
| **NFR-02** | ECB 4계층 분리 | P0 | — | `ARCHITECTURE.md` 대조 |
| **EXT-01** | 깨진 JSON → `ConfigError` | P1 | D-CFG-01 | `tests/entity/test_d_cfg_01.py` |
| **EXT-02** | cubit 0.4572 등록 → 변환 가능 | P1 | D-REG-01 | `tests/entity/test_d_reg_01.py` |
| **EXT-03** | `--format json\|csv\|table` | P1 | *(GREEN 이후)* | — |

### FR / NFR / EXT → ECB 모듈

| ID | ECB 모듈 | Track |
|----|----------|-------|
| FR-01, FR-04, FR-05 | `boundary/input_parser.py` | A (Boundary) |
| FR-02 | `entity/converter.py`, `entity/unit_registry.py` | B (Entity) |
| FR-03 | `entity/unit_registry.py`, `control/convert_use_case.py`, `cli.py` | A + B |
| NFR-01 | `entity/length_unit.py`, `entity/unit_registry.py` | B |
| NFR-02 | `entity/`, `control/`, `boundary/`, `infrastructure/` | — |
| EXT-01 | `infrastructure/config_loader.py` | B |
| EXT-02 | `entity/unit_registry.py` | B |
| EXT-03 | `boundary/output_formatter.py`, `cli.py` | A |

### Dual-Track Test ID 전체

| Track | Layer | Test ID | 파일 |
|-------|-------|---------|------|
| **B — Entity** | entity | D-CNV-01 | `tests/entity/test_d_cnv_01.py` |
| **B — Entity** | entity | D-CNV-02 | `tests/entity/test_d_cnv_02.py` |
| **B — Entity** | entity | D-CNV-03 | `tests/entity/test_d_cnv_03.py` |
| **B — Entity** | entity | D-REG-01 | `tests/entity/test_d_reg_01.py` |
| **B — Entity** | infrastructure | D-CFG-01 | `tests/entity/test_d_cfg_01.py` |
| **A — Boundary** | boundary | U-IN-01 | `tests/boundary/test_u_in_01.py` |
| **A — Boundary** | boundary | U-IN-02 | `tests/boundary/test_u_in_02.py` |
| **A — Boundary** | boundary | U-IN-03 | `tests/boundary/test_u_in_03.py` |
| **A — Boundary** | boundary | U-OUT-01 | `tests/boundary/test_u_out_01.py` |

### Mom Test 성공 기준 ↔ Test ID

| # | 성공 기준 | Test ID |
|---|-----------|---------|
| 1 | 비율 구글링 없이 입력 한 번 | U-OUT-01, D-CNV-02 |
| 2 | 3.28084 단일 출처·재판단 없음 | D-CNV-01 ~ 03 |
| 3 | 1회 1분 미만 | U-OUT-01 |
| 4 | 단순 워크플로 (입력→출력→복사) | U-IN-* |
