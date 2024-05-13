# -*- coding: utf-8 -*-
"""

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mqCWVv2sR0NkWaTs7n5UblqfCLopLGx2
"""


# 경로: /home/piai/GPTTS/TTS
# pip install -r requirements.txt
# pip install -q --no-cache-dir -e .

# 경로 : /home/piai/GPTTS/g2pK
# pip install -q --no-cache-dir "konlpy" "jamo" "nltk" "python-mecab-ko"
# pip install -q --no-cache-dir -e .

# GPTTS의 glow폴더 - config.json에서 경로 수정 (총 4개 수정)
# output_path : glow폴더 경로
# stats_path : glow폴더 경로
# test_sentences_file : glow폴더 경로
# datasets-path: /home/piai/GPTTS/ 경로 수정

# GPTTS의 hifi폴더 - config.json에서 경로 수정 (총 3개 수정)
# output_path : hifi폴더 경로
# stats_path : hifi폴더 경로
# datasets-path: /home/piai/GPTTS/ 경로 수정

# 경로 : /home/piai/GPTTS
# pip install openai==0.28.0
# pip install pygame
# pip install g2pk
# pip install IPython
# pip install pyaudio

def TTS_mo(a):
    import os
    import sys
    from pathlib import Path
    import wave

    ##########################################
    # 작업 디렉토리 변경
    vscode_work_dir = "/home/piai/GPTTS"
    os.chdir(vscode_work_dir)
    ###########################################

    import g2pk
    g2p = g2pk.G2p()

    import importlib
    import TTS.tts.utils.text.cleaners as cleaners
    importlib.reload(cleaners)
    import re
    import sys
    from unicodedata import normalize
    import IPython
    import pyaudio
    from TTS.utils.synthesizer import Synthesizer


    def play_wav_file(file_path):
        # WAV 파일 열기
        wav_file = wave.open(file_path, 'rb')
        import pyaudio
        # PyAudio 초기화
        p = pyaudio.PyAudio()

        # 스피커 출력 스트림 열기play_audio_file
        speaker_stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                                channels=wav_file.getnchannels(),
                                rate=wav_file.getframerate(),
                                output=True)

        # WAV 파일 데이터 읽고 스피커로 출력
        data = wav_file.readframes(1024)  # 데이터를play_audio_file 1024 프레임씩 읽음
        
    def normalize_text(text):
        text = text.strip()

        for c in ",;:":
            text = text.replace(c, ".")
        text = remove_duplicated_punctuations(text)

        text = jamo_text(text)

        text = g2p.idioms(text)
        text = g2pk.g2pk.english.convert_eng(text, g2p.cmu)
        text = g2pk.g2pk.utils.annotate(text, g2p.mecab)
        text = g2pk.g2pk.numerals.convert_num(text)
        text = re.sub("/[PJEB]", "", text)

        text = alphabet_text(text)

        # remove unreadable characters
        text = normalize("NFD", text)
        text = "".join(c for c in text if c in symbols)
        text = normalize("NFC", text)

        text = text.strip()
        if len(text) == 0:
            return ""

        # only single punctuation
            text += '.'

        return text

    def remove_duplicated_punctuations(text):
        text = re.sub(r"[.?!]+\?", "?", text)
        text = re.sub(r"[.?!]+!", "!", text)
        text = re.sub(r"[.?!]+\.", ".", text)
        return text

    def split_text(text):
        text = remove_duplicated_punctuations(text)

        texts = []
        for subtext in re.findall(r'[^.!?\n]*[.!?\n]', text):
            texts.append(subtext.strip())

        return texts


    def alphabet_text(text):
        text = re.sub(r"(a|A)", "에이", text)
        text = re.sub(r"(b|B)", "비", text)
        text = re.sub(r"(c|C)", "씨", text)
        text = re.sub(r"(d|D)", "디", text)
        text = re.sub(r"(e|E)", "이", text)
        text = re.sub(r"(f|F)", "에프", text)
        text = re.sub(r"(g|G)", "쥐", text)
        text = re.sub(r"(h|H)", "에이치", text)
        text = re.sub(r"(i|I)", "아이", text)
        text = re.sub(r"(j|J)", "제이", text)
        text = re.sub(r"(k|K)", "케이", text)
        text = re.sub(r"(l|L)", "엘", text)
        text = re.sub(r"(m|M)", "엠", text)
        text = re.sub(r"(n|N)", "엔", text)
        text = re.sub(r"(o|O)", "오", text)
        text = re.sub(r"(p|P)", "피", text)
        text = re.sub(r"(q|Q)", "큐", text)
        text = re.sub(r"(r|R)", "알", text)
        text = re.sub(r"(s|S)", "에스", text)
        text = re.sub(r"(t|T)", "티", text)
        text = re.sub(r"(u|U)", "유", text)
        text = re.sub(r"(v|V)", "브이", text)
        text = re.sub(r"(w|W)", "더블유", text)
        text = re.sub(r"(x|X)", "엑스", text)
        text = re.sub(r"(y|Y)", "와이", text)
        text = re.sub(r"(z|Z)", "지", text)

        return text


    def punctuation_text(text):
        # 문장부호
        text = re.sub(r"!", "느낌표", text)
        text = re.sub(r"\?", "물음표", text)
        text = re.sub(r"\.", "마침표", text)

        return text


    def jamo_text(text):
        # 기본 자모음
        text = re.sub(r"ㄱ", "기역", text)
        text = re.sub(r"ㄴ", "니은", text)
        text = re.sub(r"ㄷ", "디귿", text)
        text = re.sub(r"ㄹ", "리을", text)
        text = re.sub(r"ㅁ", "미음", text)
        text = re.sub(r"ㅂ", "비읍", text)
        text = re.sub(r"ㅅ", "시옷", text)
        text = re.sub(r"ㅇ", "이응", text)
        text = re.sub(r"ㅈ", "지읒", text)
        text = re.sub(r"ㅊ", "치읓", text)
        text = re.sub(r"ㅋ", "키읔", text)
        text = re.sub(r"ㅌ", "티읕", text)
        text = re.sub(r"ㅍ", "피읖", text)
        text = re.sub(r"ㅎ", "히읗", text)
        text = re.sub(r"ㄲ", "쌍기역", text)
        text = re.sub(r"ㄸ", "쌍디귿", text)
        text = re.sub(r"ㅃ", "쌍비읍", text)
        text = re.sub(r"ㅆ", "쌍시옷", text)
        text = re.sub(r"ㅉ", "쌍지읒", text)
        text = re.sub(r"ㄳ", "기역시옷", text)
        text = re.sub(r"ㄵ", "니은지읒", text)
        text = re.sub(r"ㄶ", "니은히읗", text)
        text = re.sub(r"ㄺ", "리을기역", text)
        text = re.sub(r"ㄻ", "리을미음", text)
        text = re.sub(r"ㄼ", "리을비읍", text)
        text = re.sub(r"ㄽ", "리을시옷", text)
        text = re.sub(r"ㄾ", "리을티읕", text)
        text = re.sub(r"ㄿ", "리을피읍", text)
        text = re.sub(r"ㅀ", "리을히읗", text)
        text = re.sub(r"ㅄ", "비읍시옷", text)
        text = re.sub(r"ㅏ", "아", text)
        text = re.sub(r"ㅑ", "야", text)
        text = re.sub(r"ㅓ", "어", text)
        text = re.sub(r"ㅕ", "여", text)
        text = re.sub(r"ㅗ", "오", text)
        text = re.sub(r"ㅛ", "요", text)
        text = re.sub(r"ㅜ", "우", text)
        text = re.sub(r"ㅠ", "유", text)
        text = re.sub(r"ㅡ", "으", text)
        text = re.sub(r"ㅣ", "이", text)
        text = re.sub(r"ㅐ", "애", text)
        text = re.sub(r"ㅒ", "얘", text)
        text = re.sub(r"ㅔ", "에", text)
        text = re.sub(r"ㅖ", "예", text)
        text = re.sub(r"ㅘ", "와", text)
        text = re.sub(r"ㅙ", "왜", text)
        text = re.sub(r"ㅚ", "외", text)
        text = re.sub(r"ㅝ", "워", text)
        text = re.sub(r"ㅞ", "웨", text)
        text = re.sub(r"ㅟ", "위", text)
        text = re.sub(r"ㅢ", "의", text)

        return text


    def normalize_multiline_text(long_text):
        texts = split_text(long_text)
        normalized_texts = [normalize_text(text).strip() for text in texts]
        return [text for text in normalized_texts if len(text) > 0]

    def synthesize(text):
        wavs = synthesizer.tts(text, None, None)
        return wavs
    
