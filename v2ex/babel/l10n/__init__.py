# coding=utf-8

import logging

# About language detecting logic:
#
# Step 1: if member.l10n is not empty/false, use it as the best choice
#
# Step 2: if Accept-Language header has something interesting, use it as the second choice
#
# Step 3: Fallback to site.l10n

def Getlang(langid):
    if langid == 'en':
        from v2ex.babel.l10n.messages import en as messages
        return messages
    if langid == 'zh-Hans':
        from v2ex.babel.l10n.messages import zhHans as messages
        return messages

def GetMessages(handler, member=False, site=False):
    logging.info(handler.request.headers)
    logging.info(site.l10n)
    if member:
        return Getlang(member.l10n)
    else:
        return Getlang(site.l10n)

def GetSupportedLanguages():
    return ['en', 'zh-Hans']

def GetSupportedLanguagesNames():
    return {'en' : 'English', 'zh-Hans' : u'简体中文'}
    
def GetLanguageSelect(current):
    lang = GetSupportedLanguages()
    names = GetSupportedLanguagesNames()
    s = '<select name="l10n">'
    for l in lang:
        if l == current:
            s = s + '<option value="' + l + '" selected="selected">' + names[l] + '</option>'
        else:
            s = s + '<option value="' + l + '">' + names[l] + '</option>'
    s = s + '</select>'
    return s