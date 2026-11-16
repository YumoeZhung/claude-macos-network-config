# 多站点检测：出口、分流、DNS 与 WebRTC

检测入口核对日期：**2026-11-13**。本页供用户和 Agent 执行登录前验收，配合 [macOS 操作手册](macos-runbook.md) 第 5 阶段使用。手机在自己的浏览器、Wi-Fi / 移动网络中分别执行，不能继承电脑结果。

全局顺序为电脑先验收、手机后验收，之后才在手机下载官方 App 并登录 / 订阅，最后登录电脑。新装用户无需安装 Claude 就能执行这些网络测试；初始浏览器旧会话清理按 macOS 手册第 0 节完成。

## 0. 前提与记录

先完成 Claude 任务，退出 Desktop、Code、扩展及相关自动任务；保持待验收的订阅、节点和 TUN 设置。检测页会主动访问多个目标、查询 DNS 或发送 STUN 请求，**不是被动检查**。用户仍在使用 Claude 时，不自行打开检测页或点击重测。

记录时间、设备、浏览器、网络类型、当前配置和最终节点。所有站点尽量在同一环境、相近时间运行；不要为取得好看的结果换节点、切全局模式、关闭 TUN 或安装修复插件。第三方页面建议不是配置变更授权。

将原始 IP、截图、解析器清单及规则链留在私有报告；公开仓库只留脱敏结论。工具打不开、请求失败或结果为空时填写“未验证”，不要填“通过”。

## 1. 综合初筛：WildAI + IPinfo.CV

