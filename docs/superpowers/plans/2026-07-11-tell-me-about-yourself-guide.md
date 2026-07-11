# Tell Me About Yourself Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a general-purpose guide explaining how to answer “Tell me about yourself” and connect it to MockBase’s interview guide and practice ecosystem.

**Architecture:** Add one standalone static HTML article using the existing interview-guide template, then expose it through the guide index, reciprocal related-guide links, and the XML sitemap. Validate the static artifact directly because the repository has no package manifest or build command.

**Tech Stack:** HTML5, CSS shared through `guides/poststyles.css`, XML sitemap, shell-based structural checks, GitHub Pages.

## Global Constraints

- Publish at `guides/interview/tell-me-about-yourself.html`.
- Use the `Present → Relevant past → Future fit` framework.
- Include 30-, 60-, and 90-second guidance plus recent graduate, experienced candidate, career changer, and management examples.
- Do not redesign the site, change stylesheets, add JavaScript, or include unrelated copy edits.
- Use `2026-07-11` for new and changed public sitemap entries.
- Keep `.DS_Store` files outside staging and commits.
- Publish directly from `main` as explicitly requested by the user.

---

### Task 1: Add the interview guide

**Files:**
- Create: `guides/interview/tell-me-about-yourself.html`

**Interfaces:**
- Consumes: shared styles from `../poststyles.css` and existing MockBase navigation URLs.
- Produces: the public route `/guides/interview/tell-me-about-yourself.html` for the index, related guides, and sitemap.

- [ ] **Step 1: Confirm the route does not already exist**

Run: `test ! -e guides/interview/tell-me-about-yourself.html`
Expected: exit code 0.

- [ ] **Step 2: Create the semantic article**

Create a complete HTML5 document with the title `How to Answer “Tell Me About Yourself” in an Interview | MockBase Guide`, a unique meta description, shared favicon/navigation markup, and these content units in order: purpose of the question; Present–Relevant past–Future fit framework; 30/60/90-second variants; tailoring method; four full candidate examples; common mistakes; worksheet; spoken practice method; final checklist; FAQ; practice CTA; related guides; preparation sources.

- [ ] **Step 3: Check required article content**

Run: `rg -n "Present|Relevant past|Future fit|30 seconds|60 seconds|90 seconds|Recent graduate|Experienced candidate|Career changer|Management candidate|Related guides|Preparation sources" guides/interview/tell-me-about-yourself.html`
Expected: every required content unit has at least one match.

- [ ] **Step 4: Validate document structure**

Run: `xmllint --html --noout guides/interview/tell-me-about-yourself.html`
Expected: exit code 0 with no structural errors.

### Task 2: Connect navigation and internal links

**Files:**
- Modify: `guides/index.html`
- Modify: `guides/interview/behavioural-interview.html`
- Modify: `guides/interview/competency-interview.html`
- Modify: `guides/interview/strength-based-interview.html`
- Modify: `guides/interview/leadership-interview.html`

**Interfaces:**
- Consumes: the new public route from Task 1.
- Produces: one guide-index entry and four reciprocal discovery links.

- [ ] **Step 1: Add the guide-index entry**

Add `<li><a href="./interview/tell-me-about-yourself.html">How to answer “Tell me about yourself” in an interview</a></li>` as the first item under Interview Preparation.

- [ ] **Step 2: Add reciprocal related-guide links**

Add `<a href="https://mockbase.app/guides/interview/tell-me-about-yourself.html">How to answer “Tell me about yourself” in an interview</a>` once inside each relevant page’s existing `Related guides` section.

- [ ] **Step 3: Verify link counts and targets**

Run: `rg -l "tell-me-about-yourself.html" guides/index.html guides/interview/*.html | wc -l`
Expected: `5` files: the index and four existing interview guides. The new guide links to related pages rather than to itself.

### Task 3: Update the sitemap

**Files:**
- Modify: `sitemap.xml`

**Interfaces:**
- Consumes: every public route changed in Tasks 1–2.
- Produces: search-engine discovery metadata for the new and changed pages.

- [ ] **Step 1: Update changed entries**

Set the guide index and the four reciprocally linked interview guides to `<lastmod>2026-07-11</lastmod>`. Add one URL entry for `https://mockbase.app/guides/interview/tell-me-about-yourself.html` with the same date.

- [ ] **Step 2: Validate sitemap XML**

Run: `xmllint --noout sitemap.xml`
Expected: exit code 0.

- [ ] **Step 3: Check sitemap invariants**

Run: `test "$(rg -c 'guides/interview/tell-me-about-yourself.html' sitemap.xml)" -eq 1 && ! rg -q '<priority>|<changefreq>' sitemap.xml`
Expected: exit code 0.

### Task 4: Verify and publish

**Files:**
- Verify: all files changed by Tasks 1–3.

**Interfaces:**
- Consumes: the complete static-site change.
- Produces: validated content committed and pushed to `origin/main`.

- [ ] **Step 1: Run changed-page local-link validation**

Run a script that extracts relative `href` values from the new guide, guide index, and four modified interview guides, resolves each path against its source file, and fails when a changed-page local target is missing.
Expected: zero missing local targets.

- [ ] **Step 2: Review the final diff**

Run: `git diff --check && git diff --stat && git status --short`
Expected: no whitespace errors; only the plan, new guide, intended index/related pages, sitemap, and the pre-existing unstaged `.DS_Store` appear.

- [ ] **Step 3: Commit only intended files**

Stage the implementation plan, article, guide index, four related guides, and sitemap by explicit path, then commit with `Add tell me about yourself interview guide`.

- [ ] **Step 4: Push production branch**

Run: `git push origin main`
Expected: `main -> main` succeeds and GitHub Pages can publish the updated static files.
