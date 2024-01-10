# Sahm OpenAPI-Python
-------------------
###### current：V1.0.0

### Install
```
for linux/macos
$>./local_install_build.sh

for windwos
$>python setup.py sdist bdist_wheel
$>cd dist
$>pip install py-sahm-openapi-1.x.x.tar.gz
###### Note: This API supports Python3.7+ 

###### Usage frot stock trade####
start interactive python programme
$>python

import stock trade test module 
>>> from hs.examples import stock_trade_demo

start test
>>>stock_trade_demo.start_trade_test(login_mobile='13662311971', login_passwd='Aa123456@', trading_passwd='123456')

import quote trade test module
>>>from hs.examples import stock_quote_demo

start test
>>>stock_quote_demo.start_quote_test(login_mobile='13662311971', login_passwd='Aa123456@')

### Api Document
access document：https://quant-open.hstong.com/api-docs/


### Change History
V1.0.5（2023-09-08） Increase and improve OpenAPI for transaction and quotation interface.
V1.0.6（2024-01-09） Added online test entrance for market conditions and transactions.