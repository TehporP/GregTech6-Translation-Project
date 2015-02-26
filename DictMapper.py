#!/bin/python3
import yaml,re,sys

def try_isotope(txt,dict1,dict2):
  tmp=re.search(r"(.*?)-(\d+)",txt)
  if tmp==None or len(tmp.groups())!=2: return ''
  a=tmp.group(1)
  b=tmp.group(2)
  if a in dict1:
    return dict1[a]+"-"+b
  if a in dict2:
    return dict2[a]+"-"+b
  return ''

def translate_multi(words,x,l):
  for eng,chs in l:
    if x+len(eng)>len(words): continue
    OK=True
    for i in range(0,len(eng)):
      if (i==len(eng)-1) and (words[x+i][-1]=='s') and (words[x+i][:-1]==eng[i]):
        break
      if words[x+i]!=eng[i]:
        OK=False
        break
    if OK: return x+len(eng),chs
  return -1,None

def translate(txt,pri,sec,unt):
  if sec==None: sec=(dict(),dict(),dict())
  re_groups=None
  group_format=""
  for t in [sec,pri]:
    ok=False
    for regex in t[2]:
      res=re.search(regex,txt)
      if res!=None:
        re_groups=res.groups()
        group_format=t[2][regex]
        ok=True
        break
    if ok: break
  if re_groups!=None:
    tmp=list()
    for t in re_groups: tmp.append(translate(t,pri,sec,unt))
    return group_format.format(tmp)


  if txt in sec[0]: return sec[0][txt]
  if txt in pri[0]: return pri[0][txt]
  words=[x for x in txt.split(' ') if x!=""]
  translated_words=list()

  i=0
  while i<len(words):
    word=words[i]
    if word in sec[1]:
      next,p=translate_multi(words,i,sec[1][word])
      if next!=-1:
        i=next
        translated_words.append(p)
        continue
    if word in pri[1]:
      next,p=translate_multi(words,i,pri[1][word])
      if next!=-1:
        i=next
        translated_words.append(p)
        continue

    if word[:5]=='Anti-':
      if 'Anti-' in sec[0]:
        translated_words.append(sec[0]['Anti-'])
      else:
        translated_words.append(pri[0]['Anti-'])
      word=word[5:]

    dict1=sec[0]
    dict2=pri[0]
    translated_word=''

    if word in dict1:
      translated_word=dict1[word]
    elif word in dict2:
      translated_word=dict2[word]

    if (translated_word=='') and (word[-1]=='s'):
        if word[:-1] in dict1:
          translated_word=dict1[word[:-1]]
        elif word[:-1] in dict2:
          translated_word=dict2[word[:-1]]

    if (translated_word=='') and (word.find('-')!=-1):
      translated_word=try_isotope(word,dict1,dict2)

    if translated_word!='':
      translated_words.append(translated_word)
    else:
      translated_words.append(' '+word)
      unt.add(word)

    i+=1
  return ''.join(translated_words)

def load_dict(rule_list):
  words=dict()
  multi=dict()
  regex=dict()
  for key_o in rule_list:
    key=key_o.strip()
    if key[0]=='#':
      regex[key[1:]]=rule_list[key_o]
    elif key[0]=='$':
      continue
    else:
      word_l=[x for x in key.split(' ') if x!='']
      if len(word_l)==1:
        words[key]=rule_list[key_o]
      else:
        if not word_l[0] in multi:
          multi[word_l[0]]=list()
        multi[word_l[0]].append((word_l,rule_list[key_o],))
  for k in multi:
      multi[k].sort(key=(lambda x:len(x[0])),reverse=True)
  return (words,multi,regex,)

def main(argc,argv):
  FILE_DICT=""
  FILE_SRC=""
  FILE_DST=""
  FILE_LOG=""
  if argc==5:
    FILE_DICT=argv[1]
    FILE_SRC=argv[2]
    FILE_DST=argv[3]
    FILE_LOG=argv[4]
  elif argc==1:
    FILE_DICT="Dicts.yml"
    FILE_SRC="GregTech_en.txt"
    FILE_DST="GregTech_cn.txt"
    FILE_LOG="UnTranslated.txt"
  else:
    print('python3 DictMapper.py [Dictionary File] [Source File] [Translated File] [UnTranslated Strings]')
    exit()

  with open(FILE_DICT,'r',encoding='UTF-8') as f:
    raw_dict=yaml.load(f.read())

  GENERIC_DICT=load_dict(raw_dict)
  GROUPED_DICT=dict()
  for key in [x for x in raw_dict if x[0]=='$']:
    GROUPED_DICT[key[1:]]=load_dict(raw_dict[key])

  with open(FILE_SRC,'r',encoding='UTF-8') as f:
    lines=f.read().split('\n')

  dst=open(FILE_DST,'w',encoding='UTF-8')
  untranslated=set()

  for line in lines:
    if line.strip()[:2]!="S:":
      dst.write(line+"\n")
    else:
      prefix,tmp=line.split(':',1)
      group,text=tmp.split('=',1)

      GROUP_DICT=None
      for m in GROUPED_DICT:
        if re.match(m,group)!=None:
          GROUP_DICT=GROUPED_DICT[m]
          break

      translated_text=translate(text,GENERIC_DICT,GROUP_DICT,untranslated)
      dst.write("%s:%s=%s\n"%(prefix,group,translated_text))

  dst.close()

  with open(FILE_LOG,'w',encoding='utf8') as f:
    t=[x for x in untranslated if x.strip()!='']
    t.sort()
    for s in t:
      f.write(s+"\n")

if __name__=="__main__":
  main(len(sys.argv),sys.argv)
