try:
   from youtube_transcript_api import YouTubeTranscriptApi
   import sys
   import argparse

   def createParser ():
       parser = argparse.ArgumentParser()
       parser.add_argument ('-n', '--name','-u','--url')

       return parser


   if __name__ == '__main__':
       parser = createParser()
       namespace = parser.parse_args(sys.argv[1:])

       print ("Получаем титры из видео по адресу, {}!".format (namespace.name) )


       def get_subtitles(video_url):
           video_id = video_url.split("watch?v=")[1]
           #имя текстового файла с титрами будет включать id видео
           subtitles_file='titles_'+video_id+'.txt'
           transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
           transcript = transcript_list.find_transcript(['ru'])
           translated_transcript = transcript.fetch()

           with open(subtitles_file, 'w', encoding='utf-8') as f:
               for line in translated_transcript:
                   f.write(line['text'] + '\n')

           print('Всё получилось. Титры записаны в созданный файл: '+subtitles_file)

       get_subtitles(namespace.name)

#обернули всё try - except, чтобы выбросить исключение и понять в чём ошибка в случае таковой
except Exception as err:
   print('Ничего не получилось, ибо: '+str(err))

