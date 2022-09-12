# 第一章 基于 VirtualBox 的网络攻防基础环境搭建



## 实验目的

- 掌握 VirtualBox 虚拟机的安装与使用；
- 掌握 VirtualBox 的虚拟网络类型和按需配置；
- 掌握 VirtualBox 的虚拟硬盘多重加载；



## 实验环境

- Windows 11 宿主机
- VirtualBox 虚拟机
- 攻击者主机（Attacker）：Kali Rolling 2019.2
- 网关（Gateway, GW）：Debian Buster
- 靶机（Victim）：From Sqli to shell / xp-sp3 / Kali



## 实验要求

- 虚拟硬盘配置成多重加载；

- 搭建满足如下拓扑图所示的虚拟机网络拓扑；

<img src="https://c4pr1c3.github.io/cuc-ns/chap0x01/attach/chap0x01/media/vb-exp-layout.png" alt="img" style="zoom:50%;" />

- 完成以下网络连通性测试；
  - [x] 靶机可以直接访问攻击者主机
  - [x] 攻击者主机无法直接访问靶机
  - [x] 网关可以直接访问攻击者主机和靶机
  - [x] 靶机的所有对外上下行流量必须经过网关
  - [x] 所有节点均可以访问互联网



## 实验步骤

配置完成后各主机 IP 地址

| 虚拟机（攻击者/被攻击者-系统-内网） |                    连接方式                    |                             IP                             |
| :---------------------------------: | :--------------------------------------------: | :--------------------------------------------------------: |
|            attacker_kali            |                    NAT 网络                    |                         10.0.2.15                          |
|              gw_debian              | NAT 网络、Host-Ohly 网络、内部网络1、内部网络2 | 10.0.2.4 \| 192.168.56.113 \| 172.16.111.1 \| 172.16.222.1 |
|            victim_xp_01             |                   内部网络1                    |                       172.16.111.146                       |
|           victim_kali_01            |                   内部网络1                    |                       172.16.111.115                       |
|            victim_xp_02             |                   内部网络2                    |                       172.16.222.124                       |
|          victim_debian_02           |                   内部网络2                    |                       172.16.222.114                       |



### 一、配置 Debian（Gateway）

#### VirtualBox 的虚拟网络配置

![gw_debian_vnetwork](img/gw_debian_vnetwork.png)



#### Debian root SSH 登录

```bash
# To enable SSH login for a root user on Debian Linux system you need to first configure SSH server. Open /etc/ssh/sshd_config
vim /etc/ssh/sshd_config

# change the following line
# FROM:
PermitRootLogin without-password
# TO:
PermitRootLogin yes

# Once you made the above change restart your SSH server
/etc/init.d/ssh restart
```



#### 检查配置文件（老师已经配完了）

```bash
# 网卡接口文件
vim /etc/network/interfaces

# 检查DNCP文件,检查是否已开机自启动
vim 
vim /etc/dnsmaq.conf
ps aux | grep dnsm

# 验证防火墙规则是否生效
/sbin/iptables -L -t nat -n
```

![gw_check](img/gw_check.png)



#### 查看 DNS 请求日志

```bash
# 查看 DNS 请求日志
tail -F /var/log/dnsmasq.log
```

![dns_log](img/dns_log.png)



### 二、配置 Windows XP（Victim）

#### VirtualBox 的虚拟网络配置

- 启用网卡1，连接方式为内部网络，局域网一对应 intnet1
- 由于 xp 系统不支持千兆网卡，故选择百兆网卡

![victim_xp_vnetwork](img/victim_xp_vnetwork.png)



#### 关闭防火墙

由于防火墙对网络起到访问控制的作用，在此关闭防火墙，可以保证网关能够访问本机

<img src="img/xp_off_fw.png" alt="xp_off_fw" style="zoom:80%;" />



#### 配置网络信息

查看本地网络链接详细信息，可以看到通过 DHCP 服务器本机已经自动获得 IP 地址、子网掩码、网关等地址信息

![xp_network_set](img/xp_network_set.png)



#### 检查网络连通性

- 网关和靶机可以互相访问，网络连通
- 靶机可以正常访问互联网，且 DNS 服务正常

![gw_xp_ping](img/gw_xp_ping.png)



### 三、配置 Kali（Victim）

#### VirtualBox 的虚拟网络配置

启用网卡1，连接方式为内部网络，intnet1

