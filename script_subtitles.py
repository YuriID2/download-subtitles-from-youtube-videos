import sys
import argparse
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


def create_parser():
    parser = argparse.ArgumentParser(
        description="Получение субтитров YouTube-видео"
    )
    parser.add_argument(
        "-n",
        "--name",
        "-u",
        "--url",
        required=True,
        help="URL YouTube-видео"
    )
    return parser


def get_video_id(video_url):
    """Извлекает ID видео из YouTube URL."""

    parsed_url = urlparse(video_url)

    # Обычный URL:
    # https://www.youtube.com/watch?v=XXXXXXXXXXX
    if parsed_url.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        video_id = parse_qs(parsed_url.query).get("v")

        if video_id:
            return video_id[0]

    # Короткий URL:
    # https://youtu.be/XXXXXXXXXXX
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/").split("/")[0]

    raise ValueError(
        "Не удалось определить ID видео. "
        "Используй обычную ссылку YouTube, например: "
        "https://www.youtube.com/watch?v=XXXXXXXXXXX"
    )


def get_subtitles(video_url):
    video_id = get_video_id(video_url)

    subtitles_file = f"titles_{video_id}.txt"

    print(f"ID видео: {video_id}")
    print("Получаем список доступных титров...")

    api = YouTubeTranscriptApi()

    # Современный API youtube-transcript-api
    transcript_list = api.list(video_id)

    print("Ищем русские титры...")

    try:
        # Сначала ищем русские субтитры
        transcript = transcript_list.find_transcript(["ru"])
    except Exception:
        print("Русские титры не найдены. Пробуем английские...")

        try:
            transcript = transcript_list.find_transcript(["en"])
        except Exception:
            raise RuntimeError(
                "Для этого видео не удалось найти русские или английские титры."
            )

    print(f"Найдены титры на языке: {transcript.language}")

    translated_transcript = transcript.fetch()

    with open(subtitles_file, "w", encoding="utf-8") as f:
        for line in translated_transcript:
            f.write(line.text + "\n")

    print()
    print("Всё получилось!")
    print(f"Титры записаны в файл: {subtitles_file}")


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    print(
        f"Получаем титры из видео по адресу:\n"
        f"{namespace.name}\n"
    )

    get_subtitles(namespace.name)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nОперация отменена.")

    except Exception as err:
        print(f"\nНичего не получилось, ибо: {err}")
       
