import mistune
import codecs
import pypandoc
import re


def txt2html(txt_path):
    input_file = codecs.open(txt_path, mode='r', encoding="utf-8")

    text = input_file.read()
    html = mistune.markdown(text)

    html_path = re.split('[.]', txt_path)[0] + '.html'
    output_file = codecs.open(html_path, mode='w', encoding="utf-8")
    output_file.write("<meta charset='utf-8'>")
    output_file.write(html)

    return html_path


def html2word(html_path):
    word_path = re.split('[.]', html_path)[0] + '.docx'
    print(word_path)
    pypandoc.convert_file(html_path, 'docx', outputfile=word_path)

    return word_path


def word2pdf(word_path):
    pdf_path = re.split('[.]', word_path)[0] + '.pdf'
    pypandoc.convert_file(word_path, 'pdf', outputfile=pdf_path)

    return pdf_path
