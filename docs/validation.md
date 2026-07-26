# データ検証

このドキュメントでは、`jp-child-allowance-data` のCSVデータ検証方法を説明します。

## 目的

このリポジトリでは、児童手当制度に関する公開情報をCSV / JSONとして提供しています。データを継続的に保守するためには、CSVファイルの構造、値の形式、出典IDの参照関係を確認できることが重要です。

検証スクリプトは、データ更新やリリース前に基本的な不整合を検出するために使用します。

## 実行方法

リポジトリ直下で以下を実行します。

```bash
python scripts/validate_data.py
```

開発環境でパッケージをインストールしていない場合は、先に以下を実行します。

```bash
pip install -e .
```

## 検証対象

検証スクリプトは、主に以下のCSVファイルを対象にします。

```text
data/csv/allowance_rules.csv
data/csv/payment_schedule.csv
data/csv/reform_history.csv
data/csv/sources.csv
data/csv/schema.csv
```

## 検証内容

検証では、以下を確認します。

- 必須カラムが存在すること
- 日付が `YYYY-MM-DD` 形式であること
- 数値項目が整数として解釈できること
- 真偽値項目が `true` / `false` として表現されていること
- 支給月や対象月が1〜12の範囲にあること
- `source_id` が `sources.csv` に存在すること
- 年齢区分や子の順序区分に明らかな逆転がないこと

## 利用タイミング

以下のタイミングで実行することを想定しています。

- CSVデータを更新した後
- JSONデータを再生成する前
- Pull Requestをレビューするとき
- Releaseを作成する前

## 注意事項

この検証は、CSVファイルの基本的な構造と形式を確認するためのものです。制度解釈や行政手続き上の正確性を保証するものではありません。制度内容の確認には、出典として記載している公式情報を参照してください。

---

## English

### CSV Validation

This section explains how to validate the CSV data included in `jp-child-allowance-data`.

#### Running validation

Run the following command from the repository root:

```bash
python scripts/validate_data.py
```

If the package is not installed in the development environment, run:

```bash
pip install -e .
```

#### Validation coverage

The validation checks:

- required columns for each CSV file
- date, integer, and boolean value formats
- valid payment-month ranges
- `source_id` references against `sources.csv`
- basic consistency of age and child-order ranges

The validator checks structural and basic semantic consistency. It does not replace verification against the official policy sources.
