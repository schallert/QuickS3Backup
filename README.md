# PyQuickS3 #
### A small helper utility for quickly sending a file to Amazon S3 ###

Often, I'll be working with some files and I'm about to make a change to one of them. I may be about to screw something up, so it's nice to have an old copy of it laying around somewhere. I don't want to just `cp old_file old_file.old`, since that clutters up whatever folder I'm working in. And if I don't end up screwing up the original then it just makes my life inconvenient, since I have a folder with unnecessary backups.

Enter **PyQuickS3**. PyQuickS3 lets you fire off a file to S3 without worrying about it. Say you're about to change `important.config`, a quick command line call to `pyqs3 important.config` will send the file to an S3 bucket that you predefine, so you know it's there if you need it. If you want to store your files under a certain folder, say `configs` in S3, then that's easy too. Use the `-p` option (prefix) to denote a folder to store your file under. So `pysq3 -p configs important.config` will put the `important.config` file in the `configs` folder in your bucket.

It's a simple handy utility for now, with more features to come.

Clone it, try it, fork it, push it. You know the drill. Enjoy.

### Usage ###
1. Copy `config.sample.json` to `config.json` and supply needed variables.
2. Make sure `boto` is installed
3. Profit?

### Note ###
In the intro above, a call was made to `pyqs3`. Right now, there is no prepackaged executable, since many people will configure this package different (mainly because it requires an external library, `boto`). For now you have to call `python quickS3Backup.py ...`. Although this isn't *quick* as the name suggests, it's not to hard to root install `boto` and move the `.py` file to an executable. Do as you please.