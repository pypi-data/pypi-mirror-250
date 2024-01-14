Download China A stock market using Tushare API

# Installation

---

```bash
pip install TushareDownloader
```


---
## Full documents

https://bagelquant.com/tusharedownloader

## First time use

**The package requires a database connection, please refer to:**

https://bagelquant.com/tusharedownloader/


Download operation will:

1. download data from Tushare
2. delete local data in the database (set delete_flag = 1)
3. insert new data

```python
# download data - stock_list
from TushareDownloader import download_stock_list

download_stock_list()
```

Update operations

update operation will:

1. query `latest_trade_date` in the local database
2. download data from `latest_trade_date` to `today`
3. append data to local database

```python
# update data stock_daily
from TushareDownloader import update_stock_daily

update_stock_daily()
```