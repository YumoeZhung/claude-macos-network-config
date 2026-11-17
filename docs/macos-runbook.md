# macOS：先验收电脑，再交接手机，最后回电脑登录

执行前读 [AGENTS.md](../AGENTS.md) 和 [README 的全局顺序](../README.md)。本手册第 0–5 节完成电脑准备；然后交给手机完成环境、安装、登录和订阅；最后才执行第 7 节电脑登录。已有客户端先结束任务，不需要删除账号、重装系统或重新注册；尚未安装者在此阶段不安装 Claude。

## 0. 只读确认客户端已退出

让用户完成任务并退出 Claude Desktop（⌘Q）、终端 Code、浏览器 Claude 扩展、相关自动任务。检查：

```bash
python3 scripts/inspect_macos.py
```

观察 `claude_processes`、`node_cli_candidates`，并与用户确认浏览器扩展状态。脚本不检查扩展的内部运行状态，也不保证识别所有改名的启动器。

如果仍有 Claude 进程：只读取它的连接，不操作网络。不要把 CC Switch、Codex 路由、其他模型服务当作同一个程序删除。

### 配置网络前，清理浏览器旧登录状态

目的是避免后续进入 Claude 登录流程时，浏览器自动恢复旧账号或已封停账号的会话，导致用户误用账号。公开文档只说明通用场景，不记录个人账号或申诉材料。

关闭 Claude 网页、退出扩展并停止相关任务后，通过浏览器设置处理站点数据，不打开 Claude 登录页来检查是否退出。新浏览器配置文件没有相关站点数据时记录“无残留”。

- **默认范围**：Chrome 设置中搜索“网站数据”，查看所有网站数据和权限，搜索并删除 `claude.ai` 及实际使用的 Claude 登录站点数据。不同版本入口名称可能不同，按当前界面核对；不要清理无关业务站点。
- **用户明确选择的简便方式**：Chrome“删除浏览数据”中选“所有时间”，勾选“Cookie 和其他网站数据”。会清除该浏览器配置文件中其他网站的登录状态，先完成 EAS / DSW 等正在进行的工作；不要顺带勾选密码、历史等其他项目。界面若有额外删除范围提示，按实际提示确认。
- 不读取或导出 Cookie 内容；只记录清理范围、时间与完成状态。备份网络配置不包含复制浏览器认证数据。
- 清 Cookie 解决的是浏览器旧会话残留，不能代替退出 Desktop / Code，也不会清除服务端记录或重置设备身份。不同账号的日常操作可用不同浏览器配置文件避免 Cookie 混用。
- 清理不会自动替用户选择正确账号；Google 等第三方登录状态、浏览器密码自动填充也可能仍在。真正登录时核对邮箱 / 账号，不直接接受默认选择，也不为此默认清除所有 Google 登录或保存密码。

## 1. 记录基线和私下备份

记录当前网络（公司 Wi-Fi / 家庭 Wi-Fi / 热点）、Clash 版本、Mihomo 版本、配置名称、选择组和最终节点。不要为了记录而重新选择节点。

Clash Verge Rev 常见配置目录：

```text
~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/
```

备份 `profiles.yaml`、当前 profile、相关 Merge/Script、`verge.yaml`、当前生成配置。实际目录与引用关系以安装版本为准。**整个目录可能含订阅链接和节点密码，只备份到用户私有目录。**

记录网络服务原状态：

```bash
networksetup -listallnetworkservices
networksetup -getinfo 'Wi-Fi'
networksetup -getinfo 'Thunderbolt Bridge'
```

后两条仅在本机确实存在这些服务时执行。对于 Manual IPv6，要完整保存地址、前缀和路由器；不能统一回滚为 Automatic。

停止条件：备份不完整、无法辨认当前配置、用户仍在进行重要会话。

## 2. 建立独立的本地配置

从用户原订阅复制一份，命名例如 `Claude 网络 · DNS 跟随 · IPv4`。保留原远程订阅，后续在界面切回即可恢复原代理配置。注意：**切订阅不会恢复 macOS IPv6 设置**，系统回滚单独执行。

