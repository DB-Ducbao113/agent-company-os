#!/usr/bin/env python3
"""Build ChatGPT install packages into dist/:
- dist/chatgpt-skills/<skill>.zip  (one per role: SKILL.md + references/ + agents/openai.yaml)
- dist/chatgpt-skills-bundle.zip   (all 10 skill zips in one download)
- dist/agent-company-os-plugin.zip (portable Agent Plugins layout: plugin.json + skills/)
Every skill zip also bundles references/os-core.md (AGENTS + Constitution + workflow + templates)
so the system works when skills are installed one by one.
Run from the repo root:  python3 scripts/build-chatgpt-packages.py
"""
import os, zipfile, json, shutil

parts = []
def add(label, path):
    if os.path.exists(path):
        parts.append(f"\n\n---\n\n# [{label}] {path}\n\n" + open(path, encoding='utf-8').read())
add("ENTRY POINT", "AGENTS.md")
add("CONSTITUTION", "constitution/CONSTITUTION.md")
for f in sorted(os.listdir("workflow")):
    if f.endswith(".md"): add("WORKFLOW", f"workflow/{f}")
for f in sorted(os.listdir("templates")):
    if f.endswith(".md"): add("TEMPLATE", f"templates/{f}")
OS_CORE = ("# Agent Company OS — Shared Core\n\nThis file is the shared operating law of Agent Company OS: "
  "entry point, constitution, workflow, routing and templates. It is bundled inside every installed role "
  "skill so the system works even when skills are installed one by one. Your own SKILL.md defines your "
  "role; this file defines the company you work in. Follow both.\n" + "".join(parts))

DISPLAY = {
 "orchestrator-intake": ("Gate 0 · Orchestrator / Intake", "Start a new task: run Gate 0 — clarify, spec, route."),
 "business-analyst": ("Gate 1 · Business Analyst", "Turn the approved spec into user stories and acceptance criteria."),
 "solution-architect": ("Gate 2 · Solution Architect", "Design the architecture and API contracts for this spec."),
 "ui-ux-design": ("Gate 3 · UI/UX Design", "Design this screen/flow from the approved requirements."),
 "security-engineer": ("Gate 4 · Security Engineer", "Threat-model this design and set the security requirements."),
 "developer": ("Gate 5 · Developer", "Implement the next task from the approved plan."),
 "code-review": ("Gate 5b · Code Review", "Review this change against the contract and the spec."),
 "integration-engineer": ("Gate 6 · Integration Engineer", "Integrate the parts and verify the contracts hold."),
 "qa-tester": ("Gate 7 · QA / Tester", "Test this feature against its acceptance criteria."),
 "release-devops": ("Gate 8 · Release / DevOps", "Prepare this release: version, changelog, rollback plan."),
}
def yaml_for(skill):
    d, p = DISPLAY[skill]
    return f'display_name: "{d} (Agent Company OS)"\ndefault_prompt: "{p}"\n'

os.makedirs("dist/chatgpt-skills", exist_ok=True)
for old in os.listdir("dist/chatgpt-skills"):
    os.remove(os.path.join("dist/chatgpt-skills", old))
for skill in sorted(os.listdir("skills")):
    with zipfile.ZipFile(f"dist/chatgpt-skills/{skill}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(f"skills/{skill}/SKILL.md", f"{skill}/SKILL.md")
        for f in sorted(os.listdir(f"skills/{skill}/references")):
            z.write(f"skills/{skill}/references/{f}", f"{skill}/references/{f}")
        z.writestr(f"{skill}/references/os-core.md", OS_CORE)
        z.writestr(f"{skill}/agents/openai.yaml", yaml_for(skill))
with zipfile.ZipFile("dist/chatgpt-skills-bundle.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir("dist/chatgpt-skills")):
        z.write(f"dist/chatgpt-skills/{f}", f)
tmp = "dist/_plugin_build/agent-company-os"
shutil.rmtree("dist/_plugin_build", ignore_errors=True)
os.makedirs(f"{tmp}/skills")
version = json.load(open(".claude-plugin/marketplace.json"))["metadata"]["version"]
json.dump({"name": "agent-company-os", "version": version,
  "description": "A gate-based operating system for AI agents: 10 role skills (Orchestrator, BA, Architect, UI/UX, Security, Developer, Code Review, Integration, QA, Release) with specs, routing, test-case gates and evidence-based handoffs.",
  "author": {"name": "Nguyen Duc Bao"},
  "onboardingSkill": "./skills/orchestrator-intake/SKILL.md"},
  open(f"{tmp}/plugin.json", "w"), indent=2)
for skill in sorted(os.listdir("skills")):
    shutil.copytree(f"skills/{skill}", f"{tmp}/skills/{skill}")
    os.makedirs(f"{tmp}/skills/{skill}/agents", exist_ok=True)
    open(f"{tmp}/skills/{skill}/agents/openai.yaml", "w").write(yaml_for(skill))
    open(f"{tmp}/skills/{skill}/references/os-core.md", "w").write(OS_CORE)
with zipfile.ZipFile("dist/agent-company-os-plugin.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("dist/_plugin_build"):
        for f in files:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, "dist/_plugin_build"))
shutil.rmtree("dist/_plugin_build")
print("ChatGPT packages built into dist/")
