# Causal Inference Study

인과추론의 개념을 공부하고 Python으로 확인하는 학습 저장소입니다.
학습 정리는 `docs/`에 Day별로 모으고, 실습 코드는 `src/`에 둡니다.
문서는 MkDocs Material로 빌드하여 GitHub Pages에 배포합니다.

## 시작하기

[uv 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)에 따라 uv를 설치한 뒤,
저장소 루트에서 실행합니다. Python 버전은 `.python-version`의 3.12를 사용합니다.

```bash
uv sync --locked
uv run mkdocs serve
```

`uv sync`가 `.venv`를 만들고 실습·문서·개발 의존성을 설치합니다.
문서 미리보기는 <http://127.0.0.1:8000>에서 볼 수 있습니다.
`uv.lock`도 함께 커밋하여 동일한 의존성 버전을 사용합니다.

## 프로젝트 구조

```text
.
├── docs/
│   ├── index.md                   # 사이트 홈
│   ├── guide.md                   # 학습 기록 작성 방법
│   ├── day-01/
│   │   └── index.md               # 직접 작성할 Day 1 학습 기록
│   └── assets/javascripts/        # 수식 렌더링 설정
├── src/
│   └── day_01/
│       └── .gitkeep               # 실습 .py 파일을 추가할 폴더
├── templates/
│   └── day.md                    # 다음 Day 기록 템플릿
├── .github/workflows/pages.yml   # 문서 빌드 및 Pages 배포
├── .python-version
├── mkdocs.yml
├── pyproject.toml
└── uv.lock
```

문서 폴더는 `day-01`, Python 폴더는 `day_01`처럼 이름을 붙입니다.
기존 루트의 `main.py`는 초기 샘플이며 학습 실습은 `src/`에서 실행합니다.

## 다음 Day 추가하기

```bash
mkdir -p docs/day-02 src/day_02
cp templates/day.md docs/day-02/index.md
```

1. `docs/day-02/index.md`에 학습 내용을 정리합니다.
2. `src/day_02/`에 실습 `.py` 파일을 추가합니다.
3. `mkdocs.yml`의 `nav → 학습 기록`에 새 문서를 등록합니다.
4. 자세한 형식은 [기록 작성 가이드](docs/guide.md)를 참고합니다.

## 검증

```bash
uv run ruff check src
uv run ruff format --check src
uv run mkdocs build --strict
```

## GitHub Pages 배포

1. 변경 사항을 GitHub 저장소의 `main` 브랜치에 push합니다.
2. 저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 설정합니다.
3. **Actions → Build and deploy docs → Run workflow**에서 `main`을 선택해 첫 배포를 실행합니다.

이후 `main`에 push할 때마다 검증을 통과한 문서가 자동으로 배포됩니다.
Pull Request에서는 검증만 실행합니다.
배포 후 사이트 주소는 <https://karim-moon.github.io/Causal/>입니다.

참고: [uv의 GitHub Actions 가이드](https://docs.astral.sh/uv/guides/integration/github/),
[GitHub Pages 워크플로 가이드](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
