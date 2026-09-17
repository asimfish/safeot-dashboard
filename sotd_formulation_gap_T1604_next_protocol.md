# 可直接实现的下一协议草案（未启动，等待本轮残余/烟测裁决）
两臂 independent-admission monitor repair（random）/counterexample repair（ranked）；核心骨架共同固定T1603 gate、N100、2%优化预算、KL.01、PPO及240/144/96真实交互。只比较训练反例场景的选择方式，不改变reward或margin。
每cycle固定原候选后访问1024个训练专用新噪声场景。共同计算每场景max normalized excess；令m=min(20,positive-count)。ranked取前m；random用预定独立PRNG从1024不放回取m。均替换原约束bank末m行，固定容量100、原20前缀不变。若m=0，两臂不二次求解。修复从同一旧actor重新求解，不把原候选当新的KL中心。reward bank仍原100；risk场景变化可改变cost方向，明示这属于同一个场景选择干预。
原候选优化+修复总共200primitive model forwards，每次分别统计reward/cost bank；冻结分配例如原候选最多100，修复最多100，两臂一致。改变原200单次求解资源是共同骨架改变，须先对无修复共同骨架做数值门，不能复用旧T1603当唯一因果对照。若需保留原候选完整200额度，必须预先把两臂统一总额登记400，不能事后追加；本草案优先200且未执行。
修复/原候选集合与安装规则须在执行前冻结，推荐固定middle=修复接受时返回actor，否则原middle；不会增加第四候选。随后共同另一个256独立模型bank资格与原真实选择/accept；PPO仍按gate受资格约束，unsafe old明确记录。搜索、优化、资格、最终测试全部新命名空间，模型费用分开列。
开发小矩阵2任务×3预登记训练seed×2臂，12k真实步/模型，配对312+1024det终评；仅当两task离线门没有数值错误后提交此冻结设计。不得以当前终评轨迹填search bank。报告每seed风险/奖励/有效更新/恢复失败/PPO替代；若以停止学习换安全或奖励退化，HOLD。无新seed确认、native/VLA或额外搜索自动授权。
