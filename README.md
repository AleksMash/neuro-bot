# Описание

Это тренировочный проект по созданию ботов в Telegram и VK, взаимодействующих с сервисом [DialogFlow](https://cloud.google.com/dialogflow/docs/) от Google.  Сервис настроен отвечать на слова приветствия и реагировать на пожелание типа "хочу работать в вашей компании". В случае ошибок в коде ботов информация о них будет направлена диалог телеграм-бота с пользователем, chat_id которого указан в файле с переменными окружения (см. ниже).

Работающий пример можно "пощупать" написав телеграмм-боту [@MashukovBot](https://t.me/MashukovBot) а также в группу [ВКонтакте](https://vk.com/club218862065)  Попробуйте обоим написать "Привет"  и "хочу работать" (либо аналогичные фразы). Если покажется что боты (один или оба) в нерабочем состоянии, но все равно захочется посмотреть - просто напишите мне в [Телеграм](https://t.me/AVMSeven)

# Как установить и настроить

1. Клонируйте репозиторий
2. Установите необходимые библиотеки `pip install -r requirements.txt`
3. В корневом каталоге проекта создайте файл `.env` со следующим содержимым

```  
GOOGLE_APPLICATION_CREDENTIALS=<путь к файлу учетных данных приложения DialogFlow>  
DF_PROJECT_ID=<ID проекта в Google Cloud>  
TG_TOKEN=<токен телеграм-бота>  
TG_BOT_OWNER_CHAT_ID=<ID чата с ботом того пользователя, которому будут отправляться логи>  
VK_BOT_TOKEN=<токен бота ВКонтакте>
```

## Обучение ботов новым знаниям )

Скрипт `create_intent.py` позволяет научить облачный сервис DialogFlow новым "знаниям" - то есть натренировать на новые вопросы и соответствующие им ответы. 

Чтобы это сделать подготовьте `*.json`  файл с  вопросами и ответами (пример см. в каталоге data). 

Запустите скрипт:

```python
python create_intent.py --file <путь к *.json файлу>
```

После выполнения срипта будет выполнено обучение DialogFlow и боты смогут реагировать на новые вопросы.