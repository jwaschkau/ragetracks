import gettext

gettext.install("ragetrack", "data/language", unicode=True)
trans = gettext.translation("ragetrack", "data/language", ["de"]) 
trans.install()


print _("Please enter a value: ")
print _("The random choice is: %s") % "hallo"