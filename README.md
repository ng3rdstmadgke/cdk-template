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
./cdk.sh synth -c stage=dev -c line=line1 cdktpl-sampleLine-dev-line1

# デプロイ
./cdk.sh deploy -c stage=dev -c line=line1 cdktpl-sampleLine-dev-line1

# 削除
./cdk.sh destroy -c stage=dev -c line=line1 cdktpl-sampleLine-dev-line1
```

# プロジェクト構成

- cdk_template
  - context  
  `Context` `ContextLoader` の実装ディレクトリです
    - context_loader_base.py  
    `Context` `ContextLoader` が継承すべき基底クラスが定義されています。
  - stack  
  `Stack` の実装ディレクトリです
    - stack_base.py  
    `Stack` が継承すべき基底クラスが定義されています。
- docker  
CDKを実行するためのdockerイメージの定義が格納されています
- tests  
単体テスト
- .cdk_version  
node.jsとpythonでcdkのバージョンを一致させるためのバージョン定義ファイルです。  
このファイルは `docker/Dockerfile` , `setup.py` にてcdkのバージョン指定に利用されています。
- app.py  
CDKのエントリーポイントです
- cdk.json  
CDKの変数定義ファイルです。  
`context.default` にはデフォルトの設定値を定義します。  
`context.overwrite` にはstage, lineレイヤで上書きするための設定を記述します。
- Makefile  
cdkのdockerイメージをビルドするためのコマンドです
- setup.py  
依存パッケージが定義されています。`.cdk_version` ファイルを読み込んでインストールするcdkバージョンを決定しています。





# 新しいスタックの追加

```bash
touch cdk_template/context/{stack_name}_context.py
touch cdk_template/stack/{stack_name}_stack.py
```

## コンテキストの実装

`cdk_template/context/{stack_name}_context.py` ではスタックにcdk.jsonの情報を渡すための `Context` と `cdk.json` の内容をロードするための `ContextLoader` を実装します。

### `Context` クラス

`Context` オブジェクトは `StageContextBase` もしくは `LineContextBase` を継承したイミュータブルなオブジェクトとして定義します。  
`Context` オブジェクトは `Stack` から `cdk.json` への依存を明確化する役割を持つため、 利用する値のみをメンバとして持ちます。

```cdk_template/context/sample_stage_context.py
from dataclasses import dataclass
from cdk_template.context.context_loader_base import (
    StageContextBase,
    StageContextLoaderBase
)


@dataclass(frozen=True)
class SampleStageContext(StageContextBase):
    sample_stage_param: str
```

### `ContextLoader` クラス

`ContextLoader` は `Context` を生成するためのクラスで、 `StageContextLoaderBase` もしくは `LineContextLoader` 継承して実装します。
`ContextLoader` は `cdk.json` を指定の `stage` や `line` のパラメータで上書きし、利用する値のみを取得して `Context` オブジェクトを生成します。  
`ContextLoader` には `cdk.json` で利用する項目名を静的メンバとして定義します。

```cdk_template/context/sample_stage_context.py
from cdk_template.context.context_loader_base import (
    StageContextBase,
    StageContextLoaderBase
)

class SampleStageContextLoader(StageContextLoaderBase):
    KEY_CONTEXT_SAMPLE_STAGE_PARAM = "sample_stage_param"  # cdk.jsonで利用する項目を静的メンバとして定義

    def load(self) -> SampleStageContext:
        return SampleStageContext(
            # ContextBase の引数
            aws_account_id=self.context_src[self.KEY_CONTEXT_AWS_ACCOUNT_ID],
            aws_region=self.context_src[self.KEY_CONTEXT_AWS_REGION],
            app_name=self.context_src[self.KEY_CONTEXT_APP_NAME],
            vpc_id=self.context_src[self.KEY_CONTEXT_VPC_ID],
            subnet_ids=self.context_src[self.KEY_CONTEXT_SUBNET_IDS],
            http_proxy=self.context_src[self.KEY_CONTEXT_HTTP_PROXY],
            https_proxy=self.context_src[self.KEY_CONTEXT_HTTPS_PROXY],
            no_proxy=self.context_src[self.KEY_CONTEXT_NO_PROXY],
            termination_protection=self.context_src[self.KEY_CONTEXT_TERMINATION_PROTECTION],
            tags=self.context_src[self.KEY_CONTEXT_TAGS],
            # StageContextBase の引数
            stage=self.stage,
            # SampleStageContextLoader の引数
            sample_stage_param=self.context_src[self.KEY_CONTEXT_SAMPLE_STAGE_PARAM]
        )
```

## スタックの実装

`cdk_template/stack/{stack_name}_stack.py` では、awsのリソースを定義します。


### `Stack` クラス 

`Stack` クラスは `Context` を利用して、awsリソースを定義するクラスで、 `StageStackBase` もしくは `LineStackBase` を継承して実装します。  

`Stack` クラスには次のメソッド・プロパティを実装します

- `def _resources(self):` (必須)  
awsリソースを定義するメソッドです。
- `STACK_NAME` (必須)  
スタック名を定義する静的メンバです。


```cdk_template/stack/sample_stage_stack.py
from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from cdk_template.context.sample_stage_context import SampleStageContext
from cdk_template.stack.stack_base import (
    StageStackBase
)

class SampleStageStack(StageStackBase):
    STACK_NAME = "sampleStage"
    context: SampleStageContext

    def _resources(self):
        topic = sns.Topic(
            self, self._get_resource_id("sampleTopic"),
            topic_name=self._get_resource_name("sampleTopic")
        )

        topic.add_subscription(subs.EmailSubscription(
            self.context.sample_stage_param
        ))
```

## エントリーポイントにStackを実装

コンテキストとスタックの実装が終わったら、 `app.py` にスタックを追加します。

```app.py
from cdk_template.context.sample_stage_context import SampleStageContextLoader
from cdk_template.stack.sample_stage_stack import SampleStageStack

app = core.App()
default_context = app.node.try_get_context(KEY_CONTEXT_DEFAULT)
overwrite_context = app.node.try_get_context(KEY_CONTEXT_OVERWRITE)

stage = app.node.try_get_context(ARG_KEY_CONTEXT_STAGE)
if stage:
    # Contextオブジェクトを生成
    sample_stage_context = SampleStageContextLoader(
        default_context=default_context,
        overwrite_context=overwrite_context,
        stage=stage
    ).load()

    # Contextを引数にとってStackを作成
    SampleStageStack(app, sample_stage_context)
```