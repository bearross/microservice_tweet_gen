from pandas import DataFrame
from torch.utils.data import Dataset, DataLoader
from transformers import T5Tokenizer
from pytorch_lightning import LightningDataModule


class T5Dataset(Dataset):
    def __init__(self, data: DataFrame, tokenizer: T5Tokenizer,
                 source_max_token: int = 512, target_max_token: int = 128):
        self.tokenizer = tokenizer
        self.data = data
        self.source_max_tokens = source_max_token
        self.target_max_tokens = target_max_token

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        data_row = self.data.iloc[index]

        source_encoding = self.tokenizer(
            data_row["texts"],
            padding="max_length",
            truncation=True,
            max_length=self.source_max_tokens,
            add_special_tokens=True,
            return_tensors='pt'
        ).input_ids

        target_encoding = self.tokenizer(
            data_row["tweet"],
            padding="max_length",
            truncation=True,
            max_length=self.target_max_tokens,
            add_special_tokens=True,
            return_tensors='pt'
        ).input_ids
        target_encoding[target_encoding == 0] = -100

        return {
            "input_ids": source_encoding.flatten(),
            "labels": target_encoding.flatten()
        }


class T5PLDataModule(LightningDataModule):
    def __init__(self, train_df: DataFrame, val_df: DataFrame, tokenizer: T5Tokenizer, batch_size: int = 8,
                 source_max_token: int = 512, target_max_token: int = 128):
        super(T5PLDataModule, self).__init__()
        self.batch_size = batch_size
        self.train_df = train_df
        self.test_df = val_df
        self.tokenizer = tokenizer
        self.source_max_token = source_max_token
        self.target_max_token = target_max_token
        self.train_dataset = T5Dataset(self.train_df, self.tokenizer, self.source_max_token, self.target_max_token)
        self.test_dataset = T5Dataset(self.test_df, self.tokenizer, self.source_max_token, self.target_max_token)

    def setup(self, stage: str = None):
        pass

    def prepare_data(self, *args, **kwargs):
        pass

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=4
        )

    def val_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=4
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=4
        )
