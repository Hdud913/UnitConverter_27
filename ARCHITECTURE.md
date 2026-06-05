# ARCHITECTURE — 목표 패키지 구조

**프로젝트:** UnitConverter_27  
**브랜치:** `spec`  
**연계:** [`README.md`](README.md) · [`TRACEABILITY.md`](TRACEABILITY.md)

---

## 디렉터리 구조

```
unit_converter/
├─ domain/
│   ├─ length_unit.py      # Protocol: name, to_meter()
│   ├─ unit_registry.py    # 등록·조회 (OCP 핵심)
│   └─ converter.py        # meter 값 → 전 단위 (SRP)
├─ infrastructure/
│   └─ config_loader.py    # JSON / YAML
├─ app/
│   ├─ input_parser.py     # "unit:value" 파싱
│   └─ output_formatter.py # json | csv | table
├─ cli.py
└─ tests/
    ├─ test_converter.py   # Domain (Track B)
    └─ test_cli.py         # Boundary (Track A)
```

---

## 레이어별 책임

| 레이어 | 모듈 | 책임 |
|--------|------|------|
| **domain** | `length_unit.py` | 단위 추상화 — `name`, `to_meter(value)` |
| **domain** | `unit_registry.py` | 단위 등록·조회; 동적 등록(EXT-02) |
| **domain** | `converter.py` | 기준 meter 환산 후 전 단위 변환 (FR-02) |
| **infrastructure** | `config_loader.py` | `units.json` / YAML 로드 (EXT-01) |
| **app** | `input_parser.py` | `meter:2.5` 파싱·검증 (FR-01, FR-04, FR-05) |
| **app** | `output_formatter.py` | `--format` 처리 (EXT-03) |
| **entry** | `cli.py` | argv 조립, 오류 처리, stdout |

---

## OCP 원칙

**새 단위 추가 = `LengthUnit` 구현 + `registry.register()`**

기존 `Converter` 코드는 수정하지 않는다.

```text
[새 단위 inch]
  1. LengthUnit 구현 (to_meter 정의)
  2. unit_registry.register(inch_unit)
  3. Converter / Parser 변경 없음  ← NFR-01
```

---

## SRP 원칙

**변환 ≠ 파싱 ≠ 출력 ≠ 설정 로드**

| 모듈 | 하지 않는 것 |
|------|----------------|
| `input_parser.py` | 변환 계산, 파일 I/O |
| `converter.py` | 문자열 파싱, 포맷 출력 |
| `output_formatter.py` | 비율 계산, 단위 등록 |
| `config_loader.py` | CLI, 변환 로직 |
| `unit_registry.py` | 입출력 포맷 |

Parser · Registry · Converter · Formatter **4개 축**으로 분리 (NFR-02).

---

## 데이터 흐름

```text
CLI argv "meter:2.5"
  → input_parser     → (unit, value)
  → unit_registry    → LengthUnit 조회
  → converter        → meter 기준값 → 전 단위 결과
  → output_formatter → table | json | csv
  → stdout
```

**설정 로드 (시작 시):**

```text
config_loader → units.json/YAML → unit_registry.register(...)
```

---

## 테스트 트랙

| Track | 범위 | 파일 |
|-------|------|------|
| **A — Boundary** | CLI, 파싱, 포맷, 오류 메시지 | `tests/test_cli.py` |
| **B — Domain** | 변환 정확도, OCP, registry | `tests/test_converter.py` |

P1 항목 추가 시: `test_config_loader.py`, `test_unit_registry.py` 확장.
