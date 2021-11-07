from text_processing import pipe


def main():
    with open('text.txt', 'r') as input_file:
        text = input_file.read()
    processed_text = pipe.Summary(text)
    processed_text.get_summary()
    with open('text_summary.txt', 'w') as output_file:
        output_file.write(processed_text.summary)  

if __name__ == '__main__':
    main()
        


