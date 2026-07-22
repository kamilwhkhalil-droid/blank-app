# Launch checklist

The site is complete and name-free. Two placeholders remain, by design. This file is the
exact path from here to live.

## 1. Create the anonymous inbox (~2 minutes)

Create a book-branded email address with no personal name in it, e.g.
`metabolicimperative@gmail.com` or `readings@<your-domain>`. This receives the
full-edition requests and advisory inquiries.

## 2. Buy the domain (~10 minutes)

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

The visible URL is then your domain; the username never appears in it.

## 3. Swap the placeholders (~1 minute)

Two strings, three files-worth of occurrences:

```bash
# the contact address (dashboard.html, 2 occurrences)
grep -rl 'your-contact-address@example.com' . | xargs sed -i 's/your-contact-address@example.com/NEW_ADDRESS/g'

# the site link in the essays (6 occurrences)
grep -rl 'SITE LINK — insert before posting' essays | xargs sed -i 's|\[SITE LINK — insert before posting\]|https://YOUR_DOMAIN/|g'
```

Or just reply in the Claude session with the address and domain, and it gets done for you.

## 4. Go live

- Commit and push; Pages redeploys automatically.
- Post essay 1 (`essays/01-the-quiet-death.md`) per `essays/POSTING-GUIDE.md`.
- When ready to charge for the full edition: create a payment link (Gumroad /
  Lemon Squeezy / Stripe) and swap it in for the "Request the full edition" mailto.

## Privacy note

The repository itself is under your GitHub account; if the repo is public, the
username is visible to anyone who inspects the repo (not the site). For complete
separation, mirror the four site files (`index.html`, `proposal.html`,
`dashboard.html`, `style.css`) to a repo under a fresh anonymous account and point
Pages + the domain there instead.
