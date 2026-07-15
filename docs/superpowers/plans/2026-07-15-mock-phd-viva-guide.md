# Mock PhD Viva Guide Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Publish the supplied mock PhD viva article and connect it to MockBase's guide index, related PhD guides, and sitemap.

**Architecture:** Add one standalone static HTML article that reuses the existing guide stylesheet and navigation. Connect it through the guide index, three reciprocal related-guide sections, and the sitemap. Validate the source artifact and rendered page directly because this repository has no build system.

**Tech Stack:** HTML5, JSON-LD, shared CSS, XML sitemap, xmllint, shell assertions, local HTTP server, browser-based responsive QA.

## Global Constraints

- Create guides/phd/mock-viva.html from /Users/yutian.tang/.codex/attachments/efd044a0-3bb3-41f6-b8fc-e039992e0264/pasted-text.txt.
- Preserve the supplied title, meta description, canonical URL, Article JSON-LD, FAQ JSON-LD, editorial content, CTA, related links, and official sources.
- Use the label “How to run a mock PhD viva” in the guide index and all three reciprocal links.
- Use 2026-07-15 for every new or changed sitemap entry.
- Do not modify CSS, add JavaScript, rewrite the guide, deploy the site, or make unrelated edits.

---

### Task 1: Add the mock PhD viva article

**Files:**
- Create: guides/phd/mock-viva.html
- Source: /Users/yutian.tang/.codex/attachments/efd044a0-3bb3-41f6-b8fc-e039992e0264/pasted-text.txt

**Interfaces:**
- Consumes: guides/poststyles.css, shared favicon assets, current navigation URLs, and the supplied 508-line HTML document.
- Produces: /guides/phd/mock-viva.html with Article and FAQ structured data.

- [ ] **Step 1: Run the failing route check**

    test -f guides/phd/mock-viva.html

Expected: exit code 1 because the route does not exist.

- [ ] **Step 2: Add the supplied document without editorial changes**

Use apply_patch to create guides/phd/mock-viva.html with the exact complete source attachment. Preserve these exact metadata values:

    <title>Mock PhD Viva: Questions, Structure and Feedback | MockBase</title>
    <meta name="description" content="Learn how to run a realistic mock PhD viva, choose examiner questions, practise follow ups, score weak answers, and turn feedback into a final preparation plan.">
    <link rel="canonical" href="https://mockbase.app/guides/phd/mock-viva.html">
    <link rel="stylesheet" href="../poststyles.css">

- [ ] **Step 3: Validate the article and required content**

    xmllint --html --noout guides/phd/mock-viva.html
    test "$(rg -c '"@type": "Article"' guides/phd/mock-viva.html)" -eq 1
    test "$(rg -c '"@type": "FAQPage"' guides/phd/mock-viva.html)" -eq 1
    rg -q '<h2>4\. A 60 minute mock viva structure</h2>' guides/phd/mock-viva.html
    rg -q '<h2>7\. Score the answer, not the candidate</h2>' guides/phd/mock-viva.html
    rg -q '<h2>10\. A seven day mock viva repair plan</h2>' guides/phd/mock-viva.html

Expected: exit code 0; HTML parses and all assertions pass.

- [ ] **Step 4: Commit the standalone article**

    git add guides/phd/mock-viva.html
    git commit -m "Add mock PhD viva guide"

### Task 2: Add guide-index and reciprocal discovery links

**Files:**
- Modify: guides/index.html
- Modify: guides/phd/phd-viva-preparation.html
- Modify: guides/phd/thesis-defence-preparation.html
- Modify: guides/phd/viva-questions.html

**Interfaces:**
- Consumes: /guides/phd/mock-viva.html from Task 1.
- Produces: one guide-index entry and one reciprocal related-guide link from each existing PhD guide.

- [ ] **Step 1: Run failing discovery-link checks**

    test "$(rg -c 'mock-viva\.html' guides/index.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/phd-viva-preparation.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/thesis-defence-preparation.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/viva-questions.html)" -eq 1

Expected: the first command exits 1, proving the new guide has no discovery links.

- [ ] **Step 2: Add the guide-index entry**

Insert after “How to prepare for a PhD viva”:

    <li><a href="./phd/mock-viva.html">How to run a mock PhD viva</a></li>

- [ ] **Step 3: Add reciprocal related-guide links**

Insert once inside each existing page's related section:

    <a href="https://mockbase.app/guides/phd/mock-viva.html">How to run a mock PhD viva</a>

