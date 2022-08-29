from typing import Literal
from pathlib import Path
from datetime import datetime

from playsound import playsound
import pyttsx3
from loguru import logger

from youtubesearchpython import VideosSearch
import speech_recognition

from browser import get_url


class Counter():
    read_next_counter = 1
    start_counter = 1
    max_len: int = 10


recognizer = speech_recognition.Recognizer()
microfone = speech_recognition.Microphone(device_index=0)


def _find_on_youtube(key: str) -> None:
    result = VideosSearch(key, limit=50).result()
    Counter.max_len = len(result["result"])
    _text_to_speech(key)
    read_next(result, Counter.start_counter)
    command = _listen_command()
    while True:
        if command == "дальше":
            _make_sound(1)
            logger.info(command)
            Counter.read_next_counter += 1
            if Counter.read_next_counter > Counter.max_len:
                _text_to_speech("Это последнее видео")
                Counter.read_next_counter = Counter.max_len
            else:
                read_next(result, Counter.read_next_counter)
        elif command == "назад":
            _make_sound(1)
            logger.info(command)
            if Counter.read_next_counter - 1 < 1:
                Counter.read_next_counter = 1
            Counter.read_next_counter -= 1
            read_next(result, Counter.read_next_counter)
        elif command == "сначала":
            _make_sound(1)
            logger.info(command)
            read_next(result, Counter.start_counter)
        elif command == "стоп":
            logger.info(command)
            Counter.read_next_counter = 1
            break

        elif command.isdigit():
            logger.info(command)
            _make_sound(1)
            get_url(result["result"][int(command)-1]["link"])
            Counter.read_next_counter = 1
            break

        else:
            logger.info(command)
        command = _listen_command()


def _text_to_speech(text: str) -> None:
    engine = pyttsx3.init()
    engine.setProperty("rate", 120)
    engine.setProperty("volume", 1)
    engine.say(f"{text}")
    engine.runAndWait()


def read_next(search_results: dict, start_with: int) -> None:
    for video in search_results["result"][(start_with-1):]:
        _text_to_speech(f'Видео №{start_with}. {video["title"]}')
        break


def _say_time() -> None:
    time = datetime.now()
    _text_to_speech
    text_to_speech = f"{time.hour} часов, {time.minute} минут"
    _text_to_speech(text_to_speech)


def do_commands() -> None:
    _make_sound(3)
    while True:
        command = _listen_command()
        logger.info(command)

        if command == "поиск":
            _make_sound(1)
            command = _listen_command()
            if command != "запрос не распознан":
                _make_sound(2)
                logger.info(command)
            _find_on_youtube(command)
        elif command == "сколько время":
            _make_sound(1)
            logger.info(command)
            _say_time()


def _listen_command() -> str:
    """The function will return the recognized command"""
    logger.info("Слушаю твои команды")
    try:
        with microfone:
            recognizer.adjust_for_ambient_noise(source=microfone)
            # logger.info("Слушаю твои команды")
            audio = recognizer.listen(source=microfone)
            query: str = recognizer.recognize_google(
                audio_data=audio, language="ru-Ru").lower()
            # logger.info("Я тебя услышал")
            logger.info(query)
        return query
    except speech_recognition.UnknownValueError:
        return 'запрос не распознан'


def _make_sound(number_sound: Literal[1, 2, 3]) -> None:
    path = str(Path('sounds', f'{number_sound}.mp3'))
    playsound(path)
