# Recent Work
[Twig Templates](pages/drupal/twig)

[Bash Scripting](pages/bash/examples)

[Sass secrets](sass/Sass)

# Download site and run locally

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
[Localhost Port 4000](http://localhost:4000)

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/milesgwood/milesgwood.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