########################################

# 경로 수정
# /home/piai/

########################################

    synthesizer = Synthesizer(
      "/home/piai/GPTTS/glow/best_model.pth.tar",
      "/home/piai/GPTTS/glow/config.json",
      None,
      "/home/piai/GPTTS/hifi/best_model.pth.tar",
      "/home/piai/GPTTS/hifi/config.json",
      None,
      None,
      False,
  )
    symbols = synthesizer.tts_config.characters.characters

    import soundfile as sf
    from io import BytesIO
    from base64 import b64encode
    from IPython.display import HTML, display
    import numpy as np

    # 문자열 받아옴
    texts=a


    all_wav = []
    for text in texts.split('\n'):  # 문장을 나누어 처리
        wav = synthesizer.tts(text, None, None)
        all_wav.append(wav)

    # 모든 오디오 데이터를 하나의 오디오로 합침
    combined_wav = np.concatenate(all_wav)  

    # 합쳐진 데이터를 바이트 형식으로 변환
    with BytesIO() as wav_file:
        sf.write(wav_file, combined_wav, 22050, format='WAV', subtype='PCM_16')
        wav_bytes = wav_file.getvalue()

    # Base64 인코딩 및 HTML 오디오 태그 생성
    audio_data = b64encode(wav_bytes).decode("utf-8")
    audio_html = f'<audio autoplay controls><source src="data:audio/wav;base64,{audio_data}" type="audio/wav"></audio>'
    display(display(HTML(audio_html)))

    ########################################

    # 파일 저장할 경로 지정
    # (output_file_path,wav_file_path)

    ########################################

    output_file_path = "/home/piai/GPTTS/output.wav"
    sf.write(output_file_path, combined_wav, 22050, format='WAV', subtype='PCM_16')


    # # 파일 불러서 출력
    # WAV 파일 경로 설정
    wav_file_path = '/home/piai/GPTTS/output.wav'

    # WAV 파일 출력
    play_wav_file(wav_file_path)