- 保留原 `proxies` / `proxy-providers` 和有效代理组；不把密码贴进聊天或仓库。
- 主选择组使用手动 `select`，末级选择一个稳定节点。必要时切换，但不做连续轮换测试。
- 在既有规则前部确保 `claude.ai`、`anthropic.com`、`claudeusercontent.com` 走该组；其他实际观察到的 Claude 服务域名也要验收。
- 同步核对 `claude.com` 及 Cloudflare 验证依赖 `challenges.cloudflare.com`、`dnstest.dev` 的实际匹配顺序、DNS 策略和末级节点。模板不是完整依赖清单；缺少必要规则时，在已授权的候选配置中补齐后验收，不把历史待验证项算作通过。
- 保留用户确实需要的业务直连。Typeless、向日葵只是现场示例，不能给所有用户无条件添加。
- **由用户选择电脑直连范围**：先记录应用 / 站点、希望直连的用途及验收方法，已有授权清单可直接沿用。应用可按进程路径匹配，浏览器中的 EAS / DSW 等业务按实际域名匹配；不要将整个浏览器设为 DIRECT。必要时配置精确 DNS 例外，检查不覆盖 Claude 及验证依赖。原订阅的宽泛国内直连规则另行说明，不宣称配置只包含用户列出的精确例外。
- 本地 profile 通常不会自动同步机场更新。更新时重新合并和验收，不直接覆盖已验证版本。

参考 [配置片段](../templates/profile-overlay.example.yaml)。它不是完整订阅，不能独立导入。

需要收紧原订阅的直连例外时，按 [规则收紧与回滚](rule-tightening.md) 单独形成删除清单、归档并验收；不要直接套用案例的 105 条数量。检查代理组的实际选择，不能仅搜索 `DIRECT`。保留国内 GeoIP 后，撤销域名例外仍可能得到直连结果。

## 3. 配置 DNS 跟随节点

核心设置：

```yaml
dns:
  nameserver:
    - "https://1.1.1.1/dns-query#实际选择组名称"
  proxy-server-nameserver:
    - 223.5.5.5
    - 119.29.29.29
```

`#` 后必须是本机真实存在的选择组；不能保留占位词，也不要写死某一个日本节点，否则改选美国节点后 DNS 仍可能走日本。

引导解析仅用于建立代理所必需的节点域名解析。引导 DNS 根据当前网络选择可达服务器，不要让它依赖自己尚未建立的代理。对常规目标域名，不要追加系统 DNS 或加入未验证的直连 fallback。

直连应用需要直连解析时，使用 `direct-nameserver` 与精确 `nameserver-policy`。检查 Claude 域名不在这些例外中。保留 fake-ip，不在同一轮同时切换 redir-host、TUN 栈和 DNS 上游。

Clash Verge 的 DNS 覆写、订阅 Merge/Script 可能改变结果。检查最终生成配置中的 `nameserver`、`nameserver-policy`、`proxy-server-nameserver`、`direct-nameserver`、`fallback` 和 `enhanced-mode`。手机的“追加系统 DNS”不是电脑 DNS 覆写的同义词。

用本机 Mihomo 的 `-t -d <数据目录> -f <候选配置>` 校验，参数先看该版本 `--help`。校验需能访问 GeoData / provider 资源；不要为了通过校验删除业务规则。语法通过后再加载独立配置。

## 4. 双层关闭 IPv6

### Clash 层

Clash Verge Rev 2.5.8 的路径：**设置 → Clash 设置 → IPv6**。关闭后检查最终配置：

```yaml
ipv6: false
dns:
  ipv6: false
```

现场版本关闭界面开关后两项都变成 false；其他版本仍需实测。DNS 的 false 只说明不提供 AAAA 答案，不代表操作系统协议栈关闭。

### macOS 网络服务层

在已授权配置范围内，对 `-listallnetworkservices` 列出的每个适用服务关闭 IPv6。命令中的名称必须来自本机清单；忽略列表说明行，正确处理禁用服务名前的标记。

```bash
networksetup -setv6off 'Wi-Fi'
networksetup -setv6off 'Thunderbolt Bridge'
networksetup -getinfo 'Wi-Fi'
networksetup -getinfo 'Thunderbolt Bridge'
```

