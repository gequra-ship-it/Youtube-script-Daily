# Miya's Note — script generation and video pipeline

English knowledge YouTube channel **Miya's Note**. Start with `CLAUDE.md` (repo map, branches, render cautions), then:

- Guideline: `docs/miyas-lab-guideline.md` (core) + `docs/guideline/` (chapters; `04-motion.md` object motion rules, `07-chalkboard.md` 7-2 note-frog rules)
- Tools and their order: `tools/README.md`; picture spec `tools/art_spec.md`
- Per video: `videos/<slug>/` (script, config, pictures `art3/`), render sources `render/<slug>/`
- Repo change log: `docs/repo-changes.md`

Branches: `render-pipeline` = video production (this), `main` = daily script generation (copies of `docs/`, `tools/`).
Pushing `render/.chunked`, `render/.slug`, `render/sample/**` or the render workflows starts a GitHub Actions render that overwrites the Drive MP4.
