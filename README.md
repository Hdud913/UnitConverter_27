# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

**브랜치:** `red` · PR [#2](https://github.com/Hdud913/UnitConverter_27/pull/2)  
**추적:** [`TRACEABILITY.md`](TRACEABILITY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)  
**배경:** Mom Test · [`Report/01.REPORT.md`](Report/01.REPORT.md) · [`Report/03.WORKBOOK.md`](Report/03.WORKBOOK.md)  
**진행 보고:** [`Report/04.REPORT.md`](Report/04.REPORT.md) (spec) · [`Report/05.REPORT.md`](Report/05.REPORT.md) (RED)

---

## 주제

meter로 된 거리를 feet로 쓸 때마다 환산 상수를 다시 찾고, 판단·계산·문서 입력에 **회당 약 1분, 월 20회** 반복되는 문제를 줄인다.

---

## 개요

- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 **Dual-Track TDD** (`tests/`)로 검증한다.

**현재 단계:** **RED** — `pytest.fail("RED: …")` 스켈레톤 9건 작성 완료 · 구현(`unit_converter/`) **미착수**

---

## 입력 형식

```
meter:2.5
```

- `단위:값` — 콜론(`:`)으로 구분
- 단위명: 소문자 ASCII (예: `meter`, `feet`, `yard`)
- **음수** · **콜론 없음** · **빈 입력** · **미지원 단위** → 거부 (Track A TC)

---

## 기본 단위

| 단위 | 설명 |
|------|------|
| `meter` | 기준 단위 |
| `feet` | |
| `yard` | |

---

## 변환 비율

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- **feet ↔ yard** 변환은 **meter 경유** (직접 비율 하드코딩 없음)

---

## Dual-Track TDD (RED)

| Track | 파일 | Test ID | 상태 |
|-------|------|---------|------|
| **A — Boundary** | [`tests/test_cli.py`](tests/test_cli.py) | U-IN-01, U-IN-02, U-IN-03, U-OUT-01 | RED (4) |
| **B — Domain** | [`tests/test_converter.py`](tests/test_converter.py) | D-CNV-01 ~ 03, D-REG-01, D-CFG-01 | RED (5) |

```bash
pytest tests/ -v
# 기대: 9 failed — Failed: RED: <Test ID> — 구현 없음
```

**Cursor:** `/tdd-red` · `/tdd-green` · [`.cursor/skills/unit-converter-tdd/SKILL.md`](.cursor/skills/unit-converter-tdd/SKILL.md)

---

## 품질 요구사항 (P0)

| 항목 | 내용 |
|------|------|
| **OCP** | 새 단위 추가 시 기존 `Converter` 코드 수정 없음 |
| **SRP** | Parser / Registry / Converter / Formatter 분리 |
| **입력 검증** | 음수 · 잘못된 형식 · 미지원 단위 거부 |

---

## 추가 요구사항 (P1)

| # | 요구 | 설명 | RED Test ID |
|---|------|------|-------------|
| ① | **설정 외부화** | `units.json` 또는 YAML에서 비율 로드 | D-CFG-01 |
| ② | **동적 등록** | `1 cubit = 0.4572 meter` 등록 후 즉시 변환 가능 | D-REG-01 |
| ③ | **출력 포맷** | `--format json \| csv \| table` | (GREEN 이후) |

---

## 실행

```bash
# 가상환경
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 현재 (레거시 CLI)
python UnitConverter.py

# 목표 (GREEN 이후)
python -m unit_converter "meter:2.5"
```

### 예상 출력 (GREEN 기준)

```
2.5 meter = 8.20210 feet
2.5 meter = 2.73403 yard
```

> `2.5 × 3.28084 = 8.2021` (feet **5자리** TC: D-CNV-02) · meter 경유 yard

---

## Mom Test 성공 기준

| # | 기준 | RED 대응 |
|---|------|----------|
| 1 | 비율 구글링 없이 입력 한 번 | U-OUT-01, D-CNV-02 |
| 2 | 3.28084 단일 출처·재판단 없음 | D-CNV-01 ~ 03 |
| 3 | 1회 1분 미만 | U-OUT-01 (CLI E2E) |
| 4 | 단순 워크플로 | U-IN-* 입력 검증 |

상세: [`Report/01.REPORT.md`](Report/01.REPORT.md)

---

## 가상환경 비활성화

```bash
deactivate
```
