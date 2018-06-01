# -*- coding: UTF-8 -*-
'''
自动生成markdown语法的目录树。
使用方法：
    python auto_catalogue article.md
然后就会自动生成一个article_after.md的文件，其中就包含了所需的目录树。
'''
import sys

filen = sys.argv[1]
orignal = open(filen, 'r', encoding='UTF-8')
content = orignal.readlines()

catalogue = []
after_content = []
for line in content:
    if line.startswith('#'):
        mark, con = line.strip('\n').split(' ', 1)
        space = "    " * (len(mark) - 1)
        link = "- [{0}](#{0})\n".format(con)
        catalogue.append(space + link)
        after_content.append('<a name="{0}"></a>\n'.format(con))
    after_content.append(line)

catalogue.extend(after_content)

out = open(filen.split(".")[0] + "_after.md", 'w', encoding='UTF-8')
out.writelines(catalogue)
out.close()
orignal.close()