# Claude macOS 网络配置与登录前验收

给普通用户和代为配置的 Agent：**先验收电脑环境，再验收手机环境；手机下载安装、登录并完成订阅后，最后登录电脑。** 主线是 **macOS + Clash Verge Rev + Mihomo + Android Clash Meta + 官方 Claude App / Desktop / Claude Code**。

流程与会话经验最后整理：**2026-11-17**。下方实测日期单独保留，整理日期不代表当天重新完成全部网络测试。

## 我们如何理解 Claude 的账号风控

**我们的工作假设：防止国内模型厂商通过账号集群大规模蒸馏，是理解 Anthropic 账号风控的重要背景。** Anthropic 已公开披露并处置此类攻击。因此，我们优先关注正常个人使用与规模化滥用之间的区别：账号由本人使用、客户端来源清楚、付款有授权、网络出口稳定、DNS 和实际请求路径协调。

“越像一个真人、越像一个长期在境外正常使用的真人”是发起人的直觉判断；本仓库把其中可执行的部分落实为**真实、稳定、可解释的个人使用环境**，不把它写成已测出的封号概率公式，也不据此伪造身份、地址、定位或设备指纹。反蒸馏之外，官方还执行其他安全、付款及地区政策，账号地区资格应先按官方要求确认。

我们采用保守的工程标准：发现 DNS 旁路、公网 IPv6 直连或请求出口异常，就暂停登录并修复；不等账号出问题后再排查。

## 本次实测经历

截至 **2026-11-12**：

- 使用独立的 Clash Verge 本地配置，实现 DNS 跟随手动选择的节点；原订阅保留，便于回滚。
- Claude 的三个主要域名经同一个日本节点访问，目标端诊断均返回日本出口和 `NRT` CDN 入口。
- Clash 的 `ipv6`、`dns.ipv6` 已关闭；macOS 现有 Wi-Fi、Thunderbolt Bridge 服务的 IPv6 均为 Off。
- Claude Desktop 及内置 Code 响应期间，采样连接经过 TUN 和选定节点。
- 通过 Android Google Play 订阅 Pro，使用经持卡人授权的 Mastercard，订阅时没有弹出 KYC；随后桌面端正常使用。

这是一次已走通的配置和短期使用记录，观察截止日期如上；后续使用记录应另行更新，不能写成长达半年的本仓库实测。详见 [现场记录](docs/field-notes.md)。

## 必须按这个顺序做

| 阶段 | 操作 | 进入下一阶段的条件 |
|---|---|---|
| 0. 退出与清理 | 完成任务，关闭旧 Claude 网页、Desktop、Code、扩展和自动任务；清理浏览器 Claude 相关 Cookie / 站点数据 | 无活动会话；清理范围和影响已知，未启动新客户端 |
| 1. 电脑留回滚 | 记录当前订阅、节点、网络服务；私下备份 | 可恢复原网络设置，备份不进 Git |
| 2. 电脑建独立配置 | 从用户自有订阅复制本地配置，保留必要业务直连 | 原订阅未覆盖、节点凭据未外传 |
| 3. 电脑配 DNS / IPv6 | DNS 绑定选择组；引导解析独立；关闭 IPv6 | 通过内核校验，加载后运行态符合预期 |
| 4. 电脑无账号验收 | WildAI、IPinfo.CV、Net.Coffee 初筛与专项测试；另验目标解析、出口和 CDN 入口 | 电脑检查完成，尚不安装或登录新的 Claude 客户端 |
| 5. 手机环境 | 配 Clash Meta、DNS / IPv6、VPN 双开关和代理保活；在实际使用的网络独立验收 | 手机有独立证据，不能照搬电脑结果；尚不下载安装新的 Claude App |
| 6. 手机安装与登录 | 从 Google Play 下载官方 Claude，设置权限与后台限制，再由用户登录 | 使用预定账号，网络仍为已验收配置 |
| 7. 手机充值 | 核对 Play 商店国家、付款资料、金额和续费条款，由用户完成授权付款 | 用户确认同一 Claude 账号的 Pro 已生效；已订阅者不重复付款 |
| 8. 最后登录电脑 | 复核电脑环境未变化，再安装官方桌面客户端（如尚未安装）并登录同一账号；按需配置 Code | 分清 Pro 登录与 API / Gateway，核对账号权益 |
| 9. 使用中复核 | 用户主动发送正常请求，Agent 被动查看连接 | Claude / Code 的实际请求走预期节点 |

