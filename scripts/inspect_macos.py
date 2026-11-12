#!/usr/bin/env python3
"""Read-only, local macOS inventory. No network probes or configuration writes."""

import json
import platform
import re
import subprocess
from pathlib import Path


def run(args):
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=10)
        return proc.returncode, proc.stdout
    except (OSError, subprocess.TimeoutExpired):
        return -1, ""


def selected_config(text):
    """Extract only scalar routing flags; never print credentials or whole YAML."""
    section = ""
    result = {}
    for line in text.splitlines():
        if line and not line[0].isspace() and not line.startswith("#"):
            section = line.split(":", 1)[0]
        match = re.fullmatch(r"(ipv6|mode):\s*(true|false|rule|global|direct)\s*", line)
        if match:
            result[match[1]] = match[2]
        match = re.fullmatch(r"  (ipv6|enable|auto-route|strict-route):\s*(true|false)\s*", line)
        if match and section in ("dns", "tun"):
            result[f"{section}.{match[1]}"] = match[2]
    return result


def parse_services(text):
    services = []
    for line in text.splitlines():
        line = line.strip()
        if not line or "denotes that a network service is disabled" in line:
            continue
        disabled = line.startswith("*")
        services.append((line[1:] if disabled else line, disabled))
    return services


def inspect():
    result = {"read_only": True, "platform": platform.system(), "errors": []}
    if platform.system() != "Darwin":
        result["errors"].append("This script requires macOS; no commands executed.")
        return result

    code, text = run(["/bin/ps", "-axo", "pid=,comm="])
    result["claude_processes"] = []
    result["node_cli_candidates"] = []
    result["mihomo_controller_socket"] = None
    if code:
        result["errors"].append("Process inventory unavailable; do not assume Claude exited.")
    else:
        for line in text.splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) != 2:
                continue
            pid, command = parts
            name = Path(command).name
            if "/Claude.app/" in command or name.lower() == "claude" or "Claude Helper" in name:
                result["claude_processes"].append({"pid": int(pid), "name": name})
            # Read arguments only for likely executables; never output their full arguments.
            if name in ("node", "bun"):
                _, args = run(["/bin/ps", "-p", pid, "-o", "args="])
                if "@anthropic-ai/claude-code" in args or re.search(r"claude-code[/\\].*cli", args):
                    result["node_cli_candidates"].append({"pid": int(pid), "name": name})
            if "mihomo" in name:
                _, args = run(["/bin/ps", "-p", pid, "-o", "args="])
                match = re.search(r"(?:^|\s)-ext-ctl-unix\s+(\S+)", args)
                if match:
                    result["mihomo_controller_socket"] = match[1]

    code, text = run(["/usr/sbin/networksetup", "-listallnetworkservices"])
    result["network_services"] = []
    if code:
        result["errors"].append("Network service inventory unavailable.")
    else:
        for service, disabled in parse_services(text):
            code, info = run(["/usr/sbin/networksetup", "-getinfo", service])
            state = next((x.partition(":")[2].strip() for x in info.splitlines() if x.startswith("IPv6:")), None)
            result["network_services"].append({"name": service, "disabled": disabled, "ipv6": state, "query_ok": code == 0})

    code, text = run(["/sbin/ifconfig"])
    result["ipv6_addresses"] = []
    interface = ""
    if code:
        result["errors"].append("Interface inventory unavailable.")
    else:
        for line in text.splitlines():
            if line and not line[0].isspace():
                interface = line.split(":", 1)[0]
            match = re.search(r"\binet6\s+(\S+)", line)
            if match:
                result["ipv6_addresses"].append({"interface": interface, "address": match[1]})

    base = Path.home() / "Library/Application Support/io.github.clash-verge-rev.clash-verge-rev"
    result["generated_config_flags"] = None
    try:
        result["generated_config_flags"] = selected_config((base / "clash-verge.yaml").read_text())
    except (OSError, UnicodeError):
        result["errors"].append("Generated Clash configuration not readable at the common path.")
    result["notes"] = [
        "Generated file flags are not runtime confirmation.",
        "Chrome extension state requires separate confirmation.",
        "No automatic pass/fail verdict; follow docs/macos-runbook.md.",
        "Keep this machine-specific output private; do not upload raw reports.",
    ]
    return result


if __name__ == "__main__":
    print(json.dumps(inspect(), ensure_ascii=False, indent=2))
