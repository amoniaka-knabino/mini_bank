### Документация

запуск: `docker-compose up --build`

Все взаимодействие через json (POST методы ожидают json, все методы возвращают json)

#### Реализованы методы api:

1. `POST /api/status` покажет информацию о пользователе с `uuid == $uuid`
    
    Формат тела:
    `{"addition":{"uuid": $uuid}}`

2. `GET /api/ping` вернет `{"status":200}` если все ОК

3. `GET /api/subs` - вернет `[{ user1_info }, { user2_info }]`

4. `POST /api/add` - добавить пользователю с `uuid == $uuid` `$sum` условных единиц на счет

    Формат тела:
    `{"addition":{"uuid": $uuid, "sum":$sum}}`

5. `POST /api/substract` - вычесть у пользователя с `uuid == $uuid` `$sum` условных единиц

    Формат тела:
    `{"addition":{"uuid": $uuid, "sum":$sum}}`

6. `GET /api/refresh` - очищает базу данных

7. `POST /api/load_db` - загружает базу данных из json

    Формат тела `[{ user1_info }, { user2_info }]`

#### общий формат ответа:

```
{
“status“ = <http_status>,
“result“: <bool:operation_status>,
“addition“: {},
“description“: {}
}
```

#### формат `{ user_info }`
```
{"uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "name": "Петров Иван Сергеевич", "balance":1700,"hold":300, "status":"True"}
```
P.S. status == True (в бд == 1) => счет открыт

### TODO
#### deploy details
done
#### code
1. закрытие соединения после запроса и открытие при запросе (`*` менеджер контекста)
2. исключения на отрицательную sum
3. `*` проверка json в отдельной функции
4. subs и load_db к общему формату
5. `*` отдельная функция формирования ответа на основе исключений
6. исправить опечатку в subtract
7. проверить завершение потоков
