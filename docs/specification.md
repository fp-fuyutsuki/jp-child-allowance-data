# jp-child-allowance-data 仕様書

## 1. プロジェクト概要

`jp-child-allowance-data` は、日本の児童手当制度に関する制度情報を、機械可読な CSV / JSON と軽量な Python API で提供する OSS です。

目的は、児童手当制度の公開情報を、開発者・教育者・データ利用者が再利用しやすい形式で整備することです。

## 2. スコープ

このプロジェクトで扱う範囲は以下です。

- 年齢区分
- 子の順序別の支給額
- 支給月
- 制度改正履歴
- 所得制限の有無・変更履歴
- 出典 URL
- CSV データ
- JSON データ
- 軽量な Python API
- テストコード
- README
- 変更履歴

## 3. 想定ユーザー

- 個人開発者
- 教育者
- 行政制度を扱う教材制作者
- データ分析・Python 学習者
- 児童手当制度の公開データを参照したい利用者

## 4. データ仕様

### allowance_rules.csv

| column | description |
|---|---|
| effective_from | 制度適用開始日 |
| effective_to | 制度適用終了日。空欄は現行制度 |
| age_min | 対象年齢の下限 |
| age_max | 対象年齢の上限 |
| age_label | 人間向けの年齢区分ラベル |
| child_order_min | 子の順序の下限 |
| child_order_max | 子の順序の上限。空欄は上限なし |
| monthly_amount_yen | 月額支給額 |
| income_status | 所得区分 |
| income_limit_applicable | 所得制限の有無 |
| source_id | 出典 ID |
| notes | 補足 |

### payment_schedule.csv

| column | description |
|---|---|
| effective_from | 支給スケジュール適用開始日 |
| effective_to | 支給スケジュール適用終了日。空欄は現行制度 |
| payment_month | 支給月 |
| covered_months | 支給対象月 |
| source_id | 出典 ID |
| notes | 補足 |

### reform_history.csv

| column | description |
|---|---|
| effective_date | 改正適用日 |
| title | 改正タイトル |
| summary | 改正概要 |
| source_id | 出典 ID |

### sources.csv

| column | description |
|---|---|
| source_id | 出典 ID |
| title | 出典名 |
| publisher | 公表主体 |
| url | URL |
| accessed_date | 確認日 |
| notes | 補足 |

## 5. Python API 仕様

- `get_monthly_amount(age, child_order, date=None, income_status=None)`
- `get_annual_amount(age, child_order, date=None, income_status=None)`
- `get_payment_months(year, date=None)`
- `get_reform_history()`
- `load_rules()`
- `load_sources()`

## 6. API 設計方針

API は、児童手当制度データの読み込みと参照に限定します。

関数名・引数・戻り値は、制度情報の参照に必要な範囲で単純に保ちます。複数の制度領域を統合する高水準 API は、このリポジトリの設計対象に含めません。

## 7. ライセンス

Apache License 2.0 を採用します。

## 8. MVP の完成条件

- CSV データが存在する
- JSON データが生成される
- Python API で月額・年額・支給月を取得できる
- 出典が明記されている
- pytest で主要ケースを検証できる
- README に利用例がある
- GitHub Actions でテストが通る
- v0.1.0 としてリリース可能

## 9. 将来追加してよい範囲

- 制度改正への追随
- データ形式の改善
- 型ヒント
- CLI
- ドキュメント整備
- 英語 README
- PyPI 公開