**不要先下载启动、登录或付款，再回头修网络。不要在 Claude 工作期间测试其他节点、重载配置、关闭 TUN 或改系统网络。** 已安装者先退出并检查残留进程，无需为了重走流程卸载客户端、删除账号或重复充值。

Cookie 清理放在电脑网络配置之前，目的是**避免后续登录沿用旧账号，尤其是自动恢复已封停账号的会话**。优先按站点清理 `claude.ai` 及实际使用的 Claude 登录站点；Chrome 也可选择“删除所有 Cookie 和网站数据”（时间范围选所有时间），但会使其他网站退出登录，影响 EAS / DSW 等工作页面，不应顺带删除密码、历史或其他资料。清理后仍要在登录页核对预定账号；这不是设备指纹或服务端记录的重置。细节见 [操作手册第 0 节](docs/macos-runbook.md)。

## 登录前检查点

- [ ] 原订阅、原网络设置、回滚步骤均已记录。
- [ ] TUN 开启，规则模式生效，手动选定节点；需要固定出口时不使用自动轮换组。
- [ ] Claude 及 Anthropic 域名没有命中 DIRECT、直连 DNS 策略或应用绕过列表。
- [ ] DNS 上游连接走选定代理，节点域名解析不会依赖尚未建立的代理造成循环。
- [ ] 常规 DNS 测试未出现未经解释的本地运营商解析器。
- [ ] 已用下方工具交叉检查；网站分流中的国内 IPv4 出口已逐项解释，Claude 及验证依赖没有意外直连。
- [ ] Clash `ipv6: false`、`dns.ipv6: false` 已生效；现有 macOS 网络服务 IPv6 Off。
- [ ] 指定公网 IPv6 地址的测试失败，同时 IPv4 测试成功。
- [ ] Claude 目标端出口地区符合预期；能取得 CDN 入口时核对其地区，异常已解释或排除。
- [ ] 用户要求直连的应用仍按原目标工作。

无法取得某项证据时填写“未验证”，不要用别人的截图、电脑端结果或相同节点名称代替本机验收。

## 网络检测入口：不要只看 WildAI

按“综合初筛 → 网站分流 → DNS → WebRTC → 目标服务路径”的顺序检查。以下测试放在**登录前的无账号验收阶段**；已经在使用 Claude 时，先完成任务并退出，再主动检测。

