# サーチモジュール

## サーチモジュールの概要

今回開発するモジュールは、`KMeansPPClustering` モジュールを用いた情報探索対象決定 (`Search`) モジュールです。 クラスタリングモジュールによってエージェント間で担当地域の分割をおこない、 担当地域内からランダムに探索対象として選択します。

## サーチモジュールの実装の準備

```{note}
以降の作業では、カレントディレクトリがプロジェクトのルートディレクトリであることを前提としています。
```

まず、サーチモジュールを記述するためのファイルを作成します。

```bash
touch src/<your_team_name>/module/complex/k_means_pp_search.py
```

次に、サーチモジュールの実装を行います。 以下のコードを `k_means_pp_search.py` に記述してください。
これが今回実装するサーチモジュールの雛形になります。

```python
import random
from typing import Optional, cast

from rcrs_core.entities.building import Building
from rcrs_core.entities.entity import Entity
from rcrs_core.entities.refuge import Refuge
from rcrs_core.worldmodel.entityID import EntityID

from adf_core_python.core.agent.develop.develop_data import DevelopData
from adf_core_python.core.agent.info.agent_info import AgentInfo
from adf_core_python.core.agent.info.scenario_info import ScenarioInfo
from adf_core_python.core.agent.info.world_info import WorldInfo
from adf_core_python.core.agent.module.module_manager import ModuleManager
from adf_core_python.core.component.module.algorithm.clustering import Clustering
from adf_core_python.core.component.module.complex.search import Search
from adf_core_python.core.logger.logger import get_agent_logger


class KMeansPPSearch(Search):
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
        self._result: Optional[EntityID] = None
        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )

    def calculate(self) -> Search:
        return self

    def get_target_entity_id(self) -> Optional[EntityID]:
        return self._result
```

## モジュールの登録

次に、作成したモジュールを登録します。
以下のように`config/module.yaml`の該当箇所を変更してください

```yaml
DefaultTacticsAmbulanceTeam:
  Search: src.<team-name>.module.complex.k_means_pp_search.KMeansPPSearch

DefaultTacticsFireBrigade:
  Search: src.<team-name>.module.complex.k_means_pp_search.KMeansPPSearch

DefaultTacticsPoliceForce:
  Search: src.<team-name>.module.complex.k_means_pp_search.KMeansPPSearch
```

## モジュールの実装

まず、`KMeansPPClustering` モジュールを呼び出せるようにします。

以下のコードを`config/module.yaml`に追記してください。

```yaml
KMeansPPSearch:
  Clustering: src.<team-name>.module.algorithm.k_means_pp_clustering.KMeansPPClustering
```

次に、`KMeansPPSearch` モジュールで `KMeansPPClustering` モジュールを呼び出せるようにします。

以下のコードを `k_means_pp_search.py` に追記してください。

```python
class KMeansPPSearch(Search):
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
        self._result: Optional[EntityID] = None

        self._logger = get_agent_logger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}",
            self._agent_info,
        )
        
        self._clustering: Clustering = cast(
            Clustering,
            module_manager.get_module(
                "KMeansPPSearch.Clustering",
                "adf_core_python.implement.module.algorithm.k_means_clustering.KMeansClustering",
            ),
        )

        self.register_sub_module(self._clustering)
```

そして、`calculate` メソッドでクラスタリングモジュールを呼び出し、探索対象を決定します。

```python
    def calculate(self) -> Search:
        # 自エージェントのエンティティIDを取得
        me: EntityID = self._agent_info.get_entity_id()
        # 自エージェントが所属するクラスターのインデックスを取得
        allocated_cluster_index: int = self._clustering.get_cluster_index(me)
        # クラスター内のエンティティIDを取得
        cluster_entity_ids: list[EntityID] = self._clustering.get_cluster_entity_ids(
            allocated_cluster_index
        )
        # 乱数で選択
        index = random.randint(0, len(cluster_entity_ids) - 1)
        # 選択したエンティティIDを結果として設定
        self._result = cluster_entity_ids[index]
        
        return self
```

以上で、`KMeansPPClustering` モジュールを用いた `KMeansPPSearch` モジュールの実装が完了しました。

実行すると、各エージェントが担当地域内からランダムに探索対象を選択し、探索を行います。

## モジュールの改善

`KMeansPPSearch` モジュールは、クラスタリングモジュールを用いて担当地域内からランダムに探索対象を選択しています。
そのため、以下のような問題があります。

- 探索対象がステップごとに変わってしまう
  - 目標にたどり着く前に探索対象が変わってしまうため、なかなか目標にたどり着けない
  - 色んなところにランダムに探索対象を選択することで、効率的な探索ができない
- すでに探索したエンティティを再度探索対象として選択してしまうため、効率的な探索ができない

などの問題があります。

## 課題

`KMeansPPSearch` モジュールを改善し、より効率的な探索を行うモジュールを実装して見てください。

### 探索対象がステップごとに変わってしまう問題

### すでに探索したエンティティを再度探索対象として選択してしまう問題