- [WildAI 网络检测](https://bewild.ai/network-detection?source=claude-subscribe)：作为此前使用的出口初筛入口。
- [IPinfo.CV：Claude AI IP 检测](https://ipinfo.cv/claude-ai-check)：补充查看出口国家、ASN / 网络属性和环境一致性提示。

记录具体字段，而不只抄“低风险”或总分。本次经历中，WildAI 低风险反馈之后仍发现过联通 DNS 与网站分流的国内 IPv4 出口，因此流程不能止于该页。这里说明的是已知检测覆盖不足，不宣称其未来版本永远没有新增功能。

IPinfo.CV 已核对页面说明和独立 DNS / WebRTC 入口；**本次文档更新没有执行其完整浏览器检测，不记录为本机已通过**。页面写“DNS 需复核”时，应进入解析器测试，不能仅凭提示认定发生泄漏。

## 2. Net.Coffee：查各目标实际看到的 IPv4 出口

打开 [ip.net.coffee](https://ip.net.coffee/)，查看首页出口以及“网站分流测试”，等待各项完成。按行记录目标名称、出口 IP、地区，并结合 Clash 连接界面或本地 `/connections` 核对**具体域名、命中规则、DIRECT / 代理链**。不要仅根据目标名称猜域名。

判读顺序：

1. 首页显示预期日本出口，仅说明这次首页请求走了日本，不能覆盖页面中其他目标。
2. 某行出现国内 IPv4，说明该目标看到了国内出口；这是 HTTP / HTTPS 分流检查，与 DNS 解析器国籍不同。
3. 若为用户明确要求的 EAS、DSW 等业务直连，记录为预期例外，并验证业务仍可用。
4. 若为 Claude、身份验证依赖或原本应代理的目标，暂停登录，先排查规则优先级与实际链路。
5. 陌生目标、未知或超时先记待核查；不自动添加直连或代理规则，也不删除所有国内直连规则。

### 现场案例：Cloudflare 中国

2026-11-12，用户在 Net.Coffee 看到多数测试项为日本出口，“Cloudflare 中国”为国内联通出口。随后被动连接记录确认该项请求 `www.cloudflare-cn.com`，命中 `GeoIP CN → DIRECT`。这表明当时配置保留了原订阅的国内直连规则，**不只有 Typeless、向日葵等精确业务例外**。

这也说明：检测页面可汇总多个端点看到的不同出口。保留分流时，不应承诺“整个浏览器只暴露同一个 IP”；验收目标是解释各条路径，并确保应代理的 Claude 相关请求没有落入直连。

`www.cloudflare-cn.com` 与登录验证使用的 `challenges.cloudflare.com` 是不同域名。后者及其子域名、Claude 自身域名和验证过程中可能使用的 `dnstest.dev` 子域名，应分别核对规则及 DNS 路径。官方验证依赖会变化，参考 [Cloudflare 文档](https://developers.cloudflare.com/cloudflare-challenges/troubleshooting/challenge-solve-issues/)，不要把一个静态列表当成永久完整清单。

当时只读检查确认 `challenges.cloudflare.com` 已有优先于国内 GeoIP 的代理规则，并与 Claude 指向同一个日本节点；`dnstest.dev` 没有专门规则，仍需检查其实际匹配路径。**这些是历史配置观察，不是完整登录挑战验收，也没有在本次文档更新中补规则。**

单独代理 `www.cloudflare-cn.com` 只能改变该测试项的出口，不能代替验证依赖检查。不要为了测试全绿扩大到所有浏览器请求，也不要移除用户需要的业务直连。

### Claude 检测页的三个出口栏与 CDN

不要混淆首页“网站分流测试”和 [Net.Coffee Claude 检测页](https://ip.net.coffee/claude/) 的字段。2026-11-13 阅读该页脚本时确认：

| 页面字段 | 当时的探针 | 能说明什么 |
|---|---|---|
| 中国 IPv4 出口 | 先请求 `https://2026.ip138.com/`，失败后请求 `https://my.ip.cn/` | 这些探针看到的来源 IP；栏目名称不保证结果一定是国内 |
| Cloudflare 出口 IP | `https://1.1.1.1/cdn-cgi/trace` | Cloudflare 探针看到的来源 IP，不是 CDN 机房地址 |
| Claude 出口 IP | `https://claude.ai/cdn-cgi/trace` | Claude 目标诊断返回的来源 IP / 地区 |

当时 Claude 探针只提取 `ip`、`loc`，没有在该卡片展示 `colo`。因此这张综合报告不能代替 [目标端 CDN 验收](macos-runbook.md)：另记录 `colo` / `CF-Ray` 才能判断入口机房。之前的 JP / NRT 结论来自单独的目标端检查，不是从“Cloudflare 出口 IP”推断。

该页 DNS 通过随机子域名与结果接口取得解析器，再显示其中一个结果；需要完整清单时用独立 DNS 页面。不得将单个卡片当成所有解析器都已展示。原生 / 跟随版的两张截图及配置对比见 [经验补充](maintenance-and-findings.md)。脚本会访问 Claude 域名，其跨站 Cookie 行为也在该文单列，避免把“无账号检测”误解成“不访问 Claude”。

## 3. DNS：必须看到解析器明细

主交叉验证使用 [BrowserLeaks DNS](https://browserleaks.com/dns) 与 [DNSLeakTest](https://www.dnsleaktest.com/) 的 Extended test；补充入口为 [Net.Coffee DNS](https://ip.net.coffee/dns/)（可选深度测试）和 [IPinfo.CV DNS](https://ipinfo.cv/dns-leak-check)。

记录解析器 IP、运营商、地区与当前网页出口。测试域名的递归解析器和目标网页看到的来源 IP 不属于同一字段：网页出口是日本，DNS 仍可能出现本地联通解析器；反过来，DNS 已按预期代理，某个网站仍可能被规则直连。

- 出现未经解释的本地运营商解析器：暂停登录，查系统 / 浏览器 DNS、Clash 上游、fallback 与 nameserver-policy。
- 出现日本与美国公共解析器：核对具体服务商与路径，继续目标域名 / CDN 验收，不按国旗数判定。
- 同一个 IP 被不同数据库标为不同国家：先比较原始 IP 和查询时间，区分数据库分歧与实际换出口。
- 只有综合评分、基础风险提示或没有解析器明细：DNS 检查尚未完成。

最终仍需按 [DNS 技术说明](dns-and-ipv6.md) 和操作手册核查 DNS 上游实际代理链、Claude 目标解析及服务端 CDN 入口。

## 4. WebRTC：核对有效地址和 UDP 路径

使用 [Net.Coffee WebRTC](https://ip.net.coffee/webrtc/) 或 [IPinfo.CV WebRTC](https://ipinfo.cv/webrtc-check)，必要时与 [BrowserLeaks WebRTC](https://browserleaks.com/webrtc) 交叉验证。记录候选地址、类型、是否为有效公网 IPv4 / IPv6，以及实际 HTTP 出口和可观察到的 STUN 连接链。

- 出现本地运营商公网 IP，即使同时有代理 IP，也要追踪这条旁路；不是只有“全部国内 IP”才处理。
- 候选公网地址与预期代理出口一致时，记录该浏览器本次采样结果。
- 无候选、超时或 UDP 被阻断时，注明原因与测试限制，不能填成“UDP 已正确代理”。
- 内网地址、mDNS 名称和格式非法的字符串，不计作已发现额外公网出口；不能仅看页面的“泄漏 IP 数”。

本页不会要求安装检测客户端或一键修复工具，也不自动申请麦克风权限。浏览器结果不能替代 Claude Desktop、Code 或手机 App 的连接检查。

## 5. 完成目标验收，再登录

电脑阶段返回 [macOS 操作手册](macos-runbook.md) 第 5.4 节完成目标域名与 CDN 核查，同时完成 IPv6 与业务直连验收，再填写 [验收报告](../templates/acceptance-report.md)。随后推进手机配置与独立验收、手机安装登录及订阅，最后回电脑登录。明确区分实测、用户反馈、历史结果与待验证。

任何未解释的本地 DNS、公网 IPv6 旁路、WebRTC 运营商出口，或 Claude / 验证请求直连，都先停在验收阶段处理。阿里云等已确认的业务直连单独记录；不把“所有站点分数全绿”作为验收目标。
