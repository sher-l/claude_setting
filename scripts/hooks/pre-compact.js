#!/usr/bin/env node

/**
 * ============================================================================
 * 预压缩钩子 (PreCompact Hook)
 * ============================================================================
 *
 * 【用途】
 * 在 Claude 压缩上下文之前运行，提供保存重要状态的机会，
 * 防止在摘要过程中丢失关键信息。
 *
 * 【平台支持】
 * 跨平台支持 (Windows, macOS, Linux)
 *
 * 【功能】
 * 1. 记录压缩事件到日志文件（带时间戳）
 * 2. 如果存在活跃的会话文件，在文件中标记压缩发生的时间
 * 3. 保存状态以便在压缩后恢复上下文
 *
 * 【使用场景】
 * - 防止上下文压缩导致的信息丢失
 * - 追踪会话中的压缩事件
 * - 维护会话连续性记录
 *
 * 【输出文件】
 * - compaction-log.txt: 压缩事件日志
 * - *.tmp: 活跃会话文件（会被标记压缩事件）
 *
 * ============================================================================
 */

const path = require('path');
const {
  getSessionsDir,
  getDateTimeString,
  getTimeString,
  findFiles,
  ensureDir,
  appendFile,
  log
} = require('../lib/utils');

async function main() {
  const sessionsDir = getSessionsDir();
  const compactionLog = path.join(sessionsDir, 'compaction-log.txt');

  ensureDir(sessionsDir);

  // Log compaction event with timestamp
  const timestamp = getDateTimeString();
  appendFile(compactionLog, `[${timestamp}] Context compaction triggered\n`);

  // If there's an active session file, note the compaction
  const sessions = findFiles(sessionsDir, '*.tmp');

  if (sessions.length > 0) {
    const activeSession = sessions[0].path;
    const timeStr = getTimeString();
    appendFile(activeSession, `\n---\n**[Compaction occurred at ${timeStr}]** - Context was summarized\n`);
  }

  log('[PreCompact] State saved before compaction');
  process.exit(0);
}

main().catch(err => {
  console.error('[PreCompact] Error:', err.message);
  process.exit(0);
});
