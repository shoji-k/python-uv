import hashlib
import json
import datetime
from typing import Dict, List, Any, Optional, Union


# https://paiza.hatenablog.com/entry/2018/05/11/Pythonでブロックチェーンを実装して採掘までやって
class Block:
    def __init__(
        self,
        index: int,
        timestamp: str,
        prev_hash: str,
        transaction: List[Any],
    ):
        self.index = index
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.transaction = transaction
        self.diff = 4
        self.now_hash = self.calc_hash()
        self.nonce: Optional[int] = None

    def calc_hash(self) -> str:
        joined_data: Dict[str, Any] = {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "transaction": self.transaction,
            "diff": self.diff,
        }
        json_text = json.dumps(joined_data, sort_keys=True)
        return hashlib.sha256(json_text.encode("ascii")).hexdigest()

    def to_json(self) -> Union[str, bool]:
        if self.nonce is None:
            return False
        joined_data: Dict[str, Any] = {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "now_hash": self.now_hash,
            "transaction": self.transaction,
            "diff": self.diff,
            "nonce": self.nonce,
        }
        json_text = json.dumps(joined_data, sort_keys=True)
        return json_text

    def check(self, nonce: int) -> bool:
        nonce_joined = self.now_hash + str(nonce)
        calced = hashlib.sha256(nonce_joined.encode("ascii")).hexdigest()
        if calced[: self.diff :].count("0") == self.diff:
            return True
        else:
            return False

    def mining(self, append_transaction: Dict[str, str]) -> int:
        nonce = 0
        self.transaction.append(append_transaction)
        self.now_hash = self.calc_hash()
        while True:
            nonce_joined = self.now_hash + str(nonce)
            calced = hashlib.sha256(nonce_joined.encode("ascii")).hexdigest()
            if calced[: self.diff :].count("0") == self.diff:
                break
            nonce += 1
        return nonce


block_chain: List[Block] = []

block = Block(0, str(datetime.datetime.now()), "-", [])  # 最初のブロックを作成
append_transaction = {"paiza": "genesis_block"}
nonce = block.mining(append_transaction)  # 最初のブロックの採掘
block.nonce = nonce  # 得られたnonceをブロックに格納

block_chain.append(block)  # 完成したブロックを追加します。

# 以降5ブロック追加してみます。
for i in range(5):
    # i+1番目のブロック, 現在時刻, 一つ前のブロックのハッシュ値, 取引データ で新しいブロックを生成します。
    block = Block(
        i + 1,
        str(datetime.datetime.now()),
        block_chain[i].now_hash,
        ["取引データ"],
    )
    append_transaction = {"paiza": "採掘報酬ゲット" + str(i)}  # 採掘報酬
    nonce = block.mining(append_transaction)  # i+1番目の採掘
    block.nonce = nonce  # 得られたnonceをブロックに格納
    block_chain.append(block)  # 完成したブロックを追加します。


for block in block_chain:
    # nonceとブロックのハッシュ値を使ってブロックがルールを満たしているか検証
    nonce_joined = block.now_hash + str(block.nonce)
    calced = hashlib.sha256(nonce_joined.encode("ascii")).hexdigest()

    print(
        "index =",
        block.index,
        "sha256(",
        block.now_hash,
        "+",
        block.nonce,
        ") =",
        calced,
    )
