import random
import pathlib
import textwrap
import sys
from fpdf import FPDF

class BingoCard:
    def __init__(self):
        self.bingo_items = self.load_bingo_items()
        self.card = self.generate_card()
        self.print_display()
        self.pdf_display()

    def load_bingo_items(self):
        file_path = pathlib.Path(__file__).parent / 'monthlist.txt'
        if not file_path.exists():
            print("Bingo items file not found.", file=sys.stderr)
            return []

        with open(file_path, 'r') as file:
            items = [line.strip() for line in file if line.strip()]
        
        if len(items) < 25:
            print("Not enough bingo items in the file.", file=sys.stderr)
            return []

        return items

    def shuffle_bingo_items(self):
        random.shuffle(self.bingo_items)
        return self.bingo_items[:25]

    def generate_card(self) -> list:
        items = self.shuffle_bingo_items()
        card = []
        columns = {
            'B': items[0:5],
            'I': items[5:10],
            'N': items[10:15],
            'G': items[15:20],
            'O': items[20:25],
        }
        
        for i in range(5):
            row = []
            for col in ['B', 'I', 'N', 'G', 'O']:
                row.append(columns[col][i])
            card.append(row)

        return card

    def print_display(self, col_width=18, cell_height=4):
        def _format_cell(text, width, height):
            lines = textwrap.wrap(str(text), width=width) or ['']
            if len(lines) > height:
                last = lines[height-1]
                lines = lines[:height]
                lines[-1] = last[:max(0, width-3)] + '...'
            while len(lines) < height:
                lines.append('')
            return [ln.center(width) for ln in lines]

        cols = ['B', 'I', 'N', 'G', 'O']
        # prepare wrapped cells for the whole card
        wrapped = [[_format_cell(cell, col_width, cell_height) for cell in row] for row in self.card]

        sep = '+' + '+'.join(['-' * (col_width + 2) for _ in cols]) + '+'
        header_cells = [c.center(col_width) for c in cols]
        header_row = '| ' + ' | '.join(header_cells) + ' |'

        print(sep)
        print(header_row)
        print(sep)
        for r in range(len(self.card)):
            for line_idx in range(cell_height):
                row_line = '| ' + ' | '.join(wrapped[r][c][line_idx] for c in range(len(cols))) + ' |'
                print(row_line)
            print(sep)

    def pdf_display(self):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=16)

        with pdf.table() as table:
            header = table.row()
            for letter in ['B', 'I', 'N', 'G', 'O']:
                header.cell(letter, align='C')
            for data_row in self.card:
                row = table.row()
                for datum in data_row:
                    row.cell(datum, align='C')


        pdf.output("bingo_card.pdf")

if __name__ == "__main__":
    BingoCard()