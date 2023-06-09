import spacy
from summarizer import Summarizer

model = Summarizer()
nlp = spacy.load('en_core_web_sm')
    
def get_summary_from_text_bert(full_text):
	result = model(full_text, min_length=80, max_length = 500 , ratio = 0.4)

	summarized_text = ''.join(result)
	return summarized_text

def extract_summary_text(input_text, count):
  summary_text = get_summary_from_text_spacy(input_text, count)
  
  json_payload = {"summary": summary_text}
  return json_payload

def get_summary_from_text_spacy(full_text, sentence_count=3):
    doc = nlp(full_text)

    # 1, 2, 3
    occurrences = {}
    def fill_occurrences(word):
        word_lemma = lemma(word)
        count = occurrences.get(word_lemma, 0)
        count += 1
        occurrences[word_lemma] = count

    each_word(doc, fill_occurrences)

    # 4, 5, 6
    ranked = get_ranked(doc.sents, sentence_count, occurrences)

    # 7
    summarized_text = " ".join([x['sentence'].text for x in ranked])
    # print("[get_summary_from_text_spacy] >>>>>>>>>>>: ",  summarized_text)
    return summarized_text

def each_word(words, func):
    for word in words:
        if word.pos_ is "PUNCT":
            continue

        func(word)

def get_ranked(sentences, sentence_count, occurrences):
    # Maintain ranked sentences for easy output
    ranked = []

    # Maintain the lowest score for easy removal
    lowest_score = -1
    lowest = 0

    for sent in sentences:
        # Fill ranked if not at capacity
        if len(ranked) < sentence_count:
            score = get_score(occurrences, sent)

            # Maintain lowest score
            if score < lowest_score or lowest_score is -1:
                lowest = len(ranked) + 1
                lowest_score = score

            ranked.append({'sentence': sent, 'score': score})
            continue

        score = get_score(occurrences, sent)
        # Insert if score is greater
        if score > lowest_score:
            # Maintain chronological order
            for i in range(lowest, len(ranked) - 1):
                ranked[i] = ranked[i+1]

            ranked[len(ranked) - 1] = {'sentence': sent, 'score': score}

            # Reset lowest_score
            lowest_score = ranked[0]['score']
            lowest = 0
            for i in range(0, len(ranked)):
                if ranked[i]['score'] < lowest_score:
                    lowest = i
                    lowest_score = ranked[i]['score']

    return ranked

def lemma(word):
    return word.lemma_

def get_score(occurrences, sentence):
    class Totaler:
        def __init__(self):
            self.score = 0
        def __call__(self, word):
            self.score += occurrences.get(lemma(word), 0)
        def total(self):
            # Should the score be divided by total words?
            return self.score

    totaler = Totaler()

    each_word(sentence, totaler)

    return totaler.total()

    
if __name__ == '__main__':
  text = "We are a B to ve digital marketing agency, and today I wannta talk about selecting Medi falb to B. Sep. retireds and the process and stuff you can take in your all kewid research, so betabeis a little bit different than you would see in your Oll C type marring right the sales cycle, or you know the length of time in takes to actually make a purchasing decision is usually a lot longer than you would see just buying something off Amazon, Right. It's gonna be usually a lot more expensive, so in order to do that, they're gonna want to bein informed about Thei recision. so in order to do that, we have to create content that helps education informs these users and the way to do. when we're developing Cubagri, so far on clientself, the first thing that we do is get receiptless So usually we'll talk with our plaint contacts and speak to them like they care about, but it also helps to give a few other stakeholders involved right, so the product marketing team or the sales team individuals that will eventually watch use that information for their clients and talking them about what they care. I want t understand how we're showing up where ore accomplished an compitencies are. so we can make sure that we're touching on all the different levels of huar usage for the different topics that we discussed in our content. like What's the level of competition you're gonna be going up against in terms of ads or videos, or a or oe sort of Google snippets right Mo as a great job of that, so use these metrires, and what they should help you do is. maybe if you're pretty close on two or three keywords that metric gathering should help you identify which one is mak. It hasf the most potential, so on and so forth so once you have that you should be gitting a good understanding of. There's no value to be hadin, Because how can you possibly try and optimize and ring four hundreds and hundreds of different variations of key words. what we try to do is focus on maybe thirty or forty theewords and really narrowed down what sort of contents gonna be created for. having that list to makes much more ompartmentalized marketing strategy, and you?Can actually look at that and wait against having you currently deploy E honting gertally. Important to use that frameworks to develop a strategy thatyo hav and an example. you'll see research, or that it's usually a lot more educational related contect that helps thet user understand it better they're not ready to buy it. They just want ta know a little bit more, but what happens Hen I ad I ona fireon, right whatif I add software well now now that Kubon has ontent. It may mean the same thing as Email marketing in some context, but software implies that there will be more a solution. and I'm starting to identify terms in which I user is more interested in purchasing. You know Relayinel pieces content on competitive websites, check those features and determine I If it's a useful product for that right, and from there you can go a little bit further and mov than into different types of content."
  print(">>>>>>: ", get_summary_from_text_spacy(text))