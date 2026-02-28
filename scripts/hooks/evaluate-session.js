#!/usr/bin/env node

/**
 * ============================================================================
 * 会话评估器钩子 (Session Evaluator Hook)
 * ============================================================================
 *
 * 【用途】
 * 持续学习功能的一部分，在会话结束时从 Claude Code 会话中提取可重用的模式。
 * 这是一个 Stop 钩子，跨平台支持 (Windows, macOS, Linux)。
 *
 * 【为什么使用 Stop 钩子而不是 UserPromptSubmit】
 * - Stop 钩子在会话结束时运行一次（轻量级）
 * - UserPromptSubmit 在每条消息时都会运行（重量级，增加延迟）
 *
 * 【功能】
 * 1. 加载配置文件（可选）
 * 2. 确保学习技能目录存在
 * 3. 从环境变量获取会话转录路径
 * 4. 统计会话中的用户消息数量
 * 5. 跳过过短的会话（默认少于10条消息）
 * 6. 通知 Claude 评估会话以提取可学习模式
 *
 * 【配置文件】
 * 位置: skills/continuous-learning/config.json
 * 参数:
 *   - min_session_length: 最小会话长度（默认10）
 *   - learned_skills_path: 学习技能保存路径
 *
 * ============================================================================
 */

const path = require('path');
const fs = require('fs');
const {
  getLearnedSkillsDir,
  ensureDir,
  readFile,
  countInFile,
  log
} = require('../lib/utils');

async function main() {
  // Get script directory to find config
  const scriptDir = __dirname;
  const configFile = path.join(scriptDir, '..', '..', 'skills', 'continuous-learning', 'config.json');

  // Default configuration
  let minSessionLength = 10;
  let learnedSkillsPath = getLearnedSkillsDir();

  // Load config if exists
  const configContent = readFile(configFile);
  if (configContent) {
    try {
      const config = JSON.parse(configContent);
      minSessionLength = config.min_session_length || 10;

      if (config.learned_skills_path) {
        // Handle ~ in path
        learnedSkillsPath = config.learned_skills_path.replace(/^~/, require('os').homedir());
      }
    } catch {
      // Invalid config, use defaults
    }
  }

  // Ensure learned skills directory exists
  ensureDir(learnedSkillsPath);

  // Get transcript path from environment (set by Claude Code)
  const transcriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;

  if (!transcriptPath || !fs.existsSync(transcriptPath)) {
    process.exit(0);
  }

  // Count user messages in session
  const messageCount = countInFile(transcriptPath, /"type":"user"/g);

  // Skip short sessions
  if (messageCount < minSessionLength) {
    log(`[ContinuousLearning] Session too short (${messageCount} messages), skipping`);
    process.exit(0);
  }

  // Signal to Claude that session should be evaluated for extractable patterns
  log(`[ContinuousLearning] Session has ${messageCount} messages - evaluate for extractable patterns`);
  log(`[ContinuousLearning] Save learned skills to: ${learnedSkillsPath}`);

  process.exit(0);
}

main().catch(err => {
  console.error('[ContinuousLearning] Error:', err.message);
  process.exit(0);
});
