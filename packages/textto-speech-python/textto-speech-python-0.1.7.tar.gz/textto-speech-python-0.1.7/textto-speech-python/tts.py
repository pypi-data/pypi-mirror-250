import torch
import sounddevice as sd
import time

def speak(speech, tof, sp):
    
    language = 'ru'
    model_id = 'ru_v3'
    sample_rate = 48000
    speaker = sp
    put_accent = True 
    put_yo = True
    device = torch.device('cpu')
    text = speech

    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                            model='silero_tts',
                            language=language,
                            speaker=model_id)
    model.to(device)

    audio = model.apply_tts(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate,
                                put_accent=put_accent,
                                put_yo=put_yo)

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / sample_rate))
    sd.stop()
    
    if tof == True:
        model.save_wav(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate)
    elif tof == False:
        pass
    
    else:
        print('the second parameter takes the values true or false')
    
def main():
    speak('Я пчелка мая! и я люблю есть детишек', True, 'aidar',) #aidar baya kseniya xenia random
    
if __name__ == '__main__':
    main()
                