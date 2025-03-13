#!/bin/bash

# Создаем папку artifacts, если её нет
mkdir -p artifacts

# Очищаем предыдущий лог
> artifacts/test_log.txt

# Функция для запуска команды и записи вывода в лог
run_test() {
    echo "Running: $1" | tee -a artifacts/test_log.txt
    eval $1 >> artifacts/test_log.txt 2>&1
    echo "" >> artifacts/test_log.txt
}

# Функция для сравнения вывода вашего скрипта и Linux-команды
compare_with_linux() {
    echo "Running (Linux): $1" | tee -a artifacts/test_log.txt
    eval $1 >> artifacts/test_log.txt 2>&1
    echo "" >> artifacts/test_log.txt
}

# nl
run_test 'printf "line1\nline278\nline3" | python cli.py nl'
compare_with_linux 'printf "line1\nline278\nline3" | nl -b a'

run_test 'printf "line1\nline278\nline3" > artifacts/test.txt; python cli.py nl artifacts/test.txt'
compare_with_linux 'printf "line1\nline278\nline3" > artifacts/test.txt; nl -b a artifacts/test.txt'

run_test 'touch artifacts/empty.txt; python cli.py nl artifacts/empty.txt'
compare_with_linux 'touch artifacts/empty.txt; nl -b a artifacts/empty.txt'

# tail
run_test 'seq 1 20 | python cli.py tail'
compare_with_linux 'seq 1 20 | tail -n 17'

run_test 'seq 1 15 > artifacts/test.txt; python cli.py tail artifacts/test.txt'
compare_with_linux 'seq 1 15 > artifacts/test.txt; tail -n 10 artifacts/test.txt'

run_test 'seq 1 5 > artifacts/test1.txt; seq 6 10 > artifacts/test2.txt; python cli.py tail artifacts/test1.txt artifacts/test2.txt'
compare_with_linux 'seq 1 5 > artifacts/test1.txt; seq 6 10 > artifacts/test2.txt; tail -n 10 artifacts/test1.txt artifacts/test2.txt'

run_test 'touch artifacts/empty.txt; python cli.py tail artifacts/empty.txt'
compare_with_linux 'touch artifacts/empty.txt; tail -n 10 artifacts/empty.txt'

# wc
run_test 'printf "line1\nline278\nline3" | python cli.py wc'
compare_with_linux 'printf "line1\nline278\nline3" | wc'

run_test 'printf "line1\nline278\nline3" > artifacts/test.txt; python cli.py wc artifacts/test.txt'
compare_with_linux 'printf "line1\nline278\nline3" > artifacts/test.txt; wc artifacts/test.txt'

run_test 'printf "line1\nline278" > artifacts/test1.txt; printf "line3\nline4" > artifacts/test2.txt; python cli.py wc artifacts/test1.txt artifacts/test2.txt'
compare_with_linux 'printf "line1\nline278" > artifacts/test1.txt; printf "line3\nline4" > artifacts/test2.txt; wc artifacts/test1.txt artifacts/test2.txt'

run_test 'touch artifacts/empty.txt; python cli.py wc artifacts/empty.txt'
compare_with_linux 'touch artifacts/empty.txt; wc artifacts/empty.txt'

# всё вместе
run_test 'printf "line1\nline278\nline3" | python cli.py nl; printf "line1\nline278\nline3" | python cli.py tail; printf "line1\nline278\nline3" | python cli.py wc'
compare_with_linux 'printf "line1\nline278\nline3" | nl -b a; printf "line1\nline278\nline3" | tail -n 17; printf "line1\nline278\nline3" | wc'

run_test 'printf "line1\nline278\nline3" > artifacts/test.txt; python cli.py nl artifacts/test.txt; python cli.py tail artifacts/test.txt; python cli.py wc artifacts/test.txt'
compare_with_linux 'printf "line1\nline278\nline3" > artifacts/test.txt; nl -b a artifacts/test.txt; tail -n 10 artifacts/test.txt; wc artifacts/test.txt'

run_test 'touch artifacts/empty1.txt artifacts/empty2.txt; python cli.py nl artifacts/empty1.txt; python cli.py tail artifacts/empty1.txt artifacts/empty2.txt; python cli.py wc artifacts/empty1.txt artifacts/empty2.txt'
compare_with_linux 'touch artifacts/empty1.txt artifacts/empty2.txt; nl -b a artifacts/empty1.txt; tail -n 10 artifacts/empty1.txt artifacts/empty2.txt; wc artifacts/empty1.txt artifacts/empty2.txt'

echo "check artifacts/test_log.txt for results."