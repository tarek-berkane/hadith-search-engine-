from whoosh.analysis import RegexTokenizer, Filter, text_type, Token

from pyarabic import araby
from tashaphyne.stemming import ArabicLightStemmer
import arabicstopwords.arabicstopwords as stp


tokenize_text = araby.tokenize_with_location


class ArabicTokenizer(RegexTokenizer):

    def __call__(self, value, positions=False, chars=False, keeporiginal=False,
                 removestops=True, start_pos=0, start_char=0, tokenize=True,
                 mode='', **kwargs):
        assert isinstance(value, text_type), "%s is not unicode" % repr(value)

        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        if not tokenize:
            t.original = t.text = value
            t.boost = 1.0
            if positions:
                t.pos = start_pos
            if chars:
                t.startchar = start_char
                t.endchar = start_char + len(value)
            yield t
        elif not self.gaps:
            # The default: expression matches are used as tokens

            for pos, match in enumerate(iter(tokenize_text(value))):
                t.text = match['token']
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = start_pos + pos
                if chars:
                    t.startchar = start_char + match['start']
                    t.endchar = start_char + match['end']
                yield t
        else:
            # When gaps=True, iterate through the matches and
            # yield the text between them.
            prevend = 0
            pos = start_pos
            for match in iter(tokenize_text(value)):
                start = prevend
                end = match['start']
                text = value[start:end]
                if text:
                    t.text = text
                    t.boost = 1.0
                    if keeporiginal:
                        t.original = t.text
                    t.stopped = False
                    if positions:
                        t.pos = pos
                        pos += 1
                    if chars:
                        t.startchar = start_char + start
                        t.endchar = start_char + end

                    yield t

                prevend = match.end()

            # If the last "gap" was before the end of the text,
            # yield the last bit of text as a final token.
            if prevend < len(value):
                t.text = value[prevend:]
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = pos
                if chars:
                    t.startchar = prevend
                    t.endchar = len(value)
                yield t


class ArabicStopWordFilter(Filter):
    def __init__(self, minsize=2, maxsize=None,
                 renumber=True, lang=None):

        self.min = minsize
        self.max = maxsize
        self.renumber = renumber

    def __call__(self, tokens):
        minsize = self.min
        maxsize = self.max
        renumber = self.renumber

        pos = None
        for t in tokens:
            text = t.text
            if (len(text) >= minsize
                    and (maxsize is None or len(text) <= maxsize)
                    and not stp.is_stop(text)):
                # This is not a stop word
                if renumber and t.positions:
                    if pos is None:
                        pos = t.pos
                    else:
                        pos += 1
                        t.pos = pos
                t.stopped = False
                yield t
            else:
                # This is a stop word
                if not t.removestops:
                    # This IS a stop word, but we're not removing them
                    t.stopped = True


class RemoveTashkilFilter(Filter):

    def __call__(self, tokens):
        for t in tokens:
            text = t.text
            text_without_tashkeel = araby.strip_tashkeel(text)

            t.text = text_without_tashkeel
            yield t


class ArabicLightStemmerFilter(Filter):
    def __init__(self):
        self.arListem = ArabicLightStemmer()

    def __call__(self, tokens):
        for t in tokens:
            text = t.text
            text_stem = self.arListem.light_stem(text)

            t.text = text_stem
            yield t


analyzer = ArabicTokenizer() | RemoveTashkilFilter() | ArabicStopWordFilter() | ArabicLightStemmerFilter()
