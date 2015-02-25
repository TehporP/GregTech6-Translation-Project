#!/bin/python3

FILE_EN="GregTech_en.txt"
#FILE_CN="GregTech_cn.txt"
FILE_UNTRANSLATED="UnTranslated.txt"
FILE_DICT="Dicts.yml"

import yaml

DICT=yaml.load(open(FILE_DICT,'r').read())
UNTRANSLATED=set()

def starts_with(string, prefix):
  return string[:len(prefix)]==prefix

def translate(txt):
  words=txt.split(' ')
  translated_words=list()
  for word in words:
    translated_word=''
    if word in DICT:
      translated_word=DICT[word]
    elif (word[-1:]=='s') and (word[:-1] in DICT):
      translated_word=DICT[word[:-1]]
    if not translated_word=='':
      translated_words.append(translated_word)
    else:
      translated_words.append(' '+word)
      UNTRANSLATED.add(word)
  return ''.join(translated_words)
  
lines=open(FILE_EN,'r').read().split('\n')
for line in lines:
  if not starts_with(line.strip(),"S:"):
    print(line)
  else:
    head,tail=line.strip().split('=',1)
    translated_tail=translate(tail)
    print("    %s=%s"%(head,translated_tail))

with open(FILE_UNTRANSLATED,'w') as f:
  for x in UNTRANSLATED:
    f.write(x+"\n")

