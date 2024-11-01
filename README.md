<!--(https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/physiopy_logo_small.png)-->
<a name="readme"></a>
<img alt="physioQC" src="https://raw.githubusercontent.com/physiopy/phys2bids/master/docs/_static/physiopy_logo_small.png" height="150">

physioQC
==========

[![Latest version](https://img.shields.io/github/v/release/physiopy/physioqc?style=flat&logo=github&sort=semver)](https://github.com/physiopy/physioqc/releases)
[![Release date](https://img.shields.io/github/release-date/physiopy/physioqc?style=flat&logo=github)](https://github.com/physiopy/physioqc/releases)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?style=flat&colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

[![Latest DOI](https://zenodo.org/badge/572539484.svg)](https://doi.org/10.5281/zenodo.12176296)
[![Licensed Apache 2.0](https://img.shields.io/github/license/physiopy/physioqc?style=flat&logo=apache)](https://github.com/physiopy/physioqc/blob/master/LICENSE)

[![Codecov](https://img.shields.io/codecov/c/gh/physiopy/physioqc?style=flat&label=codecov&logo=codecov)](https://codecov.io/gh/physiopy/physioqc)
[![Build Status](https://img.shields.io/circleci/build/github/physiopy/physioqc?style=flat&label=circleci&logo=circleci)](https://circleci.com/gh/physiopy/physioqc)
[![Documentation Status](https://img.shields.io/readthedocs/physioqc?style=flat&label=readthedocs&logo=readthedocs)](https://physioqc.readthedocs.io/en/latest/?badge=latest)

[![Latest version](https://img.shields.io/pypi/v/physioqc?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/physioqc/)
[![Supports python version](https://img.shields.io/pypi/pyversions/physioqc?style=flat&logo=python&logoColor=white)](https://pypi.org/project/physioqc/)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-8-orange.svg?style=flat)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

``physioqc`` is a python3 library dedicated to Quality Assessment and Control (QA/QC).

> If you use ``physioqc`` in your work, please support it by citing the zenodo DOI of the version you used. You can find the latest version [here](https://doi.org/10.5281/zenodo.12176296)

> We also support gathering all relevant citations via [DueCredit](http://duecredit.org).

[Read the latest documentation](https://physioqc.readthedocs.io/en/latest/) for more information on physioqc!

## Tested OSs
We would love to do that, but for the moment we cannot support **Windows or MacOS testing**. The reason is related to the cost of running such tests: for each non-Linux test, we can run up to 8 tests on Linux instead. Partial Windows and MacOS testing might be introduced in future releases.

Hence, while **we cannot ensure that physioqc will run on Windows or MacOS**, however we don't see any reason it shouldn't.
Besides, it will run on Windows Linux Subsystem.

We apologise for the discomfort.


<!-- ## Hacktoberfest
Hacktoberfest participants, welcome!
We have some issues for you [here](https://github.com/physiopy/physioqc/issues?q=is%3Aissue+is%3Aopen+label%3Ahacktoberfest)!
However, feel free to tackle any issue you'd like. Depending on the issue and extent of contribution, Hacktoberfest related PRs might not count toward being listed as contributors and authors (unless there is the specific interest). You can ask about it in the issue itself!
Feel free to ask help to the contributors over gitter, happy coding and (hopefully) enjoy hour tee (or tree)!

## The BrainWeb
BrainWeb participants, welcome!
We have a milestone [here](https://github.com/physiopy/physioqc/milestone/5) as a collection of issues you could work on with our help.
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
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mathdugre"><img src="https://avatars.githubusercontent.com/u/16450132?v=4?s=100" width="100px;" alt="Mathieu Dugré"/><br /><sub><b>Mathieu Dugré</b></sub></a><br /><a href="https://github.com/physiopy/physioqc/commits?author=mathdugre" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/goodalse2019"><img src="https://avatars.githubusercontent.com/u/60117796?v=4?s=100" width="100px;" alt="Sarah Goodale"/><br /><sub><b>Sarah Goodale</b></sub></a><br /><a href="#eventOrganizing-goodalse2019" title="Event Organizing">📋</a> <a href="#ideas-goodalse2019" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/physiopy/physioqc/pulls?q=is%3Apr+reviewed-by%3Agoodalse2019" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/smoia"><img src="https://avatars.githubusercontent.com/u/35300580?v=4?s=100" width="100px;" alt="Stefano Moia"/><br /><sub><b>Stefano Moia</b></sub></a><br /><a href="https://github.com/physiopy/physioqc/commits?author=smoia" title="Code">💻</a> <a href="#ideas-smoia" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-smoia" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#projectManagement-smoia" title="Project Management">📆</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/me-pic"><img src="https://avatars.githubusercontent.com/u/77584086?v=4?s=100" width="100px;" alt="Marie-Eve Picard"/><br /><sub><b>Marie-Eve Picard</b></sub></a><br /><a href="#infra-me-pic" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/physiopy/physioqc/pulls?q=is%3Apr+reviewed-by%3Ame-pic" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/physiopy/physioqc/issues?q=author%3Ame-pic" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/celprov"><img src="https://avatars.githubusercontent.com/u/77437752?v=4?s=100" width="100px;" alt="celprov"/><br /><sub><b>celprov</b></sub></a><br /><a href="https://github.com/physiopy/physioqc/commits?author=celprov" title="Code">💻</a> <a href="#ideas-celprov" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SRSteinkamp"><img src="https://avatars.githubusercontent.com/u/17494653?v=4?s=100" width="100px;" alt="Simon Steinkamp"/><br /><sub><b>Simon Steinkamp</b></sub></a><br /><a href="https://github.com/physiopy/physioqc/commits?author=SRSteinkamp" title="Code">💻</a> <a href="#ideas-SRSteinkamp" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/RayStick"><img src="https://avatars.githubusercontent.com/u/50215726?v=4?s=100" width="100px;" alt="Rachael Stickland"/><br /><sub><b>Rachael Stickland</b></sub></a><br /><a href="#infra-RayStick" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/neuralkn0t"><img src="https://avatars.githubusercontent.com/u/86740625?v=4?s=100" width="100px;" alt="Neuralkn0t"/><br /><sub><b>Neuralkn0t</b></sub></a><br /><a href="https://github.com/physiopy/physioqc/commits?author=neuralkn0t" title="Code">💻</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
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
