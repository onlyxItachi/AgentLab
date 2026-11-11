"""Local-only educational frontend for an explicitly selected llama-server and GGUF."""

import json
import math
import os
import secrets
import signal
import socket
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import TCPServer
from urllib.parse import urlsplit

TERMS = {
    "token": "Token, modelin işlediği metin parçasıdır.",
    "embedding": "Embedding, verinin sayısal vektör temsilidir.",
    "schema": "Schema, verinin beklenen yapısını tanımlar.",
}
TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_term",
        "description": "Look up a concept definition",
        "parameters": {
            "type": "object",
            "properties": {"term": {"type": "string", "enum": list(TERMS)}},
            "required": ["term"],
            "additionalProperties": False,
        },
    },
}


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def validate_tool(message):
    if not isinstance(message, dict):
        return None
    calls = message.get("tool_calls", [])
    if not isinstance(calls, list) or len(calls) != 1:
        return None
    call = calls[0]
    if not isinstance(call, dict) or call.get("type") != "function":
        return None
    function = call.get("function", {})
    if not isinstance(function, dict) or function.get("name") != "lookup_term":
        return None
    try:
        args = json.loads(function.get("arguments", ""), object_pairs_hook=unique_json_object)
    except (TypeError, ValueError):
        return None
    if (
        not isinstance(args, dict)
        or set(args) != {"term"}
        or not isinstance(args["term"], str)
        or args["term"] not in TERMS
    ):
        return None
    if not isinstance(call.get("id"), str) or not call["id"].strip():
        return None
    return args["term"]


def find_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Model redirect rejected", headers, fp)


def probability_rows(response, key, raw=False):
    """Keep only actual, well-formed first-step values; never invent a distribution."""
    if not isinstance(response, dict):
        raise ValueError("Invalid model response for probabilities")
    entries = response.get("completion_probabilities")
    if entries is None or entries == []:
        return [], "unavailable"
    if not isinstance(entries, list) or not isinstance(entries[0], dict):
        return [], "unavailable"
    rows = entries[0].get(key)
    if not isinstance(rows, list) or not rows:
        return [], "unavailable"
    valid = []
    incomplete = False
    for row in rows:
        if not isinstance(row, dict) or isinstance(row.get("id"), bool) or not isinstance(row.get("id"), int):
            incomplete = True
            continue
        piece = row.get("token")
        if not isinstance(piece, str) and not (
            isinstance(piece, list)
            and all(isinstance(byte, int) and not isinstance(byte, bool) and 0 <= byte <= 255 for byte in piece)
        ):
            incomplete = True
            continue
        if isinstance(piece, str):
            try:
                piece.encode("utf-8")
            except UnicodeEncodeError:
                incomplete = True
                continue
        value = row.get("logprob" if raw else "prob")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            incomplete = True
            continue
        try:
            value = float(value)
        except (ValueError, OverflowError):
            incomplete = True
            continue
        if not math.isfinite(value):
            incomplete = True
            continue
        if (raw and value > 0) or (not raw and not 0 <= value <= 1):
            incomplete = True
            continue
        result = {"id": row["id"], "token": row["token"], "prob": math.exp(value) if raw else value}
        byte_values = row.get("bytes")
        if "bytes" not in row:
            result["byte_status"] = "missing"
            incomplete = True
        elif not isinstance(byte_values, list) or not all(
            isinstance(byte, int) and not isinstance(byte, bool) and 0 <= byte <= 255 for byte in byte_values
        ):
            result["byte_status"] = "invalid"
            incomplete = True
        elif ((isinstance(piece, list) and piece != byte_values)
              or (isinstance(piece, str)
                  and piece != bytes(byte_values).decode("utf-8", errors="replace"))):
            result["byte_status"] = "mismatch"
            incomplete = True
        else:
            result["bytes"] = byte_values
            result["byte_status"] = "valid"
        valid.append(result)
    return valid, "partial" if valid and incomplete else "complete" if valid else "unavailable"


def first_step_aligned(response):
    """Accept post-sampling rows only when every reported step matches its token.

    llama.cpp may omit probability entries for incomplete UTF-8 pieces, so the
    first available entry is not necessarily the first generated token. Matching
    every position also catches a later repeated token with the same ID.
    """
    if not isinstance(response, dict):
        return False
    tokens = response.get("tokens")
    entries = response.get("completion_probabilities")
    if not isinstance(tokens, list) or not tokens or not isinstance(entries, list):
        return False
    if type(response.get("tokens_predicted")) is not int or response["tokens_predicted"] != len(tokens):
        return False
    if len(entries) != len(tokens):
        return False
    return all(
        isinstance(token, int) and not isinstance(token, bool)
        and isinstance(entry, dict) and type(entry.get("id")) is int and entry["id"] == token
        for token, entry in zip(tokens, entries)
    )


