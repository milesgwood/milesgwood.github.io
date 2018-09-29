---
layout: default
---

## Examples of Bash Scripts

The all start with the same line.
`#!/bin/bash`
Allow file to execute.
`chmod +x script`
Then run the script from the command line.
`./script`

This is the v1 script that I used to automatically clone and install my GitPages Blog

```bash
# !/bin/bash
#Pull this file out outside of this directory and run it ./pull_and_run
if ! [ -f milesgwood.github.io/_config.yml ]; then
    echo "_config.yml File not found! Cloning"
    git clone https://github.com/milesgwood/milesgwood.github.io.git && \
    git clone https://github.com/pages-themes/midnight.git && \
    cd midnight && \
    script/bootstrap && \
    echo "Changing directory to milesgwood.github.io" && \
    cd ../milesgwood.github.io/ && \
    cp -n -R ../midnight/* . && \
    echo "Copying gem 'github-pages', group: :jekyll_plugins to Gemfile"
    echo "gem 'github-pages', group: :jekyll_plugins" >> Gemfile && \
    cd ..
fi
cd milesgwood.github.io/ && \
git pull && \
python -mwebbrowser http://localhost:4000 && \
bundle update && \
bundle exec jekyll serve && \

#Commit The Changes
 git status
 read -p "Commit description: " desc
 git add . && \
 git commit -m "$desc" && \
 git push
 ```
## Database update script for drupal multisite
```bash
# !/bin/bash
echo "Starting database updates" && \
cd sites/cooper && \
echo "Updating Cooper" && \
drush updb -y && \
cd ../ceps && \
echo "Updating CEPS" && \
drush updb -y && \
cd ../certify && \
echo "Updating Certification" && \
drush updb -y  && \
cd ../sei && \
echo "Updating SEI" && \
drush updb -y && \
cd ../lead && \
echo "Updating Lead" && \
drush updb -y && \
cd ../demographics && \
echo "Updating Demographics" && \
drush updb -y && \
cd ../csr && \
echo "Updating CSR" &&
drush updb -y && \
cd ../sorensen && \
echo "Updating Sorensen" && \
drush updb -y && \
cd ../support && \
echo "Updating Support" && \
drush updb -y && \
cd ../vig && \
echo "Updating VIG" && \
drush updb -y && \
echo "Done with database updates"
```