###############################gpt#########################

import openai
import pandas as pd

# OpenAI API 키 설정
openai.api_key = "본인 KEY"

import pygame

def play_audio_file():
    # pygame 초기화
    pygame.init()
    pygame.mixer.init()

    ########################################

    # 경로 수정
    # 저장한 오디오 파일을 불러오는 코드

    ########################################

    file_path = "/home/piai/GPTTS/output.wav"
    # 오디오 파일 로드 및 재생
    print(f"Playing ---")
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    # 오디오가 끝날 때까지 대기
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# 동화 생성 함수 업데이트함
def generate_fairy_tale(prompt, category, model="gpt-3.5-turbo-instruct", temperature=0.7, max_tokens=1000):
    prompt_with_category = prompt.format(category)
    response = openai.Completion.create(
        model=model,
        prompt=prompt_with_category,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
    )
    story = response.choices[0].text.strip()
    return story


# 메인 실행 부분
if __name__ == "__main__":
    command = input("명령어: ")
    if command == "동화 생성":
        category = input("동화 카테고리: ")
        # 동화 생성
        prompt = "건희라는 1살 아이에게 읽어줄 {}와 관련된 동화를 지어줘. 굉장히 쉬운 내용이어야 해.어린이가 들으면 안될 나쁜 내용은 없어야 해. 그리고 문장 사이는 띄어쓰기로만 이루어져야 해. 줄바꿈 하지마."
        fairy_tale_text = generate_fairy_tale(prompt, category)
        print(f"Generated Fairy Tale: \n{fairy_tale_text}")

        TTS_mo(fairy_tale_text)
        play_audio_file()


    else:
        print("지원하지 않는 명령어입니다.")