from text_summarization import text_summarization
import time

if __name__ == '__main__':
    start = time.time()
    get_summary = text_summarization.TextSummarization()
    get_summary.summary()
    end = time.time()
    print(f'Процесс выполнен за {end - start} сек.')
