# Maintain Mockbase Skill Design

## Goal

Create and install a reusable Codex Skill that turns the Mockbase repository's product strategy, publishing conventions, evidence standards, compliance boundaries, and validation checks into a repeatable operating system. The Skill must help future agents extend Mockbase without rediscovering its architecture or drifting into generic interview-tool development.

## Market Logic

Mock interview demand is established, but generic AI interview practice is crowded. Mockbase should therefore compete through assessment-specific systems such as PhD viva, UK Civil Service, grant, faculty, and behavioural interviews. Its defensible assets are official-source research, structured question banks, evidence-based answer frameworks, lightweight local-first practice, focused guides, internal distribution links, and clear independence and privacy boundaries.

The Skill should preserve this differentiation. Before proposing a new product or major content track, require evidence for demand, search intent, competition, user pain, willingness to pay, target users, differentiation, lowest-cost validation, success metrics, and stopping conditions. Prefer experiments that reuse the existing static site, guide traffic, simulator previews, waitlist, Search Console data, and product analytics.

## Installation

- Name the Skill `maintain-mockbase`.
- Create it at `~/.codex/skills/maintain-mockbase` so Codex can discover it automatically.
- Generate `agents/openai.yaml` with only `display_name`, `short_description`, and a `$maintain-mockbase` default prompt.
- Do not add icons or brand metadata because none were supplied for the Skill interface.

## Skill Architecture

### Core instructions

Keep `SKILL.md` concise and procedural. Trigger it when an agent works on Mockbase strategy, guides, product tracks, static pages, SEO, structured data, internal links, sitemap registration, privacy or independence language, or release validation.

The core workflow should require agents to:

1. Inspect the repository and preserve unrelated user changes.
2. Identify the real user outcome and reusable Mockbase resources.
3. Validate the market before designing new products, templates, courses, or systems.
4. Use authoritative primary sources for academic, policy, assessment, or professional claims.
5. Preserve the static-site architecture and existing visual conventions unless redesign is explicitly requested.
6. Start implementation changes with failing checks and finish with structural and visual verification.
7. Update discovery surfaces such as the guide index, reciprocal links, canonical metadata, structured data, and sitemap when public content changes.
8. Protect privacy, trademark, non-affiliation, and no-guarantee boundaries.
9. Report evidence, metrics, and explicit stopping conditions rather than unsupported opportunity claims.

### References

Create three one-level reference files:

- `references/project-model.md`: brand purpose, audiences, product matrix, static architecture, reusable resources, data practices, legal boundaries, and current repository conventions.
- `references/publishing-rules.md`: page types, guide structure, source hierarchy, metadata, JSON-LD, links, CTAs, sitemap behavior, and verification expectations.
- `references/opportunity-validation.md`: market-validation decision framework, resource leverage, metrics, experiment design, and stopping conditions.

Keep detailed facts in the references rather than duplicating them in `SKILL.md`.

### Deterministic validation

Create `scripts/validate_mockbase.py` as a read-only validator. It should accept a repository path, return a non-zero status on violations, and check only stable invariants that can be determined from repository files:

- required public files and shared assets exist;
- HTML and sitemap XML are parseable using available local parsers;
- local links resolve;
- sitemap URLs are unique;
- sitemap does not introduce unsupported `priority` or `changefreq` fields;
- canonical URLs, when present, use the Mockbase public origin;
- JSON-LD blocks parse as JSON;
- public product or guide pages retain required independence language where the repository pattern requires it.

Do not make network requests, rewrite files, or enforce editorial taste. Add focused automated tests with temporary fixture sites and run them before relying on the validator.

## Validation Strategy

Follow documentation TDD:

1. Give independent agents realistic Mockbase tasks without the new Skill and record where they miss project-specific requirements.
2. Implement only guidance that addresses observed failures or stable repository facts.
3. Run equivalent tasks with the installed Skill and verify that agents discover the correct references, market gate, source hierarchy, integration surfaces, and validation command.
4. Run `quick_validate.py` against the Skill folder.
5. Run the bundled validator tests and the validator against the current Mockbase repository.
6. Inspect `agents/openai.yaml`, confirm the default prompt explicitly mentions `$maintain-mockbase`, and verify there are no placeholder or auxiliary files.

Forward tests must remain read-only or use temporary artifacts. They must not deploy, modify production systems, or leak the intended answers into the test prompt.

## Market Validation Metrics

For future product tracks, require a written validation record containing:

- directional keyword demand and identifiable search intent;
- named competitors and the underserved job-to-be-done;
- evidence that the assessment has a formal framework or recurring high-stakes need;
- a target user and concrete willingness-to-pay mechanism;
- the existing Mockbase assets that reduce acquisition or production cost;
- a minimum experiment, primary metric, review date, and stopping condition.

For example, validate a new assessment track with one authoritative guide, one waitlist or preview CTA, and Search Console measurement before building a full simulator. Stop or reposition if the agreed test window produces no meaningful non-brand impressions, qualified waitlist demand, or guide-to-product intent after distribution and indexing checks pass.

## Scope

Include Skill creation, UI metadata, references, a tested read-only validator, installation, structural validation, and independent forward testing. Do not redesign Mockbase, edit production pages, deploy the website, add analytics, create a new simulator, or change legal policies as part of this task.
