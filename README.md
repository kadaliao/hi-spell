# 嗨拼四级

一个 CET-4 单词拼写游戏，只需浏览器。听发音、看中文释义，一个字母一个字母地拼，每个字母当场判对错。拼错不扣分，也没有 Game Over；连对越多，画面和音乐越热闹。

玩法参考了 [dopa-drill](https://github.com/grmchn/dopa-drill)（算数版的同类设计），这里把它的核心循环搬到了英语拼写上。

## 特点

- 4521 个四级词，按「常用程度 × 单词长度」分成 16 个词阶。左边和上边的阶掌握后解锁下一阶；某阶最近 6 次里 5 次一遍拼对即算掌握，之后还能升到 ☆2、☆3
- 第一次玩先做 10 词的实力测试，自动跳到适合的起点
- 同一格错 2 次：慢速重读并给出词组提示；错 3 次：显示浅色字母
- 错词本 + 间隔复习：拼错的词会在之后的轮次里穿插出现，一遍拼对即移出
- 一遍拼对 ≥ 80% 可挑战 90 秒加时，第 k 个词加 10+5k 分
- 发音用浏览器自带的 Web Speech API，音乐和音效全部由 Web Audio 实时合成，没有音频文件
- 手机竖屏用屏幕键盘，电脑可直接打字（回车重听，Backspace 删除，Esc 退出）
- 记录只存在本浏览器的 localStorage，不上传

## 本地运行

无需构建，静态托管即可：

```bash
python3 -m http.server 8000
```

然后打开 http://localhost:8000/ 。

## 重新生成词表

`words.js` 由 `tools/build_words.py` 生成：合并原表中的重复词条、去掉 3 个字母以下的词，按字幕词频分档。源数据下载地址见脚本开头的注释。

```bash
python3 tools/build_words.py cet4.json en50k.txt
```

## 数据来源与许可

- 代码：MIT License，见 [LICENSE](LICENSE)
- 词表：来自 [KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary)，BSD-3-Clause，Copyright (c) 2022-2026, KyleBing
- 词频分档：来自 [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords)（OpenSubtitles 2018），仅用于排序
- 字体：Bungee、Shantell Sans、ZCOOL KuaiLe，通过 Google Fonts 加载（SIL OFL 1.1）
