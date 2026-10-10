# 花信 · huaxin

lyrnox.com 的静态站源码（「lyrnox · 花信」第二版），部署在 Cloudflare Worker 服务 `home`。

## 文件

- `site/index.html` — 主页面，CSS/JS 全内联，零外部资源
- `site/404.html` — 404 页面
- `site/favicon.svg` — 图标
- `site/robots.txt`
- `gen.py` — 从 `site/` 生成 `worker.js`
- `deploy-home.py` — 部署到 Cloudflare Worker
- `worker.js` — 生成产物（部署用的就是这个，别手改）

## 本地预览

```bash
cd site && python3 -m http.server 8080
```

## 重新部署

```bash
python3 gen.py site worker.js
python3 deploy-home.py --account 4da041ad422b0c9e0ac5f6a7b3bafeea
```

部署后清掉 Cloudflare 上 lyrnox.com zone 的缓存（`/`、`/index.html`、`/404.html`、`/favicon.svg`、`/robots.txt`），否则边缘会吐旧页面：

```
POST /client/v4/zones/9512b0934e802b5924da512c85260dcd/purge_cache
{"files":["https://lyrnox.com/","https://lyrnox.com/index.html","https://lyrnox.com/404.html","https://lyrnox.com/favicon.svg","https://lyrnox.com/robots.txt"]}
```
