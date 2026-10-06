# Claude Code setup (one time, about 15 minutes)

Claude Code is only the engine for scale. Every page still follows `rules/HUB_RULES.md` and `DECISIONS.md` exactly, and nothing reaches Webflow without Divit's approval.

## 1. Install and sign in
```bash
curl -fsSL https://claude.ai/install.sh | bash      # official native installer (macOS, Linux, WSL)
claude --version                                     # reopen Terminal if "command not found"
```
Run `claude` once and sign in with the Claude account Emergent uses. Official docs: https://code.claude.com/docs

## 2. Tools Claude Code needs on the Mac
- Python 3.11 or newer (`python3 --version`; if older: `brew install python`)
- git (`git --version`; installs with Xcode Command Line Tools)

## 3. The repo and the keyword workbook
```bash
git clone https://github.com/seo881/potential-enigma.git ~/emergent-hubs
cd ~/emergent-hubs
mkdir -p private && cp ~/Downloads/Emergent_Hub_Child_Pages_Final_v3.xlsx private/   # Semrush data stays out of git
bash ops/setup.sh                                    # expect: SETUP OK
```
Push access: the first `git push` asks for credentials. Use the GitHub account that owns `seo881/potential-enigma`, or the fine-grained token from the handoff as the password (macOS Keychain remembers it).

## 4. Connect Webflow
The repo ships `.mcp.json`, which registers Webflow's MCP server for this project.
1. Start Claude Code inside the repo: `cd ~/emergent-hubs && claude`
2. Approve the project server **webflow** when asked.
3. Type `/mcp`, choose **webflow**, authenticate in the browser, and grant access to the Emergent site.

Check: ask Claude Code "Run `.venv/bin/python3 ops/hubctl.py status`, then list my Webflow sites." The site `6a0edf12ef1a8562ed56d806` must appear.

## 5. Safety rails built into the repo
- `.claude/settings.json` lets repo commands (`hubctl`, QC, git commit and push) run without prompts and blocks force-pushes, hard resets and reading `private/`.
- **Every Webflow call still asks for your approval.** Approve creates only for batches you have signed off, and publishes only on your explicit go.
- Skills (`.claude/skills/`) and the writer and reviewer subagents (`.claude/agents/`) load from the repo, so updates arrive with `git pull`; nothing to reinstall.

## 6. Daily run
In `~/emergent-hubs`, start `claude` and paste the day's prompt from `KICKOFF.md` (Mode A). Usage depends on your Claude plan; about 200 pages a day of writing and review is heavy, so watch the first day's usage and size the next day to it.
