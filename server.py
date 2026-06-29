#!/usr/bin/env python3
"""
Generic local Career Coach server.

Run:
  python3 server.py

Personalize locally:
  cp context/profile.example.md context/profile.local.md
  cp context/domain-knowledge.md context/domain-knowledge.local.md
  add licensed/private notes under references.local/

The *.local.md files are ignored by git.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import datetime
import urllib.request

ROOT = Path(__file__).resolve().parent
PORT = int(os.getenv("PORT", "8421"))

MODES = {
    "general-coaching": "templates/general-coaching.md",
    "weekly-review": "templates/weekly-review.md",
    "mock-interview": "templates/mock-interview.md",
    "resume-review": "templates/resume-review.md",
    "strategy-review": "templates/strategy-review.md",
    "offer-evaluation": "templates/offer-evaluation.md",
    "self-review": "templates/self-review.md",
}


def read_text(path, fallback=""):
    file_path = ROOT / path
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return fallback


def read_markdown_dir(path, limit_chars=24000):
    dir_path = ROOT / path
    if not dir_path.exists():
        return "", 0
    chunks = []
    count = 0
    total = 0
    for file_path in sorted(dir_path.rglob("*.md")):
        if file_path.name.lower() == "readme.md":
            continue
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        header = f"\n\n## Source: {file_path.relative_to(ROOT)}\n"
        piece = header + text
        if total + len(piece) > limit_chars:
            remaining = limit_chars - total
            if remaining > len(header) + 500:
                chunks.append(piece[:remaining])
                count += 1
            break
        chunks.append(piece)
        count += 1
        total += len(piece)
    return "\n".join(chunks), count


def read_context():
    profile = read_text("context/profile.local.md") or read_text("context/profile.example.md")
    domain = read_text("context/domain-knowledge.local.md") or read_text("context/domain-knowledge.md")
    principles = read_text("context/coaching-principles.md")
    public_refs, public_ref_count = read_markdown_dir("references")
    private_refs, private_ref_count = read_markdown_dir("references.local")
    learnings, learning_count = read_markdown_dir("learning.local")
    return {
        "profile": profile,
        "domain": domain,
        "principles": principles,
        "public_refs": public_refs,
        "private_refs": private_refs,
        "learnings": learnings,
        "public_ref_count": public_ref_count,
        "private_ref_count": private_ref_count,
        "learning_count": learning_count,
        "has_private_profile": (ROOT / "context/profile.local.md").exists(),
        "has_private_domain": (ROOT / "context/domain-knowledge.local.md").exists(),
        "has_private_refs": private_ref_count > 0,
        "has_local_learnings": learning_count > 0,
    }


def build_messages(mode, user_message):
    context = read_context()
    template = read_text(MODES.get(mode, MODES["weekly-review"]))
    system = f"""You are a private local AI career coach.

Use the provided context, reference library, and workflow.

Coaching rules:
- If the user asks a general career question, answer from the public reference library and domain knowledge without requiring a personal profile.
- If the answer depends on individual context, ask up to two diagnostic questions before advising.
- If a private profile or private references are present, use them to personalize the answer.
- If local learning notes are present, use them to avoid repeated coaching mistakes and improve future responses.
- Do not fabricate source details. If the reference library does not support a claim, say what additional source is needed.
- Avoid generic motivation. Name the tradeoff behind the recommendation.
- End with one practical next action.

## User Profile
{context["profile"]}

## Domain Knowledge
{context["domain"]}

## Coaching Principles
{context["principles"]}

## Public Reference Library
{context["public_refs"] or "No public references loaded."}

## Private / Local Reference Notes
{context["private_refs"] or "No private local reference notes loaded."}

## Local Coach Learning Notes
{context["learnings"] or "No local learning notes loaded."}

## Workflow
{template}
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]


