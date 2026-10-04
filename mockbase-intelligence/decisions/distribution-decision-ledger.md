# Distribution Decision Ledger

This ledger records public MockBase content and distribution decisions so later reviews can compare outcomes against the original evidence, metric and stop condition. It must not contain passwords, tokens, cookies, personal data or private account details.

## 2026-10-04 - Research proposal defense presentation guide

- **Status:** PENDING publication.
- **Target:** `https://mockbase.app/guides/phd/research-proposal-defense-presentation.html`
- **Change:** Add a new guide on structuring a research proposal defense presentation, add it to the guide index and sitemap, and add contextual links from the closest proposal-defense guides.
- **Motivation:** Search Console shows qualified proposal-defense demand, while the existing pages cover definition, defense strategy and questions rather than the narrower task of turning the written proposal into a slide presentation and opening talk.
- **GSC baseline:** Google Search Console Performance report for `mockbase.app`, Web search, trailing 3 months, last update 8.5 hours before inspection on 2026-10-04. Totals: 56 clicks, 6.64K impressions, 0.8% CTR, average position 11.
- **Relevant query evidence:** `proposal defense` 142 impressions, `proposal defense meaning` 87 impressions, `research proposal defense` 47 impressions, `mock defense questions` 28 impressions, plus proposal-defense pages already earning impressions.
- **Relevant page evidence:** `research-proposal-defense-questions.html` 16 clicks / 1,072 impressions; `defend-research-proposal.html` 8 clicks / 550 impressions; `what-is-a-research-proposal-defense.html` 2 clicks / 1,082 impressions.
- **Decision logic:** Create one narrow, reversible page for the slide/presentation job rather than another broad proposal-defense explainer. Borrow existing MockBase resources: proposal-defense topical authority, internal links, sitemap, static-page pattern, preparation-only boundaries and practice CTA.
- **Expected result:** The page captures long-tail proposal defense presentation intent without cannibalising the existing definition, question-bank or defense-strategy pages.
- **Verification performed before publish:** MockBase validator passed; sitemap XML parsed; JSON-LD parsed; targeted link references confirmed; trailing whitespace check passed; `git diff --check` passed; local desktop and mobile preview loaded; mobile viewport 390px showed no page-wide horizontal overflow, with wide tables using the existing scroll pattern.
- **Success metric:** Within 28 days after indexing, the target page should receive at least 20 impressions, or at least one organic click, or reach average position 20 or better for the target presentation/proposal-defense cluster.
- **Review date:** 2026-11-01.
- **Stop or reversal condition:** If the page has fewer than 20 impressions and no qualified query evidence after 28 days, do not create another page in the same cluster. Improve distribution, internal linking or consolidate with an existing proposal-defense page. If an existing proposal-defense page loses impressions while this page gains none, treat it as cannibalisation and consolidate.
