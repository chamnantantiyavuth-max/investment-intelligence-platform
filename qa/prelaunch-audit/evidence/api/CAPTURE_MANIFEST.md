# Live API Capture Manifest

Base URL: `http://127.0.0.1:8000`  
Capture time: `2026-08-03 18:21–18:25 UTC+7`

Raw JSON files are preserved as valid, byte-level HTTP response bodies. The timestamp footer is carried by this manifest rather than appended to raw JSON, because an HTML comment would invalidate JSON.

| File | Request | HTTP | SHA-256 |
|---|---|---:|---|
| `openapi.json` | `GET /openapi.json` | 200 | `2cbc69b09e73e63eef76e4a7b8593c6d9a5a54d1feb3a39914bbb029783fe8dc` |
| `health.json` | `GET /api/health` | 200 | `a29ee2b15c494311c52521766e44af56a3ad2248e7a8ab465e5206463c13d288` |
| `dashboard-summary.json` | `GET /api/dashboard/summary` | 200 | `e291456de24dc43b8613336afad60a8f0c42225bcad6fac6f46557af89c8bd42` |
| `am-queue.json` | `GET /api/am-queue` | 200 | `e96964ea7f12f0eeef874b08e6e7eeb33e532fac35679c322a6dc1954c588390` |
| `am-theme-theme-ai-infra.json` | `GET /api/am-theme/theme-ai-infra` | 200 | `5a2e9ebeaf11865e44aecd4f9b8722c3d6ba52fb6ce9c07dd50da42196fba87d` |
| `am-theme-made-up.json` | `GET /api/am-theme/made-up-id` | 404 | `9c92d5968bc3f056a6909f1cc0266896792f6dd3773e570d2b1968ae9fd56f8f` |
| `cs-radar.json` | `GET /api/cs-radar` | 200 | `69b8dcf821494fb1ec7371e03b011124ba82461467cd0d9f8a56f7e00f0ae628` |
| `fo-queue.json` | `GET /api/fo-queue` | 200 | `929a4b0a49bd9b9127812ef2615c1b500d1e2ca4988f486700db27241f60d48d` |
| `fo-cheap-quality.json` | `GET /api/fo-cheap-quality` | 200 | `f556361a6621ac95241462e330c45b5bb7eb497c87751a756bef16549fba16e5` |
| `fo-package-AAPL.json` | `GET /api/fo-package/AAPL` | 200 | `2b8f9705c888b5da9cb86a671c0605088dcff669c7b366b36f70052c79682095` |
| `fo-package-made-up.json` | `GET /api/fo-package/made-up-id` | 404 | `e811a2e16f57c5bec7c93fd29214742481d11f8a5f5bbfb43252a9e1e16dce45` |

<!-- 2026-08-03 18:25 UTC+7 -->