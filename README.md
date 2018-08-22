ticket info service

## 1.3.0 - 2018-07-30 by 李帅
* [Features]
  1. 新增BDFZ_F,BDIJ_F,BDTK_F

* [Bugfixed]
  1. 无

* [Configuration]
  1. 无

## 1.2.1 - 2018-07-26 by 李帅
* [Features]
  1. 无

* [Bugfixed]
  1. 修复9c名字匹配存在的问题

* [Configuration]
  1. 无

## 1.2.0 - 2018-07-26 by 李帅
* [Features]
  1. it和9c增加超时配置
  2. it添加重复请求机制

* [Bugfixed]
  1. 修复9c名字匹配存在的问题

* [Configuration]
  1. ticket_info 新增如下配置:
  ```
  [proxy]
  dynamicProxy=H8108Y0J000R27SD:ECB9ED7FDC5C8CFE@http-dyn.abuyun.com:9020
  [it]
  timeout=10
  req_count=3
  [spring]
  timeout=10
    ```

## 1.0.1 - 2018-07-24 by 李帅
* [Features]
  1. 无

* [Bugfixed]
  1.修复9C返回参数不正确
  2.修复IT根据lastname不能够正确匹配的问题
  3.修复日志编码

* [Configuration]
  1. 无

# Release Note

# API

## url

- http://ip:port/lcc/ticket/info

## Request
```
{
  "pnr": "FBSFSS",
  "adultNumber": "1",
  "adultPrice": 490,
  "adultTax": 144,
  "childNumber": "0",
  "childPrice": 0,
  "childTax": 0,
  "ds": "9C_F",
  "ipcc": "9C_F",
  "flightOption": "oneWay",   //单程（oneWay）和往返(roundTrip)
  "startTime": "2018-06-06",
  "endTime": "",
  "toCity": "HKG",
  "fromCity": "SHA",
  "creditCardInfo":{
    "cardNumber":"6226 8988 8888 8888",
    "cvv":"123",
    "name":"CHINA EASYTRAVEL",
    "validityPeriod":"02/2021"
  },
  "fromSegments": [
    {
      "arrAirport": "HKG",
      "arrTime": "2017-06-06 12:20:00",
      "cabin": "Q",
      "carrier": "LX",
      "codeShare": false,
      "depAirport": "SHA",
      "depTime": "2018-06-06 09:20:00",
      "flightNumber": "9C8921",
      "marriageGrp": "",
      "stopAirports": "",
      "stopCities": ""
    }
  ],
  "retSegments": [],
  "passengers": [
    {
      "ageType": 0,
      "birthday": "1992-05-28",
      "cardExpired": "2031-06-06",
      "cardIssuePlace": "CN",
      "cardNum": "E12345678",
      "cardType": "PP",
      "firstName": "JINGYI",
      "gender": "F",
      "lastName": "TIAN",
      "name": "TIAN/JINGYI",
      "nationality": "CN",
      "ticketNum": "ticketNum"
    }
  ]
}

```
## Respone
```
{   "status": 0 // 0, 成功。other，错误码
    "message": "success", // error message
    "passengers" [
        {
            
            "ticketStatus": "checked" // "checked" 已经乘坐，"open" 未乘坐 
            "ageType": 0,
            "birthday": "1992-05-28",
            "cardExpired": "2031-06-06",
            "cardIssuePlace": "CN",
            "cardNum": "E12345678",
            "cardType": "PP",
            "firstName": "JINGYI",
            "gender": "F",
            "lastName": "TIAN",
            "name": "TIAN/JINGYI",
            "nationality": "CN",
            "ticketNum": "ticketNum"
        }
    ]
    
}
```
- error code

status | message | description
-------|---------|--------------
1 | Invalid request parameters! | 请求参数错误
2 | passenger info error | 乘客信息错误
3 | not found ipcc | 非法ipcc
4 | request the failure of the official network | 请求官网接口失败

