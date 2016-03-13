import sys
import copy

change = 0

def Bidir_implication_eliminations(o, tree_types=(list, tuple)): # remove bidirectional implications
    if isinstance(o, tree_types):
        if o[0] == "iff":
            o[0] = "and" 
            new = ["implies"]
            new.append(o[1])
            new.append(o[2])
            new1 = ["implies"]
            new1.append(o[2])
            new1.append(o[1])
            o[1] = new
            o[2] = new1
            
        elif o[0] == "implies":   # remove implication implications
            o[0] = "or"
            new = ["not"]
            new.append(o[1])
            o[1] = new
                     
        for value in o:
            for subvalue in Bidir_implication_eliminations(value):
                yield subvalue
    else:
        yield o
        
        

       

def demorganand(sentence): #apply demorgan law if there is a conjunct
    global change
    
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "and":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "or"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorganand(elem)
            
def demorganor(sentence):  #apply demorgan law if there is a disjunct
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "or":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "and"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorganor(elem)

def doubleneg(sentence): # delete double negations
    global change
    if isinstance(sentence, list):
        if isinstance(sentence[1], list):
            if sentence[1][0] == "not":
                if isinstance(sentence[1][1], list):
                    if sentence[1][1][0] == "not":
                       change = 1
                       sentence[1] = sentence[1][1][1]
                
        for index, elem in enumerate(sentence):
            doubleneg(elem)
    
    return sentence



def distr(sentence): # do Distributivity part
    
    if isinstance(sentence, str):
        return sentence
    if isinstance(sentence, list):     
        if (len(sentence) > 2):
            S=[]
            count = 0
            if (sentence[0] == 'or'):
                i=1                        
                j=1
                while j<(len(sentence)):
                    if isinstance(sentence[j], list): 
                        if sentence[j][0] == "and":
                            s = sentence[j]
                            sentence[j] = sentence[i]
                            sentence[i] = s
                            i = i + 1
                            count = count + 1       
                    j = j + 1
            if count > 0 :              
        
                while(count > 1):     
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    distr(sentence[1])
                    count = count - 1 
    

                i = len(sentence) - 1  
                while (i > 1):
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
            
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    distr(sentence[1])                    
                    i = i - 1
                sentence = S
            else:
                k = 1 
                while k<len(sentence):
                    sentence[k] = distr(sentence[k])
                    k = k + 1
                    
    return sentence
    
    
def assoc_and(sentence): # apply associativity with conjuncts
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'and'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "and") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = assoc_and(sentence[j])
                j = j + 1
    return sentence
    
def assoc_or(sentence): # apply associativity with disjuncts
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'or'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "or") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = assoc_or(sentence[j])
                j = j + 1
    return sentence

def Duplicates(sentence): # remove duplicates with constraints
    if isinstance(sentence,str):
        return sentence
    
    if sentence[0] == "not":       #constaraint not
        return sentence
    if sentence[0] == "or" and (len(sentence)==3):#constaraint or and duplicate
            if(sentence[1]==sentence[2]):
                sentence[0]=sentence[1]
                del(sentence[1])
            
                
    if sentence[0] == "or":        # constaraint or  and multiple duplicacate
        i=1
        while i < len(sentence):
            j =  i + 1 
            if isinstance(sentence[i], str):                           
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif isinstance(sentence[i], list):    
                while  (j < len(sentence) and isinstance(sentence[i], list)): 
                    if ( (isinstance(sentence[j],list)) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1                    
        
    if sentence[0] == "and":#constaraint and 
        i = 1 
        while i < len(sentence):            #checking inner sentence in recursion
            if (isinstance(sentence[i], list) and (len(sentence[i])> 0)):
                if sentence[i][0] == "or":
                    sentence[i] = Duplicates(sentence[i])                
            i = i + 1        
        i = 1
        while i < len(sentence):#del a duplicate
            j = i + 1 
            if isinstance(sentence[i], str):
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "not")):    #inner with not              
                while  j < len(sentence):#tautology
                    if ( (isinstance(sentence[j],list)) and ((sentence[j][0] == "not")) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "or")):    
                while  j < len(sentence):
                    equal = 0
                    flag = True
                    if ((isinstance(sentence[j], list)) and (sentence[j][0] == "or")):
                        if len(sentence[j]) == len(sentence[i]):
                            ii = 1
                            equal = 0
                            while(ii < len(sentence[i])):
                                jj = 1
                                while(jj< len(sentence[j])):
                                    if sentence[i][ii] == sentence[j][jj]:
                                        equal += 1    
                                    jj = jj + 1
                                ii = ii + 1
                            if(len(sentence[i])==len(sentence[j])==2):#identical sentences
                                sentence[j]=sentence[j][1]
                                sentence[i]=sentence[i][1]
                                flag = False
                                
                    if equal == len(sentence[j]) - 1 and flag and equal!=0:
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1  
        if len(sentence) == 2:
            sentence = sentence[1]
        elif len(sentence) == 1:
            sentence = []
            print "Empty Sentence"
        if isinstance(sentence, list):#duplicates of sentences
            if(len(sentence)==2):
                if sentence[0]==sentence[1]:
                    sentence=sentence[0]
    
    for i in range(len(sentence)):#duplicates inner sentences
        if isinstance(sentence[i], list):
            if(len(sentence[i])==2):
                if sentence[i][0]==sentence[i][1]:
                    sentence[i]=sentence[i][0]
                        
    return sentence


def postprocess(sentence): # formatting to the output requirements and final eliminations of meaningless duplicates 
    
    if isinstance(sentence, list):
        if(len(sentence)==2):
            if sentence[0]==sentence[1]:
                sentence=sentence[0]
    if isinstance(sentence, str):
        sentence = repr(sentence)
    return sentence


def Converter(sentence):
  
    global change
      
  
    for value in Bidir_implication_eliminations(sentence):
        print value
                       
    change = 1
    while(change):
        change = 0
        demorganand(sentence)
        demorganor(sentence)

    change = 1
    
    while(change):
        change = 0
        sentence = doubleneg(sentence)
    
    if sentence[0] == "not" and isinstance(sentence[1], list):
        sentence = sentence[1][1]
        sentence = assoc_and(sentence)
        
    sentence = assoc_or(sentence)
    sentence = distr(sentence)
    sentence = assoc_and(sentence)
    sentence = assoc_or(sentence)
    sentence = Duplicates(sentence)

    return sentence
 
sentence=Converter(sentence)
sentence=postprocess(sentence)

print sentence