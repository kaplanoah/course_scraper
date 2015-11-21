class CsvFile(file):

    delimiter = '|'

    def add_row(self, *columns):
        for column_index, column in enumerate(columns):

            assert self.delimiter not in column

            if column_index < len(columns) - 1:
                self.write(column + self.delimiter)
            else:
                self.write(column + '\n')
