# 使用Actions自动发送天气信息到公众号

## 效果

![result](https://github.com/ldm0715/weather_report/blob/master/images/result.jpg)

![workflow](https://github.com/ldm0715/weather_report/blob/master/images/workflow.png)

## 步骤

1. 申请一个[测试微信公众号](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)
2. 扫码添加用户
3. 创建一个模板消息接口，一个模板如下
```
日期：{{date.DATA}} 
地区：{{region.DATA}} 
天气：{{weather.DATA}} 
气温：{{temp.DATA}} 
每日一句：{{today_verse.DATA}}
```
4. 获取到appID、appSecret、OpenID（用户微信号）、模板ID用于后续编码
4. 编写代码，通过api获取天气与每日一句，通过接口发送给用户
5. 编写工作流，从Screates获取api设置与4中的值
6. 推送到github仓库

## 相关文档

- [心知天气开发文档](https://seniverse.yuque.com/hyper_data/datasets/start?)
- [古诗词·一言API](http://gushi.ci/)
- [微信开发文档 - 业务通知](https://mp.weixin.qq.com/debug/cgi-bin/readtmpl?t=tmplmsg/faq_tmpl)
- [微信开发文档 - 获取access_token](https://developers.weixin.qq.com/doc/service/api/base/api_getaccesstoken.html)
- [Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)