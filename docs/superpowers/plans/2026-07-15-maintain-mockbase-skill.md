# Maintain Mockbase Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create, install, and independently validate a reusable `maintain-mockbase` Codex Skill for evidence-led Mockbase strategy, publishing, compliance, and static-site verification.

**Architecture:** Install the Skill directly in `~/.codex/skills/maintain-mockbase`. Keep decision guidance in a concise `SKILL.md`, move stable project facts into three references, and enforce mechanical repository invariants through one read-only Python validator with standard-library tests.

**Tech Stack:** Markdown, YAML, Python 3.11 standard library, `unittest`, `xmllint`, Codex Skill Creator scripts, Git.

## Global Constraints

- Install at `/Users/yutian.tang/.codex/skills/maintain-mockbase`.
- Keep YAML frontmatter limited to `name` and `description`.
- Use only `display_name`, `short_description`, and `default_prompt` in `agents/openai.yaml`.
- Keep the validator read-only and network-free.
- Do not modify Mockbase production pages or deploy the site.
- Preserve unrelated working-tree changes.
- Use authoritative primary sources for academic, policy, assessment, or professional claims.
- Require market validation before designing a new Mockbase product, template, course, or system.

---

### Task 1: Establish the no-Skill baseline

**Files:**
- Read: `/Users/yutian.tang/Documents/GitHub/mockbase/**`
- Do not create persistent files.

**Interfaces:**
- Consumes: Three realistic read-only Mockbase prompts and the existing repository.
- Produces: Verbatim baseline outputs plus a short list of observed omissions used to shape `SKILL.md`.

- [ ] **Step 1: Dispatch three independent baseline scenarios without mentioning the new Skill**

Use fresh subagents with these exact prompts:

```text
In /Users/yutian.tang/Documents/GitHub/mockbase, evaluate whether Mockbase should build an NHS interview simulator. Return an evidence-led recommendation with validation metrics and stopping conditions. Make no file changes.
```

```text
In /Users/yutian.tang/Documents/GitHub/mockbase, outline the complete change required to publish a new UK Civil Service strengths interview guide. Identify sources, files, integration surfaces, and verification. Make no file changes.
```

```text
In /Users/yutian.tang/Documents/GitHub/mockbase, review a proposal to claim that the simulator uses official UK Civil Service scoring and to load analytics before cookie consent. Identify blockers and safer alternatives. Make no file changes.
```

- [ ] **Step 2: Record the exact outputs in the parent-agent transcript**

Expected: At least one response omits a Mockbase-specific requirement such as resource leverage, lowest-cost market validation, reciprocal discovery links, sitemap dates, official-source hierarchy, consent-gated analytics, non-affiliation language, or a stopping condition.

- [ ] **Step 3: Classify failures before authoring guidance**

Use this fixed structure in the transcript:

```text
Baseline failure | Failure type | Required Skill response
omitted required output | structural | add a required slot/checklist item
unsafe project decision | discipline | add a hard gate and red flag
missing repository fact | retrieval | route to the relevant reference
```

Do not create the Skill until the baseline failure is observed.

---

### Task 2: Initialize the installed Skill and build the validator with TDD

**Files:**
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/SKILL.md`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/agents/openai.yaml`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/scripts/test_validate_mockbase.py`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/scripts/validate_mockbase.py`
- Create directory: `/Users/yutian.tang/.codex/skills/maintain-mockbase/references`

**Interfaces:**
- Consumes: A filesystem root containing a Mockbase-like static site.
- Produces: `validate(root: Path) -> list[str]` and CLI exit code `0` for no errors, `1` for validation errors, `2` for invalid CLI usage.

- [ ] **Step 1: Initialize the Skill with deterministic UI metadata**

Run:

```bash
python3 /Users/yutian.tang/.codex/skills/.system/skill-creator/scripts/init_skill.py maintain-mockbase \
  --path /Users/yutian.tang/.codex/skills \
  --resources scripts,references \
  --interface 'display_name=Maintain Mockbase' \
  --interface 'short_description=Operate Mockbase with evidence and safeguards' \
  --interface 'default_prompt=Use $maintain-mockbase to assess and implement this Mockbase repository change safely.'
```

