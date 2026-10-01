# 嗨拼四级

**毕业这么多年，你还拼得出四级单词吗？** 在线玩：https://hi-spell.vercel.app

一个可以发到推特比一比的 CET-4 拼写挑战。听发音、看中文释义，一个字母一个字母地拼，每个字母当场判对错；连对越多，画面和音乐越热闹。

## 两种玩法

- **今日挑战**：每天 10 个词，所有人同一套题，难度从高频短词升到冷僻长词，每天只有一次机会。按四级的分制计分：满分 710，425 过线。每词 71 分，其中准确 56 分（一遍拼对 56、错过但自己拼出 34、用了浅色提示 14），速度 15 分。
- **60 秒冲刺**：不限次数，一分钟能拼几个算几个，越往后越难。分享链接 `?vs=<种子>-<词数>-<字母数>` 带着同一组词，朋友打开就是同一套题，拼得多的赢。

## 分享

- 「发到 X」：带成绩、不剧透答案的 🟩🟨🟥⬜ 格子和链接
- 「保存图片 / 分享图片」：在浏览器里用 canvas 生成 1080×1350 的成绩报告单；手机上支持系统分享时直接分享图片
- 链接预览卡片：`og.png`，由 `tools/og.html` 用 `tools/build_og.sh` 渲染

## 其他

- 拼错不会结束：同一格错 2 次慢速重读并给词组提示，错 3 次显示浅色字母
- 每日挑战中途离开会保存进度，离开期间不计时
- 发音用浏览器自带的 Web Speech API，音乐和音效全部由 Web Audio 实时合成
- 手机用屏幕键盘，电脑可直接打字（回车重听，Esc 暂停）
- 没有后端，记录只存在本浏览器的 localStorage

## 本地运行

无需构建，静态托管即可：

```bash
python3 -m http.server 8000
```

然后打开 http://localhost:8000/ 。修改 `tools/og.html` 后运行 `sh tools/build_og.sh` 重新生成 `og.png`。

## 重新生成词表

`words.js` 由 `tools/build_words.py` 生成：合并原表中的重复词条、去掉 3 个字母以下的词，按字幕词频和长度分成 16 档；游戏里再排除专有名词和释义里含英文的词。源数据下载地址见脚本开头的注释。

```bash
python3 tools/build_words.py cet4.json en50k.txt
```

## 数据来源与许可

- 代码：MIT License，见 [LICENSE](LICENSE)
- 词表：来自 [KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary)，BSD-3-Clause，Copyright (c) 2022-2026, KyleBing
- 词频分档：来自 [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords)（OpenSubtitles 2018），仅用于排序
- 字体：Bungee、Shantell Sans、ZCOOL KuaiLe，通过 Google Fonts 加载（SIL OFL 1.1）
