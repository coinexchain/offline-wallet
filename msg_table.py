

# "bankx/MsgMultiSend" not support!
MSG_TABLE = {
    "cosmos-sdk/MsgSubmitProposal": '"content","initial_deposit",[,2,"amount","denom",],"proposer"',
    "cosmos-sdk/MsgDeposit": '"amount",[,2,"amount","denom",],"depositor","proposal_id"',
    "cosmos-sdk/MsgVote": '"option","proposal_id","voter"',
    "cosmos-sdk/MsgCreateValidator": '"commission","max_change_rate","max_rate","rate",'
                                     '"delegator_address","description","details","identity","moniker","website",'
                                     '"min_self_delegation","pubkey","validator_address","value","amount",'
                                     '"denom"',
    "cosmos-sdk/MsgEditValidator": '"address","commission_rate","min_self_delegation","details","identity",'
                                   '"moniker","website"',
    "cosmos-sdk/MsgDelegate": '"amount","amount","denom","delegator_address","validator_address"',
    "cosmos-sdk/MsgUndelegate": '"amount","amount","denom","delegator_address","validator_address"',
    "cosmos-sdk/MsgBeginRedelegate": '"amount","amount","denom","delegator_address","validator_dst_address",'
                                     '"validator_src_address"',
    "cosmos-sdk/MsgVerifyInvariant": '"invariant_module_name","invariant_route","sender"',
    "bankx/MsgSetMemoRequired": '"address","required"',
    '"bankx/MsgSend"': '"amount",[,2,"amount","denom",],"from_address","to_address","unlock_time"',
    "bankx/MsgMultiSend": '"inputs"[{"address","coins"[{"amount","denom"}]}],"outputs"[{"address","coins"[{'
                          '"amount","denom"}]}]',
    "cosmos-sdk/MsgWithdrawDelegationReward": '"delegator_address","validator_address"',
    "cosmos-sdk/MsgWithdrawValidatorCommission": '"validator_address"',
    "cosmos-sdk/MsgModifyWithdrawAddress": '"delegator_address","withdraw_address"',
    "asset/MsgIssueToken": '"addr_forbiddable","burnable","description","identity","mintable","name","owner",'
                           '"symbol","token_forbiddable","total_supply","url"',
    "asset/MsgTransferOwnership": '"new_owner","original_owner","symbol"',
    "asset/MsgMintToken": '"amount","owner_address","symbol"',
    "asset/MsgBurnToken": '"amount","owner_address","symbol"',
    "asset/MsgForbidToken": '"owner_address","symbol"',
    "asset/MsgUnForbidToken": '"owner_address","symbol"',
    "asset/MsgAddTokenWhitelist": '"owner_address","symbol","whitelist"',
    "asset/MsgRemoveTokenWhitelist": '"owner_address","symbol","whitelist"',
    "asset/MsgForbidAddr": '"addresses","owner_address","symbol"',
    "asset/MsgUnForbidAddr": '"addresses","owner_address","symbol"',
    "asset/MsgModifyTokenInfo": '"description","owner_address","symbol","url"',
    "cosmos-sdk/MsgUnjail": '"address"',
    "alias/MsgAliasUpdate": '"alias","as_default","is_add","owner"',
    "bancorlite/MsgBancorInit": '"earliest_cancel_time","init_price","max_price","max_supply",'
                                '"money","owner","stock"',
    "bancorlite/MsgBancorTrade": '"amount","is_buy","money","money_limit","sender","stock"',
    "bancorlite/MsgBancorCancel": '"money","owner","stock"',
    "market/MsgCreateTradingPair": '"creator","money","price_precision","stock"',
    "market/MsgCreateOrder": '"exist_blocks","identify","order_type","price","price_precision","quantity","sender",'
                             '"side","time_in_force","trading_pair"',
    "market/MsgCancelOrder": '"order_id","sender"',
    "market/MsgCancelTradingPair": '"effective_height","sender","trading_pair"',
    "market/MsgModifyPricePrecision": '"price_precision","sender","trading_pair"',
    "comment/MsgCommentToken": '"content","content_type","donation","references",[,5,"attitudes","id","reward_amount",'
                               '"reward_target","reward_token",],"sender","title","token"',
    "distrx/MsgDonateToCommunityPool": '"amount",[,2,"amount","denom",],"from_addr"',
}

s = '{"0","coinex-test1",{[{"10000000","cet"}],"200000"},"transfer coins",[{"bankx/MsgSend",{[{"1","c"}],' \
    '"c","c","0"}}],"1"} '

sign_info = ['"account_number"', '"chain_id"', '"fee"', '"amount"', '"amount"', '"denom"', '"gas"', '"memo"', '"msgs"', '"type"', '"value"', '"sequence"']


# support: only single msg in tx; only one layer slice in msg;
def build_sign(compact_string):
    seq = ":"
    out = ""
    is_type = False
    stop_head = False
    start_tail = False
    start_msg = False
    msg_type = ""
    msg_keys = []
    element_num = 0
    i = 0
    j = 0
    unsign_list = list(compact_string)

    for k, c in enumerate(unsign_list):

        if not stop_head:
            if c == '{' or c == ',':
                out += c + sign_info[i] + seq
                if sign_info[i] == '"type"':
                    is_type = True
                    i += 1

                elif sign_info[i] == '"value"':
                    stop_head = True
                    start_msg = True
                    msg_keys = MSG_TABLE[msg_type].split(',')
                    i += 1
                    is_type = False
                    continue
                else:
                    i += 1
            else:
                out += c
            if i == len(sign_info):
                # never here in normal
                break

        if is_type:
            if c != ',':
                if c != '{':
                    msg_type += c

        if start_msg:
            if c == '{' or c == ',':
                if msg_keys[j] == ']':
                    j -= element_num
                    out += c
                else:
                    out += c + msg_keys[j] + seq
                    j += 1
            elif c == '[':
                element_num = int(msg_keys[j+1])
                out += c
                j += 2
            elif c == ']':
                out += c
                j += 1
            else:
                out += c
            if j == len(msg_keys):
                start_msg = False
                start_tail = True
                continue

        if start_tail:
            if c == ',':
                out += c + '"sequence"' + seq
            else:
                out += c

    print(out)


if __name__ == "__main__":
    build_sign(s)
