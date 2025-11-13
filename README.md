# ccusage Status Line for Claude Code

Custom status line for Claude Code that displays active block information from ccusage.

Claude Code의 활성 블록 정보를 표시하는 커스텀 상태줄입니다.

## Features / 기능

- 🔥 **Token Usage**: Display current active block token usage
- 📊 **Percentage**: Show percentage of token limit used
- 💰 **Cost**: Real-time cost tracking for active session
- ⚡ **Fast**: Optimized parsing for quick status updates

## Prerequisites / 필수 요구사항

- Python 3.6+
- Claude Code
- ccusage (`npm install -g ccusage` or use `npx ccusage@latest`)

## Installation / 설치

### 1. Clone or Download / 저장소 복제 또는 다운로드

```bash
git clone https://github.com/MilkLotion/ccusage_status_line.git
cd ccusage_status_line
```

Or download `statusline.py` directly to your `.claude` directory:
또는 `statusline.py`를 `.claude` 디렉토리에 직접 다운로드하세요:

```bash
# Linux/Mac
curl -o ~/.claude/statusline.py https://raw.githubusercontent.com/MilkLotion/ccusage_status_line/main/statusline.py

# Windows (PowerShell)
Invoke-WebRequest -Uri https://raw.githubusercontent.com/MilkLotion/ccusage_status_line/main/statusline.py -OutFile "$env:USERPROFILE\.claude\statusline.py"
```

### 2. Configure Claude Code / Claude Code 설정

Add the following to your Claude Code settings file:
Claude Code 설정 파일에 다음을 추가하세요:

**Linux/Mac**: `~/.claude/settings.json`
**Windows**: `C:\Users\<username>\.claude\settings.json`

```json
{
  "statusLine": {
    "type": "command",
    "command": "python /path/to/statusline.py",
    "padding": 0
  }
}
```

**Examples / 예시:**

```json
// Linux/Mac
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.claude/statusline.py",
    "padding": 0
  }
}

// Windows
{
  "statusLine": {
    "type": "command",
    "command": "python C:\\Users\\<username>\\.claude\\statusline.py",
    "padding": 0
  }
}
```

### 3. Restart Claude Code / Claude Code 재시작

Restart Claude Code to apply the changes.
변경사항을 적용하려면 Claude Code를 재시작하세요.

## Output Format / 출력 형식

```
12:00 AM ~ 5:00 AM | ⏱️ 0h 52m | ⏳ 4h 8m | 🔥 4,231,281 tokens | 💰 $2.84
```

- **[start time] ~ [end time]**: Active block time range / 활성 블록 시간 범위
- **⏱️ [elapsed]**: Elapsed time in current block / 현재 블록에서 경과한 시간
- **⏳ [remaining]**: Remaining time in current block / 현재 블록의 남은 시간
- **🔥 [tokens] tokens**: Total tokens used in active block / 활성 블록의 총 토큰 사용량
- **💰 [cost]**: Estimated cost for active block / 활성 블록의 예상 비용

When no active block is found:
활성 블록이 없을 때:

```
⚠️ No active block
```

## How It Works / 작동 원리

1. Runs `ccusage blocks` command / `ccusage blocks` 명령어 실행
2. Parses output to find ACTIVE block / 출력에서 ACTIVE 블록 찾기
3. Extracts time information (start, elapsed, remaining) / 시간 정보 추출 (시작, 경과, 남은 시간)
4. Extracts tokens and cost / 토큰 및 비용 추출
5. Formats and displays in status line / 상태줄에 포맷팅하여 표시

**Time Calculation / 시간 계산:**
- Block duration: 5 hours (Claude's billing block) / 블록 지속 시간: 5시간 (Claude의 빌링 블록)
- Remaining time = 5 hours - Elapsed time / 남은 시간 = 5시간 - 경과 시간

## Customization / 커스터마이징

You can customize the output format by editing the `format_statusline()` function in `statusline.py`:
`statusline.py`의 `format_statusline()` 함수를 편집하여 출력 형식을 커스터마이징할 수 있습니다:

```python
def format_statusline(data):
    """Format data for statusline display"""
    if not data:
        return "⚠️ No active block"

    time_info = data.get('time_info')

    if time_info:
        # Customize this format
        return (f"{time_info['start_time']} ~ {time_info['end_time']} | "
                f"⏱️ {time_info['elapsed']} | ⏳ {time_info['remaining']} | "
                f"🔥 {data['tokens']} tokens | 💰 {data['cost']}")
    else:
        # Fallback format if time info is not available
        return f"🔥 {data['tokens']} tokens ({data['percentage']}) | 💰 {data['cost']}"
```

**Available data fields / 사용 가능한 데이터 필드:**
- `time_info['start_time']`: Block start time / 블록 시작 시간
- `time_info['end_time']`: Block end time / 블록 종료 시간
- `time_info['elapsed']`: Elapsed time / 경과 시간
- `time_info['remaining']`: Remaining time / 남은 시간
- `data['tokens']`: Token count / 토큰 수
- `data['percentage']`: Usage percentage / 사용률
- `data['cost']`: Estimated cost / 예상 비용

## Troubleshooting / 문제 해결

### Status line not updating / 상태줄이 업데이트되지 않음

1. Check if Python is in your PATH / Python이 PATH에 있는지 확인
2. Verify the path to `statusline.py` is correct / `statusline.py` 경로가 올바른지 확인
3. Test the script manually: / 스크립트를 수동으로 테스트:
   ```bash
   python /path/to/statusline.py
   ```

### UnicodeEncodeError on Windows / Windows에서 UnicodeEncodeError 발생

The script includes UTF-8 encoding fixes for Windows. If you still encounter issues, ensure your terminal supports UTF-8:
스크립트에는 Windows용 UTF-8 인코딩 수정이 포함되어 있습니다. 여전히 문제가 발생하면 터미널이 UTF-8을 지원하는지 확인하세요:

```bash
chcp 65001
```

### ccusage command not found / ccusage 명령어를 찾을 수 없음

Install ccusage globally or use npx:
ccusage를 전역으로 설치하거나 npx를 사용하세요:

```bash
# Global installation
npm install -g ccusage

# Or the script will use npx automatically
# 또는 스크립트가 자동으로 npx를 사용합니다
```

## Performance / 성능

- **Execution time**: ~1-2 seconds (depends on ccusage response)
- **실행 시간**: ~1-2초 (ccusage 응답 속도에 따라 다름)
- **Cache**: ccusage uses offline cache for faster responses
- **캐시**: ccusage는 빠른 응답을 위해 오프라인 캐시 사용

## License / 라이선스

MIT License

## Credits / 크레딧

- Built for [Claude Code](https://claude.com/claude-code)
- Uses [ccusage](https://github.com/your-ccusage-repo) for token tracking

## Contributing / 기여

Contributions are welcome! Please feel free to submit a Pull Request.
기여를 환영합니다! Pull Request를 자유롭게 제출해주세요.

## Support / 지원

If you encounter any issues, please open an issue on GitHub.
문제가 발생하면 GitHub에서 이슈를 열어주세요.

---

**Made with ❤️ for Claude Code users**
