# Launch checklist

The site is complete, name-free, and has no payment or contact plans — it is a free
reading site: the compact edition, the proposal, and the interactive dashboard.
One placeholder remains (the essay link). This file is the exact path from here to live.

## 1. Buy the domain (~10 minutes)

Any registrar (Namecheap, Cloudflare, Porkbun). Something like `metabolicimperative.com`.

Then connect it to GitHub Pages:

1. Repo → **Settings → Pages** → Source: **Deploy from a branch** → pick the branch, `/ (root)`.
2. In the **Custom domain** field, enter your domain and save. GitHub creates a `CNAME`
   file in the repo automatically (or add one yourself containing just the domain).
3. At your registrar, add DNS records:
   - Apex domain (`metabolicimperative.com`): four **A records** →
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: one **CNAME record** → `<your-github-username>.github.io`
4. Back in Pages settings, tick **Enforce HTTPS** once the certificate is issued
   (can take up to an hour).

The visible URL is then your domain; the username never appears in it. (Renaming the
GitHub account to something neutral also removes the name from the repo itself.)

## 2. Fill in the essay link (~1 minute)

The six essays end with the placeholder `[SITE LINK — insert before posting]`:

```bash
grep -rl 'SITE LINK — insert before posting' essays | xargs sed -i 's|\[SITE LINK — insert before posting\]|https://YOUR_DOMAIN/|g'
```

Or just reply in the Claude session with the domain, and it gets done for you.

## 3. Go live

- Commit and push; Pages redeploys automatically.
- Post essay 1 (`essays/01-the-quiet-death.md`) per `essays/POSTING-GUIDE.md`.

## Privacy note

The repository itself is under your GitHub account; if the repo is public, the
username is visible to anyone who inspects the repo (not the site). Renaming the
account (GitHub → Settings → Account → Change username) fixes this in place; a
fresh anonymous account with the site files mirrored to it is the fuller
separation.
