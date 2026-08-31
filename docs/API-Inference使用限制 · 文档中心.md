---
title: "API-Inference使用限制 · 文档中心"
source: "https://modelscope.cn/docs/model-service/API-Inference/limits"
author:
published:
created: 2026-08-31
description: "ModelScope——汇聚各领域先进的机器学习模型，提供模型探索体验、推理、训练、部署和应用的一站式服务。在这里，共建模型开源社区，发现、学习、定制和分享心仪的模型。"
tags:
  - "clippings"
---
魔搭通过API-Inference，将开源模型服务化并通过API接口进行标准化， **免费** 提供给广大开发者体验。具体使用方式请参见 [说明文档](https://modelscope.cn/docs/model-service/API-Inference/intro) 。API-Inference 本身为 *非商业化，非盈利* 产品， 为了在有限的平台资源下，最大范围的服务广大开发者，并保障使用的公平性，API-Inference对于使用额度和并发会进行一定限制，同时根据实时资源使用情况，会实时进行动态调整。具体说明如下：

## API-Inference 使用限制#

- 魔搭推理API-Inference，旨在为开发者提供免费的便捷模型调用方式， **请勿用于需要高并发以及SLA保障的线上任务** ，如有商业化使用的需求，建议使用各商业化平台的API。
- 免费推理API由阿里云提供算力支持， **要求您的ModelScope账号必须首先 [绑定阿里云账号](https://modelscope.cn/docs/accounts/aliyun-binding-and-authorization)** 。同时为了防止滥用，对应云账号需已通过 [**实名认证**](https://help.aliyun.com/zh/account/real-name-authentication) 后，才可正常使用API-Inference。
- 不同模型允许的调用并发，会根据平台的压力进行动态的速率限制调整，原则上以 **保障开发者单并发正常使用** 为目标。
- 支持使用魔粒兑换 API-Inference 调用，魔粒余额充足即可调用任意次数。根据所需的基础算力和模型规模，魔粒扣减分为三档：轻量模型（0.5 魔粒/次），主流模型（1 魔粒/次），旗舰模型（2 魔粒/次）。魔粒体系说明请参考（ [链接](https://modelscope.cn/docs/magicube/intro) ）。

## 查看 API-Inference 魔粒扣减额度#

在代码范例右上角，当选择 API 提供为「魔搭社区」时，在 API 提供左侧展示「预计魔粒扣减」。 ![img.png](https://resouces.modelscope.cn/document/docdata/2026-8-30_13-22-CN/dist/model-service/API-Inference/limits/_resources/api_inference_magicube.png)

> [!important] Important
> 随着新模型的推出，比较早的模型可能逐渐从API-Inference下架.

如果需要高并发，大额度的调用，可以考虑通过 [API-Provider](https://modelscope.cn/docs/model-service/API-Inference/api-provider) 来绑定外部API提供方后使用。

## API-Inference 支持的模型范围#

当前API-Inference为魔搭平台上的部分开源 **大语言模型（LLM）** ， **多模态模型（MLLM）** ，以及 [**AIGC专区文生图模型**](https://www.modelscope.cn/aigc/models) 等，提供了可直接使用的API。

API-Inference覆盖的模型范围，主要根据模型在魔搭社区中的关注程度（参考了点赞，下载等数据）来判断。因此，在能力更强，关注度更高的下一代开源模型发布之后，支持的模型清单也会持续迭代。开发者可根据模型页面的过滤条件直接筛选，根据标记有“蓝绿色闪电”的 API-Inference logo 来判断。 ![img.png](https://resouces.modelscope.cn/document/docdata/2026-8-30_13-22-CN/dist/model-service/API-Inference/limits/_resources/api-inference-logo.png)

同时在模型详情页面右侧，对于支持API-Inference的模型，也会展示使用入口和对应的代码范例。 ![img.png](https://resouces.modelscope.cn/document/docdata/2026-8-30_13-22-CN/dist/model-service/API-Inference/limits/_resources/api-inference-sample-code.png)

后续我们会积极推进API-Inference支持的模型的覆盖范围，✌️ 敬请期待️。