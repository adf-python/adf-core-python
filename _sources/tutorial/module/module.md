# モジュールについて

## モジュールの指定方法

モジュールを指定するには、module.yamlにモジュールの名前とパスを記述します。

例えば、以下のように記述します：

```yaml
SampleSearch:
    PathPlanning: src.<your_team_name>.module.complex.sample_search.SampleSearch
    Clustering: src.<your_team_name>.module.complex.sample_search.SampleClustering
```

この場合、`SampleSearch` というモジュールで使用される、`PathPlanning` と `Clustering` というモジュールを指定しています。

## モジュールの読み込み方法

モジュール内で、他のモジュールを読み込む場合は、次のように記述します：

```python
from adf_core_python.core.agent.module.module_manager import ModuleManager

class SampleSearch(Search):
    def __init__(
        self,
        agent_info: AgentInfo,
        world_info: WorldInfo,
        scenario_info: ScenarioInfo,
        module_manager: ModuleManager,
        develop_data: DevelopData,
    ) -> None:
        super().__init__(
            agent_info, world_info, scenario_info, module_manager, develop_data
        )

        # クラスタリングモジュールの取得
        self._clustering: Clustering = cast(
            # モジュールの型を指定
            Clustering,
            # モジュールの取得
            module_manager.get_module(
                # モジュールの名前
                "DefaultSearch.Clustering",
                # 上記のモジュールの名前が指定されていない場合のデフォルトのモジュールのパス
                "adf_core_python.implement.module.algorithm.k_means_clustering.KMeansClustering",
            ),
        )

        # パスプランニングモジュールの取得
        self._path_planning: PathPlanning = cast(
            # モジュールの型を指定
            PathPlanning,
            # モジュールの取得
            module_manager.get_module(
                # モジュールの名前
                "DefaultSearch.PathPlanning",
                # 上記のモジュールの名前が指定されていない場合のデフォルトのモジュールのパス
                "adf_core_python.implement.module.algorithm.a_star_path_planning.AStarPathPlanning",
            ),
        )

        # モジュールの登録(これをしないと、モジュール内のシミュレーション環境の情報が更新されません)
        self.register_sub_module(self._clustering)
        self.register_sub_module(self._path_planning)
```

## モジュールの種類について

adf-core-pythonでは、以下のモジュールが提供されています。

| クラス               | 役割                                                                       |
| -------------------- | -------------------------------------------------------------------------- |
| TacticsFireBrigade   | 消防隊用のモジュール呼び出し (競技では変更不可)                            |
| TacticsPoliceForce   | 土木隊用のモジュール呼び出し (競技では変更不可)                            |
| TacticsAmbulanceTeam | 救急隊用のモジュール呼び出し (競技では変更不可)                            |
| BuildingDetector     | 消防隊の活動対象の選択                                                     |
| RoadDetector         | 土木隊の活動対象の選択                                                     |
| HumanDetector        | 救急隊の活動対象の選択                                                     |
| Search               | 情報探索に向けた活動対象の選択                                             |
| PathPlanning         | 経路探索                                                                   |
| DynamicClustering    | シミュレーションの進行によってクラスタが変化するクラスタリング             |
| StaticClustering     | シミュレーション開始時にクラスタが定まるクラスタリング                     |
| ExtAction            | 活動対象決定後のエージェントの動作決定                                     |
| MessageCoordinator   | 通信でメッセージ(情報)を送信する経路である、チャンネルへのメッセージの分配 |
| ChannelSubscriber    | 通信によってメッセージを受け取るチャンネルの選択                           |

自分で上記の役割以外のモジュールを作成する際は、`AbstractModule` を継承してください。
