# Pixelfeeder

## Synopsis

[Flickr](https://www.flickr.com/) is a popular photohosting site.

[Pixelfed](https://pixelfed.org/) is a photohosting platform too, but
federative one. It means it has plenity of community-driven instances and you
able to even set up your own.

Pixelfeeder helps to import user's photo from Flickr to Pixelfed instance.
Pixelfeeder has a CLI for bulk operations and a GUI for more grain control.

![screenshot](https://gitlab.com/bergentroll/pixelfeeder/-/raw/main/assets/screenshot-main.jpg)

Now with the `pixelfeeder-export` command to download all your posts!

## Installation

```shell
pip3 install pixelfeeder
```

## Preparing

1. Get your Flickr data as described in
   [documentation](https://www.flickrhelp.com/hc/en-us/articles/4404079675156-Downloading-content-from-Flickr)
   in seciton __"Download all your content"__.

   You will get a little archive with metadata JSON files and one or more with images.

2. Create a token  with `write` permission for your Pixelfed account. It may be
   done in __Edit profile__ -> __Applications__ -> __Personal access token__
   block.

3. Fill the options on the settings tab of Pixelfeeder GUI. Or place the
   obtained token file with the URL of your Pixeled instance into a
   `config.yaml` manually.

## Configuration syntax

> A config file contains a sensitive token

A config file is YAML formatted and basically has form of `variable: value`.
A config example file [available in the source code
repository](https://gitlab.com/bergentroll/pixelfeeder/-/blob/main/config.yaml).
Also the `pixelfeed-gui` creates a `~/.config/pixelfeeder/config.yaml` file.

| Value | Required | Meaning | Note |
|---|:-:|---|---|
| `instance` | * | "Base URL" of a Pixelfed instance | |
| `token` | * | User created token with `write` permission | May be placed just in a one long line |
| `ignore_ssl_verify` | | Ignore certificate issues like self-signed certs | Boolean value like `false\|true` |
| `timeout` | | HTTP requests timeout including file operations | Not yet supported by gui |
| `caption_datetime_format` | | [`strftime` compatible string](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) | Better to wrap the value into qoutes |
| `caption_order` | | Fields will be placed in this order separated by empty lines | Field may be omitted or appears more than once |
| `theme` | | Optional value for the Tk GUI | |

## Ready, steady...

> FYI: Licenses of your Pixelfed photos may be changed at once with __Edit
> profile__ `->` __Media__ section or you may just set desired option before
> uploading.

Pixelfeeder allows to reorganize caption entries with the `caption_order` config
option. Also `caption_datetime_format` defines format of the `date_taken`
entry.

The default specification `%c` respects locale, so if it is e.g. desirable to have
a lating string, environment variable may be used:

```shell
LC_CTYPE=C pixelfeeder-gui
```

Use `ignore_ssl_verify` to come through self-signed certificate.


## CLI

```shell
pixelfeeder --images-dir IMAGES_DIR [--metadata-dir METADATA_DIR] [--config-file CONFIG_FILE] [--dry-run] [--help]
```

To just upload all the data obtained from the Flickr profile you may use the
command:

```shell
pixelfeeder --images-dir PATH_TO_FLICKR_DATA
```

Both Flickr JSON files and corresponding images should be somewhere inside the
`PATH_TO_FLICKR_DATA` directory (nested dirs supported).

It is possible also to prepare a directory with selected photo files to upload only
some picture:

```shell
pixelfeeder --images-dir PATH_TO_CHOOSEN_IMAGES --metadata-dir PATH_TO_FLICKR_METADATA
```

The `pixelfeeder` command has the `-n` / `--dry-run` flag. With the flag no data
are uploading, but output is more comprehensive.

To know all the arguments use the `-h` / `--help` flag.

## GUI

```shell
pixelfeeder-gui [--config-file CONFIG_FILE] [--verbose] [--safe-mode] [--help]
```

Graphical interface has mostly the same options as the CLI, but upoads images
one-by-one in interactive mode. User able to correct caption and visibility
of a post. Tool will keep position between sessions.

> Edits are not persistent for now, so it is better to make corrections just
> before uploading

## Backup command

```shell
pixelfeeder-export --output-dir OUTPUT_DIR [--skip-media] [--config-file CONFIG_FILE] [--help]
```

Download all posts (statuses) with media of owner of the Pixelfed instance
token (see [Preparing](#user-content-preparing).

Obtained data is prepared to be uploaded with `pixelfed` with some
restrictions (e.g. no statues with multiple pictures).

See all options with the `-h` / `--help` flag.
