#!/usr/bin/env python3
"""
本能CLI - 管理持续学习v2的本能 (Instinct CLI - Manage instincts for Continuous Learning v2)

命令(Commands):
  status   - 显示所有本能及其状态
  import   - 从文件或URL导入本能
  export   - 导出本能到文件
  evolve   - 将本能聚类为技能/命令/代理
"""

import argparse
import json
import os
import sys
import re
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional

# ─────────────────────────────────────────────
# 配置 (Configuration)
# ─────────────────────────────────────────────

HOMUNCULUS_DIR = Path.home() / ".claude" / "homunculus"
INSTINCTS_DIR = HOMUNCULUS_DIR / "instincts"
PERSONAL_DIR = INSTINCTS_DIR / "personal"
INHERITED_DIR = INSTINCTS_DIR / "inherited"
EVOLVED_DIR = HOMUNCULUS_DIR / "evolved"
OBSERVATIONS_FILE = HOMUNCULUS_DIR / "observations.jsonl"

# 确保目录存在 (Ensure directories exist)
for d in [PERSONAL_DIR, INHERITED_DIR, EVOLVED_DIR / "skills", EVOLVED_DIR / "commands", EVOLVED_DIR / "agents"]:
    d.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# 本能解析器 (Instinct Parser)
# ─────────────────────────────────────────────

def parse_instinct_file(content: str) -> list[dict]:
    """解析YAML格式的本能文件 (Parse YAML-like instinct file format)."""
    instincts = []
    current = {}
    in_frontmatter = False
    content_lines = []

    for line in content.split('\n'):
        if line.strip() == '---':
            if in_frontmatter:
                # frontmatter结束 - 内容接下来，暂不追加
                in_frontmatter = False
            else:
                # frontmatter开始
                in_frontmatter = True
                if current:
                    current['content'] = '\n'.join(content_lines).strip()
                    instincts.append(current)
                current = {}
                content_lines = []
        elif in_frontmatter:
            # 解析类似YAML的frontmatter
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == 'confidence':
                    current[key] = float(value)
                else:
                    current[key] = value
        else:
            content_lines.append(line)

    # 不要忘记最后一个本能
    if current:
        current['content'] = '\n'.join(content_lines).strip()
        instincts.append(current)

    return [i for i in instincts if i.get('id')]


def load_all_instincts() -> list[dict]:
    """从personal和inherited目录加载所有本能 (Load all instincts from personal and inherited directories)."""
    instincts = []

    for directory in [PERSONAL_DIR, INHERITED_DIR]:
        if not directory.exists():
            continue
        for file in directory.glob("*.yaml"):
            try:
                content = file.read_text()
                parsed = parse_instinct_file(content)
                for inst in parsed:
                    inst['_source_file'] = str(file)
                    inst['_source_type'] = directory.name
                instincts.extend(parsed)
            except Exception as e:
                print(f"警告: 解析{file}失败: {e}", file=sys.stderr)

    return instincts


# ─────────────────────────────────────────────
# 状态命令 (Status Command)
# ─────────────────────────────────────────────

def cmd_status(args):
    """显示所有本能的状态 (Show status of all instincts)."""
    instincts = load_all_instincts()

    if not instincts:
        print("未找到本能。(No instincts found.)")
        print(f"\n本能目录(Instinct directories):")
        print(f"  个人(Personal):  {PERSONAL_DIR}")
        print(f"  继承(Inherited): {INHERITED_DIR}")
        return

    # 按领域分组 (Group by domain)
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get('domain', 'general')
        by_domain[domain].append(inst)

    # 打印标题 (Print header)
    print(f"\n{'='*60}")
    print(f"  本能状态(INSTINCT STATUS) - 共{len(instincts)}个")
    print(f"{'='*60}\n")

    # 按来源汇总 (Summary by source)
    personal = [i for i in instincts if i.get('_source_type') == 'personal']
    inherited = [i for i in instincts if i.get('_source_type') == 'inherited']
    print(f"  个人(Personal):  {len(personal)}")
    print(f"  继承(Inherited): {len(inherited)}")
    print()

    # 按领域打印 (Print by domain)
    for domain in sorted(by_domain.keys()):
        domain_instincts = by_domain[domain]
        print(f"## {domain.upper()} ({len(domain_instincts)})")
        print()

        for inst in sorted(domain_instincts, key=lambda x: -x.get('confidence', 0.5)):
            conf = inst.get('confidence', 0.5)
            conf_bar = '█' * int(conf * 10) + '░' * (10 - int(conf * 10))
            trigger = inst.get('trigger', 'unknown trigger')
            source = inst.get('source', 'unknown')

            print(f"  {conf_bar} {int(conf*100):3d}%  {inst.get('id', 'unnamed')}")
            print(f"            触发器(trigger): {trigger}")

            # 从内容提取行动 (Extract action from content)
            content = inst.get('content', '')
            action_match = re.search(r'## Action\s*\n\s*(.+?)(?:\n\n|\n##|$)', content, re.DOTALL)
            if action_match:
                action = action_match.group(1).strip().split('\n')[0]
                print(f"            行动(action): {action[:60]}{'...' if len(action) > 60 else ''}")

            print()

    # 观察统计 (Observations stats)
    if OBSERVATIONS_FILE.exists():
        obs_count = sum(1 for _ in open(OBSERVATIONS_FILE))
        print(f"─────────────────────────────────────────────────────────")
        print(f"  观察(Observations): 已记录{obs_count}个事件")
        print(f"  文件(File): {OBSERVATIONS_FILE}")

    print(f"\n{'='*60}\n")


