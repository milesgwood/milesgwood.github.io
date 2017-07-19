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
