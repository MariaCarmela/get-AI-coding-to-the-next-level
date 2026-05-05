import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR_FILE = ROOT / "src" / "agents" / "orchestrator.py"
RESEARCHER_FILE = ROOT / "src" / "agents" / "researcher.py"
WRITER_FILE = ROOT / "src" / "agents" / "writer.py"
REQUIREMENTS_FILE = ROOT / "requirements.txt"

PORTS = (8001, 8002, 8003)
SECTION_NAMES = (
    "role selection",
    "role introduction",
    "context provision",
    "task presentation",
    "response generation",
)

PLACEHOLDER_MARKERS = (
    "#todo",
    "todo:",
    "[todo",
    "[tbd",
    "placeholder",
    "lorem ipsum",
)


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def wait_for_ports(ports: tuple[int, ...], timeout_sec: int = 20) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if all(is_port_open(port) for port in ports):
            return True
        time.sleep(0.5)
    return False


def check_orchestrator_code() -> list[str]:
    errors: list[str] = []
    text = ORCHESTRATOR_FILE.read_text(encoding="utf-8").lower()

    has_sequence_loop = "for current_phase in phase_sequence" in text
    has_target_index = "target_index = phase_sequence.index(phase)" in text
    if not (has_sequence_loop and has_target_index):
        errors.append("Orchestrator sequencing not implemented in run_bid_proposal (expected target index + phase loop).")

    has_research_assign = "ctx.research = response" in text
    has_draft_assign = "ctx.draft = response" in text
    has_processed_assign = "ctx.processed = response" in text
    if not (has_research_assign and has_draft_assign and has_processed_assign):
        errors.append("Orchestrator response persistence not fully implemented in run_phase.")

    return errors


def check_prompt_structure(file_path: Path, label: str) -> list[str]:
    errors: list[str] = []
    source = file_path.read_text(encoding="utf-8")
    text = source.lower()

    prompt_candidates: list[str] = []
    for match in re.finditer(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', source, flags=re.DOTALL):
        candidate = match.group(1) if match.group(1) is not None else match.group(2)
        if candidate:
            prompt_candidates.append(candidate)

    if prompt_candidates:
        prompt_candidates.sort(
            key=lambda candidate: (
                sum(1 for section in SECTION_NAMES if section in candidate.lower()),
                len(candidate),
            ),
            reverse=True,
        )
        text = prompt_candidates[0].lower()

    missing_sections: list[str] = []
    for section in SECTION_NAMES:
        if section not in text:
            missing_sections.append(section.title())

    if missing_sections:
        errors.append(
            f"{label}: system prompt must include the exact outlined sections: "
            "Role Selection, Role Introduction, Context Provision, Task Presentation, Response Generation. "
            f"Missing: {', '.join(missing_sections)}."
        )
        return errors

    if any(marker in text for marker in PLACEHOLDER_MARKERS):
        errors.append(
            f"{label}: prompt contains placeholder text (e.g., TODO/TBD/placeholder). "
            "Replace scaffold text with concrete instructions in all sections."
        )

    positions = [text.find(section) for section in SECTION_NAMES]
    for idx, section in enumerate(SECTION_NAMES):
        start = positions[idx]
        if start < 0:
            continue
        end = positions[idx + 1] if idx + 1 < len(positions) else len(text)
        if end < 0:
            end = len(text)

        section_body = text[start + len(section): end].strip()
        word_count = len(re.findall(r"[a-zA-Z]+", section_body))
        if word_count < 8:
            errors.append(
                f"{label}: section '{section.title()}' is too thin. "
                "Add substantive guidance (at least ~8 words)."
            )

    return errors


def run_client() -> tuple[list[str], dict | None]:
    errors: list[str] = []
    cmd = [sys.executable, "-m", "src.client", "Aston Martin"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

    if result.returncode != 0:
        errors.append(f"Client execution failed with exit code {result.returncode}.")
        errors.append(result.stderr.strip() or result.stdout.strip())
        return errors, None

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        errors.append("Client output is not valid JSON.")
        return errors, None

    if payload.get("research") is None:
        errors.append("Client JSON missing non-null 'research'.")

    return errors, payload


def install_requirements() -> list[str]:
    errors: list[str] = []
    if not REQUIREMENTS_FILE.exists():
        errors.append("requirements.txt not found at project root.")
        return errors

    cmd = [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        errors.append("Dependency installation failed: pip install -r requirements.txt")
        errors.append(result.stderr.strip() or result.stdout.strip())

    return errors


def check_openai_api_key() -> list[str]:
    errors: list[str] = []
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY is not set in the environment.")
        errors.append("Set it before running evaluation, e.g. export OPENAI_API_KEY='...'.")
    return errors


def main() -> int:
    all_errors: list[str] = []

    all_errors.extend(install_requirements())
    all_errors.extend(check_openai_api_key())
    all_errors.extend(check_orchestrator_code())
    all_errors.extend(check_prompt_structure(RESEARCHER_FILE, "Researcher"))
    all_errors.extend(check_prompt_structure(WRITER_FILE, "Writer"))

    if all_errors:
        print("EVALUATION: FAIL")
        for err in all_errors:
            print(f"- {err}")
        return 1

    server_proc = subprocess.Popen(
        [sys.executable, "-m", "src.main"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        if not wait_for_ports(PORTS):
            all_errors.append("Server did not open required ports 8001/8002/8003 within timeout.")
        else:
            client_errors, payload = run_client()
            all_errors.extend(client_errors)
            if payload is not None:
                if payload.get("draft") is None:
                    all_errors.append("Client JSON missing non-null 'draft' (expected after sequencing).")
                if payload.get("processed") is None:
                    all_errors.append("Client JSON missing non-null 'processed' (expected for full pipeline).")
    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()

    if all_errors:
        print("EVALUATION: FAIL")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("EVALUATION: PASS")
    print("- Orchestrator sequencing/persistence checks passed")
    print("- Role-based prompt structure checks passed")
    print("- Runtime server/client flow checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