def call_openai_compatible(base_url, api_key, model, messages):
    payload = json.dumps({"model": model, "messages": messages, "temperature": 0.4}).encode("utf-8")
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def generate_from_messages(messages):
    if os.getenv("DEEPSEEK_API_KEY"):
        return call_openai_compatible(
            "https://api.deepseek.com",
            os.getenv("DEEPSEEK_API_KEY"),
            os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            messages,
        )

    if os.getenv("OPENAI_API_KEY"):
        return call_openai_compatible(
            "https://api.openai.com/v1",
            os.getenv("OPENAI_API_KEY"),
            os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            messages,
        )

    return (
        "No model API key is configured, so this is a local preview response.\n\n"
        "What the coach would do next:\n"
        "1. Ask for the missing career context that changes the recommendation.\n"
        "2. Evaluate the scenario using the selected workflow.\n"
        "3. Return one concrete action you can take within seven days.\n\n"
        "To enable real responses, set DEEPSEEK_API_KEY or OPENAI_API_KEY and restart server.py."
    )


def generate_reply(mode, user_message):
    return generate_from_messages(build_messages(mode, user_message))


def reflect_on_session(mode, messages):
    transcript = "\n".join(
        f"{item.get('role', '').upper()}: {item.get('content', '')}"
        for item in messages
        if item.get("role") in ("user", "coach", "assistant")
    )
    template = read_text("templates/self-review.md")
    prompt = f"""Review this Career Coach session.

Mode: {mode}

{template}

Transcript:
{transcript}
"""
    return generate_from_messages([
        {"role": "system", "content": "You are a strict QA reviewer for a local AI career coach. Be concise, concrete, and improvement-oriented."},
        {"role": "user", "content": prompt},
    ])


def save_learning(reflection):
    path = ROOT / "learning.local" / "coach-learnings.md"
    path.parent.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    entry = f"\n\n## {today}\n\n{reflection.strip()}\n"
    if not path.exists():
        path.write_text("# Coach Learning Log\n\nPrivate local notes from self-review. Do not commit.\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as file:
        file.write(entry)
    return str(path)


class Handler(BaseHTTPRequestHandler):
    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = read_text("index.html").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/status":
            context = read_context()
            self.send_json({
                "hasPrivateProfile": context["has_private_profile"],
                "hasPrivateDomain": context["has_private_domain"],
                "hasPrivateReferences": context["has_private_refs"],
                "hasLocalLearnings": context["has_local_learnings"],
                "publicReferenceCount": context["public_ref_count"],
                "privateReferenceCount": context["private_ref_count"],
                "learningCount": context["learning_count"],
                "hasDeepSeek": bool(os.getenv("DEEPSEEK_API_KEY")),
                "hasOpenAI": bool(os.getenv("OPENAI_API_KEY")),
            })
            return
        self.send_error(404)

    def do_POST(self):
        if self.path not in ("/api/chat", "/api/reflect", "/api/save-learning"):
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if self.path == "/api/reflect":
            messages = data.get("messages", [])
            mode = data.get("mode", "general-coaching")
            if not messages:
                self.send_json({"error": "messages are required"}, status=400)
                return
            try:
                self.send_json({"reflection": reflect_on_session(mode, messages)})
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=500)
            return
        if self.path == "/api/save-learning":
            reflection = data.get("reflection", "").strip()
            if not reflection:
                self.send_json({"error": "reflection is required"}, status=400)
                return
            try:
                self.send_json({"ok": True, "path": save_learning(reflection)})
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=500)
            return
        mode = data.get("mode", "weekly-review")
        message = data.get("message", "").strip()
        if not message:
            self.send_json({"error": "message is required"}, status=400)
            return
        try:
            reply = generate_reply(mode, message)
            self.send_json({"reply": reply})
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    for port in range(PORT, PORT + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            server = None
    if server is None:
        raise RuntimeError(f"No available port found from {PORT} to {PORT + 19}")
    print(f"Career Coach running at http://127.0.0.1:{server.server_port}")
    server.serve_forever()
