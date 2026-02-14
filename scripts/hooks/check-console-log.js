#!/usr/bin/env node

/**
 * ============================================================================
 * 检查 console.log 语句钩子 (Check Console Log Hook)
 * ============================================================================
 *
 * 【用途】
 * 在每次响应后运行，检查修改的 JavaScript/TypeScript 文件中是否包含 console.log 语句。
 * 这是一个 Stop 钩子，帮助开发者在提交代码前记住移除调试语句。
 *
 * 【功能】
 * 1. 检测当前是否在 Git 仓库中
 * 2. 获取已修改的 .ts/.tsx/.js/.jsx 文件列表
 * 3. 扫描每个文件中的 console.log 语句
 * 4. 发现 console.log 时输出警告信息
 *
 * 【使用场景】
 * - 防止调试代码被意外提交
 * - 代码质量检查
 * - 代码审查前的自动检查
 *
 * ============================================================================
 */

const { execSync } = require('child_process');
const fs = require('fs');

let data = '';

// Read stdin
process.stdin.on('data', chunk => {
  data += chunk;
});

process.stdin.on('end', () => {
  try {
    // Check if we're in a git repository
    try {
      execSync('git rev-parse --git-dir', { stdio: 'pipe' });
    } catch {
      // Not in a git repo, just pass through the data
      console.log(data);
      process.exit(0);
    }

    // Get list of modified files
    const files = execSync('git diff --name-only HEAD', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    })
      .split('\n')
      .filter(f => /\.(ts|tsx|js|jsx)$/.test(f) && fs.existsSync(f));

    let hasConsole = false;

    // Check each file for console.log
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      if (content.includes('console.log')) {
        console.error(`[Hook] WARNING: console.log found in ${file}`);
        hasConsole = true;
      }
    }

    if (hasConsole) {
      console.error('[Hook] Remove console.log statements before committing');
    }
  } catch (_error) {
    // Silently ignore errors (git might not be available, etc.)
  }

  // Always output the original data
  console.log(data);
});