- [ ] **Step 4: Validate modified HTML and link counts**

    for file in guides/index.html guides/phd/phd-viva-preparation.html guides/phd/thesis-defence-preparation.html guides/phd/viva-questions.html; do xmllint --html --noout "$file" || exit 1; done
    test "$(rg -c 'mock-viva\.html' guides/index.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/phd-viva-preparation.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/thesis-defence-preparation.html)" -eq 1
    test "$(rg -c 'mock-viva\.html' guides/phd/viva-questions.html)" -eq 1
    test "$(rg -l 'How to run a mock PhD viva' guides/index.html guides/phd/*.html | wc -l | tr -d ' ')" -eq 4

Expected: exit code 0 and exactly one discovery link on every intended page.

- [ ] **Step 5: Commit discovery links**

    git add guides/index.html guides/phd/phd-viva-preparation.html guides/phd/thesis-defence-preparation.html guides/phd/viva-questions.html
    git commit -m "Link mock PhD viva guide"

### Task 3: Register public routes in the sitemap

**Files:**
- Modify: sitemap.xml

**Interfaces:**
- Consumes: the new route and four changed discovery pages.
- Produces: one unique sitemap entry and current modification dates for all changed public pages.

- [ ] **Step 1: Run the failing sitemap assertion**

    test "$(rg -c 'guides/phd/mock-viva\.html' sitemap.xml)" -eq 1

Expected: exit code 1 because the new route is not registered.

- [ ] **Step 2: Add the new sitemap entry**

    <url>
      <loc>https://mockbase.app/guides/phd/mock-viva.html</loc>
      <lastmod>2026-07-15</lastmod>
    </url>

- [ ] **Step 3: Update changed sitemap dates**

Set 2026-07-15 for these existing entries:

    https://mockbase.app/guides/
    https://mockbase.app/guides/phd/phd-viva-preparation.html
    https://mockbase.app/guides/phd/thesis-defence-preparation.html
    https://mockbase.app/guides/phd/viva-questions.html

- [ ] **Step 4: Validate sitemap invariants**

    xmllint --noout sitemap.xml
    test "$(rg -c 'guides/phd/mock-viva\.html' sitemap.xml)" -eq 1
    test "$(rg -c '<lastmod>2026-07-15</lastmod>' sitemap.xml)" -eq 5
    ! rg -q '<priority>|<changefreq>' sitemap.xml

Expected: exit code 0; XML parses, the route is unique, five affected entries use the new date, and unsupported fields remain absent.

- [ ] **Step 5: Commit the sitemap update**

    git add sitemap.xml
    git commit -m "Register mock PhD viva guide in sitemap"

### Task 4: Verify the complete static-site change

**Files:**
- Verify: guides/phd/mock-viva.html
- Verify: guides/index.html
- Verify: guides/phd/phd-viva-preparation.html
- Verify: guides/phd/thesis-defence-preparation.html
- Verify: guides/phd/viva-questions.html
- Verify: sitemap.xml

**Interfaces:**
- Consumes: the complete integrated guide.
- Produces: structural, navigation, responsive-rendering, and repository evidence for handoff.

- [ ] **Step 1: Run full structural verification**

    for file in guides/phd/mock-viva.html guides/index.html guides/phd/phd-viva-preparation.html guides/phd/thesis-defence-preparation.html guides/phd/viva-questions.html; do xmllint --html --noout "$file" || exit 1; done
    xmllint --noout sitemap.xml
    git diff HEAD~3 --check

Expected: exit code 0 with no parsing or whitespace errors.

- [ ] **Step 2: Verify every local target used by the new page**

    test -f guides/poststyles.css
    test -f favicon/favicon-96x96.png
    test -f favicon/favicon.svg
    test -f favicon/favicon.ico
    test -f favicon/apple-touch-icon.png
    test -f favicon/site.webmanifest
    test -f guides/phd/phd-viva-preparation.html
    test -f guides/phd/viva-questions.html
    test -f guides/phd/thesis-defence-preparation.html

Expected: exit code 0.

- [ ] **Step 3: Verify desktop and mobile rendering**

Start a local server at the repository root. Open /guides/phd/mock-viva.html at desktop width and approximately 390 × 844 mobile width. Confirm navigation readability, no title or article overflow, intact callout/example blocks, clean list and heading wrapping, visible CTA links, and readable related/source links. Capture and inspect the latest screenshot directly.

- [ ] **Step 4: Verify the core navigation path**

Open /guides/index.html, select “How to run a mock PhD viva”, and confirm it reaches /guides/phd/mock-viva.html. Open one existing PhD guide and confirm its reciprocal link reaches the same page.

- [ ] **Step 5: Review repository scope**

    git status --short
    git log -5 --oneline

Expected: a clean working tree and only the intended design, plan, article, discovery-link, and sitemap commits.
