# coding: utf-8
from os import walk

print 'Creating the Slider and writing it to the output folder'


pic = []
for (dirpath, dirnames, filenames) in walk('/Users/miles/Downloads/Sorensen/Sorensen Website/Board'):
    pic.extend(filenames)
    break

print pic


file = open('board.html', 'w+')
file.write("<!-- Base MasterSlider style sheet --><link rel='stylesheet' href='/masterslider/style/masterslider.css' /><!-- MasterSlider Template Style --><link href='/masterslider/style/ms-staff-style.css' rel='stylesheet' type='text/css'><!-- google font Lato --><link href='https://fonts.googleapis.com/css?family=Lato:300,400' rel='stylesheet' type='text/css'><!-- jQuery --><script src='/masterslider/jquery.min.js'></script><script src='/masterslider/jquery.easing.min.js'></script><!-- Master Slider --><script src='/masterslider/masterslider.min.js'></script><!-- template for the round images--><div class='ms-staff-carousel ms-round'><!--Template for the square exclueds the ms-round class--><!--<div class='ms-staff-carousel'>--><!-- masterslider --><div class='master-slider' id='masterslider'>")

name = []
title = []
location = []
job = []
bio = []


for x in range(0, len(pic) - 1):
    name.append('Default')
    title.append('title')
    location.append('location')
    job.append('job')
    bio.append('bio')


# Write out the Individual Slide
for x in range (0, len(pic) -1 ):
    file.write("<div class='ms-slide'><img src='/masterslider/style/blank.gif'")
    file.write("data-src='/sites/sorensen/files/board-slider/" + pic[x] + "' alt='lorem ipsum dolor sit'/>")
    file.write("<div class='ms-info'>")
    file.write("<h2>" + name[x] + "</h2>")
    # file.write("<h3>Person " + str(x) + name[x] + "</h3>")
    file.write("<h4>"+ title[x] +"</h4>")
    file.write("<h4>"+ location[x] +"</h4>")
    file.write("<h4 style='font-style: italic'>"+ job[x] +"</h4>")
    # file.write("<p class='email'>Email: <a href='mailto:" + email[x] +"'>"+ email[x] + "</a></p>")
    # file.write("<p class='phone'>Phone: "+ phone[x]+"</p>")
    file.write("<p>"+ bio[x] +"</p>")
    # file.write("<ul class='ms-socials '>")
    # file.write("<li class='ms-ico-1 link'><a href='https://www.linkedin.com/in/billshobe/'>linkedin</a></li>")
    # file.write("<li class='ms-ico-2 gs'><a href='https://scholar.google.com/citations?user=09W80zgAAAAJ&hl=en&oi=sra'>google</a></li>")
    # file.write("</ul></div></div>")
    file.write("</div></div>")


file.write("<div class='ms-staff-info' id='staff-info'> </div>")
file.write("<script type='text/javascript'>    var slider = new MasterSlider();    slider.setup('masterslider' , {        loop:true,        width:240,        height:240,        speed:20,        view:'fadeBasic',        preload:0,        space:0,        space:45    });    slider.control('arrows');    slider.control('slideinfo',{insertTo:'#staff-info'});</script>")

# file.write("<script type='text/javascript'>    var slider = new MasterSlider();    slider.setup('masterslider' , {        loop:true,        width:240,        height:240,        speed:20,        view:'flow',        preload:0,        space:0,        wheel:true    });    slider.control('arrows');    slider.control('slideinfo',{insertTo:'#staff-info'}); </script></div>")



file.close()
