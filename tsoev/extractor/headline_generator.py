# from simpletransformers.t5 import T5Model
#
# model_args = {
#     "reprocess_input_data": True,
#     "overwrite_output_dir": True,
#     "max_seq_length": 256,
#     "eval_batch_size": 128,
#     "num_train_epochs": 0,
#     "save_eval_checkpoints": True,
#     "use_multiprocessing": True,
#     "num_beams": None,
#     "do_sample": False,
#     "max_length": 50,
#     "top_k": 50,
#     "top_p": 0.95,
#     "num_return_sequences": 1,
#     "use_cuda": False
# }
#
# model = T5Model("t5", "t5-small", args=model_args)
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
device = 'cpu'


def generate_headline(text):
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_text = "summarize: " + preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt").to(device)
    predicted_title = model.generate(tokenized_text)

    return tokenizer.decode(predicted_title[0])


if __name__ == '__main__':
    long_text = """summarize: We are a B to ve digital marketing agency, and today I wannta talk about selecting Medi falb to B.
         Sep. retireds and the process and stuff you can take in your all kewid research, so betabeis a little bit
         different than you would see in your Oll C type marring right the sales cycle, or you know the length of time
         in takes to actually make a purchasing decision is usually a lot longer than you would see just buying
         something off Amazon, It's important to make sure that you have in every step of your purchasing phone,
         and the way that I like to usually look down, O see it everywhere, Ioy down triangle, giv your top middle
         and fotom of piece context, and usually the top is wo be things like blogs and other sorts of informational
         content that you're gonna be having to use to reform users, the types of coics and things in thes you care
         about, and that's probably where t s something like email marketenvor exist, but female marketing software is
         probably gonnto be sitting right here in the middle where somebody's gonna wan to make an nformam decision.
         Businesses that are looking for email marketing and going, sal business base, and so, having content in three
         separate spaces and three different mofications will help you identify where your content gaps are,
         Make sure that users can move throughout your website, and throughout the Fune and inform themselves on the
         decision they're trying to make so with that Shou give you some idea of how we develop Huid research here at
         our agency, and I hope that you guys an ou lize some of these strategies in your own cubered research wherever
         you are out in the world"""
    print(generate_headline(long_text))
