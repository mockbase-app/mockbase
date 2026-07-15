# Mock PhD Viva Guide Integration Design

## Goal

Publish the supplied mock PhD viva guide as a first-class MockBase resource. The integration should make the article discoverable through the guide index, relevant PhD guide pages, and the public sitemap without changing the site's visual system or introducing new runtime behavior.

## Page

- Create `guides/phd/mock-viva.html` from the supplied complete HTML document.
- Preserve the title `Mock PhD Viva: Questions, Structure and Feedback | MockBase` and the supplied meta description.
- Preserve the canonical URL `https://mockbase.app/guides/phd/mock-viva.html`.
- Reuse `guides/poststyles.css`, the existing favicon assets, and the current MockBase navigation.
- Preserve the supplied Article and FAQ structured data, editorial sections, CTA, related-guide block, and official source links.
- Do not redesign the article, change shared stylesheets, add JavaScript, or rewrite the supplied editorial content.

## Navigation and Internal Links

- Add the new guide to the `PhD and Research Assessment` section of `guides/index.html`.
- Use the link label `How to run a mock PhD viva` so the index communicates the guide's practical purpose without duplicating its full SEO title.
- Add one reciprocal link to the existing Related guides section of each current PhD guide:
  - `guides/phd/phd-viva-preparation.html`
  - `guides/phd/thesis-defence-preparation.html`
  - `guides/phd/viva-questions.html`
- Use the reciprocal link label `How to run a mock PhD viva` consistently.
- Keep the new page's supplied links to the three existing PhD guides and the PhD Viva Practice App.

## Sitemap

- Add `https://mockbase.app/guides/phd/mock-viva.html` to `sitemap.xml`.
- Set its `lastmod` to `2026-07-15`.
- Update the guide index and the three modified PhD guide entries to `2026-07-15` because their public content changes.
- Preserve the sitemap's existing `loc` and `lastmod` structure without adding `priority` or `changefreq`.

## Data and Failure Handling

The site is a static HTML publication, so no application state or runtime data flow is introduced. The new article consumes only shared CSS and favicon assets. Failure risks are broken relative paths, duplicate sitemap entries, malformed HTML or XML, and inconsistent internal-link labels. Automated structural checks will fail the change before publication when any of these conditions occurs.

## Verification

- Start with failing checks proving that the new route, guide-index entry, reciprocal links, and sitemap entry do not yet exist.
- Validate the new page and all modified HTML files with `xmllint --html --noout`.
- Validate `sitemap.xml` with `xmllint --noout`.
- Confirm the new URL appears exactly once in the sitemap.
- Confirm the guide index and all three existing PhD guides link to the new route exactly once.
- Resolve every local link in the changed HTML pages and confirm that each target exists.
- Confirm the sitemap contains no `priority` or `changefreq` elements.
- Check the new page at desktop and mobile viewport widths, including navigation, typography, callouts, lists, CTA, related guides, and source links.
- Run `git diff --check` before completion.

## Scope

The change is limited to the supplied guide, the guide index, the three existing PhD guides, the sitemap, and the implementation documentation required by the project workflow. No site redesign, stylesheet change, JavaScript feature, unrelated copy edit, deployment, or broader PhD content-hub restructuring is included.
