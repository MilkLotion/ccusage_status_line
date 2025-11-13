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
                # Extract tokens, percentage, and cost from the line
                # Format: │ ... │ ACTIVE │ ... │ 1,787,726 │ 8.2% │ $1.43 │
                parts = [p.strip() for p in line.split('│') if p.strip()]

                if len(parts) >= 6:
                    # Expected format: [block_start, duration, models, tokens, percentage, cost]
                    tokens = parts[3]  # 4th column (0-indexed)
                    percentage = parts[4]  # 5th column
                    cost = parts[5]  # 6th column

                    return {
                        'tokens': tokens,
                        'percentage': percentage,
                        'cost': cost
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

    return f"🔥 {data['tokens']} tokens ({data['percentage']}) | 💰 {data['cost']}"

if __name__ == "__main__":
    data = parse_active_block()
    print(format_statusline(data))
