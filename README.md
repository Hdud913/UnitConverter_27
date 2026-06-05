# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

**브랜치:** `spec`  
**추적:** [`TRACEABILITY.md`](TRACEABILITY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)  
**배경:** Mom Test · [`Report/01.REPORT.md`](Report/01.REPORT.md) · [`Report/03.WORKBOOK.md`](Report/03.WORKBOOK.md)

---

## 주제

meter로 된 거리를 feet로 쓸 때마다 환산 상수를 다시 찾고, 판단·계산·문서 입력에 **회당 약 1분, 월 20회** 반복되는 문제를 줄인다.

---

## 개요

- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

---

## 입력 형식

```
meter:2.5
```

- `단위:값` — 콜론(`:`)으로 구분
- 단위명: 소문자 ASCII (예: `meter`, `feet`, `yard`)

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

## 품질 요구사항 (P0)

| 항목 | 내용 |
|------|------|
| **OCP** | 새 단위 추가 시 기존 변환기 코드 수정 없음 |
| **SRP** | Parser / Registry / Converter / Formatter 분리 |
| **입력 검증** | 음수 · 잘못된 형식 · 미지원 단위 거부 |

---

## 추가 요구사항 (P1)

| # | 요구 | 설명 |
|---|------|------|
| ① | **설정 외부화** | `units.json` 또는 YAML에서 비율 로드 |
| ② | **동적 등록** | `1 cubit = 0.4572 meter` 등록 후 즉시 변환 가능 |
| ③ | **출력 포맷** | `--format json \| csv \| table` |

---

## 실행 (목표)

```bash
# 가상환경
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

python -m unit_converter "meter:2.5"
```

### 예상 출력

```
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

> `2.5 × 3.28084 = 8.2021` · `2.5 × 1.09361 = 2.7340` (소수 4자리)

---

## 가상환경 비활성화

```bash
deactivate
```
