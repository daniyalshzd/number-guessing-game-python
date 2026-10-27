"""
Number Guessing Game  -  ONE FILE, NOTHING TO INSTALL.

How to run:   python play.py
(your browser opens by itself; press Ctrl + C in the terminal to stop)

The file has 4 parts:
  1. GAME_CODE   - your original game code, not changed
  2. PAGE        - the web page (HTML + CSS + JavaScript)
  3. GameSession - connects the page to your game (print -> page, input -> Send button)
  4. The small web server that ties it all together
"""
import json
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# =====================================================================
# 1. YOUR GAME CODE (unchanged)
# =====================================================================
GAME_CODE = r'''import random
print("                                  Hello, this is a Python program that will choose a number and you have to guess it.")
max_attempts = 5

def play_game():
    best_score = None
    while True:
        secret = random.randint(1, 10)
        attempts = 0

        while True:
            try:
                guess= int(input("Guess a number between 1 and 10 ="))
            except ValueError:
                print("                               Numbers only!!")
                continue
            if guess > 10 or guess < 1:
                print("                       Invalid Range, Enter a number between 1 and 10")
                continue
            attempts += 1 #This variable is created to add a value to attempts so it can be subtracted from max_attempts

            if guess == secret:
                total_attempts= attempts # This variable is created in a loop to show the total attempts
                print("                      You guessed it right in",total_attempts,"attempts")
                if best_score == None or total_attempts < best_score:
                    best_score = total_attempts
                    print("                      The best score is =", best_score)

                #Created a variable to show the best score and assigned it with total attempts
                break
            elif guess > secret:
                print("                         TOO HIGH!")
                x = max_attempts - attempts #This variable is used to subtract the value from attempts and displays them
                print("The attempts left are", x)
            else:
                print("                         TOO LOW!")
                x = max_attempts - attempts
                print("The attempts left are", x)

            if attempts >= max_attempts:
                print("                           You have reached the attempts limit")
                print("                            The secret number was = ",+secret)
                print("                            The best score is 0")
                break
        z = input("Do you want to play again? ")

        if z.upper() == "Yes" or z.lower() == "yes":
            continue
        else:
            break

play_game()
'''

# =====================================================================
# 2. THE WEB PAGE
# =====================================================================
PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Number Guessing Game</title>
  <style>
:root {
  --bg: #f4f5f7;
  --card: #ffffff;
  --text: #1d2433;
  --muted: #5b6475;
  --accent: #2f6fed;
  --terminal: #101521;
  --terminal-text: #e6e9f2;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  line-height: 1.5;
}

main { max-width: 860px; margin: 0 auto; padding: 32px 16px 64px; }

h1 { margin: 0 0 8px; font-size: 2rem; }
.lead { color: var(--muted); font-size: 1.05rem; margin: 0 0 24px; }

.card {
  background: var(--card);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(16, 21, 33, 0.08);
}
.card h2 { margin: 0 0 12px; font-size: 1.2rem; }
.card ol { margin: 0; padding-left: 20px; }
.card li { margin-bottom: 6px; }
.note { color: var(--muted); margin: 0 0 12px; }

