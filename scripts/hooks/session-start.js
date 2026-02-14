#!/usr/bin/env node

/**
 * ============================================================================
 * 会话启动钩子 (Session Start Hook)
 * ============================================================================
 *
 * 【用途】
 * 在新的 Claude 会话开始时运行，检查是否有最近的会话文件
 * 并通知 Claude 可以加载的上下文。
 *
 * 【平台支持】
 * 跨平台支持 (Windows, macOS, Linux)
 *
 * 【功能】
 * 1. 检查最近7天内的会话文件
 * 2. 检查已学习的技能文件
 * 3. 列出可用的会话别名
 * 4. 检测并报告包管理器类型
 * 5. 如果没有包管理器偏好设置，显示选择提示
 *
 * 【会话文件匹配格式】
 * - 旧格式: YYYY-MM-DD-session.tmp
 * - 新格式: YYYY-MM-DD-shortid-session.tmp
 *
 * 【使用场景】
 * - 恢复之前会话的上下文
 * - 加载已学习的技能
 * - 通过别名加载特定会话（使用 /sessions load <alias>）
 *
 * ============================================================================
 */

const {
  getSessionsDir,
  getLearnedSkillsDir,
  findFiles,
  ensureDir,
  log
} = require('../lib/utils');
const { getPackageManager, getSelectionPrompt } = require('../lib/package-manager');
const { listAliases } = require('../lib/session-aliases');

async function main() {
  const sessionsDir = getSessionsDir();
  const learnedDir = getLearnedSkillsDir();

  // Ensure directories exist
  ensureDir(sessionsDir);
  ensureDir(learnedDir);

  // Check for recent session files (last 7 days)
  // Match both old format (YYYY-MM-DD-session.tmp) and new format (YYYY-MM-DD-shortid-session.tmp)
  const recentSessions = findFiles(sessionsDir, '*-session.tmp', { maxAge: 7 });

  if (recentSessions.length > 0) {
    const latest = recentSessions[0];
    log(`[SessionStart] Found ${recentSessions.length} recent session(s)`);
    log(`[SessionStart] Latest: ${latest.path}`);
  }

  // Check for learned skills
  const learnedSkills = findFiles(learnedDir, '*.md');

  if (learnedSkills.length > 0) {
    log(`[SessionStart] ${learnedSkills.length} learned skill(s) available in ${learnedDir}`);
  }

  // Check for available session aliases
  const aliases = listAliases({ limit: 5 });

  if (aliases.length > 0) {
    const aliasNames = aliases.map(a => a.name).join(', ');
    log(`[SessionStart] ${aliases.length} session alias(es) available: ${aliasNames}`);
    log(`[SessionStart] Use /sessions load <alias> to continue a previous session`);
  }

  // Detect and report package manager
  const pm = getPackageManager();
  log(`[SessionStart] Package manager: ${pm.name} (${pm.source})`);

  // If package manager was detected via fallback, show selection prompt
  if (pm.source === 'fallback' || pm.source === 'default') {
    log('[SessionStart] No package manager preference found.');
    log(getSelectionPrompt());
  }

  process.exit(0);
}

main().catch(err => {
  console.error('[SessionStart] Error:', err.message);
  process.exit(0); // Don't block on errors
});
