# COMTool ![Build and Release Status](https://github.com/hydrotho/COMTool/actions/workflows/main.yml/badge.svg)

[English](README.md) | [中文](README_zh.md)

COMTool，一款高效的串口调试工具，专为 TEXT 和 HEX 模式下的串口数据收发设计。

## 快速开始

### 安装

请从 [发布页](https://github.com/hydrotho/COMTool/releases/latest) 下载适用于 Linux、Windows 和 macOS 的预构建静态链接二进制、sdist 和 wheel 文件。

### 使用

启动 COMTool 后，通过按下 `Control+T` 键即可方便地在 TEXT 和 HEX 模式之间进行切换。

```shell
❯ COMTool --help

 Usage: COMTool [OPTIONS]

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│    --version                                                                                                    │
│ *  --port                      TEXT     [required]                                                              │
│ *  --baudrate                  INTEGER  [required]                                                              │
│    --bytesize                  INTEGER  5, 6, 7, 8                                                              │
│                                         [default: 8]                                                            │
│    --parity                    TEXT     N: None, E: Even, O: Odd, M: Mark, S: Space                             │
│                                         [default: N]                                                            │
│    --stopbits                  INTEGER  1, 1.5, 2                                                               │
│                                         [default: 1]                                                            │
│    --xonxoff                                                                                                    │
│    --rtscts                                                                                                     │
│    --dsrdtr                                                                                                     │
│    --install-completion                 Install completion for the current shell.                               │
│    --show-completion                    Show completion for the current shell, to copy it or customize the      │
│                                         installation.                                                           │
│    --help                               Show this message and exit.                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 支持

如果您遇到任何问题或有任何建议，欢迎 [提出问题](https://github.com/hydrotho/COMTool/issues)。

## 许可证

本项目采用 MIT 许可证，详情请参见 [LICENSE](LICENSE) 文件。
