import pandas as pd
from save_dataset_standard import USERNAME

dataset = pd.read_csv('files/dataset/' + USERNAME + '.csv')

total_mentions = dataset["mentions_length"].sum()
total_hashtags = dataset["hashtags_length"].sum()
total_links = dataset["links_length"].sum()

print("mentions {}, links {}, hashtags {}".format(total_mentions, total_links, total_hashtags))
