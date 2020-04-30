import requests
from bs4 import BeautifulSoup
import csv
import io
import os

for file in os.listdir("/Users/novin/Desktop/Extractor"):
    if file.endswith(".html"):
        quotes = []  # a list to store quotes
        f = open(file, "r", encoding="utf-8")
        soup = BeautifulSoup(f.read(), 'html.parser')
        rows = soup.findAll('div', {"class": 'display_question question multiple_choice_question'})
        name = soup.select('div.displaying h1')[0].text
        for row in rows:
            questions = row.findAll('div', {"class": 'question_text user_content enhanced'})
            # print(len(questions))
            question = {}
            for q in questions:
                question = q.text
            options = row.select('div.answer.answer_for_')
            opts = []
            for opt in options:
                option = {'text': opt.findAll('div', {"class": 'answer_text'})[0].text,
                          'is_ans': 'correct_answer' in opt.get('class')}
                opts.append(option)
            quotes.append({'question': question, 'options': opts})

        opt_header = ['<div style="font-weight: bold;display: inline;">الف) </div>',
                      '<div style="font-weight: bold;display: inline;">ب) </div>',
                      '<div style="font-weight: bold;display: inline;">ج) </div>',
                      '<div style="font-weight: bold;display: inline;">د) </div>']

        filename = 'All_Questions.html'
        with io.open(filename, "a", encoding="utf-8") as f:
            f.write("<html dir='rtl' lang='IR-fa'> <body> "
                    "<style>"
                    '''
                    *{
                    font-family: B Mitra,Times New Roman;
                    }
                                table
                    {
                        border-collapse: collapse;
                    }

                    td
                    {
                        border: thin solid black;
                    }
                    '''
                    "</style>"
                    "\n<br>")
            f.write("<br><h1 dir='rtl'>" + name + "</h1>\n<br><table>")
            for quote in quotes:
                f.write("<tr dir='rtl'><td dir='rtl'>\n<br>")
                # print([quote['name'], quote['uni'], quote['date']])
                f.write("{0}\n".format(quote['question']))
                i = 0
                for opt in quote['options']:
                    if opt['is_ans']:
                        f.write("<div style='color:#00B050;'>")
                    f.write('<div>'+opt_header[i] + opt['text'] + "\n </div>")
                    i += 1
                    if opt['is_ans']:
                        f.write("</div>")
                f.write("</td></tr>\n")
            f.write("</table> </body> </html>")


