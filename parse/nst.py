from csv import Dialect, QUOTE_NONE
from pandas import read_csv


class nst_dialect(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ';'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_NONE


class NST:

    def __init__(self, fn="swe030224NST.pron", encoding='iso-8859-1',
                 nrows=200, exclude_accronyms=False, exclude_loanwords=False,
                 exclude_inflected=False):
        self.df = read_csv(fn, encoding=encoding, header=None,
                           dialect=nst_dialect, nrows=nrows)
        if exclude_accronyms:
            self.df = self.df[self.df[9].isnull()]
        if exclude_loanwords:
            self.df = self.df[self.df[6] == 'SWE']
        if exclude_inflected:
            self.df = self.df[self.df[31] != 'INFLECTED']
        self.df = self.df.reset_index()            

    def get_rows(self):
        return self.df

    def get_transcriptions(self):
        return self.df[11]
