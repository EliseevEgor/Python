import shutil
import os
from io import StringIO

from egoreliseev_python_hw1 import plot_ast

OUTPUT_FILE = 'artifacts/output.tex'

DOCUMENT_CLASS = '\\documentclass{article}'
USE_PACKAGE = '\\usepackage{graphicx}'
BEGIN_DOCUMENT = '\\begin{document}'
END_DOCUMENT = '\\end{document}'
PICTURE = '\\includegraphics[scale=0.15]{artifacts/example}'
HEADER_BEGIN = '\\begin'
HEADER_L = '| l '
HEADER_END = '|}'
FOOTER_END = '\\end'
STRING_END = '\\\\'
TABULAR = '{tabular}'
HLINE = '\\hline'
NEXT_LINE = '\\\\'
ENTER = '\n'
AND = ' & '


def generate_table_header(num: int, buf: StringIO):
    buf.write(HEADER_BEGIN)
    buf.write(TABULAR)
    buf.write("{")
    buf.write(num * HEADER_L)
    buf.write(HEADER_END)
    buf.write(ENTER)
    buf.write(HLINE)
    buf.write(ENTER)


def generate_table_footer(buf: StringIO):
    buf.write(FOOTER_END)
    buf.write(TABULAR)
    buf.write(ENTER)


def generate_elem(e):
    return str(e) + AND


def generate_table_string(list_of_lists: list):
    for el in list_of_lists:
        last_elem = str(el.pop(len(list_of_lists) - 1))
        without_last = ''.join(map(generate_elem, el))
        yield without_last + last_elem + STRING_END + HLINE + ENTER


def write_to_file(buf):
    with open(OUTPUT_FILE, 'w') as fd:
        buf.seek(0)
        shutil.copyfileobj(buf, fd)


def generate_table(list_of_lists: list, buf: StringIO):
    generate_table_header(len(list_of_lists[0]), buf)
    table = generate_table_string(list_of_lists)
    for el in table:
        buf.write(el)
    generate_table_footer(buf)


def generate_picture(buf: StringIO):
    plot_ast()
    buf.write(PICTURE)
    buf.write(ENTER)


def write_to_pdf():
    os.system("pdflatex %s" % OUTPUT_FILE)


def generate_latex(list_of_lists: list):
    buf = StringIO()
    buf.write(DOCUMENT_CLASS)
    buf.write(ENTER)
    buf.write(USE_PACKAGE)
    buf.write(ENTER)
    buf.write(ENTER)

    buf.write(BEGIN_DOCUMENT)
    buf.write(ENTER)

    generate_table(list_of_lists, buf)

    buf.write(NEXT_LINE)
    buf.write(ENTER)

    generate_picture(buf)

    buf.write(END_DOCUMENT)
    write_to_file(buf)
    write_to_pdf()


if __name__ == '__main__':
    lst = [[1, 2, 3], ['a', 'b', 'c'], [0.1, 0.2, 0.3]]
    generate_latex(lst)
