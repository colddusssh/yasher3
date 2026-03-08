# -*- coding: utf-8 -*-
import sys
import subprocess
import code
from tokenize import generate_tokens, NAME, NEWLINE, INDENT, DEDENT
from io import StringIO

words = {
    "внедрить": "import",
    "из": "from",
    "как": "as",
    "молвить": "print",
    "внемлить": "input",
    "правда": "True",
    "кривда": "False",
    "никто": "None",
    "ничто": "None",
    "коли": "if",
    "отнюдь": "else",
    "отнюдь_если": "elif",
    "покуда": "while",
    "для": "for",
    "воздать": "return",
    "династия": "class",
    "попытаться": "try",
    "поймать": "except",
    "поднять": "raise",
    "с_чем": "with",
    "как": "as",
    "импорт": "import",
    "не": "not",
    "и": "and",
    "или": "or",
    "в": "in",
    "есть": "is",
    "ламбда": "lambda",
    "уступить": "yield",
    "глобал": "global",
    "нелокальный": "nonlocal",
    "утверждать": "assert",
    "перерыв": "break",
    "продолжить": "continue",
    "проход": "pass",
    "удалить": "del",
    "переключатель": "match",
    "путь": "case",
    "базированно": "_",
    "длина": "len",
    "диапазон": "range",
    "тип": "type",
    "строка": "str",
    "целина": "int",
    "дробь": "float",
    "комплекс": "complex",
    "список": "list",
    "кортеж": "tuple",
    "словарь": "dict",
    "множество": "set",
    "булево": "bool",
    "байты": "bytes",
    "байтовый_массив": "bytearray",
    "нить": "str",
    "много_букав": "str",
    "открыть": "open",
    "читать": "read",
    "писать": "write",
    "закрыть": "close",
    "очередь": "queue.Queue",
    "двойня": "tuple",
    "старший": "[0]",
    "младший": "[1]",
    "оператор": "operator",
    "двинуть": "move",
    "сам": "self",
    "инициализация": "__init__",
    "строка_документации": "__doc__",
    "мощь": "pow",
    "времечко": "time.time",
    "судьба": "random.randint",
    "судьбоносный": "random.seed",
    "беда": "Exception",
    "исключение": "Exception",
    "что_случилось": "args[0]",
    "гнев_Перуна": "Exception",
    "читать_летопись": "open",
    "писать_летопись": "open",
    "летопись": "open",
    "друже": "friend",
    "окстись": "goto",
    "свет_мой_зеркальце": "template",
    "скажи": "typename",
    "царский": "_private",
    "народный": "public",
    "дружинный": "protected",
    "встрой": "inline",
    "кощей": "staticmethod",
    "местный": "self",
    "хутор": "namespace",
    "откупорить": "open",
    "закупорить": "close",
    "суд_Перуна": "auto",
    "аки": "static_cast",
    "очами_стрельнуть": "peek",
    "зачерпнуть": "input",
    "добрый_молодец": "good",
    "змей_подколодный": "fail",
    "вот_и_сказочке_конец": "eof",
    "приток_Байкала": "ostream",
    "отток_Байкала": "istream",
    "меняло": "swap",
    "отщипнуть": "get",
    "однобокая_целина": "int",
    "однобокая_буква": "int",
    "однобокий_карлик": "int",
    "однобокий_долговязый": "int",
    "однобокий_Петр_Первый": "int",
    "перепись": "enumerate",
    "счёт_древних_русов": "enumerate",
    "ноль": "0",
    "целковый": "1",
    "полушка": "2",
    "четвертушка": "3",
    "осьмушка": "4",
    "пудовичок": "5",
    "медячок": "6",
    "серебрячок": "7",
    "золотничок": "8",
    "девятичок": "9",
    "десятичок": "10",
    "очередь": "queue.Queue",
    "крайний": "queue.Queue[-1]",
    "разместить": "queue.Queue.put",
    "пуста": "queue.Queue.empty",
    "первый": "queue.Queue[0]",
    "отрезать": "queue.Queue.get",
    "приклеить": "queue.Queue.put",
    "размер": "queue.Queue.qsize",
    "взять_сосуд": "_get_container",
    "Сибирь": "Siberia",
    "звено": "Node",
    "ключик": "key",
    "высота": "height",
    "лево": "left",
    "право": "right",
    "корневище": "root",
    "условие_выравнивания": "balance_factor",
    "пересчитать_высоту": "update_height",
    "повернуть_направо": "rotate_right",
    "повернуть_налево": "rotate_left",
    "выровнять": "balance",
    "найти_и_выкорчевать_меньший": "_find_and_remove_min",
    "выкорчевать_по_ключику": "_remove",
    "вставка": "_insert",
    "отпочковать": "_copy_subtree",
    "вырубить": "_clear",
    "выкопать_корневище": "get_root",
    "посадить_корневище": "set_root",
    "прирастить": "insert",
    "выкорчевать": "remove",
    "растет_ли": "__contains__",
    "высота": "height",
    "династия": "class",
    "семейство": "class",
    "розсуд": "bool",
    "бестолочь": "None",
    "мерило": "int",
    "Петр_Первый": "int",
    "карлик": "int",
    "долговязый": "int",
    "вель_дробь": "float",
    "малый_дробь": "float",
    "буква": "str",
    "приказ_княжий": "const",
    "новь": "None",
    "казнь": "del",
    "туда_не_знаю_куда": "None",
    "НИЧТО": "None",
    "в_строченьку": "str",
    "ширь": "format",
    "получи_басурман": "raise",
    "внедрить": "import",
    "использовать": "using",
    "обозвать": "alias",
    "Русь": "sys",
    "царь_батюшка_главный": "__main__",
    "пахать": "while True",
    "покуда": "while",
    "бить_ящеров": "break",
    "добить_ящеров": "continue",
    "путевой_камень": "match",
    "прыг_скок": "end='\\n'",
    "басурман": "throw",
    "мощь": "pow",
    "кощей": "static",
    "местный": "self",
    "друже": "friend",
    "окстись": "goto",
    "времечко": "time",
    "зачерпнуть": "input",
    "добрый_молодец": "good",
    "змей_подколодный": "fail",
    "вот_и_сказочке_конец": "eof",
    "вск": "eof",
    "приток_Байкала": "print",
    "отток_Байкала": "input",
    "меняло": "swap",
    "отщипнуть": "get",
    "хутор": "namespace",
    "откупорить": "open",
    "закупорить": "close",
    "суд_Перуна": "auto",
    "аки": "cast",
    "очами_стрельнуть": "peek",
    "двойня": "tuple",
    "старший": "first",
    "младший": "second",
    "оператор": "operator",
    "двинуть": "move",
    "выйти" : "exit()",
    "выход" : "exit()",
    "помощь" : "help"
}

