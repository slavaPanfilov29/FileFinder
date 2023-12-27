FileFinder - приложение для поиска файлов на компьютере по частям их текста или названия.


УСТАНОВКА

Установить pyinstaller с помощью команды:

pip install pyinstaller

Перейти в директорию, где находится программа с помощью команды:

cd yourPathHere

Сконвертировать .py файл в .exe с помощью команды:

python -m PyInstaller --onefile main.py

Рабочий .exe файл будет находиться в указанной директории в папке dist. Необходимо скопировать ag.exe к конечному .exe файлу.


ИСПОЛЬЗОВАНИЕ

1. Необходимо выбрать директорию для начала поиска;
   
2. В поле "Искомый текст" ввести текст для поиска;

3. Поиск в названии файла и учёт регистра осуществляется за счёт включения
соответствующих пунктов;

5. Расширение файла выбирается в соответствующем выпадающем списке;
   
6. После нажатия кнопки "Найти" появляются результаты поиска: в поле справа появятся найденные фрагменты текста, а чуть выше - возможность выбрать файл среди наёденных. 


КОМАНДА ПРОЕКТА

Влад Тесленков - front-end разработка

Василий Поливаев - fullstack разработка

Вячеслав Панфилов - back-end разработка

Дарья Ромаченко - front-end разработка
