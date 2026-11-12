<p align="center">
  <img src="assets/banner.svg" alt="licensegen" width="800">
</p>

**licensegen** creates a `LICENSE` file in one command. Pick a license, and it fills in your name and the current year. One Python file, zero dependencies, works offline.

## Features

- Built-in texts: MIT, ISC, 0BSD, BSD 2-Clause, BSD 3-Clause, Unlicense
- Name defaults to your `git config user.name`
- Prints to stdout or writes `./LICENSE`
- Refuses to overwrite an existing file unless you pass `--force`

## Install

No install needed. Requires Python 3.8+:

```bash
curl -O https://raw.githubusercontent.com/ERROR404DTIR/licensegen/main/licensegen.py
python3 licensegen.py --list
```

## Usage

```bash
python3 licensegen.py --list                          # show available licenses
python3 licensegen.py mit                             # print MIT to stdout
python3 licensegen.py mit --name "Jane Doe" --write   # write ./LICENSE
python3 licensegen.py isc --year 2024 -w -f           # overwrite with ISC
```

## Options

| Option | Description |
| --- | --- |
| `--list` | List available license ids |
| `--name NAME` | Copyright holder (default: git user.name) |
| `--year YEAR` | Copyright year (default: current year) |
| `-w`, `--write` | Write `./LICENSE` instead of printing |
| `-f`, `--force` | Overwrite an existing `LICENSE` |

## Disclaimer

This tool is a convenience helper and is not legal advice. Read the license text and choose the one that fits your project.

## License

MIT
