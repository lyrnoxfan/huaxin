#!/usr/bin/env python3
"""Build worker.js from a static site directory (files inlined as JS strings).

Usage: gen.py <site_dir> <out_worker.js>
Routing: exact path match; "/" serves /index.html; unknown paths -> /404.html.
"""
import json, os, sys

MIME = {
    ".html": "text/html; charset=utf-8",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json",
    ".xml": "application/xml",
    ".webmanifest": "application/manifest+json",
}

TEMPLATE = """\
// __TITLE__ — serves the static site bundle inline.
const FILES = {
__ENTRIES__};

export default {
  async fetch(req) {
    const url = new URL(req.url);
    let path = url.pathname;
    if (path === "/") path = "/index.html";
    const f = FILES[path] || FILES["/404.html"];
    const status = FILES[path] ? 200 : 404;
    return new Response(f.body, {
      status,
      headers: {
        "content-type": f.type,
        "cache-control": "public, max-age=300",
      },
    });
  },
};
"""

def main():
    site_dir, out = sys.argv[1], sys.argv[2]
    entries = []
    for name in sorted(os.listdir(site_dir)):
        p = os.path.join(site_dir, name)
        if not os.path.isfile(p):
            continue
        ext = os.path.splitext(name)[1].lower()
        mime = MIME.get(ext, "application/octet-stream")
        with open(p, "rb") as f:
            body = f.read().decode("utf-8")
        entries.append(
            '  %s: { type: %s, body: %s },'
            % (json.dumps("/" + name), json.dumps(mime), json.dumps(body, ensure_ascii=False))
        )
    title = "lyrnox.com site worker"
    code = TEMPLATE.replace("__TITLE__", title).replace("__ENTRIES__", "\n".join(entries))
    with open(out, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {out}: {len(entries)} files, {len(code)} bytes")

if __name__ == "__main__":
    main()