Expected: the Skill directory, template `SKILL.md`, `agents/openai.yaml`, and empty resource directories exist.

- [ ] **Step 2: Write failing validator tests**

Create `scripts/test_validate_mockbase.py` with `unittest`. Build a minimal valid temporary site containing `index.html`, `about.html`, `contact.html`, `privacy.html`, `terms.html`, `cookies.html`, `styles.css`, `sitemap.xml`, both guide stylesheets, `guides/index.html`, and six favicon files. Assert:

```python
from validate_mockbase import validate

def test_valid_site_has_no_errors(self):
    self.assertEqual(validate(self.root), [])

def test_missing_required_file_is_reported(self):
    (self.root / "privacy.html").unlink()
    self.assertIn("missing required file: privacy.html", validate(self.root))

def test_broken_local_link_is_reported(self):
    self.write("about.html", '<a href="missing.html">Missing</a>')
    self.assertTrue(any("broken local link" in error for error in validate(self.root)))

def test_duplicate_sitemap_url_is_reported(self):
    self.write_sitemap(["https://mockbase.app/", "https://mockbase.app/"])
    self.assertIn("duplicate sitemap URL: https://mockbase.app/", validate(self.root))

def test_unsupported_sitemap_field_is_reported(self):
    self.write_sitemap(["https://mockbase.app/"], extra="<priority>1.0</priority>")
    self.assertIn("unsupported sitemap field: priority", validate(self.root))

def test_non_mockbase_canonical_is_reported(self):
    self.write("about.html", '<link rel="canonical" href="https://example.com/about.html">')
    self.assertTrue(any("invalid canonical origin" in error for error in validate(self.root)))

def test_invalid_json_ld_is_reported(self):
    self.write("about.html", '<script type="application/ld+json">{bad}</script>')
    self.assertTrue(any("invalid JSON-LD" in error for error in validate(self.root)))

def test_missing_independence_boundary_is_reported(self):
    self.write("index.html", "<html><body>products</body></html>")
    self.assertIn("index.html: missing non-affiliation boundary", validate(self.root))
```

- [ ] **Step 3: Run tests and verify RED**

Run:

```bash
cd /Users/yutian.tang/.codex/skills/maintain-mockbase/scripts
python3 -m unittest -v test_validate_mockbase.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'validate_mockbase'`.

- [ ] **Step 4: Implement the minimal read-only validator**

In `validate_mockbase.py`, implement:

```python
REQUIRED_FILES = (
    "index.html", "about.html", "contact.html", "privacy.html", "terms.html",
    "cookies.html", "styles.css", "sitemap.xml", "guides/index.html",
    "guides/styles.css", "guides/poststyles.css", "favicon/favicon-96x96.png",
    "favicon/favicon.svg", "favicon/favicon.ico", "favicon/apple-touch-icon.png",
    "favicon/site.webmanifest", "favicon/web-app-manifest-192x192.png",
    "favicon/web-app-manifest-512x512.png",
)

def validate(root: Path) -> list[str]:
    """Return stable, sorted validation errors without modifying root."""

def main(argv: Sequence[str] | None = None) -> int:
    """Print errors and return 0, 1, or 2."""
```

Use `xml.etree.ElementTree` for `sitemap.xml`, `html.parser.HTMLParser` for `href`, `src`, canonical, and JSON-LD extraction, `json.loads` for JSON-LD, `urllib.parse.urlsplit` for URL classification, and `subprocess.run(["xmllint", "--html", "--noout", file])` when `xmllint` exists. Treat only `index.html` and `terms.html` as mandatory non-affiliation boundary pages. Ignore external, `mailto:`, `tel:`, `data:`, and fragment-only links. Map `/` and directory URLs to `index.html`.

- [ ] **Step 5: Run tests and verify GREEN**

Run:

