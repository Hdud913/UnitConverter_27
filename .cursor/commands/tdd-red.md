# TDD RED — 실패 테스트 먼저

## 필수 선언

Phase: red | Layer: [entity/boundary] | Track: [Logic/UI]

## 절차

1. TRACEABILITY.md에서 Test ID 확인
2. AAA 패턴으로 테스트 작성 (Given/When/Then)
3. Then은 `pytest.fail("RED: [ID] — 구현 없음")` 한 줄만
4. pytest 실행 → FAIL 확인

## 금지

- src/ 구현 코드 작성
- skip / xfail / assert 완화
- 1 RED 묶음 외 ID 동시 처리
