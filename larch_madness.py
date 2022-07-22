import os
import random
import requests
import bs4
import re
from progress.bar import Bar
os.chdir(r"C:\Users\HP\Desktop\larch_madness") #or whatever your filepath is
trees=open('tree_list.txt',mode='r')
trees.seek(0)
treelist=trees.read().splitlines()
treelist=[tree.replace(" ","+").lower() for tree in treelist]
trees.close()
#this is only during debugging
testlist=random.sample(treelist,20)
baseurl="https://www.ncbi.nlm.nih.gov/pmc/?term=%22{}%22"
finalists=[]
class Tree:
    def __init__(self,binomial,popularity):
        self.binomial=binomial.replace("+"," ").capitalize()
        self.popularity=popularity
    def __str__(self):
        return self.binomial
def popsearch(baseurl,tree):
    searchurl=baseurl.format(tree)
    try:
        sresult=requests.get(searchurl,timeout=10)
    except:
        try:
            sresult=requests.get(searchurl,timeout=10)
        except:
            try:
                sresult=requests.get(searchurl,timeout=10)
            except:
                #print("timeout")
                return None
    soup=bs4.BeautifulSoup(sresult.text,"lxml")
    def noresults(soup):
        stext=str(soup)
        return "No items found." in stext
    if not noresults(soup):
        try:
            resfound=str(soup.find('a', {'title' : 'Total Results'}).text)
            #print(resfound)
            num=re.search(r"(?<=\()\d+(?=\))",resfound)
            num=num.group(0)
            #print(num)
            return(int(num))
        except:
            #print ("not found")
            return None
    else:
        #print("no results")
        return None
def avoid_riots(finalists):
    favs=['Sequoiadendron giganteum','Rhizophora mangle','Ginkgo biloba','Hura crepitans','Taxus baccata','Sequoia sempervivens','Pinus longaeva','Ceiba petandra','Hippomane mancinella','Dracaena cinnabari','Juniperus virginiana','Dendrocnide moroides','Artocarpus heterophyllus','Litchi chinensis','Angiopteris evecta','Pyrus calleryana']
    diff=list(set(finalists[0:-15]) - set(favs))
    if len(diff)<0:
        for x in range(len(diff)):
            try:
                finalists.pop()
            except:
                pass
    finalists.extend(favs)
    finalists=set(finalists)
    return list(finalists)
#TODO: add name==main
if __name__ == '__main__':
    bar = Bar('Scraping', max=len(testlist),suffix='%(percent)d%%')
    for tree in testlist:
        #print(tree.replace("+"," ").capitalize())
        popularity=popsearch(baseurl,tree)
        if popularity!=None:
            finalists.append(Tree(tree,popularity))
            #print("found")
        bar.next()
    bar.finish()
    print("\n"*3)
    finalists.sort(key=lambda x: x.popularity, reverse=True)
    print(len(finalists))
    finalists=finalists[0:64]
    tfinalists=[x.binomial for x in finalists]
    tfinalists=avoid_riots(tfinalists)
    random.shuffle(tfinalists)
    for tree in tfinalists:
        print(tree)
    with open('testlist.txt', 'w') as f:
        f.writelines("%s\n" % l for l in tfinalists)