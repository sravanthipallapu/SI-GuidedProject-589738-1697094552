from flask import Flask, render_template, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS  # corrected import statement
from heapq import nlargest

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/summarize")  # corrected route definition
def home1():
    return render_template('summarize.html')

@app.route("/submit")
def home2():
    return render_template('summarize.html')

STOP_WORDS =['other', 'not', 'show' 'whoever', 'thereby', 'indeed', 'another', 'fifty', 'hence' 'below', 'whether',
 'where', 'hereafter', 'should', 'your', 'own', 'formerly', 'go', 've', 'some', 'rather', '1', 'myself', 'top',
 'might', 'others', 'get', 'above', 'eleven, nine', 'sixty', 'beyond', 'otherwise', 'down', 'all', 'during',
 'along', 'here', 'therefore', 'us', 'give', 'his','nam','an' ,'few', 'to', 'former', 'thus', 'twenty',
 'whatever', 'but', 'fifteen', 'throughout', 'via', 'ten', 'the', 'just', 'with', 'around', 'yourselves',
'you', 'often', "d", 'without', 'which', 'amongst ','about', 'what', 'wherever', 'thereupon', 'than' ,'m',
 'those', 'two', 'sometimes', 'nobody', 'between', 'have', 'therein' 'onto', 'serious', 'already', 
 'everywhere', 'too', 'for', 'thence', 'by', 'they', 'perhaps', 'side', 'would', 'of', 'amount', 'how', 
 'themselves', 'less', 'am', 'there', 'up' ,'ometime", anyway', 'six', 'this', 'is', 'three', 'yours', 'out',
 'towards', 'becomes' 'most', 'could', 'forty', "'re", 'excep t', 'used', 'enough', 've', '11', 'her', 'behind',
 'put', 'though', 'only', 'was', 'before', 'hereupon', 'why', 'until',' ely', 'herself', 'then', 'various',
 'elsewhere', 'please', 'ca', 'itself', 'quite' 'after' 'one', 'cannot', 'several', 'befor ehand', 'yourself',
 'from', 'has', 'me' 'and', 'thereafter', 'wherein','are', 'since' 'when', 'anyhow', 'or', 'being', 'even', 
 'nothing', 'neither', 'part', 'regarding', 'four', 'beside', 'per', 'very', 'upon', 'at', 'although', 'still',
   'eithe r', 'ours', 'over', 'whose', 'on', 'five', 'can', 'full', 'in', 'thru', 'afterwards' 'doing', 'last',
'whereupon', '11', 'back', 'first', 'eight', 'name', 'always' 'take', 'well', 'herein', 'them', 'their', 
'now', 'due', 'become', 'ourselves', 'across', 'd', 'move' 'alone', 'hundred', 'whither', 'off', 'more',
 'any', 'both', 'whereas', 'hers', 'n','t', 're', 'somewhere' ,'while', 'keep', 'somehow', 've', 'else', 
 'however', 'may','really', 'nowhe ','third', 'anyone', 'many', 'that', 'whereb "every', 'these', 
 'nevertheless','again', 'mine', 'as', 'were', 're', 'who', '1', 'does', 'together', 'whenever', 's ',
 'had', 'meanwhile', 'within', 'seemed', 'front', 'whom' 'bottom', 'something', 'further', 'must' 'whence',
   'into', 'besides', 're', 'toward', 'under', 'do', 'each', 'once', 'd', 'moreover', 'seem', 'been', 'against', 
   'did', 'someone', 'also', 'twelve', 'whole', 'everyone', 'much', 'n','t', 'latterly', 'unless', 'yet', 'n',
   't', 'done' 'ever', 'we', 'whereafter', 'so', 'latter', 'least', 'be', 'empty', 'anything', 'made', 
   'becoming',' our' ,'none', 'will', 'himself', 'such', 'through', 'h ','next', 'among', 'make' 'noone' ,'re', 
   'him', 'almost', 'using', 'nor', 'see', 'anywhere', 'because' 'became', 'its', 'call', 'seems',
 'ereby', 'everything', 'she', 'it' ,'ming', 'mostly', 'never', 'he','no']

@app.route("/summary", methods=['POST'])
def summary():
    print("Hello")
    stopWords = list(STOP_WORDS)  # corrected variable name
    nlp = spacy.load('en_core_web_sm')  # corrected load statement
    doc = request.form['text']
    print(doc)
    docs = nlp(doc)
    tokens = [i.text for i in docs]
    punctuation = '#@!$%^&*(()*%$#@!#%^&*()<>:"P_\n'  # corrected punctuation variable
    print(punctuation)
    word_frequencies = {}
    for word in docs:
        if word.text.lower() not in stopWords:
            if word.text.lower() not in punctuation:  # corrected .Lower() to .lower()
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    maxFrequency = max(word_frequencies.values())
    for i in word_frequencies.keys():
        word_frequencies[i] = word_frequencies[i] / maxFrequency
    sent_tokenz = [sent for sent in docs.sents]
    sentence_score = {}
    for sent in sent_tokenz:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():  # corrected .Lower() to .lower()
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    select_len = int(len(sent_tokenz) * 0.3)
    summary = nlargest(select_len, sentence_score, key=sentence_score.get)  # corrected the key argument
    summary = [word.text for word in summary]  # Convert the sentences to strings
    summary = "".join(summary)
    print(summary)
    return render_template('summarize.html', predictionText=summary)

if __name__ == "__main__":
    app.run()
