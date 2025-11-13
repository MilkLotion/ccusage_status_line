# ccusage Status Line for Claude Code

Custom status line for Claude Code that displays active block information from ccusage.

Claude Code의 활성 블록 정보를 표시하는 커스텀 상태줄입니다.

## Features / 기능

- ⏰ **Time Tracking**: Block start/end time, elapsed and remaining time
- 🔥 **Token Usage**: Token count and percentage
- 🟢🟠🔴 **Usage Alerts**: Color-coded indicators (green/orange/red)
- 💰 **Cost**: Real-time cost tracking

## Prerequisites / 필수 요구사항

- Python 3.6+
- Claude Code

## Installation / 설치

Clone the repository:

```bash
git clone https://github.com/MilkLotion/ccusage_status_line.git
cd ccusage_status_line
```

Copy `statusline.py` to your `.claude` directory:

```bash
# Linux/Mac
cp statusline.py ~/.claude/

# Windows (PowerShell)
Copy-Item statusline.py "$env:USERPROFILE\.claude\"
```

## Configuration / 설정

Add to your Claude Code settings file (`~/.claude/settings.json`):

```json
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.claude/statusline.py",
    "padding": 0
  }
}
```

**Windows**: Use `python C:\\Users\\<username>\\.claude\\statusline.py`

Restart Claude Code to apply changes.

## Output Format / 출력 형식

```
🟢  2025-11-14 12:00 AM ~ 5:00 AM | ⏱️ 1h 1m | ⏳ 3h 59m | 🔥 7,275,167 tokens (33.4%) | 💰 $4.60
```

- 🟢/🟠/🔴 Usage indicator (≤60% / 60-80% / >80%)
- Date and time range (start ~ end)
- ⏱️ Elapsed time
- ⏳ Remaining time (5 hours total)
- 🔥 Token count with percentage
- 💰 Cost

## License

MIT License
