#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#PROJET 2: Evaluation de lexicalité 


# In[ ]:





# In[1]:


# 1. Etablir la liste de dictionnaire à partir de Glaff
chemin_dic='GLAFF-1.2.2//glaff-1.2.2.txt'
#cpt=0
liste_dic=[]

with open (chemin_dic,'r',encoding='utf-8') as dic:
    ligne=dic.readline()
    while ligne:
        mot=ligne.split('|')[0]
        liste_dic.append(mot)
        #cpt+=1
        ligne=dic.readline()
    
print ('nb de mots dans glaff :',len(liste_dic))   
    


# In[2]:


#2. Créer la liste de mots du texte
#3. intersection avec le
import glob
def lire_fichier(chemin):
    with open (chemin,'r',encoding='utf-8')as f:
        texte=f.read()
    return texte


# In[3]:


corpus='Dumas//*.txt'
dic_lex={}
for chemin in glob.glob(corpus):
    #print (chemin)
    
    #prend le nom de texte:
    dossier=chemin.split('\\')
    texte_name=dossier[-1].split('.')
    texte_name=texte_name[0]
    print (texte_name)
    
    #lire le texte et le tokenize en se servant de split():
    texte=lire_fichier(chemin)
    liste_brut=texte.split()
    print (f'texte brut :{len(liste_brut)}')
    

    #calculer le mots communs entre dic et texte brut/texte_sans_ent
    dic=set(liste_dic)
    commun_brut=set(liste_brut).intersection(dic)
    print ('mots communs entre glaff et texte_brut :',len(commun_brut))
    lex_brut=len(commun_brut)/len(set(liste_brut))#
    print ("taux de lexicalité dans la liste_brut :",lex_brut,'\n')
    
    dic_mod={}
    dic_mod['brut']=lex_brut
    dic_lex[texte_name]=dic_mod
    
    
    #break
print (dic_lex)

    


# In[ ]:





# In[4]:


#4. reconnaître les entités nommées et les enlever du texte
#5.intersectio avec le dictionnaire Glaff
import spacy
def ren(texte,nlp):
    nlp.max_length=1500000
    doc=nlp(texte)
    liste_ent=[]
    for ent in doc.ents:
        liste_ent.append(ent.text)
    return liste_ent


# In[7]:


import glob
corpus='Dumas//*.txt'

cpt=0
dic_reste={}
for chemin in glob.glob(corpus):
    
    #prend le nom de texte:
    dossier=chemin.split('\\')
    texte_name=dossier[-1].split('.')
    texte_name=texte_name[0]
    print (texte_name)
    
    
    #lire le texte et le tokenize en se servant de split():
    texte_brut=lire_fichier(chemin)
    liste_brut=texte_brut.split()
    print (f'texte brut :{len(liste_brut)}')
    
    
    #reconnaître les entités nommés via spacy et les enlever du liste_brut :
    mod='fr_core_news_lg'
    nlp=spacy.load(mod)
    liste_ent=ren(texte_brut,nlp)
    print (f'{mod}: ent dans le texte :',len(liste_ent))
    
    communs_ents=set(liste_ent).intersection(dic)
    print (f'mots communs entre ents {mod} et glaff:',len(communs_ents))
    #prouve que certains ents apparaissent dans le dictionnaire, condition pas idéale
        
    texte=texte_brut
    for ent in liste_ent:
        texte=texte.replace(ent,'')
    liste_sans_ent=texte.split()
    print (f'{mod}: texte sans ent :',len(liste_sans_ent))      
        
        
    #intersection entre glaff et liste_sans_ent:
    dic=set(liste_dic)
    commun_sans_ent=set(liste_sans_ent).intersection(dic)
    print (f'{mod}: mots communs du texte_sans_ent :',len(commun_sans_ent))
    lex_sans_ent=len(commun_sans_ent)/len(set(liste_brut))
    print (f"{mod}:taux de lexicalité dans la liste_sans_ent :",lex_sans_ent,'\n')
    
    #stoker :
    if 'lg' not in dic_lex[texte_name]:
        dic_lex[texte_name]['lg']=lex_sans_ent

    
    #cpt+=1
    #if cpt==2:
     #   break 
        
        
print (dic_lex) 
    
    


