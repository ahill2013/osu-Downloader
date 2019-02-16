# osu-library-syncer

osu! library syncer is a script to help download beatmaps from the osu! site.
This script works on two steps: first, the user creates a list of beatmaps to
download by running the script once. After this list is created, the user can
share this list with other users. If running the script with an existing sync
list in the correct location, the script will download each new beatmap from
the created list that the user does not currently have. The purpose of this
script is to synchronize your beatmaps with other users, such as friends. For
example, this allows you to run the script in the background, or before
playing, so when in a private multi lobby with friends, you no longer have to
wait to download each new song that you may not have; especially if slow
internet connection speeds are an issue.

## Commands and arguments

### sync

```
$ ./downloader.py sync [osu! Songs directory]
```

This command creates a file called `sync_list.txt` in the osu! songs directory
if one does not exist. If one does exist, it compares the list with the user's
existing beatmaps, and automatically downloads any beatmaps in the sync list
that the user does not yet have after asking for `osu.ppy.sh` user credentials.

The first argument must be specified as `sync`. The second argument must be the
full pathname to the User's osu! Songs directory:  Ex. `C:\Games\osu!\Songs`

## Credits

This project was forked from and inspired by
[this GitHub project](https://github.com/altur13/osu-Downloader). The project
was scoped down to a more niche and specialized purpose.

## License

This project uses the GNU GPL 3.0 License. The license can be found in the root directory of the project.