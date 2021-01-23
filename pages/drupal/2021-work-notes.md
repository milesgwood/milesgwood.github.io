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
