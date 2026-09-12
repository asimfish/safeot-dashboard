# FR3 逐决策记录

`manifest.json` 是公开入口，包含14个episode JSON；`shared_contract.json` 保存逐字相同的模型指令、动作schema及中文字段说明。原实验两个seed，共117次请求，含1次provider中断/usage未知。中断集summary.success=null，不能按false计入有效成功率。

每集按决策排序：中文标题 → 当时模型可见policy_observation → 输入图片标签/hash → 原始candidate → 数值执行反馈白名单 → 耗时/token/已知标准等值金额 → 视频时刻映射。S/J/K/F中的null表示当时不可见或尚无反馈；H为前两次图片对应的自身动作历史。所有policy文字均保持原文，模型memory里的位置估计是模型自己写的，不是导出器补入的物体真值。

执行反馈是动作之后的记录，不一定都对该条件下的下一次模型请求可见；是否可见应以其下一份policy_observation为准。例如minus_F不能因为台账展示执行误差就被说成给了模型该误差。

视频映射：observation_sim_time_s是观察时刻；preceding_recorded_frame_index及video_seek_s来自原始同步采样的前一帧。帧率15Hz，观测时刻和录制帧可相差最多1/15秒。相邻帧用于回看，不表示该视频帧就是送给模型的PNG，也不表示视频每帧均为输入。模型实际看到的当前/历史图只以image_evidence标签及已核hash为证。没有批量复制PNG或视频。

视频public_url初始null，由发布方使用episode_id+camera映射到已发布资源。严禁直接发布PRIVATE_SOURCE_INDEX.json、构建脚本或内部目录。只发布本public目录。公开JSON不包含鉴权、请求头、完整provider响应、绝对本地路径、privileged evaluator truth或未经核验的阶段评分。

费用是原usage对应的已知标准等值，不是账户实际扣款。usage_unknown=true时不以0填充费用，累计已知成本只是下界。录制同步通过与任务成功、训练导出验收是不同概念；此处training_export_status=not_exported。
