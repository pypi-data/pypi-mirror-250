# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmc_export', 'mmc_export.Formats', 'mmc_export.Helpers']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=2.2.2,<4.0.0',
 'aiohttp-client-cache[filesystem]>=0.7.3,<0.11.0',
 'aiohttp>=3.8.3,<4.0.0',
 'certifi>=2023.7.22,<2024.0.0',
 'cryptography>=41.0.3,<42.0.0',
 'gql-query-builder>=0.1.7,<0.2.0',
 'keyring>=23.11,<25.0',
 'murmurhash2>=0.2.10,<0.3.0',
 'tenacity>=8.1.0,<9.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'xxhash>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['mmc-export = mmc_export:main']}

setup_kwargs = {
    'name': 'mmc-export',
    'version': '2.8.7',
    'description': 'Export MMC modpack to other modpack formats',
    'long_description': '# MultiMC advanced exporter\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mmc-export)](https://www.python.org)\n[![PyPI version](https://img.shields.io/pypi/v/mmc-export?label=mmc-export&color=%2347a637)](https://pypi.org/project/mmc-export)\n[![PyPI downloads](https://img.shields.io/pypi/dm/mmc-export?color=%23894bbf)](https://pypistats.org/packages/mmc-export)\n[![GitHub license](https://img.shields.io/github/license/RozeFound/mmc-export)](/LICENSE)\n\nSince MultiMC export features are very limited, I created a script that solves this problem, with this script you can export MultiMC pack to any popular format (e.g. curseforge, modrinth, packwiz). MultiMC forks which didn\'t changed export format much also supported.\n**[PrismLauncher](https://github.com/PrismLauncher/PrismLauncher) apparently already have builtin Modrinth export feature starting with version 7.0**\n\n<table class="alert-warn" align=center>\n<tr>\n    <td> ⚠️ </td>\n    <td>\n        mmc-export development is currently in <b>the maintenance-only mode</b>.\n        This is to show that any abnormal lack of activity isn\'t going to mean it is\n        no longer maintained. mmc-export considered feature-complete, and only will be updated when bugs arrive.\n    </td>\n</tr>\n</table>\n\n# Features\n\n- Support conversion to:\n    - CurseForge\n    - Modrinth\n    - packwiz\n- Detects downloadable resourcepacks and shaders\n- Supports github parsing[¹](#github-rate-limits)\n- Loose modrinth search\n- User friendly toml config\n- Multiple output formats at once\n\n---\n### GitHub rate limits\n\nGitHub has limited requests per hour (up to 60), this means that if you have more than 60 mods, the rest will be excluded from github search. \nIf you authenticate with GitHub using `mmc-export gh-login`, the limit will be removed and requests will be faster. You can always log out with `mmc-export gh-logout`.\n\nIf you don\'t want to use github search by some reason, you can specify `--exclude-providers GitHub` as argument.\n\n# How to Use\n```\nmmc-export -i modpack.zip -c config.toml -f Modrinth packwiz -o converted_modpacks\n```\nIt\'s recommended to fill config at least with basic info like name and version, some launchers can fail import if these values are empty.\n\n## Sub-commands\n\n`gh-login` - to authrize GitHub \\\n`gh-logout` - to get info how to deauthorize GitHub \n\n`purge-cache` - to purge cache. Available arguments:\n```\n--web: to delete requests cache and downloaded mods\n--files: to delete hashes cache\n--all: equivalent to --web --files, deletes all cache (default)\n```\n\n## Syntax\n```\nmmc-export [sub-command] [-h] [-c CONFIG] -i INPUT -f FORMAT [-o OUTPUT] [-v VERSION] [--modrinth-search SEARCH_TYPE] [--exclude-providers PROVIDERS]\n```\n\n### Explanation\n```\n-h --help: prints help\n-i --input: path to modpack, must be zip file exported from MultiMC.\n-c --config: path to config, used to fill the gaps like description or lost mods.\n-f --format: output formats, must be separated by spaces.\n-o --output: directory where converted zip files will be stored.\n-v --version: specify modpack version, will be overriden by config\'s value if exists\n--modrinth-search: modrinth search accuracy\n--exclude-providers: providers you wish to exclude from search\n--provider-priority: providers priority used for packwiz\n--skip-cache: don\'t use web cache in this run\n--scheme: output filename formatting scheme, more info in #scheme-formatting\n```\n> All paths can be relative to current working directory or absolute.\n\n`--format` options (case-sensitive): \n- `CurseForge`\n- `Modrinth`\n- `packwiz`\n- `Intermediate` (only for debugging, may contain sensitive data like username)\n\n`--exclude-providers` options (case-sensitive): \n- `CurseForge`\n- `Modrinth`\n- `GitHub`\n\n`--provider-priority` options (case-sensitive): \n- `CurseForge`\n- `Modrinth`\n- `Other` or `GitHub`\n\n`--modrinth-search` options:\n- `exact` - by hash (default)\n- `accurate` - by hash or slug\n- `loose` - by hash, slug or long name\n\nThe example for the optional `--config` file [can be found here](example_config.toml). \n\nFor example, if the script says\n\n> No config entry found for resource: ModName\n\nThen you should add **one** of the following entries to the end of the config:\n\n#### Specify source URL\n```\n[[Resource]]\nname = "ModName"\nfilename = "the_name_of_the.jar" \nurl = "https://cdn.modrinth.com/data/abcdefg/versions/1.0.0/the_name_of_the.jar"\n```\n#### Hide the warning\n```\n[[Resource]]\nname = "ModName"\nfilename = "the_name_of_the.jar" \naction = "ignore"\n```\n#### Explicitly move to overrides\n```\n[[Resource]]\nname = "ModName"\nfilename = "the_name_of_the.jar" \naction = "override"\n```\n#### Delete the file altogether\n```\n[[Resource]]\nname = "ModName"\nfilename = "the_name_of_the.jar" \naction = "remove"\n```\n#### Make the mod optional\nAppend `optional = true` to any of above\n\n#### Delete any file\nThis can be defined to delete any file that isn\'t downloadable from CurseForge/Modrinth, e.g. mod config or metadata file.\n```\n[[File]]\nname = "Useless file.txt"\naction = "remove"\n```\n\n## Scheme Formatting\n\nMust be used as `--scheme "{keyword}_Literally any text"` without file extension, follows python\'s [format string syntax](https://docs.python.org/3/library/string.html#format-string-syntax)\n\n#### Available keywords: \n- `abbr` - provider abbreviation, usually 2 capitals, e.g. `MR`, `CF`\n- `format` - full format name, e.g. `CurseForge`, `Packwiz`\n- `name` same as `pack.name` - modpack name\n- `version` same as `pack.version` - modpack version\n- `pack` - pointer to [Intermediate](mmc_export/Helpers/structures.py#L50-L66) structure\n\nDefault scheme is as simple as `{abbr}_{name}`\n\n***Caution: if you don\'t use any format specifc keywords, output files will overwrite the same file several times***, can be ignored if you output to only one format.\nAlso, be aware of your filesystem limitations, unsupported characters may lead to an error, or inaccesible file.\n\n# How to Install / Update\n```\npip install -U mmc-export\n```\n',
    'author': 'RozeFound',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RozeFound/mmc-export',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
