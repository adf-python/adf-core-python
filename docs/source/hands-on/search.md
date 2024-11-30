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
  Search: src.<your_team_name>.module.complex.k_means_pp_search.KMeansPPSearch

DefaultTacticsFireBrigade:
  Search: src.<your_team_name>.module.complex.k_means_pp_search.KMeansPPSearch

DefaultTacticsPoliceForce:
  Search: src.<your_team_name>.module.complex.k_means_pp_search.KMeansPPSearch
```

## モジュールの実装

まず、`KMeansPPClustering` モジュールを呼び出せるようにします。

以下のコードを`config/module.yaml`に追記してください。

```yaml
KMeansPPSearch:
  Clustering: src.<your_team_name>.module.algorithm.k_means_pp_clustering.KMeansPPClustering
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

そして、`calculate` メソッドでクラスタリングモジュールを呼び出し、探索対象を決定するように変更します。

以下のコードを `k_means_pp_search.py` に追記してください。

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
        if cluster_entity_ids:
            self._result = random.choice(cluster_entity_ids)
        
        # ログ出力
        self._logger.info(f"Target entity ID: {self._result}")
        
        return self
```

以上で、`KMeansPPClustering` モジュールを用いた `KMeansPPSearch` モジュールの実装が完了しました。

ターミナルを2つ起動します。

片方のターミナルを開き、シミュレーションサーバーを以下のコマンドで起動します：

```bash
# Terminal A
cd WORKING_DIR/rcrs-server/scripts
./start-comprun.sh -m ../maps/tutorial_ambulance_team_only/map -c ../maps/tutorial_ambulance_team_only/config
```

その後、別のターミナルを開き、エージェントを起動します：

```bash
# Terminal B
cd WORKING_DIR/<your_team_name>
python main.py
```

## モジュールの改善

`KMeansPPSearch` モジュールは、クラスタリングモジュールを用いて担当地域内からランダムに探索対象を選択しています。
そのため、以下のような問題があります。

- 探索対象がステップごとに変わってしまう
  - 目標にたどり着く前に探索対象が変わってしまうため、なかなか目標にたどり着けない
  - 色んなところにランダムに探索対象を選択することで、効率的な探索ができない
- すでに探索したエンティティを再度探索対象として選択してしまうため、効率的な探索ができない
- 近くに未探索のエンティティがあるのに、遠くのエンティティを探索対象として選択してしまう

などの問題があります。

## 課題

`KMeansPPSearch` モジュールを改善し、より効率的な探索を行うモジュールを実装して見てください。

```{warning}
ここに上げた問題以外にも、改善すべき点が存在すると思うので、それを改善していただいても構いません。
```

```{warning}
プログラム例のプログラムにも一部問題があるので、余裕があったら修正してみてください。
```

### 探索対象がステップごとに変わってしまう問題

```{admonition} 方針のヒント
:class: hint dropdown

一度選択した探索対象に到達するまで、探索対象を変更しないようにする
```

```{admonition} プログラム例
:class: hint dropdown

````python
    def calculate(self) -> Search:
        # 自エージェントのエンティティIDを取得
        me: EntityID = self._agent_info.get_entity_id()
        # 自エージェントが所属するクラスターのインデックスを取得
        allocated_cluster_index: int = self._clustering.get_cluster_index(me)
        # クラスター内のエンティティIDを取得
        cluster_entity_ids: list[EntityID] = self._clustering.get_cluster_entity_ids(
            allocated_cluster_index
        )

        # 探索対象をすでに選んでいる場合
        if self._result:
            # 自エージェントのいる場所のエンティティIDを取得
            my_position = self._agent_info.get_position_entity_id()
            # 探索対象の場所のエンティティIDを取得
            target_position = self._world_info.get_entity_position(self._result)
            # 自エージェントのいる場所と探索対象の場所が一致している場合、探索対象をリセット
            if my_position == target_position:
                # 探索対象をリセット
                self._result = None

        # 探索対象が未選択の場合
        if not self._result and cluster_entity_ids:
            self._result = random.choice(cluster_entity_ids)

        return self
