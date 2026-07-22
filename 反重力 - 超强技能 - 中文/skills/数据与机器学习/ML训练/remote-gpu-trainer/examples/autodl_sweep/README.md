# 实战示例 — AutoDL 上的 3 单元消融扫描

6 阶段生命周期（SKILL.md）在最深配置（`profiles/autodl.md`）上的完整端到端运行。替换为你自己的项目名、别名和配置。两个实例并行运行各自的队列文件；本演练附带 `queue_1.txt` 并展示一个实例的运行。**先阅读 `profiles/autodl.md`** — 它拥有下面使用的所有路径和命令。

AutoDL 的 `SCRIPT OVERRIDES`（profiles/autodl.md §8）用于参数化模板：

```bash
export PROJECT_REPO_DIR=/root/myproj
export DATA_DIR=/root/autodl-tmp          # 每实例快速暂存（检查点）
export DURABLE_DIR=/root/autodl-fs        # 区域锁定的共享文件系统（释放后存活）
export PROXY_HOOK='source /etc/network_turbo'
export CRED_FILE=/root/.wandb_key
```

### Phase 0 — 环境审计
```bash
ssh autodl-1 'df -h /root/autodl-tmp /root/autodl-fs / && df -i /root/autodl-fs && \
              cat /sys/fs/cgroup/memory.max | numfmt --to=iec && nvidia-smi'
bash scripts/gpu_health.sh 0     # 在机器上运行：Xid / 降频预检（U22/U23）
```
预算磁盘空间：`ckpt_size × cells_in_queue + scratch`。**验证：** `nvidia-smi` 显示预期的 GPU；`df -i /root/autodl-fs` 远低于 100%（inode 上限，U7）。

### Phase 1 — SSH + 凭证
```bash
# 别名已在 ~/.ssh/config 中（references/ssh_transport.md）。通过 stdin 推送 wandb 密钥，
# 写入每实例磁盘 — 绝不写入共享文件系统（U34，且 AutoDL 的分类器会阻断它，AD 陷阱）：
printf '%s\n' "$WANDB_KEY_FROM_ENV" | ssh autodl-1 'umask 077; cat > /root/.wandb_key && chmod 600 /root/.wandb_key'
```
**验证：** `ssh autodl-1 'python -c "import torch;print(torch.cuda.is_available())"'` 输出 `True`。

### Phase 2 — 封装器 + CPU 冒烟门控
```bash
# 参数化模板，去掉 .template 后缀，在租用时间之前先在 CPU 上冒烟测试：
cp scripts/run_one.sh.template run_one.sh && cp scripts/run_queue.sh.template run_queue.sh
python -m src.train -c configs/ablation/baseline.yaml --task reconstruction \
       --limit-batches 2 --epochs 1   # 关闭日志；免费捕获导入/形状/尺度 bug
```
**验证：** 冒烟测试在 2 个批次上以退出码 0 结束。（冒烟*内容* → **必需：** `verifying-dl-experiments`。）

### Phase 3 — 脱离启动
```bash
# 将参数化的封装器 + 队列推送到共享文件系统（一份拷贝，所有实例读取）：
scp run_one.sh run_queue.sh examples/autodl_sweep/queue_1.txt autodl-1:/root/autodl-fs/
ssh autodl-1 "RUN_ONE=/root/autodl-fs/run_one.sh tmux new -d -s q1 \
  'bash /root/autodl-fs/run_queue.sh /root/autodl-fs/queue_1.txt 2>&1 | tee /root/autodl-tmp/runs/logs/q1_master.log'"
```
**60 秒内验证：** `ssh autodl-1 'tmux ls && tail -5 /root/autodl-tmp/runs/logs/q1_master.log'` 显示会话存活且有 `STARTING baseline` 行。运行期间绝不覆盖共享文件系统上的封装器（U2 / 原则 #6）。

### Phase 4 — 持久监控
```bash
ssh autodl-1 'grep -hE "STARTING|FINISHED|QUEUE DONE|ERROR|Traceback" /root/autodl-tmp/runs/logs/q1_master.log | tail -8'
```
对于多小时扫描，部署四层架构（`references/monitoring_patterns.md`）：远程自完成标记 + 会话巡逻循环。对低于典型时长 50% 就 FINISHED 的情况做标记（可能是提前停止），并重新启动**相同**配置（原则 #7），而非打补丁的配置。不要盲目重试。

### Phase 5 — 汇聚 + 验证 + 拆除
```bash
ssh autodl-1 'DATA_DIR=/root/autodl-tmp DURABLE_DIR=/root/autodl-fs bash /root/autodl-fs/aggregate_to_fs.sh'  # 门控同步（U33）
LOCAL_TARGET=/path/to/local/final_ckpts REMOTE_ALIAS=autodl-1 \
  REMOTE_PATH=/root/autodl-fs/final_ckpts bash scripts/download_loop.sh        # 可恢复的按目录拉取
python scripts/verify_local.py /path/to/local/final_ckpts/                     # 加载每个 best.pth
```
**验证：** `verify_local.py` 报告 100% OK。**铁律：** 仅当每个单元都已拉取并加载验证通过且用户批准后，才执行拆除 — 在 AutoDL 上 `关机` 停止计费并保留磁盘（可逆的例外）；`释放` 不可逆地释放。对照花名册核对，而非日志（`references/parallel_ablation.md` §6）。**必需：** `superpowers:verification-before-completion`。
