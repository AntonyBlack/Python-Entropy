from math import log2
from collections import OrderedDict
from operator import itemgetter
from tabulate import tabulate     #pip install tabulate
import pandas as pd               #pip install pandas


''' Очистка текста '''

def filtration(text, alph_, substitutions):
    text = text.lower()
    for sub in substitutions:
        text = text.replace(sub, substitutions[sub])
    for symbol in text:
        if not(symbol in alph_):
            text = text.replace(symbol, '')
    text = text.replace('  ', ' ')        
    return text

def fromDirtyTextToClear(alph_, substitutions):
    dirtyText = open("dirtyText.txt", encoding='cp1251')
    clearText = open("clearText.txt", 'w', encoding='utf-8')
    clearText.write(filtration(dirtyText.read(), alph_, substitutions))
    dirtyText.close()
    clearText.close()

def preparationOfTheText(alph_, substitutions):
    fromDirtyTextToClear(alph_, substitutions)
    print("Text cleared.")

''' Монограммы и биграммы в тексте '''

''' Частота '''

def monogramDictCreate(alp):
    monogram = {}
    for letter in alp:
        monogram[letter]=0;
    return monogram

def monogramFrequencyCount(text, monogram):
    for letter in text:
        monogram[letter]+=1           
    for mono in monogram:
        monogram[mono]/=len(text)   
    return monogram

def bigramDictCreate(alp):
    bigram = {}
    for letter1 in alp:
        for letter2 in alp:
            bigram[letter1 + letter2]=0;
    return bigram

def bigramFrequencyCountIntersection(text, bigram):
    for letter in range(len(text)-1):
        bigram[text[letter]+text[letter+1]]+=1
    for bigr in bigram:                         
        bigram[bigr]/= len(text)-1 
    return bigram

def bigramFrequencyCountNoIntersection(text, bigram):
    for letter in range(0, len(text)-1, 2):
        bigram[text[letter]+text[letter+1]]+=1
    for bigr in bigram:                         
        bigram[bigr]/= len(text)//2       
    return bigram

def showMonoFrequency(Dict):
    ordered = OrderedDict(sorted(Dict.items(), key=itemgetter(1), reverse=True))
    print(tabulate(ordered.items(), headers=["monogram", "frequency"], tablefmt="grid"))   

def showBigrFrequency(Dict, alph):             # рядок-столбик 
    al = []
    for i in range(len(alph)):
        al.append(alph[i])
    df = pd.DataFrame(columns=al, index=al)
    for i in al:
        for j in al:
            df.at[i,j] = Dict[i+j]      # set_value(index, column, value)
    return df                           # табличка съехала
        
        
''' Энтропия '''

def Entropy(Dict):
    entropy = 0
    for frequency in Dict:
        if(Dict[frequency] != 0 ):
            entropy -= Dict[frequency]*log2(Dict[frequency])
    return entropy

''' Надлишковість '''

def languageRedundancy(val1, val2):
    return 1-(((val1+val2)/2)/log2(32))

''' Сама лаба '''

def main():

    alphFile = open('alphabet.txt', encoding='utf-8')  #без Ё и Ъ
    alph = alphFile.read()
    alph = alph.strip()
    alph = alph.replace('\ufeff', '')
    alphFile.close()
    alph_ = alph + " "
    substitutions = {'\ufeff':'', 'ё':'е', 'ъ':'ь'}    # '\t' '\n' лишние, их и так удалит
    
    #preparationOfTheText(alph_, substitutions)        # 1 раз
    
    textFile_ = open('clearText.txt', encoding="utf-8")
    text_ = textFile_.read()
    textFile_.close()

    monogram = monogramDictCreate(alph)
    monogram_ = monogramDictCreate(alph_)
    bigram = bigramDictCreate(alph)
    bigram_ = bigramDictCreate(alph_)

    monogramDict_ = monogramFrequencyCount(text_, monogram_)
    bigramDictIntersection_ = bigramFrequencyCountIntersection(text_, bigram_)
    bigramDictNoIntersection_ = bigramFrequencyCountNoIntersection(text_, bigram_)

    text = text_.replace(' ', '')
    textFile = open("clearTextWithoutSpaces.txt", 'w')
    textFile.write(text)
    textFile.close()
    print("Spaces deleted.")

    monogramDict = monogramFrequencyCount(text, monogram)
    bigramDictIntersection = bigramFrequencyCountIntersection(text, bigram)
    bigramDictNoIntersection = bigramFrequencyCountNoIntersection(text, bigram)

    print("Monogram and bigram frequency:")

    print("Monograms without spaces:")
    showMonoFrequency(monogramFrequencyCount(text, monogram))
    print("Monograms with spaces:")
    showMonoFrequency(monogramFrequencyCount(text_, monogram_))
    print("Bigrams with spaces first method:\n  ", showBigrFrequency(bigramFrequencyCountIntersection(text_, bigram_), alph_))
    showBigrFrequency(bigramDictIntersection_, alph_).to_csv('Bigrams with spaces first method.csv', sep='\t', encoding='utf-8')
    print("Bigrams with spaces second method: \n ", showBigrFrequency(bigramFrequencyCountNoIntersection(text_, bigram_), alph_))
    showBigrFrequency(bigramDictNoIntersection_, alph_).to_csv('Bigrams with spaces second method.csv',sep='\t', encoding='utf-8')
    print("Bigrams without spaces first method:\n  ", showBigrFrequency(bigramFrequencyCountIntersection(text, bigram), alph))
    showBigrFrequency(bigramDictIntersection, alph).to_csv('Bigrams without spaces first method.csv', sep='\t', encoding='utf-8')
    print("Bigrams without spaces second method:\n  ", showBigrFrequency(bigramFrequencyCountNoIntersection(text, bigram), alph))
    showBigrFrequency(bigramDictNoIntersection, alph).to_csv('Bigrams without spaces second method.csv', sep='\t', encoding='utf-8')

    print("\nEntropy:")

    print("Monograms without spaces: ", str(Entropy(monogramFrequencyCount(text, monogram))))
    print("Monograms with spaces: ", str(Entropy(monogramFrequencyCount(text_, monogram_))))
    print("Bigrams with spaces first method: ", str(Entropy(bigramFrequencyCountIntersection(text_, bigram_))))
    print("Bigrams with spaces second method: ", str(Entropy(bigramFrequencyCountNoIntersection(text_, bigram_))))
    print("Bigrams without spaces first method: ", str(Entropy(bigramFrequencyCountIntersection(text, bigram))))
    print("Bigrams without spaces second method: ", str(Entropy(bigramFrequencyCountNoIntersection(text, bigram))))

    print('\nLanguage redundancy: ')
    
    print("For 10: " + str(languageRedundancy(1.926505651, 2.747919399)))
    print("For 20: " + str(languageRedundancy(1.971249285, 2.726021143)))
    print("For 30: " + str(languageRedundancy(1.830706272, 2.549344285)))
    
main()    
input()
