---
layout: default
---

# Launching sites and configuring DNS Records

So we launch the main site tomorrow. Our DNS provider is Network Solutions. All of the current sites are singular sites. Using tracert I found the old site is 54.227.239.108 and our new site is listed on the Domains section of the Production environment. We deploy to Production and make a DNS A record pointing the coopercenter.org to our new IP address.

```
C:\Users\miles>tracert coopercenter.org
This is the ip address for the old site.
  54.227.239.108
```

The other sites all have the same IP address as they all get directed to a single apache server and then dished out to different Drupal sites. I now have ssh access to these sites so tomorrow I plan to tweak the CSS a bit.

## List of the sites and their respective current IPs
```
  Main site - coopercenter.org
    54.227.239.108
  ceps.coopercenter.org -  Economic Policy
  csr.coopercenter.org - Survey Research
  certification.coopercenter.org - Constitutional officers cert
  sei.coopercenter.org - Lead trainings
  sorenseninstitute.org - Political leadership
  uip.coopercenter.org - university internship programs x
  vig.coopercenter.org - Virginia Institute of gov
    52.44.228.42
  demographics.coopercenter.org - Demographics
    128.143.21.13
```
