# 离线钱包使用手册

#### 1. 安装及运行

钱包使用kivy框架开发，(mac版)在使用前需要进行如下安装与运行步骤：

> xcode-select --install
>
> brew install python3
>
> brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
>
> pip install Cython==0.29.10
>
> pip install kivy
>
> pip3 install pexpect
>
> pip3 install pyqrcode
>
> pip3 install zbarcam
>
> git clone https://github.com/coinexchain/offline-wallet
>
> cd offline-wallet
>
> python3 ./main.py 

**钱包使用流程：**

- 节点运维人员通过cetcli创建原始交易串，并生成二维码给节点私钥持有者
- 私钥持有者使用钱包对原始交易串进行签名，钱包生成的二维码发送给运维人员
- 运维人员将原始交易串和签名信息组装，然后使用cetcli或者rest发送交易上链

下面已创建validator为例详细描述上述流程

#### 2. 主页与基础功能

Home界面如下，分为四个功能：

- 签名
- 创建key
- 列出钱包中的全部key
- 获取指定name的key的信息和二维码

![image-20191110203320565](/https://github.com/coinexchain/offline-wallet/blob/master/doc/validator%20manual.mddevops/images/image-home.png)

#### 3. 功能详解

##### 	3.1 创建秘钥

在界面中填入要创建的key的名字和保存密码，点击`genetate new key`，生成的地址和包含地址信息的二维码如下图所示。

![image-20191110180025942](/Users/helldealer/devops/images/image-create-key.png)

##### 	3.2 获取指定名字的key信息

点击home回到主页，点击get key QRcode，输入要查询的key name，点击generate address qrcode，生成key信息和二维码如下所示

![image-20191110180114908](/Users/helldealer/devops/images/image-get-key.png)

##### 	3.3 签名

​	通过cetcli或者rest接口可以生成交易的json串，这里已cetcli为例，描述创建一个validator的过程。

​	3.3.1 **创建交易json串**

​	命令如下

	cetcli tx staking create-validator --pubkey=coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e \
	--identity=keybaseNumber --moniker=bearhome --website=www.bearhome.com --from=coinex1vg35xer0e34pfszhtktggvyhjfhnqhzpd67d9y \
	--amount=500000000000000cet --commission-rate=0.1 --commission-max-rate=0.2 --commission-max-change-rate=0.01 --min-self-delegation=500000000000000 \
	--gas=500000 --fees=60000000cet --chain-id=coinexdex-test1 \
	--generate-only
​	返回的json如下：

```
{"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgCreateValidator","value":{"description":{"moniker":"bearhome","identity":"keybaseNumber","website":"www.bearhome.com","details":""},"commission":{"rate":"0.100000000000000000","max_rate":"0.200000000000000000","max_change_rate":"0.010000000000000000"},"min_self_delegation":"500000000000000","delegator_address":"coinex1vg35xer0e34pfszhtktggvyhjfhnqhzpd67d9y","validator_address":"coinexvaloper1vg35xer0e34pfszhtktggvyhjfhnqhzpk4a9ts","pubkey":"coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e","value":{"denom":"cet","amount":"500000000000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":null,"memo":""}}
```

可以看到，这里面的`signatures`字段是空的，通过各种二维码生成工具，我们用上述的字符串生成一张二维码，二维码生成建议使用python的pyqrcode库。

如下所示：

![image-20191110181305617](/Users/helldealer/devops/images/image-unsigned-tx.png)

点击钱包主页的signature按钮，进入签名页面，输入下方的key，账户，链信息，点击enter健确认

账户信息可以通过下面的命令查询

```
cetcli query account coinex1vg35xer0e34pfszhtktggvyhjfhnqhzpd67d9y --chain-id=coinexdex-test1
{
  "address": "coinex1vg35xer0e34pfszhtktggvyhjfhnqhzpd67d9y",
  "coins": [
    {
      "denom": "cet",
      "amount": "9999999900000000"
    }
  ],
  "locked_coins": null,
  "frozen_coins": [],
  "public_key": null,
  "account_number": "9",
  "sequence": "0",
  "memo_required": false
}
```

然后将上方的二维码放置到左上方的摄像采集区，生成的签名信息和包含签名信息的二维码如下：

![image-20191110181456010](/Users/helldealer/devops/images/image-signature-ui.png)

右上角为未签名交易的字符串，左下角为签名信息，右下角二维码中包含的就是左下角的签名信息。

扫描该二维码，可以获取签名信息，将该字符串添加到用cetcli获取的未签名字符串中，组成完整的可以用于广播到链上的交易字符串。如下所示，注意`signatures`字段后面要手动添加一个方括号。

```
{"type":"cosmos-sdk/StdTx","value":{"msg":[{"type":"cosmos-sdk/MsgCreateValidator","value":{"description":{"moniker":"bearhome","identity":"keybaseNumber","website":"www.bearhome.com","details":""},"commission":{"rate":"0.100000000000000000","max_rate":"0.200000000000000000","max_change_rate":"0.010000000000000000"},"min_self_delegation":"500000000000000","delegator_address":"coinex1vg35xer0e34pfszhtktggvyhjfhnqhzpd67d9y","validator_address":"coinexvaloper1vg35xer0e34pfszhtktggvyhjfhnqhzpk4a9ts","pubkey":"coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e","value":{"denom":"cet","amount":"500000000000000"}}}],"fee":{"amount":[{"denom":"cet","amount":"60000000"}],"gas":"500000"},"signatures":[{"pub_key":{"type":"tendermint/PubKeySecp256k1","value":"Ah/IYY34tIInITB/1wIeFgfKrk/euxeuSWtOg4BrXGmR"},"signature":"rWdIGhL55QYgjV5jy79AfKAPZb3UFDcEuC+BujvO1IgPpoCyj7FLDJd20eLRRNjWTt3omxmCnEwpdakmHj6HTA=="}],"memo":""}}
```

将上述字符串拷贝到myjson.txt文件中，执行下面的命令将交易发送到链上

> cetcli tx broadcast my.json --chain-id=coinexdex-test1

查询交易执行情况，发现已成功成为validator

```
cetcli query staking validator coinexvaloper1vg35xer0e34pfszhtktggvyhjfhnqhzpk4a9ts --trust-node
|
  operatoraddress: coinexvaloper1vg35xer0e34pfszhtktggvyhjfhnqhzpk4a9ts
  conspubkey: coinexvalconspub1zcjduepqgx6fm2szcuf6sqc787d20r7860zumcr40ck9yl4gcqzphl0pu07s4wau0e
  jailed: false
  status: 2
  tokens: "500000000000000"
  delegatorshares: "500000000000000.000000000000000000"
  description:
    moniker: bearhome
    identity: keybaseNumber
    website: www.bearhome.com
    details: ""
  unbondingheight: 0
  unbondingcompletiontime: 1970-01-01T00:00:00Z
  commission:
    commission_rates:
      rate: "0.100000000000000000"
      max_rate: "0.200000000000000000"
      max_change_rate: "0.010000000000000000"
    update_time: 2019-11-10T10:16:47.060879Z
  minselfdelegation: "500000000000000"
```

##### 3.4 其他功能

钱包还支持地址的导入和列举功能，目前还不支持导出和删除

> Warning 💡：main.py的目录下的data目录存有用户的公私钥，请妥善保管该目录 