# ─────────────────────────────────────────────
# 导入命令 (Import Command)
# ─────────────────────────────────────────────

def cmd_import(args):
    """从文件或URL导入本能 (Import instincts from file or URL)."""
    source = args.source

    # 获取内容 (Fetch content)
    if source.startswith('http://') or source.startswith('https://'):
        print(f"从URL获取(Fetching from URL): {source}")
        try:
            with urllib.request.urlopen(source) as response:
                content = response.read().decode('utf-8')
        except Exception as e:
            print(f"获取URL错误(Error fetching URL): {e}", file=sys.stderr)
            return 1
    else:
        path = Path(source).expanduser()
        if not path.exists():
            print(f"文件未找到(File not found): {path}", file=sys.stderr)
            return 1
        content = path.read_text()

    # 解析本能 (Parse instincts)
    new_instincts = parse_instinct_file(content)
    if not new_instincts:
        print("源中未找到有效本能。(No valid instincts found in source.)")
        return 1

    print(f"\n找到{len(new_instincts)}个本能可导入。\n")

    # 加载现有 (Load existing)
    existing = load_all_instincts()
    existing_ids = {i.get('id') for i in existing}

    # 分类 (Categorize)
    to_add = []
    duplicates = []
    to_update = []

    for inst in new_instincts:
        inst_id = inst.get('id')
        if inst_id in existing_ids:
            # 检查是否应该更新 (Check if we should update)
            existing_inst = next((e for e in existing if e.get('id') == inst_id), None)
            if existing_inst:
                if inst.get('confidence', 0) > existing_inst.get('confidence', 0):
                    to_update.append(inst)
                else:
                    duplicates.append(inst)
        else:
            to_add.append(inst)

    # 按最低置信度过滤 (Filter by minimum confidence)
    min_conf = args.min_confidence or 0.0
    to_add = [i for i in to_add if i.get('confidence', 0.5) >= min_conf]
    to_update = [i for i in to_update if i.get('confidence', 0.5) >= min_conf]

    # 显示摘要 (Display summary)
    if to_add:
        print(f"新增(NEW) ({len(to_add)}):")
        for inst in to_add:
            print(f"  + {inst.get('id')} (置信度(confidence): {inst.get('confidence', 0.5):.2f})")

    if to_update:
        print(f"\n更新(UPDATE) ({len(to_update)}):")
        for inst in to_update:
            print(f"  ~ {inst.get('id')} (置信度(confidence): {inst.get('confidence', 0.5):.2f})")

    if duplicates:
        print(f"\n跳过(SKIP) ({len(duplicates)} - 已存在且置信度相等/更高):")
        for inst in duplicates[:5]:
            print(f"  - {inst.get('id')}")
        if len(duplicates) > 5:
            print(f"  ... 还有{len(duplicates) - 5}个")

    if args.dry_run:
        print("\n[试运行(DRY RUN)] 未做任何更改。")
        return 0

    if not to_add and not to_update:
        print("\n无内容可导入。(Nothing to import.)")
        return 0

    # 确认 (Confirm)
    if not args.force:
        response = input(f"\n导入{len(to_add)}个新本能，更新{len(to_update)}个? [y/N] ")
        if response.lower() != 'y':
            print("已取消。(Cancelled.)")
            return 0

    # 写入继承目录 (Write to inherited directory)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    source_name = Path(source).stem if not source.startswith('http') else 'web-import'
    output_file = INHERITED_DIR / f"{source_name}-{timestamp}.yaml"

    all_to_write = to_add + to_update
    output_content = f"# 从{source}导入(Imported from)\n# 日期(Date): {datetime.now().isoformat()}\n\n"

    for inst in all_to_write:
        output_content += "---\n"
        output_content += f"id: {inst.get('id')}\n"
        output_content += f"trigger: \"{inst.get('trigger', 'unknown')}\"\n"
        output_content += f"confidence: {inst.get('confidence', 0.5)}\n"
        output_content += f"domain: {inst.get('domain', 'general')}\n"
        output_content += f"source: inherited\n"
        output_content += f"imported_from: \"{source}\"\n"
        if inst.get('source_repo'):
            output_content += f"source_repo: {inst.get('source_repo')}\n"
        output_content += "---\n\n"
        output_content += inst.get('content', '') + "\n\n"

    output_file.write_text(output_content)

    print(f"\n✅ 导入完成!(Import complete!)")
    print(f"   新增(Added): {len(to_add)}")
    print(f"   更新(Updated): {len(to_update)}")
    print(f"   保存到(Saved to): {output_file}")

    return 0


