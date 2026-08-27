# Deploying this to GitHub + Vercel

The folder is already a git repository with the first commit made and the remote set to
`https://github.com/intelliline/fds-demo-website.git`. Three steps left, all of which need
internet access that this session doesn't have.

---

## 1. Create the empty repo on GitHub

Go to **https://github.com/new** while signed in as `intelliline`:

- Repository name: `fds-demo-website`
- Public or private — either works with Vercel
- **Do not** add a README, .gitignore or licence (the commit already has them)

## 2. Push

Open a terminal in `C:\FDS\fds-demo-website` and run:

```bash
git push -u origin main
```

Or just double-click **`push-to-github.bat`** in this folder.

If git asks who you are, run these once first:

```bash
git config --global user.name  "IntelliLine Solutions"
git config --global user.email "support@intellilinesolutions.com"
```

## 3. Import into Vercel

1. **https://vercel.com/new** → Import Git Repository → pick `intelliline/fds-demo-website`
2. Framework preset: **Other**. Leave build command and output directory empty — it's static HTML.
3. Deploy.

You land on **`https://fds-demo-website.vercel.app`**. That's the link for Shawn.

`vercel.json` is already in the repo, so clean URLs (`/services` rather than `/services.html`),
asset caching and `X-Robots-Tag: noindex` are configured on the first deploy. The noindex matters —
it stops this preview from competing with the client's live domain in search results.

---

## Optional: put it on your own domain

In the Vercel project → **Settings → Domains → Add**, enter:

```
fds-demo-website.intellilinesolutions.com
```

Vercel shows you one CNAME record. Add it wherever `intellilinesolutions.com` DNS is managed:

| Type | Name | Value |
|---|---|---|
| CNAME | `fds-demo-website` | `cname.vercel-dns.com` |

It's usually live within a few minutes, with the certificate issued automatically.

---

## Updating it later

Edit the content in `src/build.py`, then:

```bash
python3 src/build.py          # regenerates all five pages
python3 src/build_artifact.py # regenerates the single-file version
git add -A && git commit -m "copy tweaks" && git push
```

Vercel redeploys on every push to `main`, so the URL you sent Shawn always shows the latest version.

---

## No-GitHub alternative

If you'd rather skip GitHub entirely: zip this folder, go to **https://vercel.com/new**, and drag the
zip onto the drop area. Same result, but future updates have to be re-uploaded by hand instead of
deploying on push.
