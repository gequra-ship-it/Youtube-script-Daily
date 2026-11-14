# Miya's Note — script generation and video pipeline

English knowledge YouTube channel **Miya's Note**. Start with `CLAUDE.md` (repo map, branches, render cautions), then:

- Guideline: `docs/miyas-lab-guideline.md` (core) + `docs/guideline/` (chapters; `04-motion.md` object motion rules, `07-chalkboard.md` 7-2 note-frog rules)
- Tools and their order: `tools/README.md`; picture spec `tools/art_spec.md`
- Per video: `videos/<slug>/` (script, config, pictures `art3/`), render sources `render/<slug>/`
- Repo change log: `docs/repo-changes.md`

Branches: `render-pipeline` = video production (`videos/`, `render/` and the render workflows exist only there), `main` = daily script generation (`generators/`, `scripts/<daily|owl|igwahyung>/`, plus copies of `docs/`, `tools/`), `archive/miyas-lab-2026-10-24` = old channel, read-only. `main` and `render-pipeline` are never merged.
Pushing `render/.chunked` or the render workflow `render-chunked.yml` starts a GitHub Actions render that overwrites the Drive MP4.