# In[8]:


#6.stoker les données dans un fichier json
import json
with open ("résultat.json","w",encoding='utf-8')as j:
    j.write(json.dumps(dic_lex,indent=2,ensure_ascii=False))


# In[9]:


with open ('résultat.json','r',encoding='utf-8')as j:
    dic_lex=json.load(j)
    print (dic_lex)


# In[10]:


#présenter sous forme de graphique :
import matplotlib.pyplot as pyplot
import numpy as np
donnees_brut=[]
donnees_lg=[]
for texte, subdic in dic_lex.items():
    for k, val in subdic.items():
        if k=='brut':
            donnees_brut.append(val)
        else : 
            donnees_lg.append(val)
    
print('brut:',donnees_brut)
print ('lg:',donnees_lg)

labels=['taux brut','taux sans ent']
cpt=0
for donnees in [donnees_brut,donnees_lg]:
    pyplot.bar(dic_lex.keys(),donnees,label=labels[cpt])
    cpt+=1

pyplot.legend(loc='upper left',bbox_to_anchor=(1,1))    
pyplot.xticks(rotation=45,ha='right')
pyplot.xlabel('file_name')
pyplot.ylabel('taux de lexicalité')
pyplot.title('comparaison entre les taux de lexicalité')

pyplot.tight_layout()
pyplot.savefig('comparaison entre les taux de lexicalité.png',dpi=300)

pyplot.show()


# In[ ]:





# In[13]:


#7. Compter les mots inconnus restants :
import glob
corpus='Dumas//*.txt'
dic_reste={}
for chemin in glob.glob(corpus):
    
    #prend le nom de texte:
    dossier=chemin.split('\\')
    texte_name=dossier[-1].split('.')
    texte_name=texte_name[0]
    print (texte_name)
    
    #lire le texte et le tokenize en se servant de split():
    texte_brut=lire_fichier(chemin)
    liste_brut=texte_brut.split()
    print (f'texte brut :{len(liste_brut)}')
    
    
    #reconnaître les entités nommés via spacy et les enlever du liste_brut :
    #for mod in ['fr_core_news_lg','fr_core_news_sm']:
    mod='fr_core_news_lg'
    nlp=spacy.load(mod)
    liste_ent=ren(texte_brut,nlp)
    print (f'{mod}: ent dans le texte :',len(liste_ent))
    print (len(set(liste_ent)))
    #print(liste_ent)
    
    
    communs_ents=set(liste_ent).intersection(dic)
    print (f'mots communs entre ents {mod} et glaff:',len(communs_ents))
    #prouve que certains ents apparaissent dans le dictionnaire, condition pas idéale
    #print(communs_ents)
        
    texte=texte_brut#avant d'enlever ents
    for ent in liste_ent:
        texte=texte.replace(ent,'')
    liste_sans_ent=texte.split()
    print (f'{mod}: texte sans ent :',len(liste_sans_ent))      
        
    #intersection entre glaff et liste_sans_ent:
    dic=set(liste_dic)
    commun_sans_ent=set(liste_sans_ent).intersection(dic)
    print (f'{mod}: mots communs du texte_sans_ent :',len(commun_sans_ent))
    lex_sans_ent=len(commun_sans_ent)/len(set(liste_brut))
    print (f"{mod}:taux de lexicalité dans la liste_sans_ent :",lex_sans_ent,'\n')
    dic_mod[mod]=lex_sans_ent
    dic_lex[texte_name]=dic_mod
    #print (commun_sans_ent)
 
    #------------------------------------------------------------------------------------#
    #LES CODES AU-DESSUS DE CETTE LIGNE SONT IDENTIQUES QUE LES ETAPES PRECEDENTES.
    
    #les mots inconnus restants :    
    texte_sans_ent=texte
    reste=[mot for mot in liste_sans_ent if mot not in commun_sans_ent]
    print ("reste :",len (reste),'\n')
    #print ("reste :", reste[:100])
    dic_reste[texte_name]=len(reste)
    
    
    #break 
print (dic_reste)
    


# In[14]:


with open ("mots_restants.json","w",encoding='utf-8')as j:
    j.write(json.dumps(dic_reste,indent=2,ensure_ascii=False))


# In[ ]:





# In[ ]:




