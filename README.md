# ccusage Status Line for Claude Code

Claude Code의 활성 블록 정보를 표시하는 커스텀 상태줄입니다.  
해당 코드는 Claude Pro 요금제를 사용하는 기준으로 작성되었습니다.

## Features / 기능

- ⏰ **Time Tracking**: 세션블록의 시작시간, 종료시간, 사용시간, 남은시간을 출력
- 🔥 **Token Usage**: 사용 토큰 수와 퍼센트수치를 표기
- 🟢🟠🔴 **Usage Alerts**: 토큰사용량 별 경고 인디케이터 (green/orange/red)
- 💰 **Cost**: 실시간 사용 비용

## Prerequisites / 필수 요구사항

- Python 3.6+
- Claude Code

## Installation / 설치

### 1. Repository 복사

```bash
git clone https://github.com/MilkLotion/ccusage_status_line.git
cd ccusage_status_line
```

### 2. `statusline.py`를 `.claude` 디렉토리로 복사/이동

#### Windows (PowerShell)

```bash
Copy-Item statusline.py "$env:USERPROFILE\.claude\"
```

#### Linux/Mac

```bash
cp statusline.py ~/.claude/
```

## Configuration / 설정

Claude Code settings 파일에 추가 (`~/.claude/settings.json`):

### Windows

```json
{
  "statusLine": {
    "type": "command",
    "command": "python C:\\Users\\<username>\\.claude\\statusline.py",
    "padding": 0
  }
}
```

### Linux/Mac

```json
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.claude/statusline.py",
    "padding": 0
  }
}
```

Claude Code를 재시작 하고 동작 시에 해당 출력을 확인할 수 있습니다.

## Output Format / 출력 형식

```
Session Block Info  🟢  2025-11-14 12:00 AM ~ 5:00 AM | ⏱️ 1h 1m | ⏳ 3h 59m | 🔥 7,275,167 tokens (33.4%) | 💰 $4.60
```

- 🟢/🟠/🔴 사용량 인디케이터 (≤60% / 60-80% / >80%)
- 시작시간 ~ 종료시간
- ⏱️ 사용시간
- ⏳ 남은시간(총 5 시간)
- 🔥 토큰 사용량 (% 수치)
- 💰 사용 코스트

## License

MIT License
