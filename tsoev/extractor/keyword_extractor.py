import pke
import string
import spacy
import nltk
from nltk.corpus import stopwords
from keybert import KeyBERT

nlp = spacy.load("en_core_web_sm")
keybert_model = KeyBERT('distilbert-base-nli-mean-tokens')

def get_keywords_from_text(text, max_count=20):
    out=[]

    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text)
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'PROPN'}
    #pos = {'PROPN', 'VERB', 'ADJ', 'NOUN'}
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos=pos, stoplist=stoplist)
    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha=1.1,
                                  threshold=0.75,
                                  method='average')
    keyphrases = extractor.get_n_best(n=max_count)

    for key in keyphrases:
        out.append(key[0])

    return out

def extract_keywords(nlp, sequence, special_tags : list = None):
    """ Takes a Spacy core language model,
    string sequence of text and optional
    list of special tags as arguments.
    
    If any of the words in the string are 
    in the list of special tags they are immediately 
    added to the result.  
    
    Arguments:
        sequence {str} -- string sequence to have keywords extracted from
    
    Keyword Arguments:
        tags {list} --  list of tags to be automatically added (default: {None})
    
    Returns:
        {list} -- list of the unique keywords extracted from a string
    """    
    result = []

    # custom list of part of speech tags we are interested in
    # we are interested in proper nouns, nouns, and adjectives
    # edit this list of POS tags according to your needs. 
    pos_tag = ['PROPN','NOUN','ADJ']

    # create a spacy doc object by calling the nlp object on the input sequence
    doc = nlp(sequence.lower())

    # if special tags are given and exist in the input sequence
    # add them to results by default
    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)
    
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in string.punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))

def get_keywords_from_bert(text):
  keywords = keybert_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', 
                           use_maxsum=True, nr_candidates=20, top_n=3)
  return keywords
  
