### Документация

Все взаимодействие через json (POST методы ожидают json, все методы возвращают json)

##### Реализованы методы api:

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

##### общий формат ответа:

```
{
“status“ = <http_status>,
“result“: <bool:operation_status>,
“addition“: {},
“description“: {}
}
```

### TODO
#### deploy details
done
#### code
1. таймер на вычет холда
2. done
3. json на любое обращение к апишке через фласк
4. декоратор и исключение на невозможную операцию
5. `*`исключения на неправильную инициализацию
6. done
7. done
8. написать доку
9. постгрес в докер

#### questions
1. json в nginx???
2. result в ответе отвечает на вопрос была ли операция проведена успешно?
