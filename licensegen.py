#!/usr/bin/env python3
"""licensegen - generate a LICENSE file with your name and year.

Usage:
  licensegen --list
  licensegen mit                         print MIT to stdout
  licensegen mit --name "Jane Doe"       custom copyright holder
  licensegen isc --write                 write ./LICENSE (use --force to overwrite)
"""
import argparse
import datetime
import subprocess
import sys
from pathlib import Path

MIT = """MIT License

Copyright (c) {year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

ISC_DISCLAIMER = """THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""

ISC = """ISC License

Copyright (c) {year} {name}

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

""" + ISC_DISCLAIMER

ZERO_BSD = """Copyright (C) {year} by {name}

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

""" + ISC_DISCLAIMER

BSD2 = """BSD 2-Clause License

Copyright (c) {year}, {name}

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

BSD3 = BSD2.replace("BSD 2-Clause", "BSD 3-Clause").replace(
    "THIS SOFTWARE IS PROVIDED BY",
    "3. Neither the name of the copyright holder nor the names of its\n"
    "   contributors may be used to endorse or promote products derived from\n"
    "   this software without specific prior written permission.\n\n"
    "THIS SOFTWARE IS PROVIDED BY",
    1,
)

UNLICENSE = """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""

LICENSES = {
    "mit": ("MIT License", MIT),
    "isc": ("ISC License", ISC),
    "0bsd": ("BSD Zero Clause License", ZERO_BSD),
    "bsd-2-clause": ("BSD 2-Clause License", BSD2),
    "bsd-3-clause": ("BSD 3-Clause License", BSD3),
    "unlicense": ("The Unlicense (public domain)", UNLICENSE),
}


def default_name():
    try:
        out = subprocess.run(["git", "config", "user.name"], capture_output=True,
                             text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    return out or "Your Name"


def main(argv=None):
    p = argparse.ArgumentParser(prog="licensegen", description="Generate a LICENSE file.")
    p.add_argument("license", nargs="?", type=str.lower, help="license id, see --list")
    p.add_argument("--list", action="store_true", help="show available licenses")
    p.add_argument("--name", help="copyright holder (default: git user.name)")
    p.add_argument("--year", default=str(datetime.date.today().year), help="copyright year")
    p.add_argument("-w", "--write", action="store_true", help="write ./LICENSE instead of printing")
    p.add_argument("-f", "--force", action="store_true", help="overwrite an existing LICENSE")
    a = p.parse_args(argv)

    if a.list:
        for key, (title, _) in LICENSES.items():
            print(f"{key:<14} {title}")
        return 0
    if not a.license:
        p.error("choose a license (see --list)")
    if a.license not in LICENSES:
        print(f"licensegen: unknown license {a.license!r}; try --list", file=sys.stderr)
        return 2

    text = LICENSES[a.license][1].replace("{year}", a.year).replace("{name}", a.name or default_name())
    if not a.write:
        sys.stdout.write(text)
        return 0
    target = Path("LICENSE")
    if target.exists() and not a.force:
        print("licensegen: LICENSE already exists (use --force to overwrite)", file=sys.stderr)
        return 1
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target} ({LICENSES[a.license][0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
