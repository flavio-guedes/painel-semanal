#!/usr/bin/env python3
import os
import re
import json
from datetime import datetime
from pathlib import Path

HTML_PATH = Path("/Users/mac/Library/CloudStorage/GoogleDrive-flavioguedesmkt@gmail.com/Meu Drive/_Profissional/_Planejamento profissional /Dados - CRM/00 - Painel/01 - Apoio/00 - Listas/01 - Vaga_Contratacao/01 - Sub Tier 1 - Founder:Head + Design/T1 - Founder_Head + Design - 00 - 283.html")
STATE_PATH = Path("/Users/mac/repo-painel-semanal/evolution_state.json")
REPORT_PATH = Path("/Users/mac/repo-painel-semanal/evolution_report.txt")

def extract_leads(html):
    m = re.search(r"let leads = (\[.*?\]);", html, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        return data
    except Exception as e:
        print("Erro ao parsear JSON:", e)
        return []

def compute_metrics(leads):
    total = len(leads)
    by_status = {}
    for l in leads:
        s = l.get("status") or "pendente"
        by_status[s] = by_status.get(s, 0) + 1
    done = by_status.get("encerrado", 0) + by_status.get("descarte", 0)
    pct = (done / total * 100) if total else 0
    return {
        "total": total,
        "by_status": by_status,
        "done": done,
        "pct": round(pct, 2),
    }

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}

def save_state(state):
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def build_report(metrics, prev):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [
        f"Evolução das mensagens — {now}",
        f"Arquivo: {HTML_PATH.name}",
        f"Total de leads: {metrics['total']}",
        f"Concluídos + descarte: {metrics['done']} ({metrics['pct']}%)",
        "Status:",
    ]
    for k in ["pendente", "respondido", "em andamento", "encerrado", "descarte"]:
        lines.append(f"  - {k}: {metrics['by_status'].get(k, 0)}")
    if prev:
        delta_total = metrics['total'] - prev.get('total', metrics['total'])
        delta_done = metrics['done'] - prev.get('done', metrics['done'])
        lines.append(f"Delta desde última leitura: total {delta_total:+}, concluídos {delta_done:+}")
    return "\n".join(lines)

def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    leads = extract_leads(html)
    metrics = compute_metrics(leads)
    prev = load_state()
    report = build_report(metrics, prev)
    print(report)
    REPORT_PATH.write_text(report, encoding="utf-8")
    save_state(metrics)

if __name__ == "__main__":
    main()
