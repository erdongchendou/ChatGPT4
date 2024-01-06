## 简介
使用Streamlit框架实现的ChatGPT4聊天工具，并且可以调用DALLE模型进行画图。

## 安装
### 获取openai api-key

按照以下步骤获取api-key:

1. 注册openai账号
2. 进入该网址https://platform.openai.com/account/api-keys.
3. 点击  `Create new secret key` 按钮创建api-key.
4. 复制api-key，将创建的api-key复制到config目录下的api_key.py文件中，放在双引号内


### 创建虚拟环境
在命令号执行以下命令，创建虚拟环境，并按照需要的python库

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### 运行程序
完成以上配置之后，运行以下命令，启动服务
```sh
streamlit run Chatbot.py
```
## 使用方法
<img src="assets/运行后的效果图.jpg" alt="运行后的效果图" style="zoom:30%;" />

### 聊天模式
页面左侧有聊天模式，选择聊天那么就是和GPT4进行纯文字聊天，选择画图则是使用DALLE模型进行画图
### 聊天
在页面下方的输入框，输入你想和GPT4聊天的话，按回车按钮，就可以和GPT4聊天了。
### 画图
在页面下方的输入框，输入你想生成的图片的描述，按回车按钮，就可以生成图片了。
### 英语口语练习
在页面下方的输入框，输入你想要练习的英文，按回车按钮，就会直接翻译成英文，并且会转换成语音。
### 文字转语音
在页面下方的输入框，输入文字各种语言都可以，按回车按钮，就会直转换成语音。

## 我的微信
扫码加我微信，一起交流学习python和人工智能
<img src="assets/微信.jpg" alt="微信" style="zoom:20%;" />

## 我的视频号
扫码加我视频号，可以免费学习《python零基础入门课程》，并提供免费答疑。
<img src="assets/视频号.jpg" alt="视频号" style="zoom:20%;" />

## 买一杯咖啡
如果觉得这个项目帮助到了你，你可以帮作者买一杯咖啡表示鼓励。
<img src="assets/微信收款码.jpg" alt="微信收款码" style="zoom:20%;" />
<img src="assets/支付宝收款码.jpg" alt="支付宝收款码" style="zoom:20%;" />