# Agent notes

cloudberry is the Raspberry Pi field rig for Pinchard's Island: it captures from a GoPro HERO3/HERO4 or a Pi camera module, uploads to S3 and powers down on a WittyPi boot-once schedule. Prefer one issue per chat when the work is mechanical.

## What this is

The camera system behind the Cloudberry photographs. The archive site and the grid print build scripts live in [adamsimms/cloudberry-archive](https://github.com/adamsimms/cloudberry-archive), not here.

Canonical files: [README.md](README.md), [docs/field/README.md](docs/field/README.md), `cloudberry/`.

## Private material

Private notes live in the private studio repo (adamsimms/studio). Nothing from studio comes into this repo unless Adam approves it. Never put a phone number or home address here; a global pre-commit guard blocks them.

## Bibliography / Zotero

Zotero is the source library (public library; no project collection yet, ask Adam). Writing to Zotero is publishing: only approved batches. Do not query `~/Zotero/zotero.sqlite`. Do not invent citations.

## Hard rules

- Do not invent hardware that is not in the README, `docs/field/` or code.
- Secrets only via `secrets.env`; see `.env.example`. `docs/field/secrets-reference.md` documents context, never live credentials.
- Vendor firmware zips and manual PDFs (`firmware/`, `docs/field/`) are kept as downloaded; do not edit them.

Docs policy and the decisions rule (work decision vs proposal choice vs option): [`.cursor/rules/docs.mdc`](.cursor/rules/docs.mdc).

## GitHub

Issues here are about the rig. Applications, calls and their deadlines are tracked in the private studio repo, not here. Issue titles have no kind prefix; kind lives on labels.

## Project media

Photos, test captures and video never stay in this repo's ignored folders: they are not backed up. They go to the project's synced Drive folder, `$MEDIA_DIR` (`30 STUDIO/32 PROJECTS/CLOUDBERRY/`): `01-REFERENCES`, `02-STUDIES`, `03-TESTS`, `04-ARTWORK`, `05-DOCUMENTATION`. Inside 02 and 03, one dated folder per piece of work: `<YYYY-MM>-<NAME>`. Older folders there predate this layout and are not reorganized yet.

## Support

Funder acknowledgements are not recorded here yet. Ask Adam before adding any.
