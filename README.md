<!--(https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/physiopy_logo_small.png)-->
<a name="readme"></a>
<img alt="repository" src="https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/physiopy_logo_small.png" height="150">

This is a template for physiopy's repositories (and other repositories based on the same settings).

Remember to change the licence as soon as you adopt the template.

Available Configurations
------------------------
This repository is meant to be a template for python3 projects.
- CircleCI medium docker running Linux (python 3.7, 3.10, style checks, and coverage)
- Auto release based on Github versioning with Physiopy's labels.
- `.gitattributes` for python
- `.gitignore` for python and containers
- Pre-commit (black, isort, flake8, pydocstyle, and RST documentation)
- Read the Docs (based on sphinx)
- Zenodo
- Codecov (for master branch, 90%+)
- Python setup with `extra_require` options
- Versioneer
- Issue templates (bugs, feature requests, generic)
- PR template
- Workflows (Auto release and PyPI upload)

Usage
-----
1. Find and replace the items between `<>`, for instance `<reponame>`
2. Change licence
3. Set up your default pushes to `origin` (`git config remote.pushDefault origin`)
4. Finish setting up everything.

More explanation coming soon.

<reponame>
==========

[![Latest version](https://img.shields.io/github/v/release/physiopy/<reponame>?style=flat&logo=github&sort=semver)](https://github.com/physiopy/<reponame>/releases)
[![Release date](https://img.shields.io/github/release-date/physiopy/<reponame>?style=flat&logo=github)](https://github.com/physiopy/<reponame>/releases)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?style=flat&colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

[![See the documentation at: https://<reponame>.readthedocs.io](https://img.shields.io/badge/docs-read%20latest-informational?style=flat&logo=readthedocs)](https://<reponame>.readthedocs.io/en/latest/?badge=latest)
<!-- [![Latest DOI](https://zenodo.org/badge/<doi>.svg)](https://zenodo.org/badge/latestdoi/<doi>) -->
<!-- [![Licensed Apache 2.0](https://img.shields.io/github/license/physiopy/<reponame>?style=flat&logo=apache)](https://github.com/physiopy/<reponame>/blob/master/LICENSE) -->

[![Codecov](https://img.shields.io/codecov/c/gh/physiopy/<reponame>?style=flat&label=codecov&logo=codecov)](https://codecov.io/gh/physiopy/<reponame>)
[![Build Status](https://img.shields.io/circleci/build/github/physiopy/<reponame>?style=flat&label=circleci&logo=circleci)](https://circleci.com/gh/physiopy/<reponame>)
[![Documentation Status](https://img.shields.io/readthedocs/<reponame>?style=flat&label=readthedocs&logo=readthedocs)](https://<reponame>.readthedocs.io/en/latest/?badge=latest)

[![Latest version](https://img.shields.io/pypi/v/<reponame>?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/<reponame>/)
[![Supports python version](https://img.shields.io/pypi/pyversions/<reponame>?style=flat&logo=python&logoColor=white)](https://pypi.org/project/<reponame>/)

[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto)](https://github.com/intuit/auto)
[![Supports python version](https://img.shields.io/pypi/pyversions/<reponame>)](https://pypi.org/project/<reponame>/)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

``<reponame>`` is a python3 library meant to do something.

> If you use ``<reponame>`` in your work, please support it by citing the zenodo DOI of the version you used. You can find the latest version [here](https://doi.org/10.5281/zenodo.3470091)

> We also support gathering all relevant citations via [DueCredit](http://duecredit.org).

[Read the latest documentation](https://<reponame>.readthedocs.io/en/latest/) for more information on <reponame>!

## Tested OSs
We woudl love to do that, but for teh moment we cannot support **Windows or MacOS testing**. The reason is related to the cost of running such tests: for each non-Linux test, we can run up to 8 tests on Linux instead. Partial Windows and MacOS testing might be introduced in future releases.

Hence, while **we cannot ensure that <reponame> will run on Windows or MacOS**, however we don't see any reason it shouldn't.
Besides, it will run on Windows Linux Subsistems.

We apologise for the discomfort.


<!-- ## Hacktoberfest
Hacktoberfest participants, welcome!
We have some issues for you [here](https://github.com/physiopy/<reponame>/issues?q=is%3Aissue+is%3Aopen+label%3Ahacktoberfest)!
However, feel free to tackle any issue you'd like. Depending on the issue and extent of contribution, Hacktoberfest related PRs might not count toward being listed as contributors and authors (unless there is the specific interest). You can ask about it in the issue itself!
Feel free to ask help to the contributors over gitter, happy coding and (hopefully) enjoy hour tee (or tree)!

## The BrainWeb
BrainWeb participants, welcome!
We have a milestone [here](https://github.com/physiopy/<reponame>/milestone/5) as a collection of issues you could work on with our help. 
Check the issues with a `BrainWeb` label. Of course, they are only suggestions, so feel free to tackle any issue you want, even open new ones!
You can also contact us on Gitter, in the BrainHack Mattermost (<a href="https://mattermost.brainhack.org/brainhack/channels/physiopy">#physiopy</a>), and don't hesitate to contact [Stefano](https://github.com/smoia) in other ways to jump in the development!
-->

**We're looking for code contributors,** but any suggestion/bug report is welcome! Feel free to open issues!

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

License
-------

This template is released under The Unlicense. Commented here below a copy of the Apache 2.0 Licence, adopted by Physiopy.
Remember to change the licence of your repository as soon as you adopt the template.
<!-- Copyright 2019-2020, The Physiopy community.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->