def translate_code(source, word_map):
    tokens = list(generate_tokens(StringIO(source).readline))
    result = []
    prev_end_col = 0
    prev_line = 1

    for toknum, tokval, start, end, line in tokens:
        line_num, col = start

        if line_num > prev_line:
            result.append("\n")
            if col > 0:
                result.append(" " * col)
        else:
            spaces = col - prev_end_col
            if spaces > 0:
                result.append(" " * spaces)

        if toknum == NAME and tokval in word_map:
            token_str = word_map[tokval]
        else:
            token_str = tokval

        result.append(token_str)

        prev_end_col = end[1]
        prev_line = end[0]

    return "".join(result)

class SlavicInteractiveConsole(code.InteractiveConsole):
    def __init__(self, word_map, locals=None):
        super().__init__(locals)
        self.word_map = word_map

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            translated = translate_code(source, self.word_map)
        except Exception as e:
            self.write(f"Ошибка перевода: {e}\n")
            return False
        return super().runsource(translated, filename, symbol)

def run_interactive():
    print("Славянский языкъ программирования ящер3 ('выйти' для выхода)")
    sys.ps1 = ">>> "
    sys.ps2 = "...    "
    console = SlavicInteractiveConsole(words)
    console.interact(banner="", exitmsg="До свидания!")

def main():
    args = sys.argv[1:]
    if not args:
        run_interactive()
        return

    filepath = args[0]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()

    except FileNotFoundError:
        print(f"Файл {filepath} не найден")
        sys.exit(1)

    translated = translate_code(source, words)

    out_path = f".out_{filepath}.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(translated)

    try:
        subprocess.run(["python3", out_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()