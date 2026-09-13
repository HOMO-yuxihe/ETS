from distutils.command import clean
import json
import re
from pathlib import Path

from utils import strip_html_tags, format_text_with_paragraphs

def parse_json_file(json_path: Path, output_lines: list):
    print(json_path)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # info = data.get('info', {})
        # value = info.get('value', '')
        if data['structure_type']=='collector.read':
            parse_part_a(json_path, output_lines)
        if data['structure_type']=='collector.3q5a':
            parse_part_b(json_path, output_lines)
        if data['structure_type']=='collector.picture':
            parse_part_c(json_path, output_lines)
    except Exception as e:
        output_lines.append(f"【文件读取错误错误】 {e}")

def parse_part_a(json_path: Path, output_lines: list):
    output_lines.append("【PartA 题目原文】")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        raw_value = data['info']['value']
        clean_text = format_text_with_paragraphs(raw_value)
        clean_text = re.sub(r'<[^>]+>', '\n', clean_text)
        output_lines.append(clean_text)
    except Exception as e:
        output_lines.append(f"【PartA 解析错误】 {e}")


def parse_part_b(json_path: Path, output_lines: list):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        origin = data['info']['value']
        clean_origin = format_text_with_paragraphs(origin)
        output_lines.append("【PartB 题目原文】")
        output_lines.append(clean_origin)
    
        questions = data.get('info', {}).get('question', [])
        if not questions:
            output_lines.append("未找到问题列表（info.question）")
            return
        for idx, qa in enumerate(questions, start=1):
            ask = strip_html_tags(qa.get('ask', ''))
            std_list = qa.get('std', [])
            answers = [strip_html_tags(item.get('value', '')) for item in std_list[:3]]

            output_lines.append(f"\n【问题 {idx}】 {ask}")
            output_lines.append("  候选答案：")
            for i, ans in enumerate(answers, start=1):
                lines = ans.splitlines()
                if not lines:
                    output_lines.append(f"    {i}. (空)")
                else:
                    output_lines.append(f"    {i}. {lines[0]}")
                    for line in lines[1:]:
                        output_lines.append(f"       {line}")

            if qa['role']=='a':
                output_lines.append("  回答原文：")
                answer = strip_html_tags(qa.get('answer', ''))
                answer_lines = answer.splitlines()
            
            output_lines.append("")
    except Exception as e:
        output_lines.append(f"【PartB 解析错误】 {e}")


def parse_part_c(json_path: Path, output_lines: list):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        origin = data['info']['value']
        clean_origin = format_text_with_paragraphs(origin)
        output_lines.append("【PartC 题目原文】")
        output_lines.append(clean_origin)

        analyze = data['info']['analyze']
        clean_analyze = format_text_with_paragraphs(analyze)
        output_lines.append("\n【PartC 解析】")
        output_lines.append(clean_analyze)

        answers = [i['value'] for i in data['info']['std']]
        clean_answers = [format_text_with_paragraphs(ans) for ans in answers]
        output_lines.append("\n【PartC 候选答案】")
        for idx, ans in enumerate(clean_answers, start=1):
            output_lines.append(f"  {idx}. {ans.strip()}")
    except Exception as e:
        output_lines.append(f"【PartC 解析错误】 {e}")