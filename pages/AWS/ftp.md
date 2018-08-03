---
layout: default
---

[Tutorial](https://stackoverflow.com/questions/16744863/connect-to-amazon-ec2-file-directory-using-filezilla-and-sftp)

1. Download your keyfile
2. In FileZilla go Edit > Settings > SFTP > Import Keyfile
3. After adding keys you can add the site in site manager
  - Protocol `SFTP`
  - Copy Public IPV4 DNS to hostname `ec2-54-236-45-250.compute-1.amazonaws.com`
  - Copy Username from the connect example on AWS - usually it's `ubuntu`
  - Logon Type is `Normal`
  - Leave the rest empty
4. Make sure port 22 is open for your IP in security groups
