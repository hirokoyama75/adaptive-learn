# Citation Verification Ledger

**Status:** no source below was opened. Default is `unverified`. Identifiers are **search handles**, not confirmed resolvers; confirm any DOI on the publisher page before quoting. Only a human marks `verified`, after opening the source and recording the date.

`likely` = title/venue/ID plausibly matches a real work, page unopened, reason given. `unverified` = unsourced until checked.

| Claim | Source | Identifier | Status | What to check | Risk if wrong | Used in |
|---|---|---|---|---|---|---|
| Plain GPT: practice +48%, unassisted exam −17%; tutor arm neutral; unanchored answer accuracy 51% | Bastani et al., PNAS 2025 | Title search; DOI unresolved | unverified | N≈1,000, Turkey, 4×90 min, 3 arms; the −17% and 51%; whether the tutor arm used a human key | The anti-leakage argument collapses | research §4.1–4.2; A-01 |
| Median gain >2×; d≈0.63; 49 vs 60 min; N=194 | Kestin et al., Sci Rep 2025 | Title search | unverified | Crossover design, how ">2×" is computed, no delayed test | "2× tutoring" gets repeated | research §4.1, §4.7, §10 |
| +1.3 percentile/term; 0.06–0.08 SD/yr; 18 Tennessee schools | Oreopoulos & Low, NBER w35620 | nber.org/papers/w35620 | unverified | Author list (is Low a co-author?), per-term→per-year conversion | At-scale effect overstated | research §4.1, §4.7 |
| AI slower, fewer attempts, better next attempt; delayed gains only in mastery workflow | Oreopoulos et al., NBER w35621 | nber.org/papers/w35621 | unverified | 6,000+ sample; operational meaning of "mastery workflow" | Mechanism claim unsupported | research §4.1 |
| AI affirms 49% more; raises trust, lowers repair intent; N=2,405 | Cheng et al., Science 2026 | Title search | unverified | Venue/year; 3 preregistered experiments; what "49%" measures | Sycophancy magnitude inflated | research §4.1, §4.4 |
| 58.2% sycophantic; 14.7% regressive; 78.5% persistence | SycEval, arXiv 2025 | arXiv:2502.08177 | unverified | Model set; definition of "regressive"; turn structure | 14.7% is load-bearing | research §4.1, §4.4 |
| 6–22% answer leakage; 8,538 six-turn conversations | ACL 2026 leakage study | ACL 2026; no ID supplied | unverified | Venue/year; whether 15.8/22.5 and 6.1/6.4 are models or conditions; MCQ-only | Leakage baseline wrong | research §4.1, §4.5 |
| ≥58% fabricated citations, legal domain | Dahl et al., J Legal Analysis 2024 | Title search | unverified | Model; fabrication vs misattribution | Overgeneralized to all writing | research §4.1, §4.2 |
| Self-correction without feedback: 75.9 → 75.1 → 74.7 | Huang et al., ICLR 2024 | arXiv:2310.01798 | likely — matches a widely cited 2024 self-correction paper; page unopened | GSM8K; model; rounds | Justifies banning intrinsic self-correction | research §4.1–4.2 |
| Drops when only numbers change; up to ~65% with an irrelevant clause | Mirzadeh et al., ICLR 2025 | arXiv:2410.05229 | likely — matches GSM-Symbolic; page unopened | Drop metric; models; whether 65% is relative | Overstates current fragility | research §4.1 |
| Spacing benefit robust for verbal recall | Cepeda et al., Psych. Bulletin 2006 | candidate 10.1037/0033-2909.132.3.354 | unverified | Study count; effect size; moderators | Scheduler rests on folklore again | research §3.1, §3.7 |
| Optimal gap ≈10–20% of retention interval | Cepeda et al., Psych. Science 2008 | candidate 10.1111/j.1467-9280.2008.02209.x | unverified | Ridgeline method; whether 10–20% is the reported ratio | The scheduler's core number | research §3.7; D5 |
| Retrieval practice g≈0.50 | Rowland, Psych. Bulletin 2014 | candidate 10.1037/a0037559 | unverified | Effect size; inclusion criteria | Quoted effect size | research §3.1 |
| Practice testing g≈0.61 | Adesope et al., RER 2017 | candidate 10.3102/0034654316689306 | unverified | Whether 0.61 is the overall g | Same | research §3.1 |
| Interleaving g≈0.42; math 0.34; words −0.39; expository null | Brunmair & Richter, Psych. Bulletin 2019 | candidate 10.1037/bul0000209 | unverified | Moderator values; the negative vocabulary result | Interleaving boundary unjustified | research §3.1, §3.3 |
| Expertise reversal: guidance helps novices, harms experts | Kalyuga, Educ. Psych. Review 2007 | candidate 10.1007/s10648-007-9054-3 | unverified | Review vs primary data; scope | Hint-entry rule loses warrant | research §3.3 |
| Self-explanation g≈0.55 | Bisra et al., Educ. Psych. Review 2018 | candidate 10.1007/s10648-018-9434-x | unverified | Meta-analysis scope; g definition | Scheduled prompt unjustified | research §3.6 |
| Delayed JOLs: accuracy g≈0.93, memory gain g≈0.08 | Rhodes & Tauber, Psych. Bulletin 2011 | candidate 10.1037/a0021540 | unverified | Which effect is which; "relative accuracy" definition | Calibration advice inverted | research §3.1, §3.7 |
| Metacognitive training effects small and context-bound | St. Hilaire et al. 2024 | Title search; venue unknown | unverified | Intervention; population; outcome | Used to cap calibration claims | research §13 |
| Exam wrappers: no gain in a controlled trial | Soicher & Gurung, Teaching of Psychology 2017 | candidate 10.1177/0098628316677644 | unverified | Design; n; outcome measure | "Do not add" rests on one null | research §3.1, §3.7 |
| Wise feedback improves uptake | Yeager et al., JEP: General 2014 | candidate 10.1037/a0033906 | unverified | Both studies; outcome (revision/grades) | Affect line unsupported | research §3.12 |
| Implementation intentions d≈0.65 | Gollwitzer & Sheeran, Adv. Exp. Soc. Psych. 2006 | candidate 10.1016/S0065-2601(06)38002-1 | unverified | Study count; d | Only if planning is added | research §13 |
| Tangible rewards undermine intrinsic motivation | Deci et al., Psych. Bulletin 1999 | candidate 10.1037/0033-2909.125.6.627 | unverified | 128 experiments; reward subtypes | Gamification-ban rationale | research §13 |
| Growth-mindset interventions d≈0.08 | Sisk et al., Psych. Science 2018 | candidate 10.1177/0956797617739704 | unverified | Overall d; moderators; publication bias | "Do not add" list | research §10 |
| Indirect injection via retrieved/learner documents is practical | Greshake et al., arXiv 2023 | arXiv:2302.12173 | likely — matches a widely cited 2023 injection paper; page unopened | Attack demos; coverage of learner PDFs | S-01 controls look unmotivated | research §7.1 |
| Prompt injection is LLM01 in the 2025 Top 10 | OWASP LLM Top 10, 2025 | owasp.org LLM01 page | likely — known page, exact URL not checked today | Current URL; year label; "mitigation not prevention" wording | Cites a stale page | research §7.1 |
| 87 tasks; skills lift pass rate 33.9%→50.5%; ≤3 modules beat larger bundles | SkillsBench 2026 | arXiv:2602.12670 | unverified | That the ID resolves; module-count comparison; task count | D1 rests on measurement, not this paper | research §9.7 |
| v1 requires `name`+`description`; v2 samples ≤10 support paths | OpenCode docs, v1/v2 | opencode.ai docs | unverified | Fields and limits on the installed version | Front matter could break loading | research §5.8–5.9; phase 3 |
| One third of feedback interventions reduce performance | Kluger & DeNisi, Psych. Bulletin 1996 | candidate 10.1037/0033-2909.119.2.254 | unverified | The one-third figure; 607 effect sizes | Feedback caution overstated | research §3.1 |

