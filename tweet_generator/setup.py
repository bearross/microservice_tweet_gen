from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW


MODEL_NAME = 't5-small'
device = "cpu"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME, return_dict=True)
preprocess_text = """
"In terms of Liz Cheney, she's a conservative, she did a vote of conscience and she should not be ousted because of one vote of conscience," Hutchinson told CNN's Erin Burnett on "OutFront" of Cheney's vote to impeach Trump after the January 6 insurrection at the US Capitol.
"And regardless of the reasons of what's going to happen in the vote, and it sounds like she's almost recognizing that she's going to be replaced -- but this is going to be perceived by the American body politic as an ouster because of one vote. I don't think this is healthy for our party -- that perception. We've got to get back to talking about ideas and how to unify ourselves."
Cheney, a Wyoming Republican, has faced growing opposition in her role in the No. 3 House leadership position, and party leaders, including Trump and House Minority Leader Kevin McCarthy, have been part of a mounting effort to remove her from the position.
"""

preprocess_text = "summarize: " + preprocess_text.strip().replace("\n", "")
tokenized_text = tokenizer.encode(preprocess_text, return_tensors="pt").to(device)
summary_ids = model.generate(
    tokenized_text,
    num_beams=4,
    no_repeat_ngram_size=2,
    min_length=30,
    max_length=100,
    early_stopping=True
)

tweet = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
