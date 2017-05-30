import astrolabe


class JournalPage(object): 
    def __init__(self, input_file='pagetemplate', astroday=astrolabe.Day()):
        self.symbols = {'Venus': '\\venus',
                        'Mercury': '\\mercury',
                        'Moon': '\\leftmoon',
                        'Saturn': '\\saturn',
                        'Jupiter': '\\jupiter',
                        'Mars': '\\mars',
                        'Sun': '\\astrosun'}
        self.day = astroday 
        self.substitutions = {'CITY': self.day.city,
                              'DATE': self.day.time.strftime('%D') ,
                              'DAYRULER': self.symbols[self.day.day_ruler[0]],
                              'SOLARNOON': self.day.sun_markers[1].strftime('%H:%M'),
                              'PHASE': self.day.moon_phase,
                              'DAYTABLE': self.chart(self.day.day_chart),
                              'NIGHTTABLE': self.chart(self.day.night_chart)}
        self.page = self.make_page(input_file)

    def make_page(self, input_file):
        page = []
        for line in open(input_file):
            line = line.split()
            for index, word in enumerate(line):
                if word in list(self.substitutions.keys()):
                    line[index] = self.substitutions[word]
            line = ' '.join(line)
            page.append(line + '\n')
        page = ' '.join(page)
        return page

    def chart(self, chart):
        new_chart = ''
        for row in chart:
            new_chart += self.symbols[row[0][0]] + '&' + row[1].strftime('%H:%M') + '&' + row[2].strftime('%H:%M') + \
                         '\\\\\n'
        return new_chart


def write_journal(journalpages, input_file='doctemplate', output_file='output.tex'):
    with open(output_file, 'w') as f:
        for line in open(input_file):
            line = line.split()
            for index, word in enumerate(line):
                if word == 'INSERTDOCUMENT':
                    line[index] = journalpages
            line = ' '.join(line)
            f.write(line + '\n')
