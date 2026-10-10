# 藤 · huaxin

lyrnox.com 的视觉小站源码（「lyrnox · 藤」—— 一棵挂在网上的日本紫藤），纯静态，CSS/JS 全内联、零外部资源，部署在 Cloudflare Workers（静态资源模式），服务名 `home`。

## 目录

```
site/            网站本体，部署时原样上传
  index.html     主页（样式与脚本都在里面）
  404.html       404 页面
  favicon.svg
  robots.txt
  _headers       全站响应头（安全头 / CSP），不会被当作页面公开
wrangler.toml    Cloudflare 部署配置
.github/workflows/deploy.yml   推送 main 自动部署
```

改页面就直接改 `site/` 里的文件，没有构建步骤，也没有生成产物。

## 本地预览

```bash
npm run preview          # 纯静态预览：http://localhost:8080
npm install && npm run dev   # 用 wrangler 预览，行为（404、响应头）与线上一致
```

## 部署

### 方式一：推送即上线（推荐）

在 GitHub 仓库 Settings → Secrets and variables → Actions 里添加两个 secret：

| 名称 | 内容 |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token（模板选 “Edit Cloudflare Workers”） |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账号 ID |

之后每次 push 到 `main` 都会自动部署；也可以在 Actions 页面手动运行。手机上改完文件提交就行。

### 方式二：命令行手动部署

```bash
npm install
npx wrangler login      # 首次
npm run deploy
```

### 不需要手动清缓存

静态资源每个文件都带 ETag，并且默认 `must-revalidate`，浏览器和边缘每次都会校验，部署完立刻看到新版本。

## 域名

如果 lyrnox.com 已经在 Cloudflare 面板里绑定到 `home`，什么都不用动。想用配置文件管理，就取消 `wrangler.toml` 里 `routes` 的注释。
