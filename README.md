Presentation
=========

This software let you search and download on T411 without limitation, through your terminal.

Usage
=====

```sh
./t411-client --help

Usage: t411-client.py [options]

Options:
  -h, --help     show this help message and exit

  Search torrents:
    Search torrent by keywords and category

    -s SEARCH    Expected keywords
    -c CATEGORY  video, music, game, software

  Download Torrent:
    Download torrent locally

    -d DOWNLOAD  Torrent id

```

Configuration
--------
Rename *config.ini.sample* to *config.ini* and fill it with your personnals informations
```ini
[global]
torrent-client = xdg-open %%s

[account]
username = myusername
password = mypassword
tracker = http://tracker.t411.me:56969/{my personnal key}/announce

[tracker] 
url = http://localhost:16992/announce
```

Search Torrent
-----------

**Global search**

```sh
./t411-client -s "ubuntu"
[INFO] Authentification ...  OK
[INFO] Recherche en cours ... OK
      Id                                                                  Title  Seeders   Size
----------------------------------------------------------------------------------------------------
 4536589 Linux Ubuntu 11.10 [Processeurs x86-32bits] [Format .iso bootable] [Fr       48   655.0 MB
 4967435                               Ubuntu-13.10 Desktop-Processeurs 64bits        47   883.0 MB
 5039097                               Ubuntu Linux 12.04.4 LTS Desktop 32 bits       18   731.0 MB
  166550                                       Ubuntu-v10.04- FRx32bit(desktop)        3   699.4 MB
```

**Search by category**
```sh
./t411-client -s "matrix reloaded" -c video 
[INFO] Authentification ...  OK
[INFO] Recherche en cours ... OK
      Id                                                                  Title  Seeders   Size
----------------------------------------------------------------------------------------------------
 4893405                                          Matrix Reloaded mHD 720p.mkv        74   993.1 MB
 4757948                          The Matrix Reloaded 720P X264 VOSTFR [suprex]       32   1.6 GB
 4861666                   Matrix.Reloaded.2003.FRENCH.BRRip.x264.AC3-zitoune69       12   2.1 GB
 4886547 Matrix.Reloaded.(2003).HDLight.720p.x264.MULTI.VFF.VO.AC3.5.1.MULTISUB       31   2.2 GB

```

Download Torrent
------------
**Start private tracker**
```sh
./t411-server.py 
```
**Download torrent**
```sh
./t411-client.py -d <Torrent id> 
```
