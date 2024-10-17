# API Document
## testing (with coverage report)
run this in ./backend/
`pytest --collect-only tests/ --cov-report html:coverage.html --cov=./`
## Summary
- login
- POS Page
    - get menu
    - view order
    - add order
    - finish order
    - check if the worker has paid
- main page (for worker)
    - get metadata of all restaurant
    - get info of a single restaurant
    - get history order
    - add review
- admin
    - add dish / upload dish picture
    - upload cover picture of a restaurant
    - get monthly report data
    - get monthly payment report data
    - notify unpaid user
    - get all menu
    - update menu
    - add restaurant
## login
> done
- endpoint: `/login`
- method: POST
- 在提醒日期前或者已結清 -> notify = false
- request body
    ```
    {
        user_account: "",
        user_password: ""
    }
    ```
- response
    ```
    {
        "outh_token": "",
        "user_identity": "restaurant|worker|admin",
        "restaurant_id": "", // returned only when user_identity is restaurant 
        "notify": true|false
    }
    ```

## POS page (for restaurant)
### get menu
> done
- endpoint: `/pos/menu`
- method: GET
- response
```
{
    "meals": 
    [
        {
            "dish_id": 1,
            "name": "Fried Chicken",
            "description": "Delicious",
            "combo": 0,
            "price": 200,
            "rating": 4.5,
            "order_times": 0,
            "picture": "/static/dish/chicken.png",
            "available": 1
        },
        {
            "dish_id": 2,
            "name": "Hamburger",
            "description": "Delicious",
            "combo": 0,
            "price": 150,
            "rating": 4.5,
            "order_times": 0,
            "picture": "/static/dish/chicken.png",
            "available": 1
        }
    ]
}
```
### view order
> done
- endpoint: `/pos/get_order`
- only return today's order?
- method: GET
- response
```
{
    "orders": 
    [
        {
            "order_id": ,
            "customer_id": ,
            "customer_name": ,
            "price": ,
            "order_time": "YYYY-MM-DD HH:MM:SS",
            "finish": ,
            "dishes":
            [
                {
                    "dish_id": ,
                    "number": ,
                    "dish_name": ,
                    "picture": ,
                    "number": ,
                    "price": 
                },
            ]
        },
    ]
}
```
### add order
> done
- endpoint: `/pos/add_order`
- method: POST
- request body
```
{
    "customer_id": ,
    "total_price": ,
    "dishes": 
    [
        "dish_id": ,
        "number": 
    ]
}
```
- response
```
{
    "status": "success|error",
    "error": "error_msg" // if status is error
    "order_id": // if status is success
}
```
### finish order
> done
- endpoint: `/pos/finish/<order-id>`
- method: POST
- response
```
{
    "status": "success|error",
    "error": "error_msg" // if status is error
}
```
### get customer name
> done
- endpoint: `/pos/worker_info/<id>`
- method: GET
- response
```
{
    "id": ,
    "name": ,
    "phone": 
}
```
### check if the worker has paid
- endpoint: `/pos/paid/<customer_id>`
- method: GET
- response
```
{
    "customer_id": ,
    "paid": true|false
}
```

## main page (for worker)
### get list of restaurants
> done
- endpoint: `/main/restaurant_list`
- method: GET
- response
```
{
    "restaurants":
    [
        {
            "id": ,
            "restaurant": ,
            "rating": ,
            "picture": 
        },
    ]
}
```
### get information of single restaurant
> done
- endpoint: `/main/restaurant/<id>`
- method: GET
- response example
    ```
    {
        "id": 1,
        "restaurant": "KFC",
        "phone": 0912345678,
        "picture": "/static/cover/kfc.png",
        "description": "Fast Food Restaurant",
        "rating": 4.3,
        "open_time": "12:00:00",
        "close_time": "22:00:00",
        "meals": 
        [
            {
                "dish_id": 1,
                "name": "Fried Chicken",
                "description": "Delicious",
                "combo": 0,
                "price": 200,
                "rating": 4.5,
                "order_times": 0,
                "picture": "/static/dish/chicken.png"
            },
            {
                "dish_id": 2,
                "name": "Hamburger",
                "description": "Delicious",
                "combo": 0,
                "price": 150,
                "rating": 4.5,
                "order_times": 0,
                "picture": "/static/dish/chicken.png"
            }
        ]
    }
    ```

