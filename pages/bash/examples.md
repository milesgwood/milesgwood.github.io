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


```bash
#!/bin/bash
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