需要权限时使用系统正常授权流程，由用户输入密码；禁止把密码写进命令或交给 Agent。不要关闭 Wi-Fi、拔网线或改 IPv4、网关、Clash 节点。

预期现有服务显示 `IPv6: Off`。回环 `::1`、AirDrop / AWDL 及系统虚拟接口的 `fe80::` 地址可以保留；不要为了“没有任何 IPv6 字符串”破坏系统服务。新接入的 USB 网卡、VPN 服务需要另查。

原状态为 Automatic 的服务可这样回滚：

```bash
networksetup -setv6automatic 'Wi-Fi'
networksetup -setv6automatic 'Thunderbolt Bridge'
```

原状态为 Off / Link-local / Manual 的服务按原记录恢复，不照抄上面两条。

## 5. 不登录账号的网络验收

可以由 Agent 使用 CLI 请求公开诊断地址，不启动 Claude，不发送 Cookie / API Key。测试本身会向目标站点发出普通网络请求；它不是被动检查。

### 5.1 运行态

在 Clash 首页核对独立配置、TUN、规则模式、末级节点。若需要本地 API，从运行中的 Mihomo 启动参数找 `-ext-ctl-unix`，不要只相信生成文件里的 socket：现场两者路径不同。

已有本地控制器可读取 `/version`、`/configs`、`/proxies`、`/connections`、`/dns/query`。不要为了查询开放网络监听或移除认证，不把 secret 输出到终端。没有 API 访问条件时使用 Clash 的连接界面，未取得的证据注明。

### 5.2 IPv4 / IPv6 对照

```bash
curl --noproxy '*' -4 --connect-timeout 5 --max-time 10 https://www.cloudflare.com/cdn-cgi/trace
curl --noproxy '*' -6 --connect-timeout 5 --max-time 10 --resolve 'one.one.one.one:443:[2606:4700:4700::1111]' https://one.one.one.one/cdn-cgi/trace
curl --noproxy '*' -6 --connect-timeout 5 --max-time 10 --resolve 'dns.google:443:[2001:4860:4860::8888]' https://dns.google/
```

`--noproxy '*'` 不关闭 TUN，只避免 curl 环境中的显式 HTTP 代理掩盖本机 IPv6 状态。两条 IPv6 命令指定地址，避免把“没有 AAAA 结果”误当成 IPv6 路径已阻断。

通过标准：IPv4 成功且出口符合预期；两条 IPv6 失败；网络服务 Off，物理接口无公网 IPv6。证书、HTTP 状态错误不是 IPv6 不通的证据，需检查失败阶段；任何成功的 IPv6 TCP/TLS 连接都需继续排查。单个网站超时也不够。

### 5.3 多站点初筛、分流与 DNS / WebRTC

按 [多站点检测与结果判读](network-checks.md) 执行：

