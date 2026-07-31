# Contribution Guide

## 歓迎する貢献

- 公式出典に基づくデータ修正
- 制度改正履歴の追加
- CSV / JSON スキーマの改善
- テストケースの追加
- ドキュメント改善
- Python API の軽微な改善

## 貢献のスコープ

このリポジトリは、児童手当制度データの正確性、再利用性、検証可能性を高めるための貢献を受け付けます。

提案する変更が本リポジトリのスコープに合うか迷う場合は、Issue で背景と利用目的を説明してください。

## Pull Request の条件

- 公式または信頼できる出典を `sources.csv` に追加すること
- データ変更時はテストを追加または更新すること
- `python scripts/validate_data.py` が通ること
- `pytest` が通ること

## `reform_history.csv` のテスト用データを追加する方法

`reform_history.csv` に関する検証テストは、`tests/test_validation.py` に追加します。

テストでは、リポジトリ内の実データを直接変更せず、`_copy_csv_dir` を使って一時ディレクトリにCSVファイルをコピーしてください。

以下は、正常な制度改正履歴を1行追加し、検証が成功することを確認する例です。

```python
def test_validate_new_reform_history_row_passes(tmp_path: Path):
    csv_dir = _copy_csv_dir(tmp_path)
    target = csv_dir / "reform_history.csv"

    with target.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    rows.append(
        {
            "effective_date": "2026-04-01",
            "title": "Example reform",
            "summary": "Example test fixture",
            "source_id": rows[0]["source_id"],
        }
    )

    _rewrite_csv(target, fieldnames=fieldnames, rows=rows)

    validate_csv_dir(csv_dir)
```

関連するテストだけを実行する場合は、リポジトリ直下で次を実行します。

```bash
python -m pytest tests/test_validation.py -q
```

テスト用データを追加するときは、次の点を守ってください。

- リポジトリ内の実際のCSVデータを直接変更しない
- `_copy_csv_dir` で作成した一時ディレクトリ内のCSVを変更する
- CSVの書き戻しには `_rewrite_csv` を使用する
- 正常系と異常系のどちらを確認するテストか、テスト名から分かるようにする
- 実行時のAPI動作や制度データの値を変更しない