.terminal {
  background: var(--terminal);
  color: var(--terminal-text);
  font-family: Consolas, "Courier New", monospace;
  font-size: 0.95rem;
  height: 340px;
  overflow-y: auto;
  padding: 16px;
  border-radius: 8px;
  white-space: pre-wrap;      /* keeps your spaces, so messages stay centred */
  word-break: break-word;
}
.terminal div { margin-bottom: 4px; }
.terminal .you    { color: #8ab4ff; }
.terminal .prompt { color: #ffffff; font-weight: 600; }
.terminal .good   { color: #6ee7a0; }
.terminal .warn   { color: #fbbf24; }
.terminal .bad    { color: #ff8a8a; }

#answer-form { display: flex; gap: 8px; margin-top: 12px; }
#answer {
  flex: 1;
  font-size: 1rem;
  padding: 10px 12px;
  border: 1px solid #c9cfdb;
  border-radius: 8px;
}
#answer:disabled { background: #eceef3; }

button {
  font-size: 1rem;
  padding: 10px 18px;
  border: 0;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  cursor: pointer;
}
button:disabled { background: #a9b6d6; cursor: not-allowed; }
button.secondary { background: #e3e7f0; color: var(--text); }

.footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}
#status { margin: 0; color: var(--muted); }
</style>
</head>
<body>
  <main>
    <h1>Number Guessing Game</h1>
    <p class="lead">
      This is a Python program that secretly picks a number. Your job is to guess it.
      After every guess it tells you if you were too high or too low, shows how many
      attempts you have left, and remembers your best score.
    </p>

    <section class="card">
      <h2>How to play</h2>
      <ol>
        <li>Read the question in the black box below.</li>
        <li>Type a number in the white box and press <strong>Send</strong> (or the Enter key).</li>
        <li>Keep guessing until you find the secret number, before your attempts run out.</li>
        <li>At the end, the program asks if you want to play again. Type <strong>yes</strong> to play another round.</li>
      </ol>
    </section>

    <section class="card">
      <h2>The game</h2>
      <p class="note">
        Everything the Python program says appears in the black box. When it asks you
        something, the white box becomes active so you can answer.
      </p>
      <div id="output" class="terminal" role="log" aria-live="polite"></div>
      <form id="answer-form" autocomplete="off">
        <input id="answer" type="text" placeholder="Type your answer here" aria-label="Your answer" disabled>
        <button id="send" type="submit" disabled>Send</button>
      </form>
      <div class="footer-row">
        <p id="status"></p>
        <button id="restart" type="button" class="secondary">Restart game</button>
      </div>
    </section>
  </main>
  <script>
const output = document.getElementById("output");
const form = document.getElementById("answer-form");
const answerBox = document.getElementById("answer");
const sendButton = document.getElementById("send");
const restartButton = document.getElementById("restart");
const statusText = document.getElementById("status");

// Each browser tab gets its own id, so each player has their own game.
let sid = sessionStorage.getItem("sid");
if (!sid) {
  sid = (window.crypto && crypto.randomUUID)
    ? crypto.randomUUID()
    : String(Math.random()).slice(2) + Date.now();
  sessionStorage.setItem("sid", sid);
}

async function post(url, extra) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sid, ...extra }),
  });
  if (!response.ok) throw new Error("Server error");
  return response.json();
}

// Colour a few important messages so they are easy to spot.
function lineClass(text) {
  const t = text.toLowerCase();
  if (t.includes("guessed it right") || t.includes("best score is =")) return "good";
  if (t.includes("too high") || t.includes("too low")) return "warn";
  if (t.includes("numbers only") || t.includes("invalid range") || t.includes("attempts limit")) return "bad";
  return "";
}

function addLine(text, className) {
  const line = document.createElement("div");
  line.textContent = text;
  if (className) line.className = className;
  output.appendChild(line);
}

function render(state) {
  output.innerHTML = "";
  state.lines.forEach((line) => addLine(line.text, line.you ? "you" : lineClass(line.text)));
  if (state.prompt) addLine(state.prompt, "prompt");
  output.scrollTop = output.scrollHeight;

  const waiting = Boolean(state.prompt);
  answerBox.disabled = !waiting;
  sendButton.disabled = !waiting;
  statusText.textContent = state.finished ? "The game has ended. Press \"Restart game\" to play again." : "";
  if (waiting) answerBox.focus();
}

async function startGame() {
  try {
    render(await post("/api/start"));
  } catch (error) {
    statusText.textContent = "Could not reach the game. Is the server running?";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = answerBox.value;
  answerBox.value = "";
  sendButton.disabled = true;
  try {
    render(await post("/api/send", { text }));
  } catch (error) {
    statusText.textContent = "Lost connection to the game. Press \"Restart game\".";
  }
});

