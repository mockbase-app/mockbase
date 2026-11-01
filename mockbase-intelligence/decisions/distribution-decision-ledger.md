# Distribution Decision Ledger

This ledger records public MockBase content and distribution decisions so later reviews can compare outcomes against the original evidence, metric and stop condition. It must not contain passwords, tokens, cookies, personal data or private account details.

## 2026-10-11 - Mock defense questions guide

- **Status:** PENDING publication.
- **Target:** `https://mockbase.app/guides/phd/mock-defense-questions.html`
- **Change:** Add a new guide with 30 mock defense questions, answer frameworks and a 45-minute rehearsal plan; add it to the guide index and sitemap; add contextual links from the existing mock-defense and thesis-defence pages.
- **Motivation:** Search Console shows increased demand around mock-defense intent. The existing `what-is-a-mock-defense.html` page answers meaning and process, but it does not directly complete the narrower question-bank job.
- **GSC baseline:** Google Search Console Performance report for `mockbase.app`, Web search, trailing 3 months from 2026-07-10 to 2026-10-09, last update 50 hours before inspection on 2026-10-11. Totals: 77 clicks, 9.17K impressions, 0.8% CTR, average position 9.6.
- **Relevant query evidence:** `mock defense` 1 click / 22 impressions; `what is mock defense in research` 0 clicks / 376 impressions; `mock defense meaning` 0 clicks / 208 impressions; `mock defense in research` 0 clicks / 87 impressions; `mock defense questions` 0 clicks / 56 impressions.
- **Relevant page evidence:** `what-is-a-mock-defense.html` 2 clicks / 1,111 impressions. This page satisfies the meaning query but does not provide a dedicated question bank.
- **Decision logic:** Create a narrow, reversible page for the mock-defense question-bank job rather than another meaning explainer. Borrow existing MockBase resources: mock-defense topical visibility, research-defense guide cluster, official-source pattern, internal links, sitemap, preparation-only boundaries and practice CTA.
- **Expected result:** The page captures long-tail mock defense question intent and gives the existing mock-defense explainer a next-step asset, without cannibalising the meaning page.
- **Verification planned before publish:** MockBase validator, sitemap XML parse, JSON-LD parse, targeted link reference check, `git diff --check`, local desktop and mobile preview, and live URL verification after push.
- **Success metric:** Within 28 days after indexing, the target page should receive at least 20 impressions, or at least one organic click, or reach average position 20 or better for the target mock-defense-questions cluster.
- **Review date:** 2026-11-08.
- **Stop or reversal condition:** If the page has fewer than 20 impressions and no qualified query evidence after 28 days, do not create another page in the same cluster. Improve the existing mock-defense page, internal links or consolidate. If `what-is-a-mock-defense.html` loses impressions while the new page gains none, treat it as cannibalisation and consolidate.

## 2026-10-04 - Research proposal defense presentation guide

- **Status:** PUBLISHED. Public URL verified on 2026-10-11.
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

## 2026-11-01 - Mock proposal defense rehearsal guide

- **Status:** PENDING publication.
- **Target:** https://mockbase.app/guides/phd/mock-proposal-defense.html
- **Change:** One English guide, guide index entry, reciprocal links from the mock-defense explainer and proposal presentation guide, and sitemap entry.
- **Verdict:** Small editorial experiment justified; no paid-product or blue-ocean conclusion.
- **GSC baseline:** Inspected in Chrome on 2026-11-01; Web, trailing three months, 2026-07-31 to 2026-10-30; last update 10.5 hours ago. 158 clicks, 17.6K impressions, CTR 0.9%, average position 8.2. These are site impressions, not total market search volume.
- **Query evidence:** mock proposal defense 0 clicks / 49 impressions; mock defense 3 / 1,362; mock defense questions 2 / 119; proposal defense questions 0 / 124.
- **Page evidence:** proposal questions 47 clicks / 3,226 impressions; defend-research-proposal 23 / 2,022; mock-defense-questions 20 / 3,374; proposal presentation 7 / 407; mock-defense explainer 3 / 1,249.
- **Gap and differentiation:** Existing pages cover definitions, general strategy, slide design and questions; this page completes the narrower organizer job with role assignments, a proposal-specific rehearsal agenda, an evidence-based feedback sheet and retest criteria. Existing brief mock plans create overlap risk; keep this page focused on organizing and diagnosing a proposed study.
- **Incumbents and evidence:** University of Saskatchewan, https://cgps.usask.ca/onboarding/grad-toolkit/roadmaps/thesis-roadmap/crafting.php, explicitly recommends proposal mock defenses; University of Utah Robotics, https://robotics.coe.utah.edu/academics/graduate/handbook/proposaldefense/, documents its institutional proposal format. Both checked 2026-11-01. Free authoritative alternatives exist; competitive difficulty and willingness to pay are not established.
- **Audience and uncertainty:** Candidates organizing a first proposal rehearsal need to know who to invite, what to test before results exist, and what to change afterward. Existing related-page clicks are willingness-to-read evidence only.
- **Borrowed resources:** Existing guide cluster, official university guidance, domain visibility, static CSS, internal links and sitemap. Reader resources include supervisor, peers, librarian, methods support and graduate administrators.
- **Expected result:** Qualified visitors can run a rehearsal and produce prioritized repairs, then use related guides. No new data collection or paid tool investment.
- **Success metric:** In 28 days after indexing, at least 20 target-cluster impressions AND either one organic click or average position <=20; one related-guide/practice click where existing consent-gated analytics measures it. If unavailable, report engagement as unmeasured.
- **Review date:** 2026-11-29 provisional indexing check; shift the 28-day outcome review to the actual indexing date when known.
- **Stop/reversal:** Under 20 impressions with no new query evidence after the window: no further same-cluster pages. Review links/intent; consolidate if overlapping pages lose visibility without incremental relevant traffic.
- **Verification plan:** Bundled validator (baseline passed), JSON-LD and sitemap parsing, relative links, diff review, desktop/mobile browser preview, then public URL verification after deployment.

- **Pre-publication verification update (2026-11-01):** Bundled validator passed; new-page JSON-LD parsed; all local article links resolve; sitemap XML parsed with unique URLs; diff check passed. Chrome desktop and 390px mobile previews inspected, no page-wide horizontal overflow; question-bank CTA clicked and target heading verified. Status remains PENDING until live verification.

- **Publication status update (2026-11-01): PUBLISHED.** Public article returned HTTP 200 and matched the local HTML exactly. Published through the authenticated GitHub web UI because local HTTPS/SSH credentials were unavailable and the connector returned HTTP 403. Article/related-links commit: 5007492; guide-index commit: 76916cb. Review remains provisional for 2026-11-29, with outcome window anchored to confirmed indexing.
