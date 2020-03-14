---
layout: default
---

## Drush lets you execute php directly

```
$ drush php
>>> Drupal\Core\Site\Settings::get('config_sync_directory')
=> "/var/www/html/foo/bar"
```

## Composer lets you ask why you can't install a package

```
$ composer why-not drupal/core:^8.8
```

# Remove files you shouldn't be tracking in git

```
git rm --cached foo.txt
git rm --cached -r sites/default/files/
```

# You can have multiple cursors in Atom with the control key

Hold control and click anywhere you need a new cursor. Your remove extra cursors by clicking on them a second time.
