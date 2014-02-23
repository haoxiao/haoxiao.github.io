#! /usr/bin/env python

import sys
from lxml.html import parse
from urlparse import urlparse

class viralnova:
  def __init__(self, url, out):
    self.url = url
    self.out = out
    o=urlparse(url)
    self.article = 'article'
    if o.netloc=='www.viralnova.com': self.article='entry-content'
    if o.netloc=='www.wenxuecity.com': self.article='article'
    self.get()
    

  def get(self):
    self.text=""
    self.ref=[]
    try:
      doc=parse(self.url).getroot()
      self.body = doc.find_class(self.article)[0]
    except:
      print "not seems like a valide url !\n"
      return
 
  def save2md(self):
    #for e in self.article:
    #  print e
    self.walk(self.body)

  def walk(self, tree):
    if type(tree.tag) is str:
      tagA="_%s_"%tree.tag.lower()
      stepIn = True
      if hasattr(self, tagA):
        stepIn = getattr(self, tagA).__call__(tree)
      elif tree.text:
        self.text += tree.text
      if stepIn :
        for node in tree:
          self.walk(node)
    if tree.tail:
      self.text += tree.tail

  def dump(self):
    print(self.text)
    for r in self.ref:
      print("%s\n"%r)

  def parse(self, element, prefix):
    #if (element.items())==1: yield (prefix+element.tag+"\n")
    for e in element.iter():
      print "y:%s%s%s"%(prefix, e.tag, e.text)
      yield self.parse(e, prefix+" ")

  def _a_(self, element):
    # don't link empty A (image)
    if not element.text: return True
    if not element.attrib.get("href"): return False
    ref="ref%s"%(len(self.ref)+1)
    self.text += "[%s][%s]"%(element.text, ref)
    self.ref.append("[%s]: %s"%(ref, element.attrib.get("href")))
    return True

  def _img_(self, element):
    ref="ref%s"%(len(self.ref)+1)
    self.text += "![%s][%s]"%(ref, ref)
    self.ref.append("[%s]: %s"%(ref, element.attrib.get("src")))
    return True

  def _script_(self, element):
    return False

  def _style_(self, element):
    return False

  def _form_(self, element):
    return False

def usage():
  print """
usage : %s <viralnova_story_url>
"""%sys.argv[0]
  sys.exit(1)

if __name__ == "__main__":
  if len(sys.argv) < 2 : usage()
  #v=viralnova(sys.argv[1], sys.stdout)
  v=viralnova(sys.argv[1], sys.stdout)
  v.save2md()
  v.dump()
