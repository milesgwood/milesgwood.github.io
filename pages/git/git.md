---
layout: default
---

[Reverting Git Commits](https://stackoverflow.com/questions/34519665/how-to-move-head-back-to-a-previous-location-detached-head/34519716#34519716)

Get rid of changes temporarily
git stash

See all of the recent commits and revert to a previous branch ignoring lots of commits (BAD IN GROUPS)
git reflog
git checkout HEAD@(5)
git branch new-branch
git checkout new_branch
git merge -s ours master
git checkout master
git merge new-branch

Merge changes from master into current branch deleting the master branch stuff. This is for when you fuck up master.
git merge -s ours master

## Setting Up Git Push and Pull in atom

I tried setting the global user.name and user.email in the terminal but it didn't work on my windows machine. The solution is to edit the config file. It's located at `docroot/.git/config` . You need to add your user information.

```
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
[remote "origin"]
	url = https://github.com/milesgwood/milesgwood.github.io.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[user]
	name = milesgwood
	email = miles.gwood@gmail.com
```
