# Validator Manual

### 目录

- [节点常见活动](#* 节点常见活动)
- [基础命令](#* 基础命令)
- [签名与广播](#* 签名与广播)

### 内容

#### * 节点常见活动

1. **创建validator**

   用户发送该消息成为validator

   > $ cetcli tx staking create-validator --pubkey=coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e \
   > --identity=keybaseNumber --moniker=bearhome --website=www.bearhome.com --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer \
   > --amount=500000000000000cet --commission-rate=0.1 --commission-max-rate=0.2 --commission-max-change-rate=0.01 --min-self-delegation=500000000000000 \
   > --gas=500000 --fees=60000000cet --chain-id=coinex-chain \
   > --generate-only

   **参数解释**

   - `pubkey:` 节点共识公钥，获取方式见基础命令中的[查看节点共识公钥](#1. 查看节点共识公钥) 
   - `identity:` 节点在keybase上的identity号
   - `moniker:` 节点的名字
   - `website:` 节点的网站
   - `amount:`  节点的质押数量
   -  `commission-rate:` 节点的初始佣金比例
   - `commission-max-rate:` 节点的最大佣金比例
   - `commission-max-change-rate:` 节点佣金比例24小时内最大增长比例
   - `min-self-delegation:` 节点承诺的最小自质押数量
   - `generate-only:` 只生成交易的json字符流，而不对交易进行签名和广播

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgCreateValidator","value":{"description":{"moniker":"bearhome","identity":"keybaseNumber","website":"www.bearhome.com","details":""},"commission":{"rate":"0.100000000000000000","max_rate":"0.200000000000000000","max_change_rate":"0.010000000000000000"},"min_self_delegation":"500000000000000","delegator_address":"coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer","validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh","pubkey":"coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e","value":{"denom":"cet","amount":"500000000000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

2. **编辑validator**

   > cetcli tx staking edit-validator --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer \
   > --identity=keybaseNumber2 --moniker=bearhouse --website=www.bearhouse.com --commission-rate=0.15 --min-self-delegation=5000000000000000 \
   > --gas=500000 --fees=60000000cet --chain-id=coinex-chain \
   > --generate-only

   **参数解释**

   - `identity`,`moniker`,`website`,`min-self-delegation`同创建validator
   - `commission-rate:` 修改validator的佣金比例为该设定值，该值不能大于创建validator时设置的``commission-max-rate`

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgEditValidator","value":{"Description":{"moniker":"bearhouse","identity":"keybaseNumber2","website":"www.bearhouse.com","details":"[do-not-modify]"},"address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh","commission_rate":"0.150000000000000000","min_self_delegation":"5000000000000000"}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

3. **unjail**

   当validator被关监狱后，可以发送该命令来出狱

   > cetcli tx slashing unjail --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer --chain-id=coinex-chain --gas=500000 --fees=60000000cet --generate-only

   **参数解释**

   - `from:` validator的普通用户地址

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgUnjail","value":{"address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh"}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

4. **质押**

   > cetcli tx staking delegate coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh 10000000000cet --from=coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk --chain-id=coinex-chain --gas=500000 --fees=60000000cet --generate-only

   **参数解释**

   `coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh`这个地址是要质押的delegator的operator地址，获取方式见基础命令中的[查询操作地址](#2. 查看validator操作地址)

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgDelegate","value":{"delegator_address":"coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk","validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh","amount":{"denom":"cet","amount":"10000000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

5. **redelegate**

   > cetcli tx staking redelegate coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh coinexvaloper1tfytjpdeqgwy75c264r08urh65zvxg6j3vdzgz 30000000000000cet --from=coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk --chain-id=coinex-chain --gas=500000 --fees=60000000cet --generate-only

   同样的，需要validator的operator地址

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgBeginRedelegate","value":{"delegator_address":"coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk","validator_src_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh","validator_dst_address":"coinexvaloper1tfytjpdeqgwy75c264r08urh65zvxg6j3vdzgz","amount":{"denom":"cet","amount":"30000000000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

6. **undelegate**

   > cetcli tx staking unbond coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh 1000000cet --from=coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk --chain-id=coinex-chain --gas=500000 --fees=60000000cet --generate-only

   需要validator的operator地址

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgUndelegate","value":{"delegator_address":"coinex1tfytjpdeqgwy75c264r08urh65zvxg6j2rw2xk","validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh","amount":{"denom":"cet","amount":"1000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

7. **设置质押奖励提取地址**

   > cetcli tx distribution set-withdraw-addr coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer --chain-id=coindex-chain --gas=500000 --fees=60000000cet --generate-only

   该命令指定一个新的收取收益的地址，而不是默认的地址

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgModifyWithdrawAddress","value":{"delegator_address":"coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer","withdraw_address":"coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer"}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

8. **提取质押收益**

   > cetcli tx distribution withdraw-rewards coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer --chain-id=coindex-chain --gas=500000 --fees=60000000cet --generate-only

   提取质押收益

   **输出**

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgWithdrawDelegationReward","value":{"delegator_address":"coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer","validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh"}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

9. **提取质押收益和佣金**

   > cetcli tx distribution withdraw-rewards coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh --from=coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer --commission --chain-id=coindex-chain --gas=500000 --fees=60000000cet --generate-only

   **参数解释**

   - `commission:` 加上这个flag，表示在提取收益的同时也提取出块佣金

   ```
   {"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgWithdrawDelegationReward","value":{"delegator_address":"coinex1aqd670650tg3fmvm958mkknsyumqym59sarqer","validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh"}},{"type":"cosmos-sdk/MsgWithdrawValidatorCommission","value":{"validator_address":"coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh"}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
   ```

#### * 基础命令

#####1. 查看节点共识公钥

```
$ cetd tendermint show-validator
coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e
```

##### 2. 查看validator操作地址

```
$ cetcli keys show helldealer --bech=val
- name: helldealer
  type: local
  address: coinexvaloper1aqd670650tg3fmvm958mkknsyumqym59tjqghh
  pubkey: coinexvaloperpub1addwnpepqfa7zqj26lwsr74xchnuhf3367pd6z25mzdd38fxwhclqdpskjx8v94uswh
  mnemonic: ""
  threshold: 0
  pubkeys: []
```

#### * 签名与广播

[节点常见活动](#节点常见活动)中生成的交易信息json串是不带有签名的。

节点运营者需要对该字符串进行签名，并将签名结果填入到交易信息json串的"signatures:"处，拼接后的json串可以用来调用下面的rest api进行广播

>  POST /txs

签名可以使用[钱包sdk polarbear](https://github.com/coinexchain/polarbear)或者其他钱包

