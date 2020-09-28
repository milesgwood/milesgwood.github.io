---
layout: default
---

## Cellar Supply Work

[Site](https://www.cellarsupply.com)

### Invoices and packing slips

#### Goal: Eric wants packing slips and invoices that can be printed from the admin interface.

I found this plugin `WooCommerce PDF Invoices & Packing Slips`.

## Backup for updates

- Create a backup with Updraft Plus and put it in Dropbox (mgwood account)
- Run through the [AWS Bitnami WP] tutorial(https://aws.amazon.com/getting-started/tutorials/launch-a-wordpress-website/)
- On the fresh WP site install the UpdraftPlus Plugin and connect to the remote storage (Dropbox)
- Restore the site themes and plugins
- Restore the site database
- Now when you connect to the site you should be required to use the Cellar Supply login. It won't work unless Google ReCaptcha is diabled
- SSH into the new site to change the phpmyadmin settings so you can alter the database. You need to change `Require local` to `Require all granted`

```bash
cd Dropbox/Keys
chmod 400 cellar-supply-aws-key.pem
ssh -i "cellar-supply-aws-key.pem" ubuntu@ec2-18-212-101-172.compute-1.amazonaws.com
vim apps/phpmyadmin/conf/httpd-app.conf
```

You need to change `Require local` to `Require all granted` and then restart apache

```
<IfVersion >= 2.3>
Require all granted
</IfVersion>
```

```bash
sudo /opt/bitnami/ctlscript.sh restart apache
```

- Navigate to the phpmyadmin page by adding `phpmyadmin` to the end of the site url
- Use the `default Bitnami password` and `root` as the username
- In the WP Database (default is bitnami_wordpress) find the active plugins and disable google ReCaptcha [Reference](http://www.sokhawin.com/how-to-disable-your-wordpress-plugin-directly-in-database/)

```
SELECT * FROM `wp_options` WHERE  option_name = 'active_plugins';
```

```
a:28:{i:0;s:29:"gravityforms/gravityforms.php";i:1;s:23:"blox-lite/blox-lite.php";i:2;s:23:"digg-digg/digg-digg.php";i:3;s:37:"disable-comments/disable-comments.php";i:4;s:39:"easy-theme-and-plugin-upgrades/init.php";i:5;s:59:"genesis-connect-woocommerce/genesis-connect-woocommerce.php";i:6;s:30:"genesis-logo-uploader/logo.php";i:7;s:34:"genesis-simple-sidebars/plugin.php";i:8;s:43:"google-analytics-dashboard-for-wp/gadwp.php";i:9;s:33:"google-captcha/google-captcha.php";i:10;s:47:"gravity-forms-toolbar/gravity-forms-toolbar.php";i:11;s:39:"ignitewoo-updater/ignitewoo-updater.php";i:12;s:17:"legull/legull.php";i:13;s:45:"limit-login-attempts/limit-login-attempts.php";i:14;s:27:"quick-setup/quick-setup.php";i:15;s:51:"simple-maintenance-mode/simple-maintenance-mode.php";i:16;s:23:"soliloquy/soliloquy.php";i:17;s:25:"tablepress/tablepress.php";i:18;s:27:"updraftplus/updraftplus.php";i:19;s:53:"woocommerce-dropshippers/woocommerce-dropshippers.php";i:20;s:99:"woocommerce-gateway-paypal-powered-by-braintree/woocommerce-gateway-paypal-powered-by-braintree.php";i:21;s:79:"woocommerce-gateway-simplify-commerce/woocommerce-gateway-simplify-commerce.php";i:22;s:42:"woocommerce-menu-bar-cart/wp-menu-cart.php";i:23;s:80:"woocommerce-pdf-invoices-packing-slips/woocommerce-pdf-invoices-packingslips.php";i:24;s:51:"woocommerce-ups-drop-shipping/shipping-ups_rate.php";i:25;s:27:"woocommerce/woocommerce.php";i:26;s:41:"wordpress-importer/wordpress-importer.php";i:27;s:29:"wp-mail-smtp/wp_mail_smtp.php";}
```

Decrease the array counter by one, so `a:27:{...` here. Then delete the `i:9;s:33:"google-captcha/google-captcha.php";` from the array.

```
a:27:{i:0;s:29:"gravityforms/gravityforms.php";i:1;s:23:"blox-lite/blox-lite.php";i:2;s:23:"digg-digg/digg-digg.php";i:3;s:37:"disable-comments/disable-comments.php";i:4;s:39:"easy-theme-and-plugin-upgrades/init.php";i:5;s:59:"genesis-connect-woocommerce/genesis-connect-woocommerce.php";i:6;s:30:"genesis-logo-uploader/logo.php";i:7;s:34:"genesis-simple-sidebars/plugin.php";i:8;s:43:"google-analytics-dashboard-for-wp/gadwp.php";i:10;s:47:"gravity-forms-toolbar/gravity-forms-toolbar.php";i:11;s:39:"ignitewoo-updater/ignitewoo-updater.php";i:12;s:17:"legull/legull.php";i:13;s:45:"limit-login-attempts/limit-login-attempts.php";i:14;s:27:"quick-setup/quick-setup.php";i:15;s:51:"simple-maintenance-mode/simple-maintenance-mode.php";i:16;s:23:"soliloquy/soliloquy.php";i:17;s:25:"tablepress/tablepress.php";i:18;s:27:"updraftplus/updraftplus.php";i:19;s:53:"woocommerce-dropshippers/woocommerce-dropshippers.php";i:20;s:99:"woocommerce-gateway-paypal-powered-by-braintree/woocommerce-gateway-paypal-powered-by-braintree.php";i:21;s:79:"woocommerce-gateway-simplify-commerce/woocommerce-gateway-simplify-commerce.php";i:22;s:42:"woocommerce-menu-bar-cart/wp-menu-cart.php";i:23;s:80:"woocommerce-pdf-invoices-packing-slips/woocommerce-pdf-invoices-packingslips.php";i:24;s:51:"woocommerce-ups-drop-shipping/shipping-ups_rate.php";i:25;s:27:"woocommerce/woocommerce.php";i:26;s:41:"wordpress-importer/wordpress-importer.php";i:27;s:29:"wp-mail-smtp/wp_mail_smtp.php";}
```

- Now you should be able to login using the credentials from the old site.
- The theme, pages, and settings should all be the same. The only piece missing is the actual uploads and content of the site.
- To copy over the content, use FileZilla to connect via SFTP and copy all the site files over. The content files are under the wp-content folder. If you need to configure your FTP connection there is a configuration file you can download from the Go Daddy hosting cPanel. In FileZilla go File > Import and select the XML file downloaded from cPanel.
- If you are actually migrating the site, then you will want to also correct all of the messed up URLs in the database. Use the [Find and Replace Script from interconnectit](https://interconnectit.com/products/search-and-replace-for-wordpress-databases/) to search for old links and replace them with new links. The script has to be in a very specific web accessible folder next to /wp-admin and /wp-content /wp-includes. Unzip it and then transfer the files to the server using Filezilla.

![Search Replace](../../images/search-replace.png)

I ran two replacements. I needed to replace all of the `https://www.cellarsupply.com` with `http://18.212.101.172`. Then `www.cellarsupply.com` with just `18.212.101.172`. I didn't bother to use the regex.

![dry-run](../../images/search-replace.png)

### Alternative to Filezilla wp-content transfers

Copy the current live site using rsync.

```
rsync -arvz --dry-run greatwmc@info.jmu.edu:/var/www/html/uinfo/wp-content/uploads/sites "/Volumes/OPTIMUS PRIME/web_backup_mar31_17/"
rsync -arvz --dry-run greatwmc@info-dev.jmu.edu:/var/www/html/uinfo/wp-content/uploads/sites "/Volumes/OPTIMUS PRIME/dev_web_backup_mar31_17/"
```

This is the dry-run command, obviously run it again without the dry-run option once you’re sure it is doing what you want.

# Increase Max Uplaod size with htaccess

Figured out how to increase teh max file upload size through .htaccess file in ~/public_html
https://www.cloudways.com/blog/increase-media-file-maximum-upload-size-in-wordpress/

```
php_value upload_max_filesize 64M
php_value post_max_size 128M
php_value memory_limit 256M
php_value max_execution_time 300
php_value max_input_time 300
```

# Backup and Update routine - SSH

All you need to do to create a backup is go into the cpanel and Download a `Home Directory Backup` and then download a `MYSQL database backup`.

You can ssh into the site. You have to manually enter the password. There isn't a keyfile. Go to lastpass and search for the ssh password for the command. SSH into the site and then add the cloud9 key to the site. You get this key when you create a new environment.

```
cd ~/.ssh
vim authorized_keys
```

Press `i` to insert text and then paste the public key into that authorized_keys file. To save hit `ESC` - `:wq`.

The installer isn't working so I am going to try to [manually install c9.](https://github.com/c9/install) [Additonal tutorial](https://docs.c9.io/docs/running-your-own-ssh-workspace)

This installer from github requires python 2.7 to run so you need to install it. I can't seem to install it through yum or apt-get so I am installing it manually. Current version of python is 2.6.6. I need to have at least 2.7. [This tutorial talks about how to install python without breaking the 2.6.6 version](https://tecadmin.net/install-python-2-7-on-centos-rhel/)

[Go Daddy tutorial about installing python and running it in a virtual environment](https://www.godaddy.com/garage/how-to-install-and-configure-python-on-a-hosted-server/)

## Installing local python copy

```
wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz
tar xzf Python-2.7.16.tgz
cd Python-2.7.16
```

I had to create the ~/.local directory to follow the go daddy tutorial. This prefix option specifies that we want python 2.7 installed in the folder I created.

```
./configure --prefix=$HOME/.local --enable-optimizations
make install
```

Now python 2.7 is installed in `/home/e52089674/.local/bin` and can be run from there as `./python2.7`.

## Changing bash profile

the Bash profile exists in the home ~ directoy. Edit the bash profile so that the 2.7 version is favored. I temporarily updated the path to favor the 2.7 version of python. I'm going to switch it back before starting cloud9 to see it that works.

```
vim .bash_profile
source ~/.bash_profile
```

.bash_profile Original

```
PATH=$PATH:$HOME/bin
```

.bash_profile Changed

```
PATH=$HOME/.local/bin:$PATH:$HOME/bin
```

PATH before change

```
/home/e52089674/.nvm/versions/node/v10.10.0/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/jdk/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/jdk/bin:/home/e52089674/perl5/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/cpanel/composer/bin:/opt/puppetlabs/bin:/opt/dell/srvadmin/bin:/usr/local/bin:/usr/X11R6/bin:/home/e52089674/bin:/usr/local/bin:/usr/X11R6/bin:/home/e52089674/.local/bin:/home/e52089674/bin
```

After change

```
/home/e52089674/.local/bin:/home/e52089674/.nvm/versions/node/v10.10.0/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/jdk/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/jdk/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/jdk/bin:/home/e52089674/perl5/bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/cpanel/3rdparty/lib/path-bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/cpanel/composer/bin:/opt/puppetlabs/bin:/opt/dell/srvadmin/bin:/usr/local/bin:/usr/X11R6/bin:/home/e52089674/bin:/usr/local/bin:/usr/X11R6/bin:/home/e52089674/.local/bin:/home/e52089674/bin:/usr/local/bin:/usr/X11R6/bin::/home/e52089674/bin
```

```
curl -L https://raw.githubusercontent.com/c9/install/master/install.sh | bash
```

SUCCESS!!! At the end of the cloud9 is working however this error remains.

```
Couldn't load node modules sqlite3 and sequelize from /home/e52089674/.c9/node_modules node version: v10.10.0; node execPath /home/e52089674/.nvm/versions/node/v10.10.0/bin/node Error: Cannot find module '/home/e52089674/.c9/node_modules/sqlite3/lib/binding/node-v64-linux-x64/node_sqlite3.node' Error: Cannot find module '/home/e52089674/.c9/node_modules/sqlite3/lib/binding/node-v64-linux-x64/node_sqlite3.node
```

## Update WP and Jessica

The WP update to 5.2 worked well. The WooCommerce DB update worked as well. Now I need to update the jessica woocommerce theme templates.

These jessica templates are out of date

```
jessica/woocommerce/emails/admin-new-order.php version 2.5.0 is out of date. The core version is 3.5.0,
jessica/woocommerce/emails/email-header.php,
jessica/woocommerce/single-product/meta.php
jessica/taxonomy-product_tag.php
```

I am unable to update the `Ignite Woo updater` plugin. It fails to update. I'm hoping that once the theme is updated the plugin will sucessfully update.

To update jessica I had to login to the [9seeds account](https://9seeds.com) and reactivate the jessica theme annual subscripttion. The current version is 1.3.4 and the new version is 1.7.1. I renewed the annual purchase and downloaded the new theme files.

Current Jessica version is 1.7.1. Now there is a 1.8.2 that I need to upgrade to before doing the PHP update.

[Update Jessica Instructions](https://9seeds.com/forum/jessica-instructions/)

I removed the old jessica files leaving the .git directory in place. Then I copied the new files to the jessica folder. Checked the `woocommerce status` page and it now reads jessica 1.8.2. Copying the files suceeded.

Now I just need to make sure the email templates transferred. I need to [update the outdated templates.](https://docs.woocommerce.com/document/fix-outdated-templates-woocommerce/)

Copy the default template from wp-content/plugins/woocommerce/templates/[path-to-the-template] and paste it in your theme folder found at: wp-content/themes/[path-to-theme].

The admin-new-order.php has no custom text. The `email-header.php` does have custom code.

# Updating PHP

Use the backup wizard under the cpanel to download a full backup of the site.

Currently the site is on PHP 5.6.. WooCommerce 3.8.1, WordPress 5.3

Updating your PHP version shouldn't be a problem, however we can't guarantee that it's not. To protect your site, perform all of the following as part of changing the PHP version:

[update instructions](https://www.godaddy.com/help/recommended-php-version-for-wordpress-32201)

1. Backup WordPress.
2. Update WordPress.
3. Update WordPress Theme.
4. Update WordPress Plugins.
5. Check PHP 7 compatibility of WordPress plugins and themes.
6. Install the "PHP Compatibility Checker" plugin in WordPress.
   Change the PHP version by selecting the steps that correspond to the hosting platform your WordPress site is hosted on:
   cPanel
   Verify that your site is running on the correct version of PHP by using a phpinfo file.

# Errors in Cellar Supply Products Feeds

The `g:image_link` field has two erroneous characters in it for 2 products. Removing those backspace chars from the image links solved the issue.

[Overview Tutorial for Product Feeds](https://www.youtube.com/watch?v=s76d0pfhfXg)

```
<g:id>1086</g:id>
      <g:identifier_exists>FALSE</g:identifier_exists>
      <g:tax>0</g:tax>
      <g:title>Check Valve - Tri Clamp</g:title>
      <g:description>Spring Loaded Check Valve, with tri clover Clamp Ends. Easy to disassemble with 3' tri clover clamp holding the units external cavity together. Four prong internal fins on valve gate help to keep valve gate seated properly. Spring Loaded tri clover Check Valve-- Spring Loaded Check Valves open when pressure below the valve seat is greater than above the valve seat. Therefore when pressure equalizes, the valve closes. Specifications of the T316L Sanitary Stainless Steel Clamp Check Valve : Operating Pressure to 145 PSI, Temperature Range ( 0 °F -- 250° F ), Cracking (opening pressure) 0.65 -- 1.35 psi</g:description>
      <g:link>https://www.cellarsupply.com/product/spring-loaded-check-valve-clamp-ends/?utm_source=Google%20Shopping&amp;amp;utm_campaign=Cellar%20Supply%20Google%20Feeds&amp;amp;utm_medium=cpc&amp;amp;utm_term=1086</g:link>
      <g:image_link>https://www.cellarsupply.com/wp-content/uploads/2016/03/Spring-Loaded-Check-Valve-Clamp-Ends.jpeg</g:image_link>
      <g:availability>in stock</g:availability>
      <g:price>USD 68.45</g:price>
      <g:google_product_category>3577</g:google_product_category>
      <g:condition>New</g:condition>
      <g:shipping/>

Line 266 image has a backspace char in it - CHAR 8 or %08 in address bar.

      <item>
        <g:id>1428</g:id>
        <g:identifier_exists>FALSE</g:identifier_exists>
        <g:tax>0</g:tax>
        <g:title>Sanitizer Foamer Gun</g:title>
        <g:description>This SANI-LAV hose end Sanitizer offers automatic dilution that is convenient and easy to control where and how the solution is applied.  Designed to help with cleaning, degreasing and disinfecting. Using air and water only produces a thick, rich foam spray. Use the quick disconnect coupling to release the spray nozzle to follow sanitizing with a clear water rinses. Includes:   (1) Model N2 spray nozzle (1) Model N2FC aluminum coupler (1) Model N2FS4L sanitizer lid kit (includes suction tube and foot strainer) (1) 48 oz. container (1) Model N2FM metering tip kit with 14 colored tips (see chart below)</g:description>
        <g:link>https://www.cellarsupply.com/product/sanitizer-foamer-gun/?utm_source=Google%20Shopping&amp;amp;utm_campaign=Cellar%20Supply%20Google%20Feeds&amp;amp;utm_medium=cpc&amp;amp;utm_term=1428</g:link>
        <g:image_link>https://www.cellarsupply.com/wp-content/uploads/2016/03/Sanitizer-Foamer-Gun.png</g:image_link>
        <g:availability>in stock</g:availability>
        <g:price>USD 104.25</g:price>
        <g:google_product_category>3577</g:google_product_category>
        <g:condition>New</g:condition>
        <g:shipping/>
      </item>
```

Now I need to figure out why there are only 31 products being exported when we have 64 products.

# Google Shopping Ads

**Ad Campaigns** are organized around a theme, in our case `Shopping Ads` focused on the Search Network. We're selling physical items, not trying to generate calls etc.

You have Ad Groups within a campaign perhaps representing a specific type of item you sell.

Keywords connect to Ad Groups. A good keyword indicates intent to purchase like "bulk carbonation stones". "Appliance repair service" is far better than "appliances" as a keyword.

Avoid single-term keywords.

You can use automatic bidding to start and then switch once you have some data to see how much clicks cost.

## Conversion Tracking

These are conversion action sets. Two actions were already setup on 2/12/20 regarding sales and phone calls. I updated the sales tracking to just reflect if they added the item to their cart.

I need to setup a conversion tracking tag. The GA property ID isn't listed on my google analytics account anymore. Eric must have set it up with his GA account ending in `619-1`

[Loves Data - Tutorial](https://www.youtube.com/watch?v=VxFJcfqsbFE)

[Google Ads Conversion Tracking with Google Analytics](https://youtu.be/rH6YQ2MbX30)

Within Google Analytics you can set goals that announce their completion on a confirmation page loading. `https://www.cellarsupply.com/checkout/order-received/8521/?key=` is the current goal setup in February.

8521 is the order that Eric Setup with him on february 12th as an example.

In analytics I created a new goal that will report anytime someone hits the order received page - `https://www.cellarsupply.com/checkout/order-received` and it's called **Reached Order Received Page - Sales Tracking July, 26 2020 - Miles**. Upon verifying the goal I get a 4.5% conversion rate for the last 7 days.

Now in ads I go to tools > Conversions and click the plus arrow and select Import from google analytics. Now the conversion tracking should be working.

# Fixing Purchase button on Hoses

const buy = document.querySelector('.woocommerce-variation-add-to-cart button');
if(buyButton){
buyButton.style.width = "200px";
buyButton.innerText = "Call For Shipping Quote";
buyButton.disabled = true;
}