restartButton.addEventListener("click", startGame);
startGame();
</script>
</body>
</html>
'''

# =====================================================================
# 3. THE BRIDGE BETWEEN THE PAGE AND YOUR GAME
# =====================================================================
MAX_IDLE_SECONDS = 30 * 60
WAIT_SECONDS = 5


class _Closed(BaseException):
    """Raised inside the game when its session is closed."""


class GameSession:
    """One player's running copy of your game."""

    def __init__(self):
        self.lines = []          # everything shown in the black box
        self.prompt = None       # the question the game is waiting on
        self.answer = None
        self.has_answer = False
        self.finished = False
        self.closed = False
        self.last_used = time.time()
        self.cond = threading.Condition()
        threading.Thread(target=self._run, daemon=True).start()
        self._wait_for_game()

    # stand-ins for print() and input() that your game will use
    def _print(self, *args, sep=" ", **kwargs):
        with self.cond:
            self.lines.append({"text": sep.join(str(a) for a in args), "you": False})

    def _input(self, prompt=""):
        with self.cond:
            self.prompt = str(prompt)
            self.cond.notify_all()
            while not self.has_answer and not self.closed:
                self.cond.wait()
            if self.closed:
                raise _Closed()
            self.has_answer = False
            return self.answer

    def _run(self):
        try:
            namespace = {"__name__": "game", "print": self._print, "input": self._input}
            exec(compile(GAME_CODE, "game.py", "exec"), namespace)
        except _Closed:
            pass
        except Exception as error:
            with self.cond:
                self.lines.append({"text": "Error in the game: " + str(error), "you": False})
        finally:
            with self.cond:
                self.finished = True
                self.prompt = None
                self.cond.notify_all()

    def _wait_for_game(self):
        with self.cond:
            self.cond.wait_for(lambda: self.prompt is not None or self.finished,
                               timeout=WAIT_SECONDS)

    def send(self, text):
        with self.cond:
            self.last_used = time.time()
            if self.prompt is None:
                return
            self.lines.append({"text": self.prompt.rstrip() + " " + text, "you": True})
            self.answer = text
            self.has_answer = True
            self.prompt = None
            self.cond.notify_all()
            self.cond.wait_for(lambda: self.prompt is not None or self.finished,
                               timeout=WAIT_SECONDS)

    def state(self):
        with self.cond:
            self.last_used = time.time()
            return {"lines": list(self.lines), "prompt": self.prompt, "finished": self.finished}

    def close(self):
        with self.cond:
            self.closed = True
            self.cond.notify_all()


SESSIONS = {}
SESSIONS_LOCK = threading.Lock()


def start_session(sid):
    session = GameSession()
    with SESSIONS_LOCK:
        old = SESSIONS.get(sid)
        SESSIONS[sid] = session
        now = time.time()
        stale_ids = [k for k, s in SESSIONS.items() if now - s.last_used > MAX_IDLE_SECONDS]
        stale = [SESSIONS.pop(k) for k in stale_ids]
    for s in ([old] if old else []) + stale:
        s.close()
    return session


# =====================================================================
# 4. THE WEB SERVER
# =====================================================================
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):      # keep the terminal quiet
        pass

    def _reply(self, status, body, content_type):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, payload):
        self._reply(status, json.dumps(payload), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._reply(200, PAGE, "text/html; charset=utf-8")
        else:
            self._reply(404, "Not found", "text/plain")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            data = {}
        sid = str(data.get("sid", ""))[:100]

        if self.path == "/api/start" and sid:
            self._json(200, start_session(sid).state())
        elif self.path == "/api/send":
            with SESSIONS_LOCK:
                session = SESSIONS.get(sid)
            if session is None:
                self._json(404, {"error": "no game running"})
            else:
                session.send(str(data.get("text", "")).strip()[:100])
                self._json(200, session.state())
        else:
            self._json(400, {"error": "bad request"})


def main():
    server = None
    for port in range(5000, 5011):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if server is None:
        print("Could not find a free port. Close other programs and try again.")
        return
    url = "http://127.0.0.1:%d" % port
    print("Game is running at " + url)
    print("(your browser should open by itself - press Ctrl + C here to stop)")
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
