#!/bin/bash
# 战略压缩建议器 (Strategic Compact Suggester)
# 在PreToolUse时运行或定期建议在逻辑间隔手动压缩
#
# 为什么手动优于自动压缩：
# - 自动压缩在任意点发生，经常在任务中间
# - 战略压缩通过逻辑阶段保留上下文
# - 探索后、执行前压缩
# - 完成里程碑后、开始下一个前压缩
#
# 钩子配置（在~/.claude/settings.json）：
# {
#   "hooks": {
#     "PreToolUse": [{
#       "matcher": "Edit|Write",
#       "hooks": [{
#         "type": "command",
#         "command": "~/.claude/skills/strategic-compact/suggest-compact.sh"
#       }]
#     }]
#   }
# }
#
# 建议压缩的标准：
# - 会话已运行较长时间
# - 进行了大量工具调用
# - 正从研究/探索过渡到实现
# - 计划已确定

# 跟踪工具调用计数（在临时文件中递增）
COUNTER_FILE="/tmp/claude-tool-count-$$"
THRESHOLD=${COMPACT_THRESHOLD:-50}

# 初始化或递增计数器
if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
  count=$((count + 1))
  echo "$count" > "$COUNTER_FILE"
else
  echo "1" > "$COUNTER_FILE"
  count=1
fi

# 在阈值工具调用后建议压缩
if [ "$count" -eq "$THRESHOLD" ]; then
  echo "[StrategicCompact] 已达到 $THRESHOLD 次工具调用 - 如果正在转换阶段，考虑使用 /compact" >&2
fi

# 阈值后定期提醒
if [ "$count" -gt "$THRESHOLD" ] && [ $((count % 25)) -eq 0 ]; then
  echo "[StrategicCompact] $count 次工具调用 - 如果上下文陈旧，这是 /compact 的好检查点" >&2
fi