```bash
cd /Users/yutian.tang/.codex/skills/maintain-mockbase/scripts
python3 -m unittest -v test_validate_mockbase.py
```

Expected: all tests pass with `OK`.

- [ ] **Step 6: Run the validator on the real repository**

Run:

```bash
python3 /Users/yutian.tang/.codex/skills/maintain-mockbase/scripts/validate_mockbase.py /Users/yutian.tang/Documents/GitHub/mockbase
```

Expected after inspecting the repository: exit code `1` with five pre-existing nested-guide favicon path failures. Preserve these findings as the baseline; do not weaken the validator or modify production pages within this Skill task.

---

### Task 3: Author the minimal Skill and project references

**Files:**
- Modify: `/Users/yutian.tang/.codex/skills/maintain-mockbase/SKILL.md`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/references/project-model.md`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/references/publishing-rules.md`
- Create: `/Users/yutian.tang/.codex/skills/maintain-mockbase/references/opportunity-validation.md`

**Interfaces:**
- Consumes: The baseline failure classification and current Mockbase repository facts.
- Produces: Trigger-optimized operating instructions and three directly linked references.

- [ ] **Step 1: Replace the generated template with trigger-only frontmatter**

Use exactly:

```yaml
---
name: maintain-mockbase
description: Use when working on the Mockbase repository or brand, including assessment-product opportunities, market validation, preparation guides, static HTML, SEO, JSON-LD, internal links, sitemaps, privacy, non-affiliation language, or release verification.
---
```

- [ ] **Step 2: Write the concise core workflow**

Require this output contract for opportunity work:

```text
Verdict → demand evidence → named competitors → underserved user/job →
borrowed Mockbase resources → cheapest experiment → metric/review date → stop condition
```

Require this contract for publishing work:

```text
official sources → target page → metadata/JSON-LD → index and reciprocal links →
sitemap → privacy/non-affiliation boundaries → failing checks → implementation → full verification
```

Direct the agent to read exactly one or more of the three references according to the task, run `scripts/validate_mockbase.py <repo>`, preserve unrelated changes, avoid deployment without authorization, and use a browser for responsive visual QA when public pages change.

- [ ] **Step 3: Write `references/project-model.md`**

Document these stable facts:

- Mockbase is a lightweight hub for structured practice in high-stakes assessments.
- Primary users include doctoral candidates, academic applicants, grant applicants, UK public-sector applicants, international students, and professionals.
- Live tracks are faculty, PhD viva, behavioural, grant, and UK Civil Service; TOEFL and IELTS are coming soon; Life in the UK is planned.
- The hub is static HTML/CSS with no build system; product apps live on separate domains.
- Reusable assets are brand trust, official-source guides, question banks, answer frameworks, guide-to-product links, waitlist, preview funnel, local progress tracking, analytics with consent, and public search data.
- Preserve independence, trademark, preparation-only, no-guarantee, privacy, consent, and local-storage boundaries.

- [ ] **Step 4: Write `references/publishing-rules.md`**

Document source priority, guide anatomy, canonical/metadata/JSON-LD rules, relative paths, index and reciprocal discovery, sitemap uniqueness and dates, CTA alignment, local-link resolution, HTML/XML checks, `git diff --check`, responsive QA, and prohibited unrequested redesign/deployment.

- [ ] **Step 5: Write `references/opportunity-validation.md`**

Document the required market fields: demand and search intent, competition, blue-ocean test, pain, willingness to pay, target user, differentiation, borrowed resources, minimum experiment, metric, review date, and stop condition. Include the example of validating one authoritative guide plus one preview/waitlist CTA before building a simulator.

- [ ] **Step 6: Check content quality**

Run:

```bash
wc -l /Users/yutian.tang/.codex/skills/maintain-mockbase/SKILL.md
rg -n 'TODO|TBD|FIXME|XXX' /Users/yutian.tang/.codex/skills/maintain-mockbase
```

Expected: `SKILL.md` is below 500 lines and the placeholder scan returns no matches.

---

### Task 4: Validate discovery metadata and forward-test behavior

