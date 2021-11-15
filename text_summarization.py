import os

from dotenv import load_dotenv

from text_processing import pipe

load_dotenv()


def main():
    path = os.environ.get('PATH_TO_FILE')
    files = os.listdir(path)
    for file in files:
        file_path = path + '/'
        text_name = os.path.join(path, file)
        summary_name = ''.join(text_name.split('.')[0] + '_summary' + '.txt')
        with open(file_path + file, 'r', encoding='utf-8') as input_file:
            text = input_file.read()
        processed_text = pipe.Summary(text, file)
        processed_text.get_summary()
        with open(summary_name, 'w', encoding='utf-8') as output_file:
            output_file.write(processed_text.summary)  

if __name__ == '__main__':
    main()



