# ARCHITECTURE — ECB 패키지 구조

**프로젝트:** UnitConverter_27  
**패턴:** Entity · Control · Boundary (ECB)  
**연계:** [`README.md`](README.md) · [`TRACEABILITY.md`](TRACEABILITY.md)

---

## ECB 개요

| 계층 | 역할 | import 제약 |
|------|------|-------------|
| **Entity** | 순수 도메인 로직 (단위, 변환, 등록) | `boundary` · `control` import **금지** |
| **Control** | 유스케이스 조율 (입력 → 변환 → 출력 흐름) | I/O 검증·UI 문자열 처리 **금지** |
| **Boundary** | 입출력 창구 (파싱, 포맷, CLI) | Domain **알고리즘** 구현 **금지** |

**Infrastructure**는 Entity를 지원하는 외부 설정 로드(`config_loader`)만 담당한다.

---

## 소스 구조

```
unit_converter/
├─ entity/                    # 순수 도메인 (boundary/control import 금지)
│   ├─ length_unit.py         # Protocol: name, to_meter()
│   ├─ unit_registry.py       # 등록·조회 (OCP 핵심)
│   └─ converter.py           # meter값 → 전 단위 (SRP)
├─ control/                   # 유스케이스 조율
│   └─ convert_use_case.py    # 입력 → 변환 → 출력 조율
├─ boundary/                  # 입출력 창구
│   ├─ input_parser.py        # "unit:value" 파싱·검증
│   └─ output_formatter.py    # json | csv | table 포맷
├─ infrastructure/
│   └─ config_loader.py       # JSON / YAML
└─ cli.py                     # entry — argv 조립, 오류 처리, stdout
```

---

## 테스트 구조

```
tests/
├─ entity/                    # Track B — Domain Mock 금지
│   ├─ test_d_cnv_01.py
│   ├─ test_d_cnv_02.py
│   ├─ test_d_cnv_03.py
│   ├─ test_d_reg_01.py
│   └─ test_d_cfg_01.py
└─ boundary/                  # Track A — Domain Mock 허용
    ├─ test_u_in_01.py
    ├─ test_u_in_02.py
    ├─ test_u_in_03.py
    └─ test_u_out_01.py
```

| Track | Layer | Mock 정책 | 범위 |
|-------|-------|-----------|------|
| **A — Boundary** | boundary | Domain Mock **허용** | CLI, 파싱, 포맷, 오류 메시지 |
| **B — Entity** | entity | Domain Mock **금지** | 변환 정확도, OCP, registry, 설정 로드 |

---

## ECB 레이어별 책임

| 계층 | 모듈 | 책임 | 하지 않는 것 |
|------|------|------|----------------|
| **Entity** | `length_unit.py` | 단위 추상화 — `name`, `to_meter(value)` | 파싱, 포맷, CLI, 파일 I/O |
| **Entity** | `unit_registry.py` | 단위 등록·조회; 동적 등록 (EXT-02) | 입출력 포맷, 유스케이스 조율 |
| **Entity** | `converter.py` | meter 기준값 → 전 단위 변환 (FR-02) | 문자열 파싱, stdout |
| **Control** | `convert_use_case.py` | `(unit, value)` → registry 조회 → convert → 결과 dict | 형식 검증, UI 문자열, `--format` |
| **Boundary** | `input_parser.py` | `meter:2.5` 파싱·검증 (FR-01, FR-04, FR-05) | 변환 계산, 비율 상수 |
| **Boundary** | `output_formatter.py` | `--format` table \| json \| csv (EXT-03) | 비율 계산, 단위 등록 |
| **Infrastructure** | `config_loader.py` | `units.json` / YAML 로드 (EXT-01) | CLI, 변환 로직 |
| **Entry** | `cli.py` | argv·stdin 조립, 예외 → 메시지, stdout | 변환 알고리즘, 파싱 규칙 |

---

## ECB 규칙 (의존 방향)

```text
boundary ──→ control ──→ entity
                ↑
infrastructure ─┘ (entity/registry 초기화 시)
```

| 계층 | 허용 | 금지 |
|------|------|------|
| **Entity** | entity 내부, infrastructure(설정 데이터만) | `boundary` · `control` import |
| **Control** | `entity`, `infrastructure` | I/O 검증, UI/오류 **문자열** 생성, stdout |
| **Boundary** | `control`, `entity`(조회·예외 타입만) | 변환 **알고리즘** 직접 구현 |

---

## OCP 원칙

**새 단위 추가 = `LengthUnit` 구현 + `registry.register()`**

기존 `Converter` · `ConvertUseCase` 코드는 수정하지 않는다.

```text
[새 단위 inch]
  1. LengthUnit 구현 (to_meter 정의)
  2. unit_registry.register(inch_unit)
  3. Converter / ConvertUseCase / Parser 변경 없음  ← NFR-01
```

---

## SRP 원칙

**Entity · Control · Boundary · Infrastructure 4축 분리** (NFR-02)

| 축 | 단일 책임 |
|----|-----------|
| Entity | 비율·변환·등록 |
| Control | 유스케이스 흐름 조율 |
| Boundary | 문자열 입출력 |
| Infrastructure | 설정 파일 로드 |

---

## 데이터 흐름

```text
CLI "meter:2.5"
  → boundary/input_parser     → (unit, value)
  → control/convert_use_case  → registry 조회 → converter → results
  → boundary/output_formatter → table | json | csv
  → cli.py                    → stdout
```

**설정 로드 (시작 시):**

```text
infrastructure/config_loader → units.json/YAML → entity/unit_registry.register(...)
```

---

## C2C 매핑 (Concept → ECB)

| ID | 모듈 (목표) | Track |
|----|-------------|-------|
| FR-01, FR-04, FR-05 | `boundary/input_parser.py` | A |
| FR-02 | `entity/converter.py`, `entity/unit_registry.py` | B |
| FR-03 | `entity/unit_registry.py`, `control/convert_use_case.py`, `cli.py` | A + B |
| NFR-01 | `entity/length_unit.py`, `entity/unit_registry.py` | B |
| NFR-02 | ECB 4계층 패키지 분리 | — |
| EXT-01 | `infrastructure/config_loader.py` | B |
| EXT-02 | `entity/unit_registry.py` | B |
| EXT-03 | `boundary/output_formatter.py`, `cli.py` | A |

---

## Test ID ↔ 파일

| Test ID | 테스트 파일 | 구현 (GREEN 목표) |
|---------|-------------|-------------------|
| D-CNV-01 | `tests/entity/test_d_cnv_01.py` | `entity/length_unit.py` |
| D-CNV-02 | `tests/entity/test_d_cnv_02.py` | `entity/converter.py` |
| D-CNV-03 | `tests/entity/test_d_cnv_03.py` | `entity/converter.py` |
| D-REG-01 | `tests/entity/test_d_reg_01.py` | `entity/unit_registry.py` |
| D-CFG-01 | `tests/entity/test_d_cfg_01.py` | `infrastructure/config_loader.py` |
| U-IN-01 | `tests/boundary/test_u_in_01.py` | `boundary/input_parser.py` |
| U-IN-02 | `tests/boundary/test_u_in_02.py` | `boundary/input_parser.py` |
| U-IN-03 | `tests/boundary/test_u_in_03.py` | `boundary/input_parser.py` |
| U-OUT-01 | `tests/boundary/test_u_out_01.py` | `boundary/output_formatter.py`, `control/convert_use_case.py`, `cli.py` |
