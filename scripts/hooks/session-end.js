#!/usr/bin/env node

/**
 * ============================================================================
 * 会话结束钩子 (Session End Hook)
 * ============================================================================
 *
 * 【用途】
 * 在 Claude 会话结束时运行，创建/更新会话日志文件，
 * 用于持续性和追踪。
 *
 * 【平台支持】
 * 跨平台支持 (Windows, macOS, Linux)
 *
 * 【功能】
 * 1. 检查是否存在当天的会话文件
 * 2. 如果存在，更新最后修改时间
 * 3. 如果不存在，创建新的会话文件（使用模板）
 * 4. 会话文件名包含日期和短ID以实现唯一性
 *
 * 【会话文件模板内容】
 * - 日期和开始时间
 * - 当前状态区域
 * - 已完成事项清单
 * - 进行中事项清单
 * - 下次会话注意事项
 * - 需要加载的上下文文件列表
 *
 * 【文件命名格式】
 * YYYY-MM-DD-shortid-session.tmp
 *
 * ============================================================================
 */

const path = require('path');
const fs = require('fs');
const {
  getSessionsDir,
  getDateString,
  getTimeString,
  getSessionIdShort,
  ensureDir,
  writeFile,
  replaceInFile,
  log
} = require('../lib/utils');

async function main() {
  const sessionsDir = getSessionsDir();
  const today = getDateString();
  const shortId = getSessionIdShort();
  // Include session ID in filename for unique per-session tracking
  const sessionFile = path.join(sessionsDir, `${today}-${shortId}-session.tmp`);

  ensureDir(sessionsDir);

  const currentTime = getTimeString();

  // If session file exists for today, update the end time
  if (fs.existsSync(sessionFile)) {
    const success = replaceInFile(
      sessionFile,
      /\*\*Last Updated:\*\*.*/,
      `**Last Updated:** ${currentTime}`
    );

    if (success) {
      log(`[SessionEnd] Updated session file: ${sessionFile}`);
    }
  } else {
    // Create new session file with template
    const template = `# Session: ${today}
**Date:** ${today}
**Started:** ${currentTime}
**Last Updated:** ${currentTime}

---

## Current State

[Session context goes here]

### Completed
- [ ]

### In Progress
- [ ]

### Notes for Next Session
-

### Context to Load
\`\`\`
[relevant files]
\`\`\`
`;

    writeFile(sessionFile, template);
    log(`[SessionEnd] Created session file: ${sessionFile}`);
  }

  process.exit(0);
}

main().catch(err => {
  console.error('[SessionEnd] Error:', err.message);
  process.exit(0);
});
