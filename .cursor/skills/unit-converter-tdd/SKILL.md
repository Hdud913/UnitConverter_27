---
name: unit-converter-tdd
description: UnitConverter Dual-Track TDD 개발 시 Agent가 따를 절차
---

# UnitConverter Dual-Track TDD

## 언제 사용

- RED / GREEN / REFACTOR 단계를 진행할 때
- `TRACEABILITY.md`의 Test ID를 구현·검증할 때
- `/tdd-red`, `/tdd-green` Command와 함께 작업할 때

**연계:** [`.cursor/rules/tdd-rules.mdc`](../../rules/tdd-rules.mdc) · [`TRACEABILITY.md`](../../../TRACEABILITY.md) · [`ARCHITECTURE.md`](../../../ARCHITECTURE.md)

---

## Dual-Track 구분

| Track | Layer | 파일 | 범위 |
|-------|-------|------|------|
| **A — UI/Boundary** | boundary | `tests/test_cli.py` | 입력 검증, CLI 오류, 출력 형식 (`--format`) |
| **B — Domain/Logic** | entity | `tests/test_converter.py` | 변환 비율, `UnitRegistry`, OCP |

- Test ID → Track 매핑은 `TRACEABILITY.md` C2C 표를 따른다.
- **1 RED 묶음 = 1 Test ID (또는 동일 시나리오 묶음) = 1 커밋**

---

## RED 절차

**선언:** `Phase: red | Layer: [entity/boundary] | Track: [Logic/UI]`

1. `TRACEABILITY.md`에서 **Test ID** 확인
2. **AAA** 패턴으로 테스트 작성 (Given / When / Then)
3. Then은 `pytest.fail("RED: [ID] — 구현 없음")` **한 줄만**
4. `pytest` 실행 → **FAIL** 확인

**금지**

- `unit_converter/` 구현 코드 작성
- skip / xfail / assert 완화
- 1 RED 묶음 외 ID 동시 처리

→ 상세: [`.cursor/commands/tdd-red.md`](../../commands/tdd-red.md)

---

## GREEN 절차

**선언:** `Phase: green | Layer: [entity/boundary] | Track: [Logic/UI]`

1. RED 테스트 **FAIL** 상태 재확인
2. `pytest.fail()` 제거 → **실제 assert**로 교체
3. **최소 구현**만 작성 (하드코딩·매직넘버 금지; 비율은 단일 출처)
4. `pytest` 실행 → **PASS** 확인
5. `git commit` (1 RED 묶음 = 1 커밋)

**금지**

- 이번 RED 묶음 외 ID 동시 해결
- REFACTOR 진입
- assert 완화

→ 상세: [`.cursor/commands/tdd-green.md`](../../commands/tdd-green.md)

---

## REFACTOR 절차

**선언:** `Phase: refactor | Layer: [entity/boundary] | Track: [Logic/UI]`

1. **Golden Master** 확보 — 현재 전체 테스트 PASS 스냅샷
2. **스멜 탐지** — OCP/SRP 위반, 중복 비율, 레이어 침범
3. **Safe Refactor** — 동작 변경 없이 구조만 개선
4. `pytest` **전체** 실행 → PASS 유지 확인
5. 필요 시 별도 커밋 (`refactor: ...`)

**원칙**

- `converter.py`는 새 단위 추가 시에도 수정하지 않음 (OCP)
- Parser / Registry / Converter / Formatter 분리 유지 (SRP)

---

## 금지 (전 단계 공통)

- **Domain Mock on Logic Track** — Track B에서 도메인 로직을 Mock으로 대체하지 않음
- **assert 완화** — 테스트 기준을 낮춰 PASS 만들지 않음
- **skip / xfail** — RED 우회 금지
- **근사 비율 혼용** — `3.281`, `3.28` 등 (`tdd-rules.mdc` 참조)

---

## 비율 단일 출처 (Domain Track)

```
1 meter = 3.28084 feet
1 meter = 1.09361 yard
feet ↔ yard → meter 경유만
```

예상값 (FR-02): `meter:2.5` → `feet≈8.2021`, `yard≈2.7340`
