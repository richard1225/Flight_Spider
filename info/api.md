## 南航
廉价机票QueryUrl: https://b2c.csair.com/portal/minPrice/queryMinPriceInAirLines?jsoncallback=getMinPrice&inter=N&callback=getMinPrice&_=1534227944338

> timestamp 临时生成一个就ok

返回`Example1`
```
... // 若干出发地
{
    "DEPCTIYNAME_EN": "Shenzhen",
    "FLIGHT": [
        ..., // 若干目的地
        {
            "MINPRICE": "560",
            "money": "RMB",
            "RETURNDATE": null,
            "ARRCTIYNAME_ZH": "杭州",
            "DEPDATE": "2018-09-23",
            "SEGTYPE": "S",
            "ARRCITY": "HGH",
            "ARRCTIYNAME_EN": "Hangzhou"
        },
        ..., // 若干目的地
    ],
    "DEPCITY": "SZX",
    "DEPCTIYNAME_ZH": "深圳",
    "REGION_CODE": "HN",
    "REGION": "华南"
},
... // 若干出发地

```

机票详情查询: 

* url: https://b2c.csair.com/B2C40/newTrips/static/main/page/booking/index.html?t=S&c1=SZX&c2=HGH&d1=2018-09-23&at=1&ct=0&it=0
> `t1` 为 `FLIGHT` 数组中的 `SEGTYPE`;  
`c1` 为 `DEPCITY`;  
`c2` 为对应的 `ARRCITY`;  
`d1` 为 `DEPDATE`; 
`at`, `ct`, `it`, 分别对应成人, 小孩, 婴儿的票数, 默认1, 0, 0就ok