class Llama:
    def __init__(self, port, key):
        if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
            raise ValueError("Invalid local model port")
        self.port, self.key = port, key
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), RejectRedirect())

    def request(self, route, payload=None):
        if route not in {"/health", "/tokenize", "/completion", "/props", "/v1/chat/completions"}:
            raise ValueError("Invalid local model route")
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{route}",
            data=body,
            headers={
                "Authorization": "Bearer " + self.key,
                "Content-Type": "application/json",
            },
        )
        try:
            with self.opener.open(request, timeout=180) as response:
                data = json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 400:
                try:
                    error = json.loads(exc.read(8192)).get("error", {})
                except (UnicodeError, json.JSONDecodeError, AttributeError):
                    error = {}
                finally:
                    exc.close()
                if isinstance(error, dict) and error.get("type") == "exceed_context_size_error":
                    raise ValueError(
                        "Girdi modelin bağlam sınırına ulaşıyor veya aşıyor; metni kısaltın. "
                        "The input meets or exceeds the model context limit; shorten the text."
                    ) from exc
            raise
        if not isinstance(data, dict):
            raise ValueError("Invalid model response")
        return data

    def tokenize(self, text):
        return self.request("/tokenize", {"content": text, "with_pieces": True})

    def generate(self, data):
        text = data["text"]
        common = {
            "prompt": text,
            "temperature": data["temperature"],
            "top_k": data["top_k"],
            "top_p": data["top_p"],
            "min_p": 0,
            "n_probs": 8,
        }
        raw = self.request(
            "/completion", {**common, "n_predict": 1, "post_sampling_probs": False}
        )
        produced = self.request(
            "/completion",
            {**common, "n_predict": data["max_tokens"], "post_sampling_probs": True, "return_tokens": True},
        )
        raw_rows, raw_status = probability_rows(raw, "top_logprobs", raw=True)
        if first_step_aligned(produced):
            post_rows, sampled_status = probability_rows(produced, "top_probs")
        else:
            post_rows, sampled_status = [], "unavailable"
        props = self.request("/props")
        if not isinstance(produced, dict) or not isinstance(produced.get("content"), str):
            raise ValueError("Invalid model generation response")
        for field in ("tokens_evaluated", "tokens_predicted"):
            if isinstance(produced.get(field), bool) or not isinstance(produced.get(field), int) or produced[field] < 0:
                raise ValueError("Invalid model generation response: " + field)
        settings = props.get("default_generation_settings")
        if not isinstance(settings, dict):
            settings = {}
        return {
            "raw": raw_rows,
            "sampled": post_rows,
            "raw_status": raw_status,
            "sampled_status": sampled_status,
            "text": produced["content"],
            "input_tokens": produced["tokens_evaluated"],
            "generated_tokens": produced["tokens_predicted"],
            "requested_tokens": data["max_tokens"],
            "first_generated_id": (produced["tokens"][0] if isinstance(produced.get("tokens"), list) and produced["tokens"] and type(produced["tokens"][0]) is int else None),
            "truncated": produced.get("truncated"),
            "stop_type": produced.get("stop_type"),
            "context": settings.get("n_ctx"),
        }

    def tool(self, text):
        messages = [{"role": "user", "content": text}]
        params = {
            "tools": [TOOL],
            "tool_choice": "auto",
            "temperature": 0,
            "max_tokens": 160,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        first = self.request("/v1/chat/completions", {**params, "messages": messages})[
            "choices"
        ][0]["message"]
        term = validate_tool(first)
        if term is None:
            return {
                "proposal": first,
                "verified": False,
                "reason": "No valid allowed tool call; nothing executed.",
            }
        messages.extend(
            [
                first,
                {
                    "role": "tool",
                    "tool_call_id": first["tool_calls"][0]["id"],
                    "content": TERMS[term],
                },
            ]
        )
        last = self.request("/v1/chat/completions", {**params, "messages": messages})[
            "choices"
        ][0]["message"]
        return {
            "proposal": first,
            "verified": True,
            "result": TERMS[term],
            "answer": last.get("content", ""),
            "additional_call_not_executed": bool(last.get("tool_calls")),
        }


def validate_input(body):
    if (
        not isinstance(body, dict)
        or not isinstance(body.get("text"), str)
        or len(body["text"]) > 8000
        or not body["text"]
    ):
        raise ValueError("Enter text (maximum 8000 characters).")
    if body.get("mode") not in {"tokenize", "generate", "tool"}:
        raise ValueError("Invalid mode")
    if body["mode"] == "generate":
        for name, low, high in (
            ("temperature", 0.01, 2),
            ("top_k", 1, 200),
            ("top_p", 0.01, 1),
            ("max_tokens", 1, 128),
        ):
            v = body.get(name)
            if (
                isinstance(v, bool)
                or not isinstance(v, (int, float))
                or not low <= v <= high
                or not math.isfinite(v)
            ):
                raise ValueError("Invalid " + name)
            if name in {"top_k", "max_tokens"} and not isinstance(v, int):
                raise ValueError("Invalid " + name)
    return body


class LoopbackHTTPServer(ThreadingHTTPServer):
    def server_bind(self):
        # HTTPServer.server_bind resolves a hostname; this server only uses IPv4 loopback.
        TCPServer.server_bind(self)
        self.server_name = "127.0.0.1"
        self.server_port = self.server_address[1]


def build_server(llama, token):
    html = Path(__file__).with_name("index.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def reply(self, status, data, content_type="application/json; charset=utf-8"):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(data)

        def allowed(self):
            return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

        def do_GET(self):
            if not self.allowed() or urlsplit(self.path).path != "/" + token:
                return self.reply(404, b"Not found", "text/plain")
            self.reply(200, html, "text/html; charset=utf-8")

        def do_POST(self):
            if (
                not self.allowed()
                or self.path != "/" + token
                or self.headers.get("Origin")
                != f"http://127.0.0.1:{self.server.server_port}"
            ):
                return self.reply(403, b"Forbidden", "text/plain")
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 40000:
                    raise ValueError("Invalid request size")
                data = validate_input(json.loads(self.rfile.read(length)))
                result = {
                    "tokenize": llama.tokenize,
                    "generate": llama.generate,
                    "tool": llama.tool,
                }[data["mode"]](data["text"] if data["mode"] != "generate" else data)
                self.reply(200, json.dumps(result, ensure_ascii=False).encode())
            except (
                ValueError,
                KeyError,
                TypeError,
                IndexError,
                OSError,
                urllib.error.URLError,
            ) as exc:
                self.reply(
                    400, json.dumps({"error": str(exc)}, ensure_ascii=False).encode()
                )

    return LoopbackHTTPServer(("127.0.0.1", 0), Handler)


def serve(llama):
    token = secrets.token_urlsafe(24)
    server = build_server(llama, token)
    print(
        "AgentLab açık; durdurmak için bu pencerede Ctrl+C kullanın.",
        flush=True,
    )
    webbrowser.open(f"http://127.0.0.1:{server.server_port}/{token}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


@contextmanager
def cleanup_on_termination():
    """Let Python run finally blocks for catchable SIGTERM on the main thread."""
    previous = {}
    if threading.current_thread() is threading.main_thread() and hasattr(signal, "SIGTERM"):
        def stop(signum, frame):
            raise SystemExit(128 + signum)

        previous[signal.SIGTERM] = signal.signal(signal.SIGTERM, stop)
    try:
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


@contextmanager
def defer_startup_termination():
    """Remember catchable signals until Popen's child is assigned for cleanup."""
    previous = {}
    pending = []
    if threading.current_thread() is threading.main_thread():
        def remember(signum, frame):
            if not pending:
                pending.append(signum)

        for signum in (signal.SIGINT, signal.SIGTERM):
            previous[signum] = signal.signal(signum, remember)
    try:
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        if pending:
            raise SystemExit(128 + pending[0])


def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "AgentLab",
        "Önce indirdiğiniz llama-server programını, sonra Qwen3.5 GGUF model dosyasını seçin.",
    )
    executable = filedialog.askopenfilename(
        title="llama-server seçin / Select llama-server"
    )
    if not executable:
        return
    if Path(executable).name.lower() not in {"llama-server", "llama-server.exe"}:
        messagebox.showerror("AgentLab", "llama-server seçilmedi.")
        return
    model = filedialog.askopenfilename(
        title="GGUF model seçin / Select GGUF model", filetypes=[("GGUF", "*.gguf")]
    )
    if not model:
        return
    port, key = find_port(), secrets.token_urlsafe(32)
    process = None
    with cleanup_on_termination(), tempfile.TemporaryDirectory(prefix="agentlab-server-") as directory:
        keyfile = Path(directory) / "key"
        keyfile.write_text(key, encoding="ascii")
        try:
            os.chmod(keyfile, 0o600)
            with defer_startup_termination():
                process = subprocess.Popen(
                    [
                        executable,
                        "--model",
                        model,
                        "--host",
                        "127.0.0.1",
                        "--port",
                        str(port),
                        "--ctx-size",
                        "2048",
                        "--jinja",
                        "--no-ui",
                        "--api-key-file",
                        str(keyfile),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            llama = Llama(port, key)
            for _ in range(120):
                if process.poll() is not None:
                    raise RuntimeError(
                        "llama-server could not start; check the model and executable."
                    )
                try:
                    if llama.request("/health").get("status") == "ok":
                        break
                except (OSError, ValueError):
                    time.sleep(1)
            else:
                raise RuntimeError("Model did not start within 120 seconds.")
            root.destroy()
            serve(llama)
        except (OSError, RuntimeError) as exc:
            messagebox.showerror("AgentLab", str(exc))
        finally:
            if process and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    main()
