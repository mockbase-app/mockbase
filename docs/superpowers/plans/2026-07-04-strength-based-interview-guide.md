# Strength Based Interview Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a formatted strength based interview guide and make it discoverable through MockBase navigation and the sitemap.

**Architecture:** Add one static HTML article that follows the existing interview-guide template. Update the static guide index, reciprocal related-guide sections, and XML sitemap without changing shared styles or runtime behavior.

**Tech Stack:** Static HTML5, CSS references, XML sitemap, shell-based structural verification

---

## File Structure

- Create `guides/interview/strength-based-interview.html`: complete public article and its page-specific metadata, navigation, CTA, related links, and sources.
- Modify `guides/index.html`: add the guide to the Interview Preparation list.
- Modify `guides/interview/behavioural-interview.html`: add a reciprocal related-guide link.
- Modify `guides/interview/competency-interview.html`: add a reciprocal related-guide link.
- Modify `guides/civil-service/civil-service-behaviour-questions.html`: add a reciprocal related-guide link.
- Modify `sitemap.xml`: update the guide index date and add the new canonical public URL.

### Task 1: Create the guide page

**Files:**
- Create: `guides/interview/strength-based-interview.html`

- [ ] **Step 1: Create semantic article HTML**

Use `guides/interview/behavioural-interview.html` as the structural template. Set the title to `How to Answer Strength Based Interview Questions | MockBase Guide`, include a matching meta description, convert all 13 supplied sections into paragraphs, lists, `.callout`, and `.example` blocks, and finish with the standard MockBase CTA, related guides, and cited preparation sources.

- [ ] **Step 2: Check required page elements**

Run:

```bash
rg -n '<title>|meta name="description"|<h1>|Core idea:|Practise strength based|Related guides|Preparation sources' guides/interview/strength-based-interview.html
```

Expected: each named page element appears once in the output.

- [ ] **Step 3: Check local links from the new page**

Run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

page = Path('guides/interview/strength-based-interview.html')
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if href.startswith('https://mockbase.app/guides/') and href.endswith('.html'):
                self.links.append(href)
parser = Links()
parser.feed(page.read_text())
missing = [url for url in parser.links if not Path(url.removeprefix('https://mockbase.app/')).exists()]
assert not missing, missing
print(f'PASS: {len(parser.links)} guide links resolve')
PY
```

Expected: `PASS` and no missing paths.

### Task 2: Add navigation and reciprocal links

**Files:**
- Modify: `guides/index.html`
- Modify: `guides/interview/behavioural-interview.html`
- Modify: `guides/interview/competency-interview.html`
- Modify: `guides/civil-service/civil-service-behaviour-questions.html`

- [ ] **Step 1: Add the index entry**

Add this item to the Interview Preparation list:

```html
<li><a href="./interview/strength-based-interview.html">How to answer strength based interview questions</a></li>
```

- [ ] **Step 2: Add reciprocal related-guide links**

Add this link inside each listed article's existing `<section class="related">`:

```html
<a href="https://mockbase.app/guides/interview/strength-based-interview.html">How to answer strength based interview questions</a>
```

- [ ] **Step 3: Verify discovery links**

Run:

```bash
rg -l 'strength-based-interview\.html' guides/index.html guides/interview/behavioural-interview.html guides/interview/competency-interview.html guides/civil-service/civil-service-behaviour-questions.html
```

Expected: all four file paths are printed.

### Task 3: Update and validate the sitemap

**Files:**
- Modify: `sitemap.xml`

- [ ] **Step 1: Update the index entry and add the article entry**

Set the existing `https://mockbase.app/guides/` entry's `lastmod` to `2026-07-04` and add:

```xml
<url>
  <loc>https://mockbase.app/guides/interview/strength-based-interview.html</loc>
  <lastmod>2026-07-04</lastmod>
</url>
```

- [ ] **Step 2: Validate XML and sitemap constraints**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
from xml.etree import ElementTree as ET

text = Path('sitemap.xml').read_text()
ET.fromstring(text)
url = 'https://mockbase.app/guides/interview/strength-based-interview.html'
assert text.count(url) == 1
assert '<priority>' not in text
assert '<changefreq>' not in text
print('PASS: sitemap is valid and contains the new route once')
PY
```

Expected: `PASS: sitemap is valid and contains the new route once`.

### Task 4: Final verification

**Files:**
- Verify: `guides/interview/strength-based-interview.html`
- Verify: `guides/index.html`
- Verify: `guides/interview/behavioural-interview.html`
- Verify: `guides/interview/competency-interview.html`
- Verify: `guides/civil-service/civil-service-behaviour-questions.html`
- Verify: `sitemap.xml`

- [ ] **Step 1: Check whitespace errors**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 2: Parse every changed HTML file**

Run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path

files = [
    Path('guides/interview/strength-based-interview.html'),
    Path('guides/index.html'),
    Path('guides/interview/behavioural-interview.html'),
    Path('guides/interview/competency-interview.html'),
    Path('guides/civil-service/civil-service-behaviour-questions.html'),
]
for file in files:
    parser = HTMLParser()
    parser.feed(file.read_text())
print(f'PASS: parsed {len(files)} HTML files')
PY
```

Expected: `PASS: parsed 5 HTML files`.

- [ ] **Step 3: Review final scope**

Run:

```bash
git status --short && git diff --stat
```

Expected: only the planned guide, index, related-guide, sitemap, and plan files appear, plus any unrelated pre-existing user changes such as `.DS_Store` that remain untouched.
