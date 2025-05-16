import hashlib
import json
import datetime


class Block:
    def __init__(self, index, timestamp, prev_hash, transaction):
        self.index = index  # そのブロックの番号(配列番号的な
        self.timestamp = timestamp  # 前後関係と言いましたがBitcoinで言うと時系列で取引記録がされるので一応日付を記録
        self.prev_hash = prev_hash  # 一つ前のブロックのハッシュ値
        self.transaction = transaction  # とりあえずデータを記録するというていでトランザクションを保存することにします。
        self.now_hash = (
            self.calc_hash()
        )  # これはこのブロック自身のハッシュ値を計算します。

    def calc_hash(self):  # ハッシュ値の計算
        # ここではnow_hash(自分自身のブロック)を除いたデータをjsonに変換しsha256でハッシュ化します。
        joined_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "transaction": self.transaction,
        }
        json_text = json.dumps(joined_data, sort_keys=True)
        return hashlib.sha256(json_text.encode("ascii")).hexdigest()


# 実際にいくつかブロックを生成しブロックチェーン的なものを作る
block_chain = []  # ただの配列ですがブロックを追加していくブロックチェーンです。

# 一番最初のブロックは一つ前のブロックが存在しないため、一つ前のブロックのハッシュ値を'-'として作成してしまいます。
genesis = Block(0, str(datetime.datetime.now()), "-", "取引データ")
block_chain.append(genesis)

# 次以降のブロックはgenesisブロックのハッシュ値からそれぞれブロックを繋げて作成していきます。とりあえず5ブロック追加します。
for i in range(5):
    new_block = Block(
        i + 1,
        str(datetime.datetime.now()),
        block_chain[i].now_hash,
        "取引データ" + str(i + 1),
    )
    block_chain.append(new_block)

# 順にブロックの番号とそのブロックのハッシュ値、一つ前のハッシュ値、取引データと表示してみます。
for block in block_chain:
    print(block.index, block.now_hash, block.prev_hash, block.transaction)
