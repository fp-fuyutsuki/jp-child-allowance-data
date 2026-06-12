![Python tests](https://github.com/fp-fuyutsuki/jp-child-allowance-data/actions/workflows/test.yml/badge.svg)

# jp-child-allowance-data

日本の児童手当制度を、機械可読な CSV / JSON と軽量な Python API で提供する OSS です。

このリポジトリは、児童手当制度の金額、年齢区分、子の順序区分、支給月、制度改正履歴、出典メタデータを扱います。

## 背景

児童手当制度は、制度改正により支給対象、支給額、支給月、所得制限の扱いなどが変わることがあります。一方で、制度情報は人間向けのWebページや資料として提供されることが多く、プログラムから再利用しやすい形で参照・検証・更新するには追加の整理が必要です。

このリポジトリは、児童手当制度に関する公開情報を、出典を確認できる機械可読データとして整理し、継続的に保守しやすくすることを目的としています。

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
data/csv/schema.csv

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

## データ検証

CSVデータは、付属の検証スクリプトで確認できます。

```bash
python scripts/validate_data.py
```

この検証では、必須カラム、基本的な数値・日付・真偽値形式、`sources.csv` に対する `source_id` の参照関係を確認します。

## スコープ

この OSS のスコープは、児童手当制度の公開情報を再利用しやすい形式で整理し、データと軽量な参照 API として提供することです。

## License

Apache License 2.0

## English Summary

jp-child-allowance-data provides machine-readable CSV/JSON data and a lightweight Python API for Japan's child allowance system.

The project focuses on public policy data that can be referenced, validated, and maintained over time. It includes allowance rules, payment schedules, reform history, and source metadata.