if __name__ == "__main__":
  """
  install the langauge model using the subprocess package
  useful when hosting the service in the cloud as it prevents against
  us forgetting to do this via the CLI
  """
  # subprocess.call("python -m spacy download en_core_web_sm",shell=True)

  text = "I oen to another white word Friday. My name is Coty Begeniel and I'm an Seo manager at ability. We are a B to ve digital marketing agency, and today I wannta talk about selecting Medi falb to B. Sep. retireds and the process and stuff you can take in your all kewid research, so betabeis a little bit different than you would see in your Oll C type marring right the sales cycle, or you know the length of time in takes to actually make a purchasing decision is usually a lot longer than you would see just buying something off Amazon, Right. It's gon t take Mulc stakeholders individuals, A are gon Ao be involved in that process. It's gonna be usually a lot more expensive, so in order to do that, they're gonna want to bein informed about Thei recision. They're gonna have to look up content and information across the Web to help inform that decision, and make sure that they're doing the right thing for their own business. so in order to do that, we have to create content that helps education informs these users and the way to do.That is binding keybiards that matter and builing concent around them. so. when we're developing Cubagri, so far on clientself, the first thing that we do is get receiptless So usually we'll talk with our plaint contacts and speak to them like they care about, but it also helps to give a few other stakeholders involved right, so the product marketing team or the sales team individuals that will eventually watch use that information for their clients and talking them about what they care. A what do they want to show up for what's important to them and that will sort of help frame the conversation you wan ta be having and give you understanding or an idea of where eventually you want to take this keyboard research, and it should be very long. It's a see list. It should eventually grow right so once you've done that and have a base. Understand whatever you want to go. The next thing you can do is review the contents that you have on your own website, and that can start your home. Pangh. You know what's the way that you?Describe yourselves to the greater masses which the flasship page have to say about what you offer right. You can go a little bit deeper into some of your other toplevel pages and abotus, but try to generate and understanding of how you speak to your product, especially in relation to your clients in the industry that you're in. you can use that, and from there you can go a little bit further go through your blogk, closts to see how you speak O the industry and educate and form individuals go to newsletters. Just tryg to get an understanding of what exists currently on the website, where your efficiencies may be, and of course where your deficiencies are elack of contexts that will help you generate ideas on where you need to look for more keywords or modifications, Han te kees, you half speaking, Which with the cubars that you currently have as important to know how you stand, so. at this point, I try to look to see how we're ranking the greaish E thing, and there's a lot of differentrols that you can use for that search.Counsils a great way to see how potentiall uses cross the web are going to your website. Currently that can help be filter by page or by corry. You can get an understanding of what's getting collection toe and interest, but you can also use other thools you know Scm rush five food arafts, moths. Of course. they'll all give you a keyboard list that can help you determine what users are searching for howver to find a website and where they currently ring in search, Ingan result page. An Usually these lists are pretty extensive. I mean they can be anything from a few hundred and two few thousand terms, so it helps to firstsit down ate wa, I like tu biltry by things like you know if it has no search volume, Nix it If it's Brandon term. I don't like to included because you should' be showing out for your grand at terms already, and maybe if it's outside the top fifty and rankings things like that. I don't want that information here. right now. I want t understand how we're showing up where ore accomplished an compitencies are.And how we can leverage that our human research so that should help the list be a little bit more convenced, but one of the things you C also look at is not just in termal, but exter right so you can look at your competition and see how we're ranking are comparing. at least on web. What do they use? what sort of content do they have on their websites? What are they promoting? How are they framing that conversation of using blockpost? All that information is gonna be useful for maybe developing your own strategies or maybe findin a nish, Where if you have a particularl stif copetition you can find areas of not discressivg but use that competition is a framework for identifying areas and potential opportunities, and how the general public or industry speaks to someof. the contant Y you're interested in writing about so once you have that they should be pretty big good idea of the egosystem you're working with is forem to gather metrics, and this is gonna contextiualize the information that you have right you want to make.Inform decisions. Someth cupers Taeven have so this metric gathering Woull be important, and there's a lot of different ways you can do intpeer ability. We might categorize them by different content types. so we can make sure that we're touching on all the different levels of huar usage for the different topics that we discussed in our content. You can look at things like search volume. There's a lot of different chools that do that. the singles that mention they're their an noma I fro a see Im rush. There's a graa show we use called Hubri Ka that Cind serve it aggregates all of them, but Ion gete an idea of search Voluin on a monthly basis, but you can also use other metrics. Things like difficult. You like how hard it is to ring, compared to some of the other people on the web, or oranicall, The ra. like What's the level of competition you're gonna be going up against in terms of ads or videos, or a or oe sort of Google snippets right Mo as a great job of that, so use these metrires, and what they should help you do is.Contextualize the information so that. maybe if you're pretty close on two or three keywords that metric gathering should help you identify which one is mak. ae easiest. It hasf the most potential, so on and so forth so once you have that you should be gitting a good understanding of. whereas those keywords lives and you should be selecting your targets. now, I've flun through a ton of clients who formatedcees have sent Ee list of three to four hundred heroes hat. They'e trying to rain, for I cannotstand it. There's no value to be hadin, Because how can you possibly try and optimize and ring four hundreds and hundreds of different variations of key words. It would take to long right, and you could spend years in that red hole. what we try to do is focus on maybe thirty or forty theewords and really narrowed down what sort of contents gonna be created for. If what you need to optimize doesn't exist on a website. If not whatever we need to make. having that list to makes much more ompartmentalized marketing strategy, and you?Can actually look at that and wait against having you currently deploy E honting gertally. You can look at access. minthens an gak y eyes. I. It just helps to have something a little bit more tangible to bite down on. and of course you can grow from that. right. you start ranking well for those twenty third germs, and you can add few more on andiate but again I think it's really important to focus on at very s select number, caetorizing. them by. you know the importance of which one should I go first and start there, Because this processing content creation takes a long time, but once you'v selected those, it's also important to consider intenton. you can see live outlines intente here a little bit more in depth, And what do I mean by that well the best way that I've seen intend described online as an equation. So every querry is Cmmated in two parts. Right, The incliciv. An explicit right work, Are you sane? And what do you mean when you're saying it, and so when I think of that Inm trying to relate it to Kebards. it, it's really.Important to use that frameworks to develop a strategy thatyo hav and an example. I have yers email mark right, so what's the eplicit and Exlsn Asa O that well, Email marketing is a prety broad term, so implicitly they're probably looking to educate themselves on the topic. Learn o a little bit more about what it's about. you'll see research, or that it's usually a lot more educational related contect that helps thet user understand it better they're not ready to buy it. They just want ta know a little bit more, but what happens Hen I ad I ona fireon, right whatif I add software well now now that Kubon has ontent. It may mean the same thing as Email marketing in some context, but software implies that there will be more a solution. We now going down the Fael. and I'm starting to identify terms in which I user is more interested in purchasing. and so that type of content is goinna be significantly different and it's gonnao be more anely ply on features of benefits than just the email marketing, so that intent is important to.Frignn your kubers. It's important to make sure that you have in every step of your purchasing phone, and the way that I like to usually look down, O see it everywhere, Ioy down triangle, giv your top middle and fotom of piece context, and usually the top is wo be things like blogs and other sorts of informational content that you're gonna be having to use to reform users, the types of coics and things in thes you care about, and that's probably where t s something like email marketenvor exist, but female marketing software is probably gonnto be sitting right here in the middle where somebody's gonna wan to make an nformam decision. You know Relayinel pieces content on competitive websites, check those features and determine I If it's a useful product for that right, and from there you can go a little bit further and mov than into different types of content. Maybe email Arin software for small business, right, That's far more Nyowantan pecific, and maybe you'll have a white faver or demo, a specifically tailore to.Businesses that are looking for email marketing and going, sal business base, and so, having content in three separate spaces and three different mofications will help you identify where your content gaps are, Make sure that users can move throughout your website, and throughout the Fune and inform themselves on the decision they're trying to make so with that Shou give you some idea of how we develop Huid research here at our agency, and I hope that you guys an ou lize some of these strategies in your own cubered research wherever you are out in the world, So they Shou have to listenin, happy New Year, Take care."
  # print(extract_keywords(nlp,"We are a B to ve digital marketing agency, and today I wannta talk about selecting Medi falb to B. Sep. retireds and the process and stuff you can take in your all kewid research, so betabeis a little bit different than you would see in your Oll C type marring right the sales cycle, or you know the length of time in takes to actually make a purchasing decision is usually a lot longer than you would see just buying something off Amazon, Right. It's gonna be usually a lot more expensive, so in order to do that, they're gonna want to bein informed about Thei recision. so in order to do that, we have to create content that helps education informs these users and the way to do. when we're developing Cubagri, so far on clientself, the first thing that we do is get receiptless So usually we'll talk with our plaint contacts and speak to them like they care about, but it also helps to give a few other stakeholders involved right, so the product marketing team or the sales team individuals that will eventually watch use that information for their clients and talking them about what they care. I want t understand how we're showing up where ore accomplished an compitencies are. so we can make sure that we're touching on all the different levels of huar usage for the different topics that we discussed in our content. like What's the level of competition you're gonna be going up against in terms of ads or videos, or a or oe sort of Google snippets right Mo as a great job of that, so use these metrires, and what they should help you do is. maybe if you're pretty close on two or three keywords that metric gathering should help you identify which one is mak. It hasf the most potential, so on and so forth so once you have that you should be gitting a good understanding of. There's no value to be hadin, Because how can you possibly try and optimize and ring four hundreds and hundreds of different variations of key words. what we try to do is focus on maybe thirty or forty theewords and really narrowed down what sort of contents gonna be created for. having that list to makes much more ompartmentalized marketing strategy, and you?Can actually look at that and wait against having you currently deploy E honting gertally. Important to use that frameworks to develop a strategy thatyo hav and an example. you'll see research, or that it's usually a lot more educational related contect that helps thet user understand it better they're not ready to buy it. They just want ta know a little bit more, but what happens Hen I ad I ona fireon, right whatif I add software well now now that Kubon has ontent. It may mean the same thing as Email marketing in some context, but software implies that there will be more a solution. and I'm starting to identify terms in which I user is more interested in purchasing. You know Relayinel pieces content on competitive websites, check those features and determine I If it's a useful product for that right, and from there you can go a little bit further and mov than into different types of content."))
  print(">>>>>>>>>>>>>>: ", get_keywords_from_bert(text))