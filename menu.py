import gettext

#trans = gettext.translation("ragetrack", "data/language", ["de"]) 
gettext.install("ragetrack", "data/language", unicode=True)


print _("Please enter a value: ")
print _("The random choice is: %s") % "hallo"