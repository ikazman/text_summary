import os

from dotenv import load_dotenv

from text_processing import pipe

load_dotenv()


class TextSummarization:

    def __init__(self):
        self.path = os.environ.get('PATH_TO_FILE')
        self.files = os.listdir(self.path + '/texts/')
        self.texts_path = self.path + '/texts/'
        self.summaries_path = self.path + '/summaries/'

    def already_summarized(self, path, summary_name):
        return summary_name in os.listdir(path + '/summaries/')

    def summary(self):
        for file in self.files:
            text_path = self.texts_path + file
            summary_name = file.split('.')[0] + '_summary' + '.txt'
            summary_path = self.summaries_path + summary_name
            if self.already_summarized(self.path, summary_name):
                print(f'Пропускаем текст {file}: резюме уже существует.')
                continue
            with open(text_path, 'r', encoding='utf-8') as input_file:
                text = input_file.read()
            processed_text = pipe.Summary(text, file)
            processed_text.get_summary()
            with open(summary_path, 'w', encoding='utf-8') as output_file:
                output_file.write(processed_text.summary)