| 入口 | 本仓库用它检查什么 |
|---|---|
| [WildAI 网络检测](https://bewild.ai/network-detection?source=claude-subscribe) | 保留为出口初筛；此前的低风险结果没有覆盖后来发现的联通 DNS 和网站国内直连出口 |
| [IPinfo.CV：Claude AI IP 检测](https://ipinfo.cv/claude-ai-check) | 补充出口地区、网络属性与环境提示；DNS / WebRTC 告警继续看独立测试明细 |
| [Net.Coffee：IP 查询与网站分流](https://ip.net.coffee/) | 比较访问不同目标的实际出口，排查浏览器是否还会向某些目标暴露国内 IPv4 |
| [Net.Coffee DNS](https://ip.net.coffee/dns/) / [IPinfo.CV DNS](https://ipinfo.cv/dns-leak-check) | 查看解析器地址和运营商，与 [BrowserLeaks DNS](https://browserleaks.com/dns) / [DNSLeakTest](https://www.dnsleaktest.com/) 交叉验证 |
| [Net.Coffee WebRTC](https://ip.net.coffee/webrtc/) / [IPinfo.CV WebRTC](https://ipinfo.cv/webrtc-check) | 核对浏览器候选公网地址与预期代理出口，单独排查 UDP 路径 |

**DNS 解析器、网站看到的 IPv4 出口、WebRTC 候选地址是不同检查项。** 综合评分不能替代这些明细。阿里云 EAS / DSW 等用户明确要求的直连应保留；发现国内出口时查具体域名与命中规则，不为了页面全绿把整个浏览器改为代理。

**电脑哪些应用或站点直连，由使用者自行选择。** Agent 先整理用户的直连清单，再配置对应规则和必要的 DNS 例外，并验证业务。Typeless、向日葵、EAS、DSW 只是本次案例，不默认加入其他人的配置；也不把整个 Chrome 设为直连。

**2026-11-17 更新**：Mac 本地配置撤销 105 条非必要直连例外，规则从 2,479 条降至 2,374 条，DNS 与节点选择未变。保留本地网络、明确业务、国内 IP / 国内媒体规则，其余默认代理。这是整份订阅的规则数，不是 Claude 专用规则数；手机尚未同步。完整变更、实测边界和回滚流程见 [直连规则收紧](docs/rule-tightening.md)。

详细操作、Cloudflare 中国案例及停止条件见 [多站点检测与结果判读](docs/network-checks.md)。

## 手机使用前再检查

除了 Clash Meta 的 DNS / IPv6 配置，还建议在手机 VPN 设置中同时开启 **“始终开启的 VPN”** 与 **“屏蔽未使用 VPN 的所有连接”**；把 **Claude、Google Play 商店** 的省电策略设为 **“禁止后台运行”**，而 **Clash Meta 保持后台无限制并允许自启动**。系统文案可能不同，须按实际界面核对。禁止后台运行不等于强行停止；切节点前仍须停止 Claude。具体步骤和验收见 [Android / 小米补充](docs/android.md)。

要退出 Claude 后恢复境内直连，先在系统应用信息中**强行停止 Claude**，再按需解除 VPN 阻断并断开 VPN；下次先恢复代理与保护开关、验收后再开 Claude。阻断仍开启时，关闭 VPN 通常会断网，不会自动恢复直连。

## 让你的 Agent 开始工作

把下面这段发给有本机操作权限的 Agent：

```text
请读取这个仓库的 AGENTS.md 和 docs/macos-runbook.md，按阶段完成本机配置。
先只读检查 Claude Desktop、Claude Code、扩展和后台任务。
如果仍在运行，只做被动检查，先让我结束任务；不要切节点或重载网络。
配置电脑网络前，按明确范围清理 Claude 相关 Cookie / 站点数据；不要默认清掉所有网站登录状态。
在已获授权的配置范围内，备份后建立独立的本地配置，保留原订阅和业务直连规则。
先确认我希望保持直连的应用和站点；按我的清单配置并验收，不照搬案例中的应用，也不把整个浏览器设为直连。
不要收集或上传我的订阅链接、节点密码、账号凭据、聊天内容、Cookie、付款资料。
先用测试网站及目标端诊断验收电脑，再配置和验收手机；然后才下载手机官方 Claude App、让我登录和订阅。
确认手机订阅已生效后，最后让我在电脑登录同一账号；已有订阅不要重复付款。
不要代发测试聊天、代填身份材料或代付费。
最后按 templates/acceptance-report.md 交付本机证据和回滚方法。
```

## 文件导航

- [AGENTS.md](AGENTS.md)：Agent 的执行契约、禁止动作、停止条件。
- [macOS 操作手册](docs/macos-runbook.md)：从退出进程到实际请求验收。
- [多站点检测与结果判读](docs/network-checks.md)：WildAI、IPinfo.CV、Net.Coffee 的分工，DNS / 国内 IPv4 / WebRTC 的检查顺序。
- [DNS / IPv6 技术说明](docs/dns-and-ipv6.md)：为什么这样配、如何判断地区不一致。
- [Android 补充](docs/android.md)：Clash Meta 三层 IPv6、VPN 断线阻断、后台保活。
- [现场记录](docs/field-notes.md)：成功经历、踩坑、已经做过和没有做过的检查。
- [维护与经验补充](docs/maintenance-and-findings.md)：原生与跟随版对比、订阅更新、检测工具误报及当前待办。
- [直连规则收紧与回滚](docs/rule-tightening.md)：105 条例外删除、GeoIP / MATCH 解释、运行态验收与节点故障范围。
- [资料与帖子对照](docs/sources.md)：网络工程建议的取舍和官方来源。
- [配置片段](templates/profile-overlay.example.yaml)：仅供合并，不能直接导入作为完整订阅。
- [验收报告模板](templates/acceptance-report.md)：给用户交付，也便于下一个 Agent 接手。

可先运行只读的本机检查：

```bash
python3 scripts/inspect_macos.py
```

它不会联网测试、修改配置、退出应用或启动 Claude；输出仅是初步盘点，不能替代运行态与目标端验收。本仓库不附机场订阅、真实节点服务器、账户或支付材料，也不推荐购买“防封”设备、代 KYC、指纹伪装服务。
