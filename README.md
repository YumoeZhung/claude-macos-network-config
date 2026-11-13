# Claude macOS 网络配置与登录前验收

给普通用户和代为配置的 Agent：先收敛网络路径，再登录 Claude。主线是 **macOS + Clash Verge Rev + Mihomo + 官方 Claude Desktop / Claude Code**，附 Android Clash Meta 的对应设置。

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
| 0. 确认状态 | 检查 Claude Desktop、Code、浏览器扩展、自动任务是否仍运行 | 配置变更前退出账号客户端；未退出时仅被动检查 |
| 1. 留回滚 | 记录当前订阅、节点、网络服务；私下备份 | 可恢复到原设置，备份不进 Git |
| 2. 建独立配置 | 从用户自有订阅复制本地配置，保留必要直连规则 | 原订阅未覆盖、节点凭据未外传 |
| 3. 配 DNS / IPv6 | DNS 绑定选择组；引导解析独立；关闭 IPv6 | 配置通过内核校验，加载后运行态符合预期 |
| 4. 无账号验收 | 测出口、DNS、IPv6、目标域名与 CDN | 下方所有登录前检查通过 |
| 5. 登录与订阅 | 官方客户端、同一 Claude 账号、用户本人完成认证和付款 | 用户确认账号和订阅状态 |
| 6. 使用中复核 | 用户主动发送正常请求，Agent 被动查看连接 | Claude / Code 的实际请求走预期节点 |

**不要先登录试试看，再修网络。不要在 Claude 工作期间测试其他节点、重载配置、关闭 TUN 或改系统网络。** 如果已经登录，也不必为了重走流程删账号、清 Cookie 或重装；先退出并检查残留进程。

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
在已获授权的配置范围内，备份后建立独立的本地配置，保留原订阅和业务直连规则。
不要收集或上传我的订阅链接、节点密码、账号凭据、聊天内容、Cookie、付款资料。
先验收网络，再让我登录；不要代发测试聊天、代填身份材料或代付费。
最后按 templates/acceptance-report.md 交付本机证据和回滚方法。
```

## 文件导航

- [AGENTS.md](AGENTS.md)：Agent 的执行契约、禁止动作、停止条件。
- [macOS 操作手册](docs/macos-runbook.md)：从退出进程到实际请求验收。
- [多站点检测与结果判读](docs/network-checks.md)：WildAI、IPinfo.CV、Net.Coffee 的分工，DNS / 国内 IPv4 / WebRTC 的检查顺序。
- [DNS / IPv6 技术说明](docs/dns-and-ipv6.md)：为什么这样配、如何判断地区不一致。
- [Android 补充](docs/android.md)：Clash Meta 三层 IPv6、VPN 断线阻断、后台保活。
- [现场记录](docs/field-notes.md)：成功经历、踩坑、已经做过和没有做过的检查。
- [资料与帖子对照](docs/sources.md)：网络工程建议的取舍和官方来源。
- [配置片段](templates/profile-overlay.example.yaml)：仅供合并，不能直接导入作为完整订阅。
- [验收报告模板](templates/acceptance-report.md)：给用户交付，也便于下一个 Agent 接手。

可先运行只读的本机检查：

```bash
python3 scripts/inspect_macos.py
```

它不会联网测试、修改配置、退出应用或启动 Claude；输出仅是初步盘点，不能替代运行态与目标端验收。本仓库不附机场订阅、真实节点服务器、账户或支付材料，也不推荐购买“防封”设备、代 KYC、指纹伪装服务。
