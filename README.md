# cdk.sh用のイメージビルド

```bash
make prepare
```

# デプロイ

引数として指定するコンテキスト

```
-c stage={stage_name} : ステージ名を指定します
-c line={line_name} : ライン名を指定します。
```

```bash
# デプロイできるスタック一覧
./cdk.sh list -c stage=dev -c line=line1

# cfn出力
./cdk.sh synth -c stage=dev -c line=line1 mido-sampleLine-dev-line1

# デプロイ
./cdk.sh deploy -c stage=dev -c line=line1 mido-sampleLine-dev-line1

# 削除
./cdk.sh destroy -c stage=dev -c line=line1 mido-sampleLine-dev-line1
```