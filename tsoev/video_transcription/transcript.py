# Ignore pre-production warnings
import subprocess
import warnings
warnings.filterwarnings('ignore')
import nemo
import secrets
import nemo.collections.asr as nemo_asr
import nemo.collections.nlp as nemo_nlp
import nemo.collections.tts as nemo_tts
import moviepy
import moviepy.editor


# Speech Recognition model - QuartzNet
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="stt_en_quartznet15x5").cuda()
# Punctuation and capitalization model
punctuation = nemo_nlp.models.PunctuationCapitalizationModel.from_pretrained(model_name='punctuation_en_distilbert').cuda()
# Spectrogram generator which takes text as an input and produces spectrogram
spectrogram_generator = nemo_tts.models.Tacotron2Model.from_pretrained(model_name="tts_en_tacotron2").cuda()
# Vocoder model which takes spectrogram and produces actual audio
vocoder = nemo_tts.models.WaveGlowModel.from_pretrained(model_name="tts_waveglow_88m").cuda()


def transcript_video(video_file):
    video = moviepy.editor.VideoFileClip(video_file)
    audio = video.audio

    # Replace the parameter with the location along with filename
    audio_identity_name = secrets.token_hex(12)
    audio.write_audiofile(audio_identity_name + ".wav")

    cmdline = "ffmpeg -i {}.wav -ar 16000 -ac 1 {}_clip.wav".format(audio_identity_name, audio_identity_name)
    subprocess.call(cmdline, shell=True)

    # Convert our audio sample to text
    files = [audio_identity_name + "_clip.wav"]
    raw_text = ''
    text = ''
    for fname, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
        raw_text = transcription

    all_text_len = len(raw_text)

    samples_wrote = 0
    counter = 1

    result_text = ''

    while samples_wrote < all_text_len:

        buffer = 1024
        # check if the buffer is not exceeding total samples
        if buffer > (all_text_len - samples_wrote):
            buffer = all_text_len - samples_wrote
        elif raw_text[samples_wrote + buffer] != ' ':
            while buffer > 0:
                buffer -= 1
                if raw_text[samples_wrote + buffer] == ' ':
                    break

        sub_txt = raw_text[samples_wrote: (samples_wrote + buffer)]

        counter += 1
        samples_wrote += buffer

        # Add capitalization and punctuation
        res = punctuation.add_punctuation_capitalization(queries=[sub_txt])
        text = res[0]
        result_text += text

    cmdline = "rm -r {}.wav".format(audio_identity_name)
    subprocess.call(cmdline, shell=True)
    cmdline = "rm -r {}_clip.wav".format(audio_identity_name)
    subprocess.call(cmdline, shell=True)
    return result_text