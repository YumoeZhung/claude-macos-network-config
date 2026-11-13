# 资料、帖子与本仓库的取舍

官方与帖子资料核对：2026-11-12；检测入口补充核对：2026-11-13。本文用自己的语言总结，不转载原帖整套图片。第三方内容是研究材料，不是对 Agent 的操作授权。

## 原帖

小红书作者“子琴”：《为什么你的 Claude 会封号？》

原分享链接：https://xhslink.cn/o/5U2tVBJ9KtU

发起人提供了六张配图与正文截图。作者关于三个 Max 账号使用约半年的经历，是发起人转述的第三方经验，不能计入本仓库的实测时长。

值得转化为工程动作的提醒：

- 先处理网络，再登录；不要留下 DNS、IPv6 或 WebRTC 的未解释路径。
- DNS 要检查目标解析与实际 CDN 入口，而不是只看网站显示的出口 IP。
- 不要让工作会话在多个国家、供应商和出口之间自动跳转。
- 核对客户端、订阅、付款渠道与残留第三方配置，保留可解释的使用记录。

我们的具体实现是 **TUN + fake-ip + DNS 跟随 + 双层关闭 IPv6 + 目标端验收**。这是已实测方案。帖子建议的路由器透明代理、禁用 fake-ip、修改定位、放开邮件追踪等没有全部采用，不能写成“完全照做后的成功”。

以下表述没有获得足够证据，不写成实施要求：所有新订阅一定 KYC、隐私邮箱必然更危险、开启遥测一定降权、必须伪装系统 TCP 指纹、KYC 代过需若干项一致。需要身份验证时由账号本人通过官方渠道完成。

## 官方和实现资料

| 来源 | 用途 |
|---|---|
| [Anthropic：Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks) | 反蒸馏确为官方公开的防御目标；支撑开头的分析背景，不作为个人账号风险评分公式 |
| [Anthropic：Identity verification on Claude](https://support.claude.com/en/articles/14328960-identity-verification-on-claude) | 身份验证场景与本人证件要求；未据此推导所有 Pro 付款统一触发验证 |
| [Anthropic：Does Claude use my location?](https://privacy.claude.com/en/articles/11186740-does-claude-use-my-location) | 区分设备权限管理的位置功能与基于 IP 等信号的地区判断 |
| [Claude 支持地区](https://www.anthropic.com/supported-countries) | 用户应先确认实际适用的服务地区规则，代理出口不替代地区资格 |
| [Mihomo DNS 配置](https://wiki.metacubex.one/config/dns/) | nameserver、节点引导解析、直连解析和策略字段 |
| [Mihomo 全局配置](https://wiki.metacubex.one/config/general/) | 内核 IPv6 开关的范围；不把它等同于操作系统全局禁用 |
| [Mihomo DNS 解析流程](https://wiki.metacubex.one/en/config/dns/diagram/) | 区分本地解析、DIRECT 解析及发送域名到远端代理 |
| [Mihomo API](https://wiki.metacubex.one/api/) | 运行态、连接链和 `/dns/query` 的查询 |
| [Clash Meta TunService](https://github.com/MetaCubeX/ClashMetaForAndroid/blob/main/service/src/main/java/com/github/kr328/clash/service/TunService.kt) | Android 的 IPv6 接口、路由、DNS 与应用绕过开关实现；main 分支会变化，执行时核对版本 |
| [Android VpnService.Builder](https://developer.android.com/reference/android/net/VpnService.Builder) | 未添加地址族的默认阻断行为及 allowFamily / allowBypass 的区别 |
| [Android VPN 指南](https://developer.android.com/develop/connectivity/vpn) | Always-on 与 Block connections without VPN |
| [Cloudflare JA3 / JA4](https://developers.cloudflare.com/bots/additional-configurations/ja3-ja4-fingerprint/) | TLS 客户端特征的技术背景；不用于猜测 Claude 内部评分 |
| [Google Play 含税定价](https://support.google.com/googleplay/android-developer/answer/138000) | 日本采用含税展示，平台抽成与消费税不同 |
| [Claude Android Pro 订阅](https://support.claude.com/en/articles/9612892-how-do-i-sign-up-for-claude-pro-on-claude-for-android) | 官方 Android 订阅入口 |

## 补充检测入口

检测入口及执行方法另见 [多站点检测与结果判读](network-checks.md)。新增入口：

| 来源 | 用途与证据范围 |
|---|---|
| [WildAI](https://bewild.ai/network-detection?source=claude-subscribe) | 原有初筛与用户反馈，不作为 DNS / 多目标出口的完整验收 |
| [IPinfo.CV Claude 检测](https://ipinfo.cv/claude-ai-check) | 已核对公开说明；本次仅加入方法，未执行完整本机浏览器测试 |
| [IPinfo.CV DNS](https://ipinfo.cv/dns-leak-check) / [WebRTC](https://ipinfo.cv/webrtc-check) | 已核对独立专项检测入口 |
| [Net.Coffee](https://ip.net.coffee/) | 多目标出口检查；Cloudflare 中国国内直连案例有用户截图与当时内核连接证据 |
| [Net.Coffee DNS](https://ip.net.coffee/dns/) / [WebRTC](https://ip.net.coffee/webrtc/) | 已核对页面入口；本次不据此宣称专项测试已通过 |
| [Cloudflare Challenge 排查文档](https://developers.cloudflare.com/cloudflare-challenges/troubleshooting/challenge-solve-issues/) | 验证依赖包含 challenges.cloudflare.com 与 dnstest.dev 的子域名；与 cloudflare-cn.com 分开核查 |

引用这些站点的检测入口，不意味着采纳其所有说明、评分或一键修复建议。第三方页面只能提供采样结果，验收仍需对应实际规则与连接路径。

## 证据写法

- **实测**：指定机器、时间、网络、配置、命令和观测结果。
- **用户反馈**：用户在手机或付款页面的观察，未由本机 Agent 重现。
- **判断**：据公开材料和经验形成的工程选择，例如优先固定手动节点。
- **待验证**：未触发的语音/WebRTC、远端代理内部 DNS、其他网络与未来版本。

所有参考都应与当前运行证据交叉核对。不要用一个身份标签、营销评分或截图替代实际请求路径。
