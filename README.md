# 16-paintcan（刷墙涂料）

Paintcan — 墙面积 − 门窗开洞；按涂布率与遍数换升数

## 启动

```bash
docker compose up --build
```

| 入口 | 地址 |
| --- | --- |
| 前端 | http://localhost:4500 |
| API | http://localhost:9500 |

## 主链

房间墙面减门窗 → 涂料升数 → 用量清单

## 墙腰双色分带

估漆可按腰线离地高度把四面墙净面积切成下带/上带，两带各自涂布率与遍数换升数并分列回包，另给合计升数。

- 请求：`POST /api/estimate` 增加可选 `band`：`{enabled, waist_height, lower_coverage, upper_coverage, lower_coats?, upper_coats?}`（遍数缺省沿用公共 `coats`）。
- 缺省关闭分带时，升数与未分带同房同参一致。
- 门窗开洞仍只从总墙面积扣除一次，再按带高比例切分净面积，不重复扣除。
- 腰线 ≤0 或 ≥层高、或任一带涂布率非正 → 400 整单拒绝，不写记录。
- `persist=false` 只回包；`persist=true` 钉选腰线、两带升数与合计（`input_json`/`result_json`），历史记录随后续参数变更保持不动。

## 技术栈

Python 3.12 + FastAPI + SQLite；Vue 3 + Vite + Nginx。
