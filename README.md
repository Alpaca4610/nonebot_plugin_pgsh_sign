<div align="center">

# nonebot-plugin-pgsh-sign
</div>

# 介绍
- 自用的胖乖生活自动签到获取积分的nonebot插件
- **核心签到脚本来源于网络**，具有时效性
- 签到任务没有写并发，但是不会阻塞机器人其他插件
- IP被ban的话可以将core.py部署到阿里云FC函数计算上，修改调用接口即可
- **使用脚本签到有黑号的风险**

# 使用方法
- 普通用户：
  1. 输入 `开启自动签到 胖乖生活绑定的手机号码`
  2. 直接回复验证码

    完成上述步骤即可开启自动签到，自动签到时间为凌晨一点

- 机器人管理员：

    输入 `立即签到` 即可立即执行签到任务
