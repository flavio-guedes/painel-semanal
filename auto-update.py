#!/usr/bin/env python3
import time
import subprocess
import os
from pathlib import Path

REPO = Path("/Users/mac/repo-painel-semanal")
BRANCH = "main"
SLEEP_SECONDS = 60

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd or REPO, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    print(f"[LOOP] Iniciando atualizador do painel em {REPO}")
    while True:
        try:
            code, out, err = run("git status -sb")
            if code != 0:
                print(f"[LOOP] Erro no git status: {err}")
                time.sleep(SLEEP_SECONDS)
                continue

            if "nothing to commit" in out or "working tree clean" in out:
                print(f"[LOOP] Nada para atualizar ({time.strftime('%H:%M:%S')})")
            else:
                print(f"[LOOP] Mudanças detectadas, atualizando...")
                code, out, err = run("git add -A")
                if code != 0:
                    print(f"[LOOP] Erro no git add: {err}")
                    time.sleep(SLEEP_SECONDS)
                    continue
                code, out, err = run('git commit -m "chore: atualizacao automatica do painel"')
                if code != 0:
                    print(f"[LOOP] Erro no commit: {err}")
                    time.sleep(SLEEP_SECONDS)
                    continue
                code, out, err = run("git push origin main")
                if code != 0:
                    print(f"[LOOP] Erro no push: {err}")
                else:
                    print(f"[LOOP] Painel atualizado com sucesso ({time.strftime('%H:%M:%S')})")

            time.sleep(SLEEP_SECONDS)
        except KeyboardInterrupt:
            print("\n[LOOP] Atualizador encerrado.")
            break
        except Exception as e:
            print(f"[LOOP] Erro inesperado: {e}")
            time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
