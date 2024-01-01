# COMTool ![Build and Release Status](https://github.com/hydrotho/COMTool/actions/workflows/main.yml/badge.svg)

[English](README.md) | [中文](README_zh.md)

COMTool, an efficient serial port debugging tool, specifically designed for receiving and transmitting data through serial ports in TEXT and HEX modes.

## Quick Start

### Installation

Download prebuilt statically-linked binaries, sdist and wheel files from [Releases](https://github.com/hydrotho/COMTool/releases/latest) for Linux, Windows and macOS.

### Usage

Once COMTool is launched, you can easily switch between TEXT and HEX modes by pressing `Control+T`.

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

## Support

If you encounter any issues or have any suggestions, please [open an issue](https://github.com/hydrotho/COMTool/issues).

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.