1. 用 [WildAI](https://bewild.ai/network-detection?source=claude-subscribe) 与 [IPinfo.CV Claude 检测](https://ipinfo.cv/claude-ai-check) 做综合初筛，保留字段明细。
2. 用 [Net.Coffee](https://ip.net.coffee/) 的网站分流测试检查不同目标看到的 IPv4 出口；出现国内出口时查具体域名与命中规则。保留用户要求的 EAS / DSW 等直连，Claude 与验证依赖的意外直连须处理。
3. 做下述 DNS 交叉验证；可用 [Net.Coffee DNS](https://ip.net.coffee/dns/) 与 [IPinfo.CV DNS](https://ipinfo.cv/dns-leak-check) 补充。
4. 用 [Net.Coffee WebRTC](https://ip.net.coffee/webrtc/) 或 [IPinfo.CV WebRTC](https://ipinfo.cv/webrtc-check) 核对有效公网候选地址和 UDP 路径。无候选或超时记未验证，不视为代理通过。

综合检测页低风险不能结束验收。保持原节点与模式，不为消除红色提示开启全局代理或删除业务直连规则。

使用用户实际浏览器访问 [BrowserLeaks DNS](https://browserleaks.com/dns) 与 [DNSLeakTest](https://www.dnsleaktest.com/)（Extended test）。记录出口、解析器归属和时间。

- 初始发现本地联通解析器参与，属于需追踪的旁路信号，暂停登录。
- 日本出口下出现日本 / 美国公共解析器，进入目标域名核查；不要按国旗数量直接判定失败或通过。
- 核对浏览器安全 DNS、系统私人 DNS、应用自带 DoH 是否另有路径。不要批量禁用安全功能；只在采用 Clash 统一解析方案时明确统一入口。

### 5.4 目标域名与 CDN（必做）

检查 `claude.ai`、`api.anthropic.com`、`bridge.claudeusercontent.com`：

1. 系统解析结果：fake-ip 模式下通常为 `198.18.x.x`，这是本地映射。
2. 内核 `/dns/query?name=<域名>&type=A` 查询真实答案；DNS listener 的 AAAA 查询确认空答案。
3. 沿当前代理访问配置的 Cloudflare DoH，查询同一域名，比较真实答案。轮换的 CDN 地址不要求逐字相同，但需解释是否属于同一服务及合理调度。
4. 查看 `1.1.1.1:443` DNS 连接的实际代理链，确认走当前末级节点。
5. 对目标发送无账号诊断请求：

```bash
curl --noproxy '*' --connect-timeout 5 --max-time 10 https://claude.ai/cdn-cgi/trace
curl --noproxy '*' --connect-timeout 5 --max-time 10 https://api.anthropic.com/cdn-cgi/trace
curl --noproxy '*' --connect-timeout 5 --max-time 10 https://bridge.claudeusercontent.com/cdn-cgi/trace
```

记录 `ip`、`loc`、`colo`，与出口一致性比对；同时核对连接中的规则与代理链。响应带 `CF-Ray` 时可参考其机房后缀。路径将来若不可用、返回挑战页或没有这些字段，不绕过验证，不把 403 / 缺字段当作验证通过，改用可取得的服务端证据并写清待验证项。

不要通过 IP 地理数据库把 Anycast 地址强行映射到唯一国家；服务端 `colo` 更能反映本次入口。本次现场三域名均返回 JP / NRT，详见 [DNS 说明](dns-and-ipv6.md)。远端节点内部的二次解析仍是可见性边界。

### 5.5 业务直连与回滚验收

确认用户要直连的应用命中精确规则，必要业务可用。仅 HTTP 成功不能替代语音识别、远控会话的完整业务验收。不要借机打开与本任务无关的账号页面。

填好 [验收报告](../templates/acceptance-report.md)。任何关键项未完成，不引导用户登录。

## 6. 电脑验收后，转手机环境、安装与付款

记录电脑第 5 阶段结果后，保持电脑配置与节点，执行 [Android 手册](android.md) 的顺序：手机配置 → 手机独立验收 → Google Play 下载官方 App → 设置后台 / 权限 → 用户登录 → 用户完成订阅。不要因电脑测试通过就提前登录 Desktop 或 Code。

手机订阅阶段只记录用户确认的权益结果，不采集凭据或付款材料。已有有效 Pro 订阅时核对即可，不重复付款。整个流程中如某台设备已登录，先退出相关任务，按既有用户分支检查，不强制重装。

## 7. 最后安装并登录电脑，然后被动复核

确认手机环境和订阅阶段完成，复核电脑仍是已验收配置 / 节点；若电脑换过网络或配置，先重新验收，再登录。尚未安装 Desktop 时，此时从官方渠道下载安装；已安装则核对来源，无需重装。不要先启动客户端再连接代理。

用户自行在电脑登录与手机相同的 Claude 账号，核对 Pro 权益，再按需使用 Code。Code 走订阅登录还是 API / Gateway 要分清；不要泄露密钥，也不要把第三方网关额度当作 Pro 权益。

用户发送一条正常消息后，读取进程套接字和 Clash 连接：实际域名、进程、IPv4/IPv6、TCP/UDP、命中规则、最终节点。没有观察到 UDP 只代表采样期间的情况；语音 / WebRTC 应单独验收。

结束时复核订阅与节点没有漂移，交付回滚位置。需要换节点或更新本地配置时，先退出任务，再复用第 5 阶段；不要让 Agent 自动在“问题节点”之间试错。

订阅更新的完整顺序见 [维护与经验补充](maintenance-and-findings.md)。维护已有配置不要求重复手机充值或重装客户端。
