# 기록 작성 가이드

## 폴더 규칙

한 Day의 문서와 이미지는 `docs/day-XX/`에 모읍니다.
실습 코드는 같은 번호의 `src/day_XX/`에 둡니다.

```text
docs/day-02/
├── index.md
└── figures/
    └── result.png

src/day_02/
└── experiment.py
```

문서에서 이미지는 `![실습 결과](figures/result.png)`처럼 상대 경로로 연결합니다.
공유할 그림은 해당 Day의 `figures/`에 저장하고,
임시 실험 결과는 Git에서 제외되는 루트 `outputs/`에 저장합니다.

## 새 기록 만들기

```bash
mkdir -p docs/day-02 src/day_02
cp templates/day.md docs/day-02/index.md
```

템플릿의 Day 번호와 제목을 수정하고, 실습 파일을 추가합니다.
`mkdocs.yml`의 `nav`에 다음 항목을 기존 Day와 같은 들여쓰기로 추가합니다.

```yaml
nav:
  - 홈: index.md
  - 학습 기록:
      - Day 01: day-01/index.md
      - Day 02: day-02/index.md
  - 기록 작성 가이드: guide.md
```

홈의 학습 기록 표에도 링크를 추가합니다.
사이트에서 실습 파일을 연결할 때는 GitHub의 코드 URL을 사용합니다.
`src/`는 문서 사이트에 포함되지 않으므로 `../../src/...` 링크는 사용하지 않습니다.

## 문서 형식

각 기록은 **오늘의 질문 → 핵심 개념 → 실습 → 결과 해석 → 남은 질문** 순서로 작성합니다.
직접 관찰한 결과, 그 결과를 인과적으로 해석하기 위한 가정, 아직 이해하지 못한 점을 구분합니다.
참고한 책·논문·강의의 링크와 읽은 범위도 기록합니다.

수식은 인라인 `$Y(1)$` 또는 블록 `$$ ... $$` 문법으로 작성합니다.
코드는 언어를 지정한 코드 블록으로 작성합니다.

## 확인하고 올리기

```bash
uv run mkdocs serve
uv run mkdocs build --strict
uv run ruff check src
uv run ruff format --check src
```

추가한 Python 실습도 직접 실행한 뒤 커밋합니다.
GitHub Pages 설정을 마치면 `main`에 push할 때 사이트가 갱신됩니다.