## Claims to remove or qualify

1. **"AI tutoring doubles learning."** One course, one semester, non-blinded, ceiling effects, no delayed test. Always attach caveats.
2. **"Local means private."** Use: no network requests; provider processes chat; synced folders and backups may copy files.
3. **"−17%" / "51%" as general facts.** One 2023-model, one-school result. Date-stamp.
4. **"14.7% regressive."** Synthetic rebuttals, preprint. Say "one benchmark."
5. **"Retrieval always beats rereading."** False for complex, high-interactivity material.
6. **"Interleaving helps."** Negative for vocabulary.
7. **Effect sizes (g/d) in reader-facing files.** Keep them in research; README rightly makes no numeric claim.
8. **"Helper is secure."** TOCTOU, PATH-resolved `git`, no code pinning remain. Qualify or omit.
9. **Any citation the implementer has not opened.** No DOI without a landing-page check.

## 10-minute verification routine

1. Open the identifier. If it 404s, search title + first author + venue. Never guess a DOI.
2. Confirm title, all authors, year, venue, peer-review status. A working paper stays one.
3. Read the abstract and the sentence holding the number. Record the statistic and denominator, not a paraphrase.
4. Check design: sample, population, duration, comparison, delayed test. Write one line on what it cannot show.
5. Update the row: status, `checked-by`, `checked-on` (YYYY-MM-DD), corrected number. Sweep `research.md` and any file repeating it.

Record: `claim-id | status | verified-by | date | URL | corrected wording`. Batch by DOI; stop at 10 minutes, keep the partial ledger, never mark `verified` from a secondary source.