![victim_kali_vnetwork](img/victim_kali_vnetwork.png)



#### 检查网络分配情况和网络连通性

- 网关和靶机可以互相访问，网络连通
- 靶机可以正常访问互联网，且 DNS 服务正常

![gw_kali_ping](img/gw_kali_ping.png)



### 四、配置 Kali（Attacker）

#### VirtualBox 的虚拟网络配置

![attacker_kali_vnetwork](img/attacker_kali_vnetwork.png)



#### 网络连通性测试

- 靶机可以直接访问攻击者主机

- 攻击者主机无法直接访问靶机、网关

  ![attacker_ping](img/attacker_ping.png)

- 网关可以直接访问攻击者主机和靶机

  <img src="img/gw_attacker_victim_ping.png" alt="gw_attacker_victim_ping" style="zoom:80%;" />

- 攻击者主机可以访问互联网

  ![attacker_ping_Internet](img/attacker_ping_Internet.png)



### 五、网关网络流量监测

#### 抓包实验

```bash
# 新建一个工作目录，用于存放抓包文件
mkdir workplace
cd workplace

# 利用工具 tcpdump 抓包，并保存
tcpdump -i enp0s9 -n -w 20220912.1.pcap
```

在靶机 victim_xp_01 和 victim_kali_01 上进行网络操作，产生网络流量后退出抓包即可



#### 用 Wireshark 分析抓包

```bash
# 将抓到的包复制在宿主机中方便分析

# 在 Windows Terminal 中打开
scp root@192.168.56.113:/root/workspace20220912.1.pcap ./
```

抓包数据如下

![wireshark](img/wireshark.png)

说明靶机的所有对外上下行流量必须经过网关



## 参考资料

- [VirtualBox Network Settings: Complete Guide](https://www.nakivo.com/blog/virtualbox-network-setting-guide/#:~:text=Network%20Modes%20section.-,NAT%20Network,external%20networks%20including%20the%20internet.)
- [Virtualbox 中 Nat 和 Nat Network 模式区别](https://www.zhihu.com/question/277077127)
- [网络安全电子书 黄玮](https://c4pr1c3.github.io/cuc-ns/)



## 课后思考题

以下⾏为分别破坏了CIA和AAA中哪⼀个属性或多个属性？

- 小明抄小强的作业
- 小明把小强的系统折腾死机了
- 小明修改了小强的淘宝订单
- 小明冒充小强的信用卡账单签名
- 小明把自⼰电脑的IP修改为小强电脑的IP，导致小强的电脑⽆法上⽹



有⼀次，小明⼝袋里有100元，因为打瞌睡，被小偷偷⾛了，搞得晚上没饭吃。又⼀天，小明⼝袋里有200元，这次小明为了防范小偷，不打瞌睡了，但却被强盗持⼑威胁抢⾛了，搞得⼀天没饭吃，小明当天就报警了。

- 试分析两次失窃事件中的：风险、资产、威胁、弱点、攻击、影响
- 试用P2DR模型分析以上案例中的“现⾦被抢”事件中的安全策略、安全防护、安全检测和安全响应
- “被抢”事件中，小明的安全策略存在何问题？



针对下述论点，分别设计⼀场景案例（必须和课程相关），使得该论点在该场景中成立

- 预防比检测和恢复更重要
- 检测比预防和恢复更重要
- 恢复比预防和检测更重要



试分析“CAPTCHA图片验证码技术可以阻⽌恶意批量注册⾏为”这句话中的安全策略、安全机制和安全假设分别是什么？CAPTCHA图片举例

![img](https://c4pr1c3.github.io/cuc-ns-ppt/images/chap0x01/captcha-demo.jpg)



某⼤型软件开发公司的总裁担⼼公司的专利软件设计⽅法被内部员⼯泄露给其他公司，他打算防⽌泄密事件的发⽣。于是他设计了这样⼀个安全机制： **所有员⼯必须每天向他汇报自⼰和其他竞争对⼿公司员⼯的所有联系(包括IM、电⼦邮件、电话等等)** 。你认为该安全机制能达到总裁的预期安全效果吗？为什么？



请列举你经常使用的互联⽹服务有哪些，通过公开渠道检索这些服务提供商在历史上是否经历过安全事件？据此，撰写⼀篇主题为：《某某互联⽹服务安全问题概要》的调研报告。
