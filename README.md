![Python tests](https://github.com/fp-fuyutsuki/jp-child-allowance-data/actions/workflows/test.yml/badge.svg)

# jp-child-allowance-data

日本の児童手当制度を、機械可読な CSV / JSON と軽量な Python API で提供する OSS です。

このリポジトリは、児童手当制度の金額、年齢区分、子の順序区分、支給月、制度改正履歴、出典メタデータを扱います。

## 提供するもの

- 児童手当の月額支給額
- 年齢区分
- 第1子・第2子・第3子以降の区分
- 支給月
- 制度改正履歴
- 出典メタデータ
- CSV / JSON データ
- Python API

## インストール

開発中はリポジトリ直下で以下を実行してください。

```bash
pip install -e .
```

## 使い方

```python
from jp_child_allowance_data import get_monthly_amount, get_annual_amount

# 令和6年10月分以降: 3歳未満・第1子
get_monthly_amount(age=2, child_order=1, date="2026-06-01")
# 15000

# 令和6年10月分以降: 3歳未満・第3子以降
get_monthly_amount(age=2, child_order=3, date="2026-06-01")
# 30000

# 年額換算
get_annual_amount(age=2, child_order=1, date="2026-06-01")
# 180000
```

支給月を取得できます。

```python
from jp_child_allowance_data import get_payment_months

get_payment_months(2026, date="2026-06-01")
# [2, 4, 6, 8, 10, 12]
```

拡充前制度の特例給付も参照できます。

```python
from jp_child_allowance_data import get_monthly_amount

get_monthly_amount(
    age=8,
    child_order=1,
    date="2024-09-01",
    income_status="above_limit_below_cap",
)
# 5000
```

## データファイル

```text
data/csv/allowance_rules.csv
data/csv/payment_schedule.csv
data/csv/reform_history.csv
data/csv/sources.csv

data/json/allowance_rules.json
data/json/payment_schedule.json
data/json/reform_history.json
data/json/sources.json
```

## 注意事項

- 本リポジトリは制度データの参照用途を想定しています。
- 支給日は自治体等により異なるため、支給月のみを扱います。
- 年齢区分は軽量な参照用途として単純な `age_min` / `age_max` で表現しています。年度末基準の厳密判定が必要な場合は利用側で補正してください。
- 本リポジトリは法務・税務・行政手続きの代替ではありません。

## 開発

```bash
python scripts/validate_data.py
python scripts/build_json.py
pytest
```

## スコープ

この OSS のスコープは、児童手当制度の公開情報を再利用しやすい形式で整理し、データと軽量な参照 API として提供することです。

## License

Apache License 2.0
