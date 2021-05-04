---
layout: default
---

# New SSL certificate for dev sites

The dev sites SSL certificate expires Janurary 24. I need to get a new one to cover all of the dev sites. We want

## Generate the CSR in Acquia

A wildcard SSL certificate can't have any Server Alternate Names (SANs). It would just cover `*.coopercenter.org`.

If you need a SSL Cert to cover multiple wildcard domains, the Common Name (CN) value has to be a non-wildcard domain, with wildcard SANs added.

Common Name: `coopercenter.org`
Subject alternative name(s): `*.coopercenter.org, *.dev1.coopercenter.org`

## Request SSL server certificate from UVA Service Now

[UVA Service Now](https://virginia.service-now.com/its/?id=itsweb_kb_article&sys_id=a1be1813db7acb804f32fb671d961908) provides the SSL certificates.

Copy the CSR into a text document and upload it to your request.
Certificate Type: `InCommon Multi Domain SSL (SHA-2)`

# DNS and new SSL certificate for Prod

I need to create a new SSL certificate before Feb 24 2021. I'd like to get it done even earlier to give myself room for error. We have a lot of domains to cover. It seems that not explicitly listing the www subdomains has resulted in lots of DNS warnings.

List of domains from Acquia:

```
coopercenter.org, *.coopercenter.org, beheardcva.com, beheardcva.org, beheardcville.com, beheardcville.org, beheardva.com, beheardva.org, sorenseninstitute.org, www.beheardcva.com, www.beheardcva.org, www.beheardcville.com, www.beheardcville.org, www.beheardva.com, www.beheardva.org, www.sorenseninstitute.org
```

## Generate CSR in Acquia for Prod

Common Name: `coopercenter.org`
Subject alternative name(s): `*.coopercenter.org`, `beheardcva.org`, `www.beheardcva.org`, `sorenseninstitute.org`, `www.sorenseninstitute.org`

# Lets Encrypt Free SSL certificates

[Tutorial from Acquia](https://support.acquia.com/hc/en-us/articles/360009491013-Using-Let-s-Encrypt-SSL-on-Acquia-Cloud)

[Tutorial for DNS records](https://dev.acquia.com/blog/installing-lets-encrypt-wildcard-certificate-acquia-hosting)

This second tutorial is preferred as it allows you to validate the certificate with a DNS TXT record rather than creating a directory on the server and modifying .htaccess.

Install certbot on Mac `brew install certbot`

Generate your certificate locally for the dev server.

```
sudo certbot certonly --manual --no-eff-email --agree-tos -m mg9jd@virginia.edu -d coopercenter.org -d *.coopercenter.org -d *.dev1.coopercenter.org --preferred-challenges=dns --server https://acme-v02.api.letsencrypt.org/directory
```

`manual` - Provide laborious manual instructions for obtaining a certificate (default: False)
`no-eff-email` - Don't share your e-mail address with EFF
`--server` - What Certificate Authority at Let's Encrypt should we use

The Preferred Challenges flag tells letsencrypt that validation of the cert will happen at the DNS level, not through a special file added to our repo. That makes things much, much easier, since we’ll only need to add a single TXT record on our DNS, rather than having to generate new CSRs or new challenge directories on the server itself.

## Enter DNS TXT Record

Please deploy a DNS TXT record under the name
\_acme-challenge.dev1.coopercenter.org with the following value:

-2dK5eXoG1C9ygHoc8NIlZ8tB5tge99dtZ2uWxbPgr4

Please deploy a DNS TXT record under the name
\_acme-challenge.coopercenter.org with the following value:

Q-3vzH9lz8eheI_g5IAh-A2tBIOevIlZE1GqQNO-CyQ

In Network Solutions you only need to enter everything before the domain in the left side, keep the TTL as the default, and on the right side enter the value.

`Control + C` the terminal before the verifications to let the TXT values propagate.

Rerun the certbot command once the TXT records have had time to propagate.

Enter these two TXT records at 2:53pm and check their propagation before continuing. Use dig to get the TXT records. The `sudo killall -HUP mDNSResponder` command clears local cache.

```
dig -t TXT _acme-challenge.dev1.coopercenter.org +short
dig -t TXT _acme-challenge.coopercenter.org +short

sudo killall -HUP mDNSResponder
```

Use [online tool to check TXT records.](https://mxtoolbox.com/SuperTool.aspx?action=txt%3a_acme-challenge.coopercenter.org&run=toolpage)

## Install issued certificate in Acquia

IMPORTANT NOTES:

- Congratulations! Your certificate and chain have been saved at:
  `/etc/letsencrypt/live/coopercenter.org/fullchain.pem`
  Your key file has been saved at:
  `/etc/letsencrypt/live/coopercenter.org/privkey.pem`
  Your certificate will expire on 2021-04-26. To obtain a new or
  tweaked version of this certificate in the future, simply run
  certbot again. To non-interactively renew _all_ of your
  certificates, run "certbot renew"

Log into the Acquia Control panel, and go to the SSL section of any environment you want to protect. In the Label field, give the record any name you’d like. For example: something like ‘Letsencrypt-date’.

SSL Certificate Field
`sudo cat /etc/letsencrypt/live/coopercenter.org/cert.pem | pbcopy`

SSL Private Key Field
`sudo cat /etc/letsencrypt/live/coopercenter.org/privkey.pem | pbcopy`

CA intermediate certificates field
`sudo cat /etc/letsencrypt/live/coopercenter.org/chain.pem | pbcopy`

# VDOT Receipts Improt 2021

I need to import the VDOT recipts for 2020 into the site. First I'll make sure that the diff between the locality names between the two years shows no errors.

Within the `vdot_user_csv_migration` module, clone the 2019 install `.yml` file named `migrate_plus.migration.vdot_receipts_2019.yml`. Change the path to the new vdot receipts csv file as well as the id name. The header row is ignored so the change doesn't matter.

My two csv files are identical and have the same localities listed. The only change is from header FY19 ALLOC to FY20 ALLOC.

Import the partial configuration change:

```
cd docroot/sites/vdot

drush config-import -y --partial --source=modules/custom/vdot_user_csv_migration/config/install
```

Result:

```
+------------+------------------------------------------------------+-----------+
| Collection | Config                                               | Operation |
+------------+------------------------------------------------------+-----------+
|            | migrate_plus.migration.vdot_receipts_2020            | Create    |
|            | migrate_plus.migration.vdot_users_missing_localities | Update    |
|            | migrate_plus.migration.vdot_users                    | Update    |
|            | migrate_plus.migration.vdot_receipts_2019            | Update    |
|            | migrate_plus.migration.vdot_receipts_2018            | Update    |
+------------+------------------------------------------------------+-----------+
```

Aftter visiting the VDOT migration page within the drupal admin theme I saw that there were 92 entries to be processed instead of 87 (which is the number of localites). There were some extra commas at the bottom of the csv file. After deleting them the migration page looks correct.

I added an entry to the csv file to represtent my admin accounts receipt for 2020. Upon import it should update the receipt I see in the form. It worked!!!

Now I need to clone the webform node to accept new submissions. I'll log into the test account under `sck7x@virginia.edu` to check that the form works.

Within the webform, update all 2019 years to 2020. The current year field must have its default value set as well.

Update the Redirect after login value to the correct cloned page.

The Finished Submissions and Survey page always have a table when the user is logged in. I'll display a login message if they still need to login.

```html
<div class="alert alert-warning" id="login-message" style="display: none;">
  Please <a href="/user/login">login</a> to view this page.
</div>
<script>
  if (document.querySelector('th') == null) {
    document.querySelector('#login-message').style.display = 'block';
  }
</script>
```

# Getting SASS module working again in a fresh terminal

If you run `sass --watch scss:css` and get an error check which version of node you are running `node --version`. If it is v4, then you need to run the following.

```
source ~/.bashrc && nvm use --delete-prefix v14.14.0 && sass --watch scss:css
```

# Defer javascript until jQuery is loaded

This simple defer method will delay the execution of JS until jQuery is loaded and valid.

<script>
function defer(method) {
    if (window.jQuery) {
        method();
    } else {
        setTimeout(function() { defer(method) }, 50);
    }
}

function appendOverview(){
jQuery(".view-content").append(`<div class="card views-row special"><div class="views-field views-field-title"><h2 class="field-content card-header">OVERVIEW</h2></div><div class="views-field views-field-body"><div class="field-content card-body"><p>The Weldon Cooper Center for Public Service serves leaders and communities throughout the Commwealth by providing top quality research, innovative leadership development programs, and government support services. The Center is comprised of five units: three research units and two leadership &amp; government support units. </p></div></div></div>`);
}
defer(appendOverview);
</script>

# Full width 3 cards on homepage

First add the `.only-3` class to the card-container within the view css. Then add this in the footer text area.

```css
<style type="text/css">
.paragraph--id--666 .paragraph__column {
    padding-left: 0;
    padding-right: 0;
}
</style>
```

# Statchat Modify Hosts file for temporary domain work

Edit your hosts file to force statchatva.org to direct to the correct IP.

C:\Windows\System32\Drivers\etc\

Backup and then open the hosts file in txt editor.

```
# Temporary direction of statchat to reclaim hosting
206.81.7.108 statchatva.org
```

Then check the IP of the site in terminal.

```
dig statchatva.org
```