### get history order
> done
- endpoint: `/main/history`
- method: GET
- only select the order of current month
- if the order hasn't been reviewed, set all rating to -1
- response
```
{
    "orders":
    [
        {
            "order_id": ,
            "order_time": "YYYY-MM-DD HH:MM:SS",
            "restaurant_id": ,
            "total_price": ,
            "finished": ,
            "reviewed": 1|0,
            "overall_rating": ,
            "dishes": 
            [
                {
                    "dish_id": ,
                    "dish_name": ,
                    "picture": ,
                    "number": ,
                    "price": ,
                    "rating": ,
                }
            ]
        }
    ]
}
```
### add review
> done
- endpoint: `/main/add_review`
- method: POST
- request body
```
{
    "order_id": ,
    "overall_rating": , // 1 to 5
    "dishes_rating": 
    [
        {
            "dish_id": ,
            "rating": 
        }, 
        {
            "dish_id": ,
            "rating": 
        }
    ]
}
```
- response
```
{
    "status": "success|error",
    "error": "error_msg" // if status is error
}
```
## admin page
### add dish
> done
- endpoint: `/admin/add_dish`
- method: POST
- request body
```
{
    "restaurant_id": ,
    "name": ,
    "description": ,
    "combo": ,
    "picture_filename": , // upload picture first to get filename
    "price":
}
```
- response
```
{
    "status": "success|fail", 
    "error": // if status is fail
}
```

### upload picture of a dish
> done
- endpoint: `/admin/upload/dish`
- method: `POST`
- 看起來需要 `<input name='image'>` 才收的到 (name 要和後端收的 key 一樣)
- 這個應該一定得用表單上傳，方便的話順便送個 restaurant id (不行的話再看看可以怎麼做)
- accept file extension: png, jpg, jpeg
- response
```
{
    "status": "success|fail",
    "filename": "", // if status is success
    "error": "error msg" // if status is fail
}
```
### upload cover picture of the restaurant
> done
- endpoint: `/admin/upload/cover`
- method: `POST`
- 看起來需要 `<input name='image'>` 才收的到 (name 要和後端收的 key 一樣)
- 這個應該一定得用表單上傳，方便的話順便送個 restaurant id (不行的話再看看可以怎麼做)
- accept file extension: png, jpg, jpeg
- response
```
{
    "status": "success|fail",
    "filename": ""
}
```
### get monthly report
> done
- endpoint: `/admin/monthly_report`
- method: `POST`
- you can only request a monthly report after the whole month ends
- request: 
```
{
    "year": ,
    "month": 
}
```
- response: automatically download the csv file

### get monthly payment report
> done
- endpoint: `/admin/monthly_payment_report`
- method: `POST`
- you can only request a monthly report after the whole month ends
- request: 
```
{
    "year": ,
    "month": 
}
```
- response: automatically download the csv file

### notify unpaid user
> done
> how? To be discussed
- set a flag in login api

### get menus of all restaurant
> done
- endpoint: `/admin/get_menus`
- method: GET
- response
```
{
    "restaurants": 
    [
        {
            "restaurant_id": , 
            "restaurant_name": ,
            "phone": ,
            "open_time": "HH:MM",
            "close_time": "HH:MM",
            "overall_rating": ,
            "dishes": 
            [
                {
                    "dish_id": ,
                    "dish_name": ,
                    "combo": ,
                    "price": ,
                    "available": true|false,
                    "ordered_times": ,
                    "rating": 
                }
            ]
        }, 
    ]
}
```

### update price
> done
- endpoint: `/admin/update_price`
- method: POST
- request
```
{
    "dish_id": ,
    "updated_price": 
}
```
- response
```
{
    "status": "success|fail",
    "error": "error_msg" // if status is fail
}
```

### update menu
> done
- endpoint: `/admin/update_menu`
- method: POST
- 所有在 available dish id 裡的餐點裡都會變 availabe，其他的都變 unavailable
- request
```
{
    "available_dish_id":
    [

    ]
}
```
- response
```
{
    "status": "success|fail",
    "error": "error msg" // if status is fail
}
```

### add restaurant
> done
- endpoint: `/admin/add_restaurant`
- method: POST
- request
```
{
    "restaurant_name": ,
    "phone": ,
    "open_time": "HH:MM",
    "close_time": "HH:MM",
    "description": 
}
```
- response
```
{
    "status": "success|fail",
    "restaurant_id": , // if status is success
    "error": "error msg" // if status is fail
}
```