# ─────────────────────────────────────────────
# 导出命令 (Export Command)
# ─────────────────────────────────────────────

def cmd_export(args):
    """导出本能到文件 (Export instincts to file)."""
    instincts = load_all_instincts()

    if not instincts:
        print("无本能可导出。(No instincts to export.)")
        return 1

    # 按领域过滤 (Filter by domain if specified)
    if args.domain:
        instincts = [i for i in instincts if i.get('domain') == args.domain]

    # 按最低置信度过滤 (Filter by minimum confidence)
    if args.min_confidence:
        instincts = [i for i in instincts if i.get('confidence', 0.5) >= args.min_confidence]

    if not instincts:
        print("无本能符合条件。(No instincts match the criteria.)")
        return 1

    # 生成输出 (Generate output)
    output = f"# 本能导出(Instincts export)\n# 日期(Date): {datetime.now().isoformat()}\n# 总计(Total): {len(instincts)}\n\n"

    for inst in instincts:
        output += "---\n"
        for key in ['id', 'trigger', 'confidence', 'domain', 'source', 'source_repo']:
            if inst.get(key):
                value = inst[key]
                if key == 'trigger':
                    output += f'{key}: "{value}"\n'
                else:
                    output += f"{key}: {value}\n"
        output += "---\n\n"
        output += inst.get('content', '') + "\n\n"

    # 写入文件或标准输出 (Write to file or stdout)
    if args.output:
        Path(args.output).write_text(output)
        print(f"已导出{len(instincts)}个本能到{args.output}")
    else:
        print(output)

    return 0


# ─────────────────────────────────────────────
# 演化命令 (Evolve Command)
# ─────────────────────────────────────────────

def cmd_evolve(args):
    """分析本能并建议演化为技能/命令/代理 (Analyze instincts and suggest evolutions to skills/commands/agents)."""
    instincts = load_all_instincts()

    if len(instincts) < 3:
        print("需要至少3个本能来分析模式。(Need at least 3 instincts to analyze patterns.)")
        print(f"当前拥有(Currently have): {len(instincts)}")
        return 1

    print(f"\n{'='*60}")
    print(f"  演化分析(EVOLVE ANALYSIS) - {len(instincts)}个本能")
    print(f"{'='*60}\n")

    # 按领域分组 (Group by domain)
    by_domain = defaultdict(list)
    for inst in instincts:
        domain = inst.get('domain', 'general')
        by_domain[domain].append(inst)

    # 高置信度本能按领域（技能候选）(High-confidence instincts by domain - candidates for skills)
    high_conf = [i for i in instincts if i.get('confidence', 0) >= 0.8]
    print(f"高置信度本能(>=80%): {len(high_conf)}")

    # 查找聚类（具有相似触发器的本能）(Find clusters - instincts with similar triggers)
    trigger_clusters = defaultdict(list)
    for inst in instincts:
        trigger = inst.get('trigger', '')
        # 标准化触发器 (Normalize trigger)
        trigger_key = trigger.lower()
        for keyword in ['when', 'creating', 'writing', 'adding', 'implementing', 'testing']:
            trigger_key = trigger_key.replace(keyword, '').strip()
        trigger_clusters[trigger_key].append(inst)

    # 查找有3+本能的聚类（好的技能候选）(Find clusters with 3+ instincts - good skill candidates)
    skill_candidates = []
    for trigger, cluster in trigger_clusters.items():
        if len(cluster) >= 2:
            avg_conf = sum(i.get('confidence', 0.5) for i in cluster) / len(cluster)
            skill_candidates.append({
                'trigger': trigger,
                'instincts': cluster,
                'avg_confidence': avg_conf,
                'domains': list(set(i.get('domain', 'general') for i in cluster))
            })

    # 按聚类大小和置信度排序 (Sort by cluster size and confidence)
    skill_candidates.sort(key=lambda x: (-len(x['instincts']), -x['avg_confidence']))

    print(f"\n发现潜在技能聚类: {len(skill_candidates)}")

    if skill_candidates:
        print(f"\n## 技能候选(SKILL CANDIDATES)\n")
        for i, cand in enumerate(skill_candidates[:5], 1):
            print(f"{i}. 聚类(Cluster): \"{cand['trigger']}\"")
            print(f"   本能(Instincts): {len(cand['instincts'])}")
            print(f"   平均置信度(Avg confidence): {cand['avg_confidence']:.0%}")
            print(f"   领域(Domains): {', '.join(cand['domains'])}")
            print(f"   本能列表(Instincts):")
            for inst in cand['instincts'][:3]:
                print(f"     - {inst.get('id')}")
            print()

    # 命令候选（高置信度工作流本能）(Command candidates - workflow instincts with high confidence)
    workflow_instincts = [i for i in instincts if i.get('domain') == 'workflow' and i.get('confidence', 0) >= 0.7]
    if workflow_instincts:
        print(f"\n## 命令候选(COMMAND CANDIDATES) ({len(workflow_instincts)})\n")
        for inst in workflow_instincts[:5]:
            trigger = inst.get('trigger', 'unknown')
            # 建议命令名称 (Suggest command name)
            cmd_name = trigger.replace('when ', '').replace('implementing ', '').replace('a ', '')
            cmd_name = cmd_name.replace(' ', '-')[:20]
            print(f"  /{cmd_name}")
            print(f"    来自(From): {inst.get('id')}")
            print(f"    置信度(Confidence): {inst.get('confidence', 0.5):.0%}")
            print()

    # 代理候选（复杂多步模式）(Agent candidates - complex multi-step patterns)
    agent_candidates = [c for c in skill_candidates if len(c['instincts']) >= 3 and c['avg_confidence'] >= 0.75]
    if agent_candidates:
        print(f"\n## 代理候选(AGENT CANDIDATES) ({len(agent_candidates)})\n")
        for cand in agent_candidates[:3]:
            agent_name = cand['trigger'].replace(' ', '-')[:20] + '-agent'
            print(f"  {agent_name}")
            print(f"    覆盖{len(cand['instincts'])}个本能")
            print(f"    平均置信度(Avg confidence): {cand['avg_confidence']:.0%}")
            print()

    if args.generate:
        print("\n[将在此生成演化结构(Would generate evolved structures here)]")
        print("  技能将保存到(Skills would be saved to):", EVOLVED_DIR / "skills")
        print("  命令将保存到(Commands would be saved to):", EVOLVED_DIR / "commands")
        print("  代理将保存到(Agents would be saved to):", EVOLVED_DIR / "agents")

    print(f"\n{'='*60}\n")
    return 0


# ─────────────────────────────────────────────
# 主程序 (Main)
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='持续学习v2的本能CLI (Instinct CLI for Continuous Learning v2)')
    subparsers = parser.add_subparsers(dest='command', help='可用命令(Available commands)')

    # 状态 (Status)
    status_parser = subparsers.add_parser('status', help='显示本能状态(Show instinct status)')

    # 导入 (Import)
    import_parser = subparsers.add_parser('import', help='导入本能(Import instincts)')
    import_parser.add_argument('source', help='文件路径或URL(File path or URL)')
    import_parser.add_argument('--dry-run', action='store_true', help='预览而不导入(Preview without importing)')
    import_parser.add_argument('--force', action='store_true', help='跳过确认(Skip confirmation)')
    import_parser.add_argument('--min-confidence', type=float, help='最低置信度阈值(Minimum confidence threshold)')

    # 导出 (Export)
    export_parser = subparsers.add_parser('export', help='导出本能(Export instincts)')
    export_parser.add_argument('--output', '-o', help='输出文件(Output file)')
    export_parser.add_argument('--domain', help='按领域过滤(Filter by domain)')
    export_parser.add_argument('--min-confidence', type=float, help='最低置信度(Minimum confidence)')

    # 演化 (Evolve)
    evolve_parser = subparsers.add_parser('evolve', help='分析并演化本能(Analyze and evolve instincts)')
    evolve_parser.add_argument('--generate', action='store_true', help='生成演化结构(Generate evolved structures)')

    args = parser.parse_args()

    if args.command == 'status':
        return cmd_status(args)
    elif args.command == 'import':
        return cmd_import(args)
    elif args.command == 'export':
        return cmd_export(args)
    elif args.command == 'evolve':
        return cmd_evolve(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main() or 0)
