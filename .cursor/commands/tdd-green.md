# TDD GREEN — 통과하는 최소 구현

## 필수 선언

Phase: green | Layer: [entity/boundary] | Track: [Logic/UI]

## 절차

1. RED 테스트 FAIL 상태 재확인
2. `pytest.fail()` 제거 → 실제 assert로 교체
3. 최소 구현만 작성 (하드코딩·매직넘버 금지)
4. pytest 실행 → PASS 확인
5. git commit (1 RED 묶음 = 1 커밋)

## 금지

- 이번 RED 묶음 외 ID 동시 해결
- REFACTOR 진입
- assert 완화
