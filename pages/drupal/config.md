---
layout: default
---

Run `drush config-export vcs` to sync the config with the current site.
Install the needed modules for the new feature.
Copy over all the new config files into the config folder.
Update `core.entity_form_display.user.user.default.yml` adding the following so the employee profile shows up.

```
dependencies:
  config:
    - field.field.user.user.field_employee_profile
content:
  field_employee_profile:
    weight: -100
    settings:
      match_operator: CONTAINS
      size: 60
      placeholder: ''
    third_party_settings: {  }
    type: entity_reference_autocomplete
    region: content
```

Run `drush config-import vcs` to install all the new config.
Check the site for the new content types and updated forms.


image.style.media_library.1.yml

From the /ssh-keys directory on laptop
```
 ssh -i id_rsa2 uvacooper.test@staging-17490.prod.hosting.acquia.com
 ssh -i id_rsa2 -A uvacooper.test@staging-17490.prod.hosting.acquia.com ls

```
