# 项目状态板

## 当前阶段
MVP 已完成，稳定运行中。

## 最后更新
2026-07-19

## 核心文件
- 配置：`config/hr_sources.json`
- 脚本：`scripts/update_hr_radar.py`
- 网页：`hr/index.html`
- 数据：`data/hr-radar.json`
- 工作流：`.github/workflows/update-hr-radar.yml`

## 最近完成
- [x] GitHub Pages 部署
- [x] Actions 自动更新（工作日 08:30）
- [x] 手动运行验证通过

## 当前阻塞
（填入当前遇到的问题，例如：某个来源抓取失败、网页样式错误等）

## 下一步
（填入你下次想做的 1–2 件事，例如：接入上海人社局 RSS）

---

## 快速诊断命令

```bash
# 1. 检查当前分支和提交历史
git log --oneline -5

# 2. 检查文件是否齐全
Test-Path config/hr_sources.json
Test-Path scripts/update_hr_radar.py
Test-Path hr/index.html
Test-Path data/hr-radar.json

# 3. 检查 JSON 数据是否正常
python -m json.tool data/hr-radar.json | Select-Object -First 20

# 4. 检查工作流文件
Get-Content .github/workflows/update-hr-radar.yml -TotalCount 30

# 5. 本地测试运行（不修改远程）
py scripts/update_hr_radar.py