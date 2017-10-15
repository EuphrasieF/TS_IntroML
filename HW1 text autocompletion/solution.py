import pymorphy2 as pm2

# объявим где хранятся исходные данные
PATH_TRAIN = 'C:/Users/eitherlast/Desktop/train.csv'
PATH_TEST = 'C:/Users/eitherlast/Desktop/test.csv'

# объявим куда сохраним результат
PATH_PRED = 'pred.csv'


## Из тренировочного набора собираем статистику о встречаемости слов

# создаем словарь для хранения статистики
word_stat_dict = {}

freq_dict = {}

# открываем файл на чтение в режиме текста
fl = open(PATH_TRAIN, 'rt', encoding = 'UTF-8')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()


# в цикле читаем строчки из файла
for line in fl:
    # разбиваем строчку на три строковые переменные
    Id, Sample, Prediction = line.strip().split(',')
    # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
    word1, word2 = Prediction.split(' ')
    word_1, word_2 = Sample.split(' ')


    
    key = word1 + '$' + word_2[:2]
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if word2 not in word_stat_dict[key]:
        word_stat_dict[key][word2] = 0
    # увеличим значение счетчика по текущему слову на 1
    word_stat_dict[key][word2] += 1

    
    key = word2[:2]
    if key not in freq_dict:
        freq_dict[key] = {}
    if word2 not in freq_dict[key]:
        freq_dict[key][word2] = 0
    freq_dict[key][word2] += 1
    key = word1[:2]
    if key not in freq_dict:
        freq_dict[key] = {}
    if word1 not in freq_dict[key]:
        freq_dict[key][word1] = 0
    freq_dict[key][word1] += 1
    

# закрываем файл
fl.close()

## Строим модель

## Выполняем предсказание

# открываем файл на чтение в режиме текста
fl = open(PATH_TEST, 'rt', encoding = 'UTF-8')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()

# открываем файл на запись в режиме текста
out_fl = open(PATH_PRED, 'wt', encoding = 'UTF-8')

# записываем заголовок таблицы
out_fl.write('Id,Prediction\n')

# в цикле читаем строчки из тестового файла
for line in fl:
    # разбиваем строчку на две строковые переменные
    Id, Sample = line.strip().split(',')
    # строковая переменная Sample содержит в себе полностью первое слово и кусок второго слова, разделим их
    word1, word2_chunk = Sample.split(' ')
    # вычислим ключ для заданного фрагмента второго слова

    key = word1 + '$' + word2_chunk[:2]
    key2 = word2_chunk[:2]
    if key not in word_stat_dict:
        if key2 not in freq_dict:
            out_fl.write('%s, %s %s\n' % (Id, word1, 'и') )
        else:
            while len(word2_chunk) > 0:
                suitable_words = [word for word in freq_dict[key2] if word.startswith(word2_chunk)]
                if len(suitable_words) == 0:
                    word2_chunk = word2_chunk[:-1]
                    continue
                prediction = max(suitable_words, key=freq_dict[key2].get)
                out_fl.write('%s,%s %s\n' % (Id, word1, prediction) )
                break
    else:
        occurences = word_stat_dict[key]
        while len(word2_chunk) > 0:
            suitable_words = [word for word in occurences if word.startswith(word2_chunk)]
            if len(suitable_words) == 0:
                word2_chunk = word2_chunk[:-1]
                continue
            prediction = max(suitable_words, key=occurences.get)
            out_fl.write('%s,%s %s\n' % (Id, word1, prediction) )
            break

    

# закрываем файлы
fl.close()
out_fl.close()

#кино смотреть
#смотреть кино - учитывать очередность
#DONE

#выбрали просто частотность второго слова, нужна частотность сочетаемости
#DONE

#нужна нормализация по word2

#сочетаемость частей речи

#большой словарь
