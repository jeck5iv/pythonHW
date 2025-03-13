import sys
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', type=click.File('r'), required=False)
def nl(file):
    lines = file.readlines() if file else sys.stdin.readlines()
    for i, line in enumerate(lines, start=1):
        # выравниваем номер строки по правому краю до 6 символов
        print(f"{i:>6}\t{line.rstrip()}")


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def tail(files):
    lines_to_show = 10 if files else 17

    def print_tail(file, show_filename=False, is_not_last_file=False):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if show_filename:
            print(f"==> {file} <==")
        if lines:
            print("".join(lines[-lines_to_show:]), end="")
        if show_filename and is_not_last_file:
            print()

    if not files:
        lines = click.get_text_stream("stdin").readlines()
        print("".join(lines[-lines_to_show:]), end="")
    else:
        for i, file in enumerate(files):
            print_tail(file, show_filename=(len(files) > 1),
                       is_not_last_file=(i != len(files) - 1))


@cli.command()
@click.argument('files', type=click.Path(exists=True), nargs=-1)
def wc(files):
    def count_stats(f):
        content = f.read()
        lines_count = content.count('\n')
        words = len(content.split())
        bytes_size = len(content.encode('utf-8'))
        return lines_count, words, bytes_size

    total_lines, total_words, total_bytes = 0, 0, 0

    # для выравнивания
    line_counts = []
    word_counts = []
    byte_counts = []

    # если нет файлов, то работаем с stdin
    if not files:
        lines, words, bytes_size = count_stats(sys.stdin)
        line_counts.append(lines)
        word_counts.append(words)
        byte_counts.append(bytes_size)
    else:
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                lines, words, bytes_size = count_stats(f)
                line_counts.append(lines)
                word_counts.append(words)
                byte_counts.append(bytes_size)
                total_lines += lines
                total_words += words
                total_bytes += bytes_size

        if len(files) > 1:
            line_counts.append(total_lines)
            word_counts.append(total_words)
            byte_counts.append(total_bytes)

    max_line_len = max(len(str(num)) for num in line_counts)
    max_word_len = max(len(str(num)) for num in word_counts)
    max_byte_len = max(len(str(num)) for num in byte_counts)
    max_len = max(max_line_len, max_word_len, max_byte_len)

    if not files:
        # wc в терминале почему-то выравнивает именно так (по 7 символам в столбце), а внутри числа по правому краю
        max_len = 7
        print(f"{line_counts[0]:>{max_len}} {word_counts[0]:>{max_len}} {byte_counts[0]:>{max_len}}")

    else:
        # wc по файлам выравнивает по максимальной длине числа в таблице, а внутри числа по правому краю
        for i, file in enumerate(files):
            print(f"{line_counts[i]:>{max_len}} {word_counts[i]:>{max_len}} "
                  f"{byte_counts[i]:>{max_len}} {file}")

        if len(files) > 1:
            print(f"{line_counts[-1]:>{max_len}} {word_counts[-1]:>{max_len}} "
                  f"{byte_counts[-1]:>{max_len}} total")


if __name__ == "__main__":
    cli()
