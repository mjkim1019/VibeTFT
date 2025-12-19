# Task Master MCP 설정 가이드

## 개요

**Task Master MCP**는 AI 기반 작업 관리 시스템으로, PRD(제품 요구사항 명세서)를 실행 가능한 작업으로 변환하고 개발 워크플로우를 관리합니다.

## 설정 완료 내용

프로젝트에 Task Master MCP가 다음과 같이 설정되었습니다:

### 설정 파일: `.claude.json`

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai@latest"],
      "env": {
        "TASK_MASTER_TOOLS": "core"
      }
    }
  }
}
```

### 주요 설정 사항

- **도구 모드**: `core` (최소 필수 도구 - 컨텍스트 효율성 최적화)
- **실행 방식**: `npx`를 통한 최신 버전 자동 실행
- **범위**: 프로젝트 레벨 (이 프로젝트에만 적용)

## 주요 기능

### 1. PRD를 작업으로 변환
- `docs/PRD.md`를 분석하여 구조화된 작업 목록 생성
- 작업 간 의존성 관리
- 우선순위 자동 설정

### 2. 작업 계층 관리
- 상위 작업(Epic) → 하위 작업(Story) → 세부 작업(Task) 구조
- 진행 상황 추적
- 완료율 자동 계산

### 3. 리서치 통합
- 프로젝트 컨텍스트를 고려한 최신 베스트 프랙티스 검색
- 기술 스택 관련 정보 자동 수집

### 4. 멀티 모델 지원
- Claude, OpenAI, Google Gemini, Perplexity 등 지원
- Claude Code와 원활한 통합

## 사용 방법

### Task Master 초기화

Claude Code에서 다음과 같이 요청:

```
task-master를 사용하여 docs/PRD.md를 작업 목록으로 변환해줘
```

### 작업 생성 및 관리

```
새로운 작업 생성: "데이터 크롤링 모듈 구현"
```

```
현재 진행 중인 작업 보여줘
```

```
작업 "RAG 파이프라인 구축" 완료로 표시
```

### 리서치 수행

```
ChromaDB를 사용한 벡터 검색 최적화 방법 리서치
```

```
Streamlit 오디오 입력 처리 베스트 프랙티스 조사
```

## VibeTFT Navigator 프로젝트 적용 예시

### 1. Phase 1 작업 분해

```
PRD의 Phase 1을 세부 작업으로 분해해줘:
- lolchess.gg 크롤링 스크립트
- JSON/Markdown 변환
- ChromaDB 임베딩
```

### 2. 기술 스택 리서치

```
task-master로 다음 항목 리서치:
1. BeautifulSoup4 vs Selenium 성능 비교
2. Streamlit 모바일 최적화 방법
3. OpenAI Whisper API 한국어 정확도 개선
```

### 3. 진행 상황 추적

```
현재 완료된 작업과 남은 작업 요약해줘
```

## 환경 변수 옵션

`TASK_MASTER_TOOLS` 환경 변수로 도구 세트 조정 가능:

| 값 | 설명 | 용도 |
|---|------|------|
| `core` | 최소 필수 도구 | 컨텍스트 효율성 우선 (권장) |
| `standard` | 표준 도구 세트 | 균형잡힌 기능 |
| `all` | 전체 기능 세트 | 최대 기능 활용 |
| `lean` | 경량 모드 | 빠른 응답 우선 |

현재는 `core` 모드로 설정되어 있으며, 필요시 `.claude.json`에서 변경 가능합니다.

## 요구사항

### 필수 사항
- **Node.js**: `npx` 실행을 위해 필요
- **Claude Code**: task-master와의 통합을 위해 필요

### 선택 사항
- API 키: Claude Code 사용 시 별도 API 키 불필요 (구독에 포함)

## 문제 해결

### MCP 서버가 연결되지 않는 경우

1. Node.js 설치 확인:
   ```bash
   node --version
   npm --version
   ```

2. `.claude.json` 파일 권한 확인:
   ```bash
   ls -la .claude.json
   ```

3. Claude Code 재시작

### 도구가 너무 많아 응답이 느린 경우

`.claude.json`에서 `TASK_MASTER_TOOLS`를 `core`로 변경:
```json
"env": {
  "TASK_MASTER_TOOLS": "core"
}
```

## 참고 자료

- [공식 GitHub 저장소](https://github.com/eyaltoledano/claude-task-master)
- [Task Master MCP 서버 문서](https://playbooks.com/mcp/eyaltoledano-task-master)
- [Claude Code MCP 가이드](https://code.claude.com/docs/en/mcp)

## 다음 단계

1. ✅ Task Master MCP 설정 완료
2. 📝 `docs/PRD.md`를 task-master로 분석
3. 🎯 Phase 1 작업 목록 생성
4. 🚀 개발 시작

---

**작성일**: 2025-12-18
**버전**: 1.0
**상태**: 설정 완료
