# Strength Based Interview Guide Design

## Goal

Publish the supplied strength based interview article as a MockBase guide, expose it through the guide index and related-guide navigation, and add its public URL to the sitemap.

## Page

- Create `guides/interview/strength-based-interview.html`.
- Follow the structure, typography, navigation, metadata, favicon links, callouts, examples, CTA, related guides, and source section used by the existing interview guides.
- Use the supplied article as the editorial source while converting plain-text examples and numbered material into semantic HTML.
- Use the title `How to Answer Strength Based Interview Questions` and a concise search description matching the article.
- Link the CTA to the relevant MockBase behavioural interview practice tool and the main guide index.

## Navigation

- Add the new page to the Interview Preparation section of `guides/index.html`.
- Add relevant reciprocal links from the behavioural, competency, and Civil Service behaviour guides where their existing Related guides sections support the new article.
- Keep link labels consistent with the existing sentence-case style.

## Sitemap

- Add `https://mockbase.app/guides/interview/strength-based-interview.html` to `sitemap.xml` with `lastmod` set to `2026-07-04`.
- Update the guide index sitemap entry to the same date because its public content changes.
- Use only `loc` and `lastmod`; do not add `priority` or `changefreq`.

## Verification

- Validate the changed HTML and XML structurally.
- Confirm the new guide is linked from the index and included once in the sitemap.
- Confirm the sitemap contains no `priority` or `changefreq` elements.
- Confirm all related local guide targets exist.
- This repository is a static site with no package or production-build command, so verification does not include a build.

## Scope

No layout redesign, stylesheet changes, or unrelated content edits are included.
