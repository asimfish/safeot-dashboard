# Astra PsiBot 身份与成绩只读核验

不是所有已有实验都只是Franka。bjxy_5090 `/home/liyufeng/astra_psibot_grasp_e3` 确实有Astra控制原生PsiBot的历史证据，不能被最近FR3七输入消融覆盖或混算。

实际运行 `artifacts/e3_full02/scene_manifest.json` 记录机器人资产：`/mnt/nas/data/safelab/retreat/lyf-back/chembench/psilab/assets/usd/robots/psibot/psibot_normal.usd`，受控腕 `arm2_link7`，右手六维 hand2_joint_link_{1_1,2_1,3_1,4_1,5_1,1_2}；5个从动关节保留原生PhysX mimic。sim_backend加载 `imitation_learning/grasp/scenes/room_cfg.py` 的 `PSI_DC_Grasp_CFG`，不是FR3 pick_place配置。

Astra输入：4RGB、真实robot腕/base pose、arm/hand q/qd/limits、hand语义与mimic、相机实际K/T、simtime、数值执行feedback、自身memory、任务与预算；不含物体真值/接触/抓点轨迹。输出：execute_motion的1–2个**绝对WORLD arm2_link7 EEF pose + 六维手关节rad**，不是现在FR3的relative EEF + 单宽度；通用DLS转7维手臂目标，6维手命令与5个原生mimic。另一只手臂保持初始目标。不能把两种接口当作同一受控消融。

成绩归属：

- **9/10（xhigh放置）是E3-FR3**，来源本地 `astra_e3_continuation_20260910/fr3/FINAL_MESSAGE.md`，不是PsiBot。
- **PsiBot E3稳定抓起3/10**，曾抬升>=50mm为4/10，有效seed9201–9204、9211–9216，每集<=8请求。任务是直立抓取并稳定抬升，不是放置/长程。9205–9208基础设施无效保留，9209/9210未跑。有效总73请求，整个历史81尝试包括无效与未知。报告给出三个成功seed9212/9214/9215。
- PsiBot E2原官方xhigh0/5，E3统一速度口径回评1/5；它不是新的采集成功，原评分不改。

证据边界：本轮只读核机器人实际scene manifest、sim_backend、动作contract和已有评估报告，未重新运行PsiBot或逐帧重验历史全部56视频。源文本与SHA保存于 `psibot_identity/REMOTE_SOURCE_EVIDENCE.json`。上述计数来自Astra实验记录，不来自普通脚本采集总量。主线后续应单独列PsiBot资产、6维手接口和实际新门/新集状态。
