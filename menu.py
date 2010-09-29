import gettext

#gettext.bindtextdomain('ragetracks', '/data/language/')
#gettext.textdomain('ragetracks')
#_ = gettext.gettext

#trans = gettext.translation('ragetracks', './tools/po/', ['de']) 
#trans.install()

#gettext.install('ragetracks', '/tools/po', ['de'])

#gettext.bindtextdomain('ragetracks', '/tools/po')
#gettext.textdomain('ragetracks')
#_ = gettext.gettext
print gettext.find("ragetrack")
trans = gettext.translation("ragetrack", "/home/pinguin/RegaTracks/rangetracks/trunk", languages=["de","en"]) 
trans.install()


print _("Please enter a value: ")
print _("The random choice is: %s") % "hallo"