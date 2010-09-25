import gettext

#gettext.bindtextdomain('ragetracks', '/data/language/')
#gettext.textdomain('ragetracks')
#_ = gettext.gettext

#trans = gettext.translation('ragetracks', './data/language/', ['de']) 
#trans.install()
gettext.install('ragetracks', '/data/language/', ['de'])
 

print _("Please enter a value: ")
print _("The random choice is: %s") % "hallo"