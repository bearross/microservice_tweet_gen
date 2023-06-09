from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from tweet_gen.extras.dataset import T5PLDataModule
from sklearn.model_selection import train_test_split
import logging

MODEL_NAME = 't5-small'
NUM_EPOCHS = 5
BATCH_SIZE = 2
TEST_SPLIT = 0.2
NUM_GPU = 0
PROGRESS_REFRESH_RATE = 1
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)


class TweetGenerator(pl.LightningModule):
    def __init__(self):
        super(TweetGenerator, self).__init__()
        self.model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME, return_dict=True)

    def forward(self, input_ids, labels=None):
        """
        Forward function from pl.LightningModule
        :param input_ids: Input vectors
        :param labels: Labels for the vectors
        :return: loss and logits
        """
        output = self.model(input_ids=input_ids, labels=labels)

        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
        """
        A training step, this function is overwritten from pl.LightningModule
        :param batch: Batch data
        :param batch_idx: Batch index
        :return: loss
        """
        loss, outputs = self(batch["input_ids"], batch["labels"])
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        """
        A validation step function overwritten from pl.LightningModule
        :param batch: Batch data
        :param batch_idx: Batch index
        :return: loss
        """
        loss, outputs = self(batch["input_ids"], batch["labels"])
        self.log("val_loss", loss, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        """
        A test step function overwritten from pl.LightningModule
        :param batch: Batch data
        :param batch_idx: Batch index
        :return: loss
        """
        loss, outputs = self(batch["input_ids"], batch["labels"])
        self.log("test_loss", loss, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        """
        Configuring optimizer for pl.LightningModule
        :return: A Optimizer
        """
        return AdamW(self.parameters(), lr=0.0001)


def train(user_id: int) -> None:
    """
    Using the user ID, this function specify dataset for the user.
    Fine-tunes the user model.
    :param user_id: User ID from relational database
    """
    logging.info("{} fine-tuning".format(user_id))
    model = TweetGenerator()
    checkpoint_callback = ModelCheckpoint(
        dirpath="files/checkpoints",
        filename="{}".format(user_id),
        save_top_k=1,
        verbose=True,
        monitor="val_loss",
        mode="min"
    )

    trainer = pl.Trainer(
        checkpoint_callback=checkpoint_callback,
        max_epochs=NUM_EPOCHS,
        gpus=NUM_GPU,
        progress_bar_refresh_rate=PROGRESS_REFRESH_RATE
    )

    df = pd.read_csv("files/dataset/{}.csv".format(user_id))[["tweet", "texts"]]
    df = df.dropna()
    train_df, val_df = train_test_split(df, test_size=TEST_SPLIT)
    data_module = T5PLDataModule(train_df, val_df, tokenizer, BATCH_SIZE)
    trainer.fit(model, datamodule=data_module)
    logging.info("{} done fine-tuning".format(user_id))
