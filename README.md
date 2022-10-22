# SuperMacro
### Система макросов, использующая macroLang

# Как использовать
### 1. Загрузить последнюю версию
### 2. Создать файл с любым именем и расширением
### 3. Записать в него код

# Пример кода
```macroLang
hotkey f1
click i
press h
release h
type 10 Привет ребята!
```

# Документация
```macroLang
press <button> - зажимает кнопку <button>
release <button> - отпускает кнопку <button>
click <button> - нажимает и отпускает кнопку <button>
delay <ms> - задержка в <ms> миллисекунд
type <ms> <text> - напечатать текст <text> с задержкой <ms>
hotkey <button> - забиндить макрос на клавишу <button> (ОБЯЗАТЕЛЬНО В НАЧАЛЕ МАКРОСА)
```

# CLI аргументы
```bash
-script <path> - запустить макрос из файла <path>
-debug - включить режим отладки
```
