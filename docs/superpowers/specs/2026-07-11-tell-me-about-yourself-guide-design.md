# Tell Me About Yourself Interview Guide Design

## Goal

Publish a broadly useful interview guide targeting candidates searching for help answering “Tell me about yourself.” The guide should attract general interview-preparation traffic, give readers a practical answer framework, and lead them into MockBase’s related interview content and practice tools.

## Page

- Create `guides/interview/tell-me-about-yourself.html`.
- Use the title `How to Answer “Tell Me About Yourself” in an Interview`.
- Follow the metadata, navigation, typography, callout, example, checklist, CTA, related-guide, and source patterns used by the existing interview guides.
- Use a concise search description that mentions the answer framework, examples, and common mistakes.
- Keep the page self-contained and useful to candidates across industries and experience levels.

## Editorial Structure

- Explain what interviewers assess with this opening question.
- Teach a `Present → Relevant past → Future fit` answer framework.
- Show how to adapt the answer to approximately 30, 60, and 90 seconds.
- Provide complete examples for a recent graduate, an experienced candidate, a career changer, and a management candidate.
- Explain how to tailor the answer to a job description without repeating a CV.
- Cover common mistakes, including irrelevant personal history, excessive chronology, generic claims, memorised delivery, and answers without a role connection.
- Include a preparation worksheet, practice method, final checklist, and concise FAQ.
- Use original examples and wording; external sources support factual guidance but are not copied.

## Navigation and Internal Links

- Add the new page to the Interview Preparation section of `guides/index.html`.
- Link from the new page to the behavioural, competency, strength-based, and leadership interview guides where contextually useful.
- Add reciprocal links from relevant existing interview guides through their Related guides sections.
- Link the primary CTA to the most relevant live MockBase interview practice tool and include a secondary route back to the guide index.
- Keep link labels consistent with the existing sentence-case style.

## Sitemap

- Add `https://mockbase.app/guides/interview/tell-me-about-yourself.html` to `sitemap.xml` with `lastmod` set to `2026-07-11`.
- Update the guide index sitemap entry to the same date because its public content changes.
- Update `lastmod` for any existing guide receiving a reciprocal public link.
- Retain the sitemap’s existing `loc` and `lastmod` structure without adding `priority` or `changefreq`.

## Verification

- Validate changed HTML and XML structurally.
- Confirm the new guide is linked from the guide index and appears exactly once in the sitemap.
- Confirm every changed local guide link resolves to an existing file.
- Confirm the sitemap contains no `priority` or `changefreq` elements.
- Check that the page title and meta description are present and unique.
- Review the page at desktop and mobile widths for readable layout and intact navigation.
- This repository is a static site with no package manifest or production-build command, so the production artifact is the source HTML itself.

## Scope

No site redesign, stylesheet changes, JavaScript features, or unrelated copy edits are included. Generated `.DS_Store` files and unrelated working-tree changes remain outside the commit and push scope.
