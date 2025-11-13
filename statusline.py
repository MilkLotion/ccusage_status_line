#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Custom StatusLine Generator
Generates custom statusline output based on context
"""
import subprocess
import re
import sys
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def remove_ansi_codes(text):
    """Remove ANSI color codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_time_info(block_start_str):
    """Parse time information from block start string"""
    # Format: "2025-11-14, 12:00:00 a.m. (0h 52m" or "2025-11-14, 12:00:00 a.m. (0h 43m elapsed, 4h 17m remaining)"
    try:
        # Extract start time
        time_match = re.search(r'(\d{1,2}):(\d{2}):(\d{2})\s+(a\.m\.|p\.m\.)', block_start_str)
        if not time_match:
            return None

        hour = int(time_match.group(1))
        minute = time_match.group(2)
        period = time_match.group(4)

        # Convert to 24-hour format for calculation
        if period == 'p.m.' and hour != 12:
            hour_24 = hour + 12
        elif period == 'a.m.' and hour == 12:
            hour_24 = 0
        else:
            hour_24 = hour

        # Calculate end time (start + 5 hours for Claude's 5-hour block)
        end_hour_24 = (hour_24 + 5) % 24

        # Format times
        start_time = f"{hour}:{minute} {period.replace('.', '').upper()}"

        # Format end time
        end_hour = end_hour_24 if end_hour_24 <= 12 else end_hour_24 - 12
        if end_hour == 0:
            end_hour = 12
        end_period = 'AM' if end_hour_24 < 12 else 'PM'
        end_time = f"{end_hour}:{minute} {end_period}"

        # Extract elapsed time - try different patterns
        elapsed = None
        # Pattern 1: "0h 43m elapsed"
        elapsed_match = re.search(r'(\d+h\s+\d+m)\s+elapsed', block_start_str)
        if elapsed_match:
            elapsed = elapsed_match.group(1)
        else:
            # Pattern 2: "(0h 52m" - just the time in parentheses
            elapsed_match = re.search(r'\((\d+h\s+\d+m)', block_start_str)
            if elapsed_match:
                elapsed = elapsed_match.group(1)

        # Extract remaining time
        remaining = None
        remaining_match = re.search(r'(\d+h\s+\d+m)\s+remaining', block_start_str)
        if remaining_match:
            remaining = remaining_match.group(1)
        elif elapsed:
            # Calculate remaining time (5h total - elapsed)
            elapsed_match = re.match(r'(\d+)h\s+(\d+)m', elapsed)
            if elapsed_match:
                elapsed_hours = int(elapsed_match.group(1))
                elapsed_minutes = int(elapsed_match.group(2))

                total_minutes = 5 * 60  # 5 hours
                elapsed_total_minutes = elapsed_hours * 60 + elapsed_minutes
                remaining_minutes = total_minutes - elapsed_total_minutes

                remaining_hours = remaining_minutes // 60
                remaining_mins = remaining_minutes % 60
                remaining = f"{remaining_hours}h {remaining_mins}m"

        return {
            'start_time': start_time,
            'end_time': end_time,
            'elapsed': elapsed or 'N/A',
            'remaining': remaining or 'N/A'
        }
    except Exception:
        return None

def parse_active_block():
    """Parse ccusage blocks output and extract ACTIVE block info"""
    try:
        # Run ccusage blocks command
        result = subprocess.run(
            'npx ccusage@latest blocks',
            capture_output=True,
            text=True,
            timeout=10,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            return None

        # Remove ANSI codes
        output = remove_ansi_codes(result.stdout)

        # Find ACTIVE line
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if 'ACTIVE' in line:
                # Extract all information from the line
                # Format: │ 2025-11-14, 12:00:00 a.m. (0h 43m elapsed, 4h 17m remaining) │ ACTIVE │ - haiku-4-5 │ 1,787,726 │ 8.2% │ $1.43 │
                parts = [p.strip() for p in line.split('│') if p.strip()]

                if len(parts) >= 6:
                    # Expected format: [block_start, duration, models, tokens, percentage, cost]
                    block_start = parts[0]  # Time info
                    tokens = parts[3]  # 4th column (0-indexed)
                    percentage = parts[4]  # 5th column
                    cost = parts[5]  # 6th column

                    # Parse time information
                    time_info = parse_time_info(block_start)

                    return {
                        'tokens': tokens,
                        'percentage': percentage,
                        'cost': cost,
                        'time_info': time_info
                    }

        return None

    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def format_statusline(data):
    """Format data for statusline display"""
    if not data:
        return "⚠️ No active block"

    time_info = data.get('time_info')

    if time_info:
        # Format: 시작 ~ 종료 | Elapsed 시간 | Remaining 시간 | 토큰 | 달러
        return (f"{time_info['start_time']} ~ {time_info['end_time']} | "
                f"⏱️ {time_info['elapsed']} | ⏳ {time_info['remaining']} | "
                f"🔥 {data['tokens']} tokens | 💰 {data['cost']}")
    else:
        # Fallback format if time info is not available
        return f"🔥 {data['tokens']} tokens ({data['percentage']}) | 💰 {data['cost']}"

if __name__ == "__main__":
    data = parse_active_block()
    print(format_statusline(data))
