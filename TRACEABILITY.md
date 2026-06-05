# TRACEABILITY — C2C 추적표

**프로젝트:** UnitConverter_27  
**브랜치:** `spec`  
**연계:** [`README.md`](README.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

| ID | 요구 | Given | Then | P | 테스트 (목표) |
|----|------|-------|------|---|---------------|
| FR-01 | `meter:2.5` 파싱 | 유효 문자열 `"meter:2.5"` | `value=2.5`, `unit=meter` | P0 | `test_cli.py` / `test_input_parser.py` |
| FR-02 | 전 단위 출력 | `meter` 2.5 | `feet≈8.2021`, `yard≈2.7340` | P0 | `test_converter.py` |
| FR-03 | 미지 단위 | `cubit:1` (미등록) | 명확한 오류 메시지 | P0 | `test_cli.py` |
| FR-04 | 음수 | `meter:-1` | 거부 / 예외 | P0 | `test_input_parser.py` |
| FR-05 | 잘못된 형식 | `meter` / `abc` | 형식 오류 메시지 | P0 | `test_input_parser.py` |
| NFR-01 | OCP | `inch` 단위 추가 | 기존 `Converter` 코드 비수정 | P0 | `test_converter.py` + 구조 리뷰 |
| NFR-02 | SRP | — | Parser / Registry / Converter / Printer 분리 | P0 | `ARCHITECTURE.md` 대조 |
| EXT-01 | 설정 파일 | `units.json` (또는 YAML) | 비율 로드 후 변환 | P1 | `test_config_loader.py` |
| EXT-02 | 동적 등록 | `1 cubit = 0.4572 meter` | 등록 직후 변환 가능 | P1 | `test_unit_registry.py` |
| EXT-03 | 출력 포맷 | `--format json \| csv \| table` | 포맷별 출력 검증 | P1 | `test_cli.py` |

---

## 우선순위

| 우선순위 | 범위 | ID |
|----------|------|-----|
| **P0** | 기본 기능 · 품질 · 입력 검증 | FR-01 ~ FR-05, NFR-01, NFR-02 |
| **P1** | 설정 · 동적 등록 · 출력 포맷 | EXT-01 ~ EXT-03 |

---

## C2C 매핑 (Concept → Code)

| ID | 모듈 (목표) | Track |
|----|-------------|-------|
| FR-01, FR-04, FR-05 | `app/input_parser.py` | A (Boundary) |
| FR-02 | `domain/converter.py`, `domain/unit_registry.py` | B (Domain) |
| FR-03 | `domain/unit_registry.py`, `cli.py` | A + B |
| NFR-01 | `domain/length_unit.py`, `domain/unit_registry.py` | B |
| NFR-02 | `app/`, `domain/`, `infrastructure/` 패키지 분리 | — |
| EXT-01 | `infrastructure/config_loader.py` | B |
| EXT-02 | `domain/unit_registry.py` | B |
| EXT-03 | `app/output_formatter.py`, `cli.py` | A |
