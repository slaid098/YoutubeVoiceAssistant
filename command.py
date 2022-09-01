from typing import Literal
from pathlib import Path
import os
import time

from playsound import playsound
import gtts
from loguru import logger

from youtubesearchpython import VideosSearch
import speech_recognition
from selenium.common.exceptions import WebDriverException

from browser import get_url, driver


class Counter():
    read_next_counter = 1
    start_counter = 1
    max_len: int = 10


recognizer = speech_recognition.Recognizer()
microfone = speech_recognition.Microphone(device_index=0)


def do_commands() -> None:
    _make_sound(3)
    while True:
        command = _listen_command()
        logger.info(command)

        if "слушай вики" in command:
            _make_sound(1)
            command = _listen_command()
            if command != "запрос не распознан":
                _make_sound(2)
                logger.info(command)
                _find_on_youtube(command)
            else:
                _text_to_speech("Я вас не поняла")
                _make_sound(4)
        elif "вики" in command:
            _make_sound(1)
            _browser_to_front()
            _make_sound(4)


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


def _make_sound(number_sound: Literal[1, 2, 3, 4]) -> None:
    path = str(Path('sounds', f'{number_sound}.mp3'))
    playsound(path)


def _find_on_youtube(key: str) -> None:
    result = VideosSearch(key, limit=50).result()
    Counter.max_len = len(result["result"])
    _text_to_speech(key)
    _read_next(result, Counter.start_counter)
    command = _listen_command()
    while True:
        if "дальше" in command:
            _make_sound(1)
            logger.info(command)
            Counter.read_next_counter += 1
            if Counter.read_next_counter > Counter.max_len:
                _text_to_speech("Это последнее видео")
                Counter.read_next_counter = Counter.max_len
                _make_sound(4)
            else:
                _read_next(result, Counter.read_next_counter)
                _make_sound(4)
        elif "назад" in command:
            _make_sound(1)
            logger.info(command)
            if Counter.read_next_counter - 1 < 1:
                Counter.read_next_counter = 1
            Counter.read_next_counter -= 1
            _read_next(result, Counter.read_next_counter)
            _make_sound(4)
        elif "сначала" in command:
            _make_sound(1)
            logger.info(command)
            _read_next(result, Counter.start_counter)
            _make_sound(4)
        elif "стоп" in command:
            _make_sound(1)
            logger.info(command)
            Counter.read_next_counter = 1
            _make_sound(4)
            break

        elif command.isdigit():
            logger.info(command)
            _make_sound(1)
            get_url(result["result"][int(command)-1]["link"])
            Counter.read_next_counter = 1
            break

        else:
            logger.info(command)
            _make_sound(1)
            _text_to_speech("Я вас не поняла")
            _text_to_speech("Список комманд в режиме поиска видео:"
                            "дальше, назад, сначала, стоп и номер видео,"
                            "например, 1")
            _make_sound(4)

        command = _listen_command()


def _read_next(search_results: dict, start_with: int) -> None:
    for video in search_results["result"][(start_with-1):]:
        _text_to_speech(f'Видео №{start_with}. {video["title"]}')
        break


def _text_to_speech(text: str) -> None:
    path = Path('sounds', f'{int(time.time())}.mp3')
    tts = gtts.gTTS(text, lang="ru")
    tts.save(str(path))
    playsound(str(path))
    os.remove(path)


def _browser_to_front() -> None:
    try:
        driver.minimize_window()
        driver.maximize_window()
    except WebDriverException as ex:
        logger.warning(f"{type(ex)} {ex}")
    except Exception as ex:
        logger.warning(f"{type(ex)} {ex}")