```

### すでに探索したエンティティを再度探索対象として選択してしまう問題

```{admonition} 方針のヒント
:class: hint dropdown

すでに探索したエンティティを何かしらの方法で記録し、再度探索対象として選択しないようにする
```

```{admonition} プログラム例
:class: hint dropdown

````python
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

        # 探索したいエンティティIDのリスト(追加)
        self._search_entity_ids: list[EntityID] = []

    def calculate(self) -> Search:
        # 探索したいエンティティIDのリストが空の場合
        if not self._search_entity_ids:
            # 自エージェントのエンティティIDを取得
            me: EntityID = self._agent_info.get_entity_id()
            # 自エージェントが所属するクラスターのインデックスを取得
            allocated_cluster_index: int = self._clustering.get_cluster_index(me)
            # クラスター内のエンティティIDを取得(変更)
            self._search_entity_ids: list[EntityID] = (
                self._clustering.get_cluster_entity_ids(allocated_cluster_index)
            )

        # 探索対象をすでに選んでいる場合
        if self._result:
            # 自エージェントのいる場所のエンティティIDを取得
            my_position = self._agent_info.get_position_entity_id()
            # 探索対象の場所のエンティティIDを取得
            target_position = self._world_info.get_entity_position(self._result)
            # 自エージェントのいる場所と探索対象の場所が一致している場合、探索対象をリセット
            if my_position == target_position:
                # 探索したいエンティティIDのリストから探索対象を削除
                self._search_entity_ids.remove(self._result)
                # 探索対象をリセット
                self._result = None

        # 探索対象が未選択の場合(変更)
        if not self._result and self._search_entity_ids:
            self._result = random.choice(self._search_entity_ids)

        return self
```

### 近くに未探索のエンティティがあるのに、遠くのエンティティを探索対象として選択してしまう

```{admonition} 方針のヒント
:class: hint dropdown

エンティティ間の距離を計算し、もっとも近いエンティティを探索対象として選択する
```

```{admonition} プログラム例
:class: hint dropdown

````python
    def calculate(self) -> Search:
        # 探索したいエンティティIDのリストが空の場合
        if not self._search_entity_ids:
            # 自エージェントのエンティティIDを取得
            me: EntityID = self._agent_info.get_entity_id()
            # 自エージェントが所属するクラスターのインデックスを取得
            allocated_cluster_index: int = self._clustering.get_cluster_index(me)
            # クラスター内のエンティティIDを取得
            self._search_entity_ids: list[EntityID] = (
                self._clustering.get_cluster_entity_ids(allocated_cluster_index)
            )

        # 探索対象をすでに選んでいる場合
        if self._result:
            # 自エージェントのいる場所のエンティティIDを取得
            my_position = self._agent_info.get_position_entity_id()
            # 探索対象の場所のエンティティIDを取得
            target_position = self._world_info.get_entity_position(self._result)
            # 自エージェントのいる場所と探索対象の場所が一致している場合、探索対象をリセット
            if my_position == target_position:
                # 探索したいエンティティIDのリストから探索対象を削除
                self._search_entity_ids.remove(self._result)
                # 探索対象をリセット
                self._result = None

        # 探索対象が未選択の場合
        if not self._result and self._search_entity_ids:
            nearest_entity_id: Optional[EntityID] = None
            nearest_distance: float = float("inf")
            me: EntityID = self._agent_info.get_entity_id()
            # 探索対象の中で自エージェントに最も近いエンティティIDを選択(変更)
            for entity_id in self._search_entity_ids:
                distance = self._world_info.get_distance(me, entity_id)
                if distance < nearest_distance:
                    nearest_entity_id = entity_id
                    nearest_distance = distance
            self._result = nearest_entity_id
```