**Files:**
- Verify: `/Users/yutian.tang/.codex/skills/maintain-mockbase/**`
- Modify only if a test exposes a real gap.

**Interfaces:**
- Consumes: Installed Skill, references, validator, and the three baseline scenarios.
- Produces: Valid Skill metadata, passing validator tests, and independent evidence that the Skill changes behavior correctly.

- [ ] **Step 1: Run structural Skill validation**

Run:

```bash
python3 /Users/yutian.tang/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/yutian.tang/.codex/skills/maintain-mockbase
```

Expected: `Skill is valid!`.

- [ ] **Step 2: Inspect `agents/openai.yaml`**

Assert:

```bash
rg -q 'display_name: "Maintain Mockbase"' /Users/yutian.tang/.codex/skills/maintain-mockbase/agents/openai.yaml
rg -q 'short_description: "Operate Mockbase with evidence and safeguards"' /Users/yutian.tang/.codex/skills/maintain-mockbase/agents/openai.yaml
rg -Fq 'Use $maintain-mockbase' /Users/yutian.tang/.codex/skills/maintain-mockbase/agents/openai.yaml
```

Expected: exit code `0`.

- [ ] **Step 3: Run the three equivalent GREEN scenarios in fresh subagents**

Prefix each Task 1 prompt with:

```text
Use $maintain-mockbase at /Users/yutian.tang/.codex/skills/maintain-mockbase.
```

Expected:

- Opportunity output contains every required contract field and does not jump to product development.
- Publishing output names official sources, route, metadata, JSON-LD decision, guide index, reciprocal links, sitemap, failing checks, validator, and visual QA.
- Safety output rejects official-affiliation claims and pre-consent analytics, then offers non-affiliated and consent-gated alternatives.

- [ ] **Step 4: Refactor only for observed forward-test gaps**

If a required field is omitted, add it as a structural slot in the relevant quick-reference table. If an unsafe shortcut appears, add the exact shortcut to the red-flags section. Do not add speculative guidance.

- [ ] **Step 5: Re-run all gates after any refactor**

Run:

```bash
cd /Users/yutian.tang/.codex/skills/maintain-mockbase/scripts
python3 -m unittest -v test_validate_mockbase.py
python3 validate_mockbase.py /Users/yutian.tang/Documents/GitHub/mockbase
python3 /Users/yutian.tang/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/yutian.tang/.codex/skills/maintain-mockbase
```

Expected: tests report `OK`, Skill validation reports `Skill is valid!`, and repository validation reports only the five documented pre-existing favicon path failures. Any additional repository error is a regression and must be resolved before handoff.

- [ ] **Step 6: Verify installation and file hygiene**

Run:

```bash
find /Users/yutian.tang/.codex/skills/maintain-mockbase -maxdepth 3 -type f -print | sort
git -C /Users/yutian.tang/Documents/GitHub/mockbase status --short
```

Expected: only `SKILL.md`, `agents/openai.yaml`, three reference files, the validator, and its test are installed; the Mockbase repository contains only the committed design and plan changes.

---

### Task 5: Complete installation handoff

**Files:**
- Verify: `/Users/yutian.tang/.codex/skills/maintain-mockbase/**`
- Verify: `/Users/yutian.tang/Documents/GitHub/mockbase/**`

**Interfaces:**
- Consumes: Passing implementation and forward-test evidence.
- Produces: A concise installation handoff with current verification evidence.

- [ ] **Step 1: Run final repository checks**

Run:

```bash
git -C /Users/yutian.tang/Documents/GitHub/mockbase diff --check
git -C /Users/yutian.tang/Documents/GitHub/mockbase status --short
```

Expected: no whitespace errors and a clean Mockbase working tree. The installed Skill is outside this repository and is therefore reported separately rather than staged here.

- [ ] **Step 2: Report the installed entry point and verification evidence**

Report `/Users/yutian.tang/.codex/skills/maintain-mockbase/SKILL.md`, the passing unit-test count, real-repository validator result, `quick_validate.py` result, forward-test outcomes, and any limitations discovered.
