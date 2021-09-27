import re, os, pathlib
import os.path as pth
from datetime import datetime
import json
from copy import deepcopy

def importBookNote(path):
    lines = []
    indent_levels = []
    is_table = []

    with open(path,'r') as readFile:
        lines = readFile.readlines()
    
    for i,line in enumerate(lines):
        line = parseBolding(line)
        line = parseItalics(line)
        line = parseHighlight(line)
        line = parseLink(line)
        line = parseLinkIcon(line)
        
        line_starts_table = re.search(r'{{\[\[table\]\]}}', line)

        if line_starts_table:
            is_table.append(True)
            line = re.sub(r'{{\[\[table\]\]}}','',line)

        if not line_starts_table:
            is_table.append(False)

        line_is_header = line[:4] == '- ##' or line[:5] == '- <b>'

        if line_is_header:
            line = parseH2Header(line)
            indent_levels.append(0)
        
        if not line_is_header:

            indent_segment_search = re.search('([\s]+)\-\s', line)

            if indent_segment_search:
                indent_segment = indent_segment_search.group(1)
                indent_levels.append(len(indent_segment)//4)
            
            if not indent_segment_search:
                indent_levels.append(0)

            line = removeForwardSegment(line) 
         
        lines[i] = line
    return lines, indent_levels, is_table

def removeForwardSegment(line):
    return re.sub(
                r'^[\s]*\-\s',
                r'',
                line
            )

def parseH2Header(line):
    if line[:5] == '- ###':
        line = line[5:]
    if line[:4] == '- ##':
        line = line[4:]
    if line[:5] =='- <b>':
        line = re.sub(r'</b>','',line)
        line = line[5:]
    return '<h2>{0}</h2>'.format(line)
    

def parseLinkIcon(line):
    return re.sub(
            r'<->',
            r'&#128279;',
            line
        )

def parseLink(line):
    link_pattern = r'\[([^\[\]]+)\]\(([^\(\)]+)\)'

    search_link = re.search(link_pattern,line)
    
    if search_link:
        link_target = search_link.group(2)
    
        target_is_page = link_target[:2] == '[[' and link_target[-2:] == ']]'
    
        if target_is_page:
            return re.sub(link_pattern,r'\1',line)
        
        if not target_is_page:
            return re.sub(link_pattern,r'<a href="\2">\1</a>',line)

    if not search_link:
        return line

def parseHighlight(line):
    return re.sub(
            r'\^\^([^\^]+)\^\^',
            r'<span class="highlight">\1</span>',
            line
        )

def parseItalics(line):
    return re.sub(
            r'__([^_]+)__',
            r'<i>\1</i>',
            line
        )

def parseBolding(line):
    return re.sub(
            r'\*\*([^\*]+)\*\*',
            r'<b>\1</b>',
            line
        )

def toUrlName(title):
    title = re.sub(
        r',\s',
        '_',
        title
    )
    title = re.sub(
        r'\s',
        '-',
        title
    )
    return title

def authorTitleExtract(name):
    parts = name.split(', ')
    title = ', '.join(parts[:-1])
    author = parts[-1]
    return title, author

def processIndents(lines,indent_levels,is_table,dedentFactor=1):
    indent_levels = [max(0,n-dedentFactor) for n in indent_levels]
    prior_indent_level = 0
    table_close_level = None

    for i,line in enumerate(lines):
        current_indent_level = indent_levels[i]
        current_is_table = is_table[i]

        if current_is_table:
            next_is_table = True

            if (table_close_level is None):
                table_close_level = current_indent_level
                line = _startTable(line)
            else:
                if (current_indent_level <= table_close_level):
                    table_close_level = None
                    next_is_table = False
                    line = _endTable(line)
                else:
                    if (current_indent_level > table_close_level):
                        line = _tagTableData(line)
                    if (current_indent_level == table_close_level+1):
                        line = _startNewTableRow(line)

            try:
                is_table[i+1] = next_is_table
            except IndexError:
                pass

        if not current_is_table:
            if current_indent_level > 0:
                line = _tagList(line)
            if current_indent_level == 0:
                line = _tagParagraph(line) 
            if current_indent_level > prior_indent_level:
                line = _indentUnorderedList(prior_indent_level, line, current_indent_level)
            if current_indent_level < prior_indent_level:
                line = _dedentUnorderedList(prior_indent_level, line, current_indent_level)
        
        lines[i] = line
        prior_indent_level = current_indent_level

    lines.append('</ul>'*prior_indent_level)
    return lines

def _startNewTableRow(line):
    return '</tr><tr>' + "\n" + line

def _tagTableData(line):
    return '<td>{0}</td>'.format(line)

def _startTable(line):
    return '<table class="ui table"><tr>' + line

def _endTable(line):
    return  '\n' + '</tr></table>' + line

def _dedentUnorderedList(prior_indent_level, line, current_indent_level):
    return '</ul>'*(prior_indent_level-current_indent_level)+'\n'+line

def _indentUnorderedList(prior_indent_level, line, current_indent_level):
    return '<ul>'*(current_indent_level-prior_indent_level)+'\n'+line

def _tagParagraph(line):
    return '<p>{0}</p>'.format(line)

def _tagList(line):
    return '<li>{0}</li>'.format(line)

def extractScore(lines, indent_levels, is_table):
    score = None
    myMatch = re.match(r'^([0-9]{1,2})\/10',lines[0])
    if myMatch:
        score = myMatch.group(1)
        lines = lines[1:]
        indent_levels = indent_levels[1:]
        is_table = is_table[1:]
    return lines, indent_levels, is_table, score


out_template = (
"""---
bookName: {bookName}
authorName: {authorName}
{scoreline}
layout: booknote
---
{content}
"""
)

now = datetime.now()
default_item_config = {
    'dedentFactor': 1,
    'day': now.day,
    'month': now.month,
    'year': now.year
}

root_path = pth.dirname(__file__)
raw_path = pth.join(root_path, 'raw')
output_path = pth.join(root_path, '..', '_posts')
config_path = pth.join(root_path,'config.json')

config = {}
if pth.exists(config_path):
    with open(config_path,'r') as configFile:
        config = json.loads(configFile.read())

for file in os.listdir(raw_path):
    title = file.split('.')[0]

    thisConfig = {}

    if title in config:
        thisConfig = config[title]
    else:
        thisConfig = deepcopy(default_item_config)
        config[title] = thisConfig

    urlName = toUrlName(title)
    bookName, bookAuthor = authorTitleExtract(title)
    lines, indent_levels, is_table = importBookNote(pth.join(raw_path,file))
    lines, indent_levels, is_table, score = extractScore(lines, indent_levels, is_table)
    lines = processIndents(lines, indent_levels, is_table, dedentFactor=thisConfig['dedentFactor'])

    content = '\n'.join(lines)

    scoreline = ''
    if score is not None:
        scoreline = 'score: {score}'.format(score=score)
        
    output = out_template.format(
        content=content,bookName=bookName, authorName=bookAuthor, scoreline = scoreline,
    )
    
    output_file = pth.join(output_path,'{y}-{m}-{d}-{title}.html'.format(
        d = thisConfig['day'],
        m = thisConfig['month'],
        y = thisConfig['year'],
        title = urlName
    ))
    with open(output_file,'w') as file:
        file.write(output)

with open(config_path,'w') as configFile:
    configFile.write(
        json.dumps(config)
    )








