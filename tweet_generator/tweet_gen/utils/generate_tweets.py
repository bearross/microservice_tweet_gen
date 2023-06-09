import torch
from tweet_gen.utils.train import TweetGenerator, tokenizer
import glob
from tweet_gen.utils.collect_texts import collect_text_url

device = torch.device('cpu')


def generate_tweet(user_id: int, url: str) -> [str, str]:
    """
    Generates tweet from fined tuned-model for the user.

    :param user_id: User ID from relational database
    :param url: URL of the source content
    :return: tuple(str, str)
    """
    tweet = None
    preprocess_text = None
    try:
        model = glob.glob('files/checkpoints/{}*.ckpt'.format(user_id))[-1]
        model = TweetGenerator.load_from_checkpoint(model)
        model.freeze()

        text = collect_text_url(url)
        preprocess_text = text.strip().replace("\n", "")
        t5_prepared_text = "summarize: " + preprocess_text

        tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt").to(device)
        summary_ids = model.model.generate(
            tokenized_text,
            num_beams=4,
            no_repeat_ngram_size=2,
            min_length=30,
            max_length=100,
            early_stopping=True
        )

        tweet = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except AttributeError:
        pass

    return tweet, preprocess_text

