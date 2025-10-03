## Development Plan – GitHub Preparation

Date: 2025-10-03

Objective
- Prepare the repository for public posting on GitHub with clear top-level documentation and an explicit license.

Scope
- Create or update a top-level README explaining what the repo contains and why it exists.
- Add Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0) license at the root.
- Preserve existing subproject READMEs and link to them from the top-level README.
- Do not alter scientific content; focus on organization and clarity.

Assumptions
- License preference is Creative Commons Non-Commercial with attribution (CC BY-NC 4.0).
- No code execution or build changes are required for this task.

Milestones
1) Audit repository structure and existing documentation.
2) Draft and add top-level README.md summarizing structure, purpose, and how to navigate.
3) Add CC BY-NC 4.0 LICENSE file at the root.
4) Update this plan with completion summary and any follow-ups.

Acceptance Criteria
- README.md exists at the root and concisely explains the repo, subdirectories, and key documents.
- LICENSE exists at the root with CC BY-NC 4.0 terms (or canonical reference).
- Planning document updated at start and end of task.

Kickoff Notes
- Initiated audit and documentation task. Next action: scan key READMEs and index docs to draft the top-level README.

Completion Notes (2025-10-03)
- Audited repository structure and key documentation.
- Added root `README.md` summarizing purpose, contents, and navigation.
- Added `LICENSE` with Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0).
- Preserved subpackage licenses and READMEs (e.g., `UFRF-Graphene/`).
- Next Steps: If desired, add `CITATION.cff` at root and a short `CODE_OF_CONDUCT.md` referencing subpackages.

---

AI Usage Protections Task – Kickoff (2025-10-03)

Objective
- Add explicit AI/ML usage restrictions and crawler directives to discourage model training on repository content.

Scope
- Create `AI_USE_POLICY.md` with a clear prohibition on AI/ML training, dataset creation, and embedding extraction without a separate license.
- Add `robots.txt` and `ai.txt` for future GitHub Pages hosting; document platform limitations for GitHub repository crawling.
- Update `README.md` to link the policy and note the prohibition.

Notes
- Root license remains CC BY-NC 4.0; AI policy clarifies that no rights are granted for AI/ML uses. For enforceable field-of-use restrictions beyond CC, consider dual-licensing on request.

AI Usage Protections – Completion (2025-10-03)
- Added `AI_USE_POLICY.md` prohibiting AI/ML training, dataset creation, and embedding extraction without separate license.
- Added advisory `robots.txt` and `ai.txt` (for GitHub Pages; GitHub repos do not honor per-repo robots).
- Updated `README.md` with AI/automation notice and policy links.
- Next: If hosting on Pages, ensure these files are served from site root.

---

GitHub Publishing – Kickoff (2025-10-03)

Objective
- Publish this repository to GitHub at `UFRFv2` with history initialized and documentation/licensing included.

Scope
- Add minimal `.gitignore` (Python, macOS, notebooks, build artifacts).
- Initialize git, commit initial contents, create remote repo `UFRFv2`, and push `main`.
- Confirm README and LICENSE render correctly.

Notes
- Prefer `gh repo create` for non-interactive creation; fallback to manual remote if needed.

