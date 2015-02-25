#!/bin/python3

FILE_EN="GregTech_en.txt"
FILE_UNTRANSLATED="UnTranslated.txt"
FILE_DICT="Dicts.yml"

import yaml

DICT=dict()
MULTI_DICT=dict()
d=yaml.load(open(FILE_DICT,'r').read())
for key in d:
  key_strip=key.strip()
  if key_strip.find(' ')==-1:
    DICT[key_strip]=d[key]
  else:
    t=[x for x in key_strip.split(' ') if x!='']
    if not t[0] in MULTI_DICT:
      MULTI_DICT[t[0]]=list()
    MULTI_DICT[t[0]].append((t,d[key],))
UNTRANSLATED=set()

def starts_with(string, prefix):
  return string[:len(prefix)]==prefix

def translate_multi(words,x,l):
  for eng,chs in l:
    if x+len(eng)>len(words): continue
    OK=True
    for i in range(0,len(eng)):
      if words[x+i]!=eng[i]:
        OK=False
        break
    if OK: return x+len(eng),chs
  return -1,None

def is_isotope(word):
  t=word.split('-')
  try:
    tmp=int(t[1])
  except:
    return False
  return t[0] in DICT
  
def translate(txt):
  if txt in DICT: return DICT[txt]
  words=[x for x in txt.split(' ') if x!=""]
  translated_words=list()
  
  i=0
  while i<len(words):
    word=words[i]
    
    if word in MULTI_DICT:
      next,p=translate_multi(words,i,MULTI_DICT[word])
      if next!=-1:
        i=next
        translated_words.append(p)
        continue
    
    if word[:5]=='Anti-':
      translated_words.append(DICT['Anti-'])
      word=word[5:]
    translated_word=''
    if word in DICT:
      translated_word=DICT[word]
    elif (word.find('-')!=-1) and is_isotope(word):
      translated_word=DICT[word.split('-')[0]]+"-"+word.split('-')[1]
    elif (word[-1:]=='s') and (word[:-1] in DICT):
      translated_word=DICT[word[:-1]]
    if not translated_word=='':
      translated_words.append(translated_word)
    else:
      translated_words.append(' '+word)
      UNTRANSLATED.add(word)
    i+=1
  

  return ''.join(translated_words)
  
lines=open(FILE_EN,'r').read().split('\n')
for line in lines:
  if (not starts_with(line.strip(),"S:")) or starts_with(line.strip(),'S:"'):
    print(line)
  else:
    head,tail=line.strip().split('=',1)
    translated_tail=translate(tail)
    print("    %s=%s"%(head,translated_tail))

with open(FILE_UNTRANSLATED,'w') as f:
  for x in UNTRANSLATED:
    f.write(x+"\n")

