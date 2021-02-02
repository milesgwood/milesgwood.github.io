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
_acme-challenge.dev1.coopercenter.org with the following value:

-2dK5eXoG1C9ygHoc8NIlZ8tB5tge99dtZ2uWxbPgr4

Please deploy a DNS TXT record under the name
_acme-challenge.coopercenter.org with the following value:

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
   certbot again. To non-interactively renew *all* of your
   certificates, run "certbot renew"

Log into the Acquia Control panel, and go to the SSL section of any environment you want to protect. In the Label field, give the record any name you’d like. For example: something like ‘Letsencrypt-date’.

SSL Certificate Field
`sudo cat /etc/letsencrypt/live/coopercenter.org/cert.pem | pbcopy`

SSL Private Key Field
`sudo cat /etc/letsencrypt/live/coopercenter.org/privkey.pem | pbcopy`

CA intermediate certificates field
`sudo cat /etc/letsencrypt/live/coopercenter.org/chain.pem | pbcopy`
