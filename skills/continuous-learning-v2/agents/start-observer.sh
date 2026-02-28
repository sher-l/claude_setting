#!/bin/bash
# 持续学习v2 - 观察者代理启动器 (Continuous Learning v2 - Observer Agent Launcher)
#
# 启动分析观察并创建本能的后台观察者代理。
# 使用Haiku模型以节省成本。
#
# 用法(Usage):
#   start-observer.sh        # 后台启动观察者
#   start-observer.sh stop   # 停止运行中的观察者
#   start-observer.sh status # 检查观察者是否在运行

set -e

CONFIG_DIR="${HOME}/.claude/homunculus"
PID_FILE="${CONFIG_DIR}/.observer.pid"
LOG_FILE="${CONFIG_DIR}/observer.log"
OBSERVATIONS_FILE="${CONFIG_DIR}/observations.jsonl"

mkdir -p "$CONFIG_DIR"

case "${1:-start}" in
  stop)
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if kill -0 "$pid" 2>/dev/null; then
        echo "正在停止观察者 (PID: $pid)..."
        kill "$pid"
        rm -f "$PID_FILE"
        echo "观察者已停止。"
      else
        echo "观察者未运行（过期PID文件）。"
        rm -f "$PID_FILE"
      fi
    else
      echo "观察者未运行。"
    fi
    exit 0
    ;;

  status)
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if kill -0 "$pid" 2>/dev/null; then
        echo "观察者正在运行 (PID: $pid)"
        echo "日志(Log): $LOG_FILE"
        echo "观察(Observations): $(wc -l < "$OBSERVATIONS_FILE" 2>/dev/null || echo 0) 行"
        exit 0
      else
        echo "观察者未运行（过期PID文件）"
        rm -f "$PID_FILE"
        exit 1
      fi
    else
      echo "观察者未运行"
      exit 1
    fi
    ;;

  start)
    # 检查是否已在运行
    if [ -f "$PID_FILE" ]; then
      pid=$(cat "$PID_FILE")
      if kill -0 "$pid" 2>/dev/null; then
        echo "观察者已在运行 (PID: $pid)"
        exit 0
      fi
      rm -f "$PID_FILE"
    fi

    echo "正在启动观察者代理..."

    # 观察者循环
    (
      trap 'rm -f "$PID_FILE"; exit 0' TERM INT

      analyze_observations() {
        # 只有在足够观察时才分析
        obs_count=$(wc -l < "$OBSERVATIONS_FILE" 2>/dev/null || echo 0)
        if [ "$obs_count" -lt 10 ]; then
          return
        fi

        echo "[$(date)] 正在分析 $obs_count 个观察..." >> "$LOG_FILE"

        # 使用带Haiku的Claude Code分析观察
        # 这会生成一个快速分析会话
        if command -v claude &> /dev/null; then
          claude --model haiku --max-turns 3 --print \
            "读取 $OBSERVATIONS_FILE 并识别模式。如果你发现同一模式出现3次以上，按照观察者代理规范在 $CONFIG_DIR/instincts/personal/ 创建本能文件。要保守 - 只为清晰模式创建本能。" \
            >> "$LOG_FILE" 2>&1 || true
        fi

        # 归档已处理的观察
        if [ -f "$OBSERVATIONS_FILE" ]; then
          archive_dir="${CONFIG_DIR}/observations.archive"
          mkdir -p "$archive_dir"
          mv "$OBSERVATIONS_FILE" "$archive_dir/processed-$(date +%Y%m%d-%H%M%S).jsonl"
          touch "$OBSERVATIONS_FILE"
        fi
      }

      # 处理SIGUSR1用于按需分析
      trap 'analyze_observations' USR1

      echo "$$" > "$PID_FILE"
      echo "[$(date)] 观察者已启动 (PID: $$)" >> "$LOG_FILE"

      while true; do
        # 每5分钟检查一次
        sleep 300

        analyze_observations
      done
    ) &

    disown

    # 等待PID文件
    sleep 1

    if [ -f "$PID_FILE" ]; then
      echo "观察者已启动 (PID: $(cat "$PID_FILE"))"
      echo "日志(Log): $LOG_FILE"
    else
      echo "启动观察者失败"
      exit 1
    fi
    ;;

  *)
    echo "用法(Usage): $0 {start|stop|status}"
    exit 1
    ;;
esac
