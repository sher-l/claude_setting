#!/usr/bin/env node

/**
 * ============================================================================
 * 智能压缩建议器钩子 (Strategic Compact Suggester Hook)
 * ============================================================================
 *
 * 【用途】
 * 在 PreToolUse 或定期运行，在逻辑间隔点建议手动压缩上下文。
 *
 * 【平台支持】
 * 跨平台支持 (Windows, macOS, Linux)
 *
 * 【为什么选择手动压缩而非自动压缩】
 * - 自动压缩发生在任意时刻，通常在任务中间
 * - 策略性压缩通过逻辑阶段保留上下文
 * - 在探索后、执行前压缩
 * - 在完成里程碑后、开始下一个任务前压缩
 *
 * 【功能】
 * 1. 跟踪工具调用次数（使用临时文件）
 * 2. 在达到阈值（默认50次）时建议压缩
 * 3. 在阈值之后每隔25次工具调用提醒一次
 * 4. 使用会话特定的计数器文件（基于PID或会话ID）
 *
 * 【配置】
 * - COMPACT_THRESHOLD 环境变量: 设置建议压缩的阈值（默认50）
 *
 * 【使用场景】
 * - 在阶段转换时提醒压缩
 * - 在上下文过时时提醒检查点
 *
 * ============================================================================
 */

const path = require('path');
const {
  getTempDir,
  readFile,
  writeFile,
  log
} = require('../lib/utils');

async function main() {
  // Track tool call count (increment in a temp file)
  // Use a session-specific counter file based on PID from parent process
  // or session ID from environment
  const sessionId = process.env.CLAUDE_SESSION_ID || process.ppid || 'default';
  const counterFile = path.join(getTempDir(), `claude-tool-count-${sessionId}`);
  const threshold = parseInt(process.env.COMPACT_THRESHOLD || '50', 10);

  let count = 1;

  // Read existing count or start at 1
  const existing = readFile(counterFile);
  if (existing) {
    count = parseInt(existing.trim(), 10) + 1;
  }

  // Save updated count
  writeFile(counterFile, String(count));

  // Suggest compact after threshold tool calls
  if (count === threshold) {
    log(`[StrategicCompact] ${threshold} tool calls reached - consider /compact if transitioning phases`);
  }

  // Suggest at regular intervals after threshold
  if (count > threshold && count % 25 === 0) {
    log(`[StrategicCompact] ${count} tool calls - good checkpoint for /compact if context is stale`);
  }

  process.exit(0);
}

main().catch(err => {
  console.error('[StrategicCompact] Error:', err.message);
  process.exit(0);
});
