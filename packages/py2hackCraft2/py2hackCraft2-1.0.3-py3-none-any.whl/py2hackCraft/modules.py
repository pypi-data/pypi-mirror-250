import websocket
import threading
import time
import json
import logging
from dataclasses import dataclass
from typing import Callable, Any

def str_to_bool(s):
    """
    文字列をブール値に変換する。

    Args:
        s (str): "true" または "false"（大文字小文字は無視）

    Returns:
        bool: 変換されたブール値。"true"ならTrue、"false"ならFalse
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot covert {s} to a boolean.")  # 有効な文字列でない場合はエラー

class UninitializedClientError(Exception):
    """WebSocketClientが初期化されていないことを示すカスタム例外。"""
    pass


class WebSocketClient:
    def __init__(self):
        self.lock = threading.Lock()
        self.connected = False
        self.response_event = threading.Event()  # イベントオブジェクトを追加
        self.last_message = None  # 最後に受信したメッセージを保持
        self.callbacks = {}  # コールバック関数を保持

    def connect(self, host:str, port:int):
        self.host = host
        self.port = port
        self.url = "ws://%s:%d/ws" %(host, port)
        logging.debug("connecting '%s'" % (self.url))
        self.connected = False
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.run_forever()

    def disconnect(self):
        self.connected = False
        self.host = None
        self.port = None
        self.close()

    def _setCallback(self, eventName, callbackFunc):
            # イベント名に対応するコールバックリストがまだ存在しない場合は、新しいリストを作成する
            if eventName not in self.callbacks:
                self.callbacks[eventName] = []
            
            # 指定されたイベント名のリストにコールバック関数を追加する
            self.callbacks[eventName].append(callbackFunc)

    def on_message(self, ws, message):
        logging.debug("on_message '%s'" % message)
        try:
            jsonMessage = json.loads(message)
            type = jsonMessage['type']
            data = jsonMessage['data']
            if(type == 'result'):
                self.result = data
            elif(type == 'error'):
                self.error = data
            elif(type == 'logged'):
                self.connected = True
                self.result = data
            elif(type == 'entities'):
                self.result = data
            elif(type == 'event'):
                jsonEvent = json.loads(data)
                eventName = jsonEvent['name']
                logging.debug("on event %s '%s'" %(eventName, jsonEvent['data']))
                # 指定されたイベント名に対応するすべてのコールバック関数を実行する
                if eventName in self.callbacks:
                    for callback in self.callbacks[eventName]:
                        # 新しいスレッドでコールバック関数を実行
                        callback_thread = threading.Thread(target=callback, args=(jsonEvent['data'],))
                        callback_thread.start()
                        # callback(jsonEvent['data'])
                return
            print("*** イベントをセットして、メッセージの受信を通知")
            self.response_event.set()  # イベントをセットして、メッセージの受信を通知
        except json.JSONDecodeError:
            logging.error("JSONDecodeError '%s'" % message)    

    def on_error(self, ws, error):
        logging.debug("on_error '%s'" % error)

    def on_close(self, ws, close_status_code, close_msg):
        logging.debug("### closed ###")
        self.connected = False

    def on_open(self, ws):
        logging.debug("Opened connection")
        self.connected = True

    def run_forever(self):
        self.thread.start()

    def wait_for_connection(self):
        while not self.connected:
            time.sleep(0.1)  # Wait for connection to be established

    def send(self, message):
        logging.debug("send sending'%s'" % message)
        self.wait_for_connection()
        with self.lock:
            print("*** イベントをクリアして新しいレスポンスの準備をする")
            self.response_event.clear()  # イベントをクリアして新しいレスポンスの準備をする
            self.ws.send(message)
            print("*** サーバーからのレスポンスを待つ")
            self.response_event.wait()  # サーバーからのレスポンスを待つ
        logging.debug("send result: '%s'" % self.last_message)
        return self.last_message  # 最後に受信したメッセージを返す

    def close(self):
        self.ws.close()
        self.thread.join()

    def sendCall(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args            
        message = {
            "type": "call",
            "data": data
        }
        self.send(json.dumps(message))

@dataclass
class Location:
    x: int
    y: int
    z: int
    world: str = "world"


@dataclass
class ChatMessage:
    """
    チャットメッセージを表すデータクラス。

    Attributes:
        player (str): プレイヤー名または識別子。
        uuid (str): プレイヤーの一意の識別子（UUID）。
        message (str): プレイヤーがチャットで送信したメッセージの内容。
    """
    player: str
    uuid: str
    entity: str
    entityUuid: str
    message: str

@dataclass
class RedstonePower:
    """
    レッドストーン信号を表すデータクラス。

    Attributes:
        oldCurrent (int): 前のレッドストーン信号の強さ
        newCurrent (int): 最新のレッドストーン信号の強さ
    """
    entity: str
    entityUuid: str
    oldCurrent: int
    newCurrent: int

@dataclass
class Block:
    """
    ブロックを表すデータクラス。

    Attributes:
        name (str): ブロックの種類。
        data (int): ブロックのデータ値。
        isLiquid (bool): 液体ブロックかどうか。
        isAir (bool): 空気ブロックかどうか。
        isBurnable (bool): 燃えるブロックかどうか。
        isFuel (bool): 燃料ブロックかどうか。
        isOccluding (bool): 透過しないブロックかどうか。
        isSolid (bool): 壁のあるブロックかどうか。
        isPassable (bool): 通過可能なブロックかどうか。
        x (int): ブロックのX座標。
        y (int): ブロックのY座標。
        z (int): ブロックのZ座標。
    """
    name: str
    data: int = 0
    isLiquid: bool = False
    isAir: bool = False
    isBurnable: bool = False
    isFuel: bool = False
    isOccluding: bool = False
    isSolid: bool = False
    isPassable: bool = False
    x: int = 0
    y: int = 0
    z: int = 0

class Player:
    def __init__(self, player: str):
        self.player = player

    def login(self, host:str, port:int):
        self.client = WebSocketClient()
        self.client.connect(host, port)
        self.client.send(json.dumps({
            "type": "login",
            "data": {
                "player": self.player,
            }
        }))
        logging.debug("login '%s'" % self.client.result)
        self.playerUUID = self.client.result

    def logout(self):
        self.client.disconnect()    

    def getEntity(self, name: str) -> 'Entity': 
        """
        指定された名前のエンティティを取得する。

        Args:
            name (str): エンティティの名前。

        Returns:
            Entity: 取得したエンティティ。

        Raises:
            UninitializedClientError: クライアントが初期化されていない場合。        
        """
        if self.client is None or not self.client.connected:  # 接続状態をチェック
            raise UninitializedClientError("Client is not initialized")

        message = {
            "type": "entities",
        }
        self.client.send(json.dumps(message))
        entities = self.client.result
        entity = next((entity for entity in entities if entity['name'] == name), None)

        return Entity(self.client, entity['entityUuid'])


class Entity:
    """
    エンティティを表すクラス。
    """
    def __init__(self, client: WebSocketClient, entity: str):
        self.client = client  # 初期化時にはWebSocketClientはNone
        self.entity = entity

    def setOnPlayerChat(self, callbackFunc: Callable[['Entity', 'ChatMessage'], Any]):
        """
        チャットを受信したときに呼び出されるコールバック関数を設定する。
        """
        def callbackWrapper(data):
            if(data['entityUuid'] == self.entity):
                logging.debug("callbackWrapper '%s'" % data)            
                chatMessage = ChatMessage(**data)            
                callbackFunc(self, chatMessage)
        self.client._setCallback('onPlayerChat', callbackWrapper)

    def setOnRedstoneChange(self, callbackFunc: Callable[['Entity', 'RedstonePower'], Any]):
        """
        レッドストーンを受信したときに呼び出されるコールバック関数を設定する。
        """
        def callbackWrapper(data):
            logging.debug("setOnRedstoneChange callbackWrapper '%s'" % data)
            if(data['entityUuid'] == self.entity):
                logging.debug("callbackWrapper '%s'" % data)
                power = RedstonePower(**data)
                callbackFunc(self, power)
        self.client._setCallback('onEntityRedstone', callbackWrapper)

    def forward(self):
        """
        エンティティを前方に移動させる。
        """
        self.client.sendCall(self.entity, "forward")

    def back(self):
        """
        エンティティを後方に移動させる。
        """
        self.client.sendCall(self.entity, "back")

    def up(self):
        """
        エンティティを上方に移動させる。
        """
        self.client.sendCall(self.entity, "up")

    def down(self):
        """
        エンティティを下方に移動させる。
        """
        self.client.sendCall(self.entity, "down")

    def stepLeft(self):
        """
        エンティティを左に移動させる。
        """
        self.client.sendCall(self.entity, "stepLeft")

    def stepRight(self):
        """
        エンティティを右に移動させる。
        """
        self.client.sendCall(self.entity, "stepRight")

    def turnLeft(self):
        """
        エンティティを左に回転させる。
        """
        self.client.sendCall(self.entity, "turnLeft")

    def turnRight(self):
        """
        エンティティを右に回転させる。
        """
        self.client.sendCall(self.entity, "turnRight")

    def makeSound(self):
        """
        エンティティを鳴かせる。
        """
        self.client.sendCall(self.entity, "sound")

    def accelerate(self, speed: float):
        """
        エンティティを加速させる。

        Args:
            speed (float): 加速する速度。
        """
        self.client.sendCall(self.entity, "move", [speed])

    def turn(self, degrees: int):
        """
        エンティティを回転させる。

        Args:
            degrees (int): 回転する速度。
        """
        self.client.sendCall(self.entity, "turn", [degrees])      

    def jump(self):
        """
        エンティティをジャンプさせる。
        """
        self.client.sendCall(self.entity, "jump")

    def place(self):
        """
        エンティティの前方にブロックを設置する。
        """
        self.client.sendCall(self.entity, "placeFront")

    def placeUp(self):
        """
        エンティティの真上にブロックを設置する。
        """
        self.client.sendCall(self.entity, "placeUp")

    def placeDown(self):
        """
        エンティティの真下にブロックを設置する。
        """
        self.client.sendCall(self.entity, "placeDown")

    def useItem(self):
        """
        エンティティの前方にアイテムを使う
        """
        self.client.sendCall(self.entity, "useItemFront")

    def useItemUp(self):
        """
        エンティティの真上にアイテムを使う
        """
        self.client.sendCall(self.entity, "useItemUp")

    def useItemDown(self):
        """
        エンティティの真下にアイテムを使う
        """
        self.client.sendCall(self.entity, "useItemDown")

    def dig(self):
        """
        エンティティの前方のブロックを壊す。
        """
        self.client.sendCall(self.entity, "digFront")

    def digUp(self):
        """
        エンティティの真上のブロックを壊す。
        """
        self.client.sendCall(self.entity, "digUp")

    def digDown(self):
        """
        エンティティの真下のブロックを壊す。
        """
        self.client.sendCall(self.entity, "digDown")

    def setItem(self, slot: int, block: str):
        """
        エンティティのインベントリにアイテムを設定する。

        Args:
            slot (int): 設定するアイテムのスロット番号。
            block (str): 設定するブロックの種類。
        """
        self.client.sendCall(self.entity, "setItem", [slot, block])

    def holdItem(self, slot: int):
        """
        指定されたスロットからアイテムをエンティティの手に持たせる。

        Args:
            slot (int): アイテムを持たせたいスロットの番号。
        """
        self.client.sendCall(self.entity, "grabItem", [slot])

    def say(self, message: str):
        """
        エンティティに指定されたメッセージをチャットとして送信させる。

        Args:
            message (str): エンティティがチャットで送信するメッセージの内容。
        """
        self.client.sendCall(self.entity, "sendChat", [message])

    def blockColor(self, color: str) -> Block :
        """
        指定された色に近いブロックを調べる。

        Args:
            color (str): ブロックの色(HexRGB形式)
        """
        self.client.sendCall(self.entity, "blockColor", [color])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect(self, x: int, y: int, z: int) -> Block :
        """
        指定された座標のブロックを調べる。

        Args:
            x (int): 相対的なX座標。
            y (int): 相対的なY座標。
            z (int): 相対的なZ座標。
        Returns:
            Block: 調べたブロックの情報。    
        """
        self.client.sendCall(self.entity, "inspect", [x, y, z])
        block = Block(** json.loads(self.client.result))
        return block

    def getLocation(self) -> Location :
        """
        エンティティの現在位置を調べる。
        Returns:
            Location: 調べた位置情報。    
        """
        self.client.sendCall(self.entity, "getPosition")
        location = Location(** json.loads(self.client.result))
        return location
    
    def teleport(self, x: int, y: int, z: int) :
        """
        指定された座標に移動する。
        Args:
            x (int): 絶対的なX座標。
            y (int): 絶対的なY座標。
            z (int): 絶対的なZ座標。
        """
        self.client.sendCall(self.entity, "teleport", [x, y, z])

    def isBlocked(self) -> str :
        """
        エンティティの前方にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall(self.entity, "isBlockedFront")
        return str_to_bool(self.client.result)

    def isBlockedUp(self) -> str :
        """
        エンティティの真上にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall(self.entity, "isBlockedUp")
        return str_to_bool(self.client.result)

    def isBlockedDown(self) -> bool :
        """
        エンティティの真下にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall(self.entity, "isBlockedDown")
        return str_to_bool(self.client.result)
