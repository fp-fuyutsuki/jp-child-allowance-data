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
python -m pip install -e ".[dev]"
```

## 推奨する検証順序

CSVがauthoritative sourceであり、JSONは `scripts/build_json.py` から生成する派生データです。JSONを直接編集せず、次の順序で検証してください。JSONはLF改行で決定的に生成されます。

```bash
python scripts/validate_data.py
python scripts/build_json.py
python scripts/validate_data.py
python -m pytest
```

生成されたJSONの変更もPull Requestまたはcommitの対象に含めてください。

生成されたJSONをstagingした後、またはcommit済みのcleanなworking treeで、次を実行して未反映の生成差分がないことを確認します。

```bash
python scripts/build_json.py
git diff --exit-code -- jp_child_allowance_data/data/json
```

## 検証対象

検証スクリプトは、主に以下のCSVファイルを対象にします。

```text
jp_child_allowance_data/data/csv/allowance_rules.csv
jp_child_allowance_data/data/csv/payment_schedule.csv
jp_child_allowance_data/data/csv/reform_history.csv
jp_child_allowance_data/data/csv/sources.csv
jp_child_allowance_data/data/csv/schema.csv
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
python -m pip install -e ".[dev]"
```

#### Recommended validation sequence

CSV is the authoritative source. Generate JSON with `scripts/build_json.py` rather than editing JSON directly. JSON generation is deterministic and uses LF line endings.

```bash
python scripts/validate_data.py
python scripts/build_json.py
python scripts/validate_data.py
python -m pytest
```

Include the generated JSON changes in the pull request or commit.

After staging the generated JSON, or from a clean working tree containing the committed JSON, run the following commands to confirm that no generated changes remain:

```bash
python scripts/build_json.py
git diff --exit-code -- jp_child_allowance_data/data/json
```

#### Validation coverage

The validation checks:

- required columns for each CSV file
- date, integer, and boolean value formats
- valid payment-month ranges
- `source_id` references against `sources.csv`
- basic consistency of age and child-order ranges

The validator checks structural and basic semantic consistency. It does not replace verification against the official policy sources.
