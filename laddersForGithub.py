import json, os
import urllib.parse

ladders = json.loads(open('ladders.json').read())

s = ''

s += '''# A2OJ-Ladder

| Checkbox | ID  | Name | Problems Count |
|:---:|:---:|:---:|:---:|
'''

problemStrHeader = '''# Ladder Name: {}

| Checkbox | ID  | Problem Name | Online Judge | Difficulty |
|---|:---:|:---:|---|---|
'''

for ladder in ladders:
  s += '|&#9744; Done|{}|[{}]({})|{}|\n'.format(ladder['id'], ladder['name'], 'ladders/{}/README.md'.format(urllib.parse.quote(ladder['name'])), ladder['problemsCount'])

  try:
    os.makedirs('./ladders/{}'.format(ladder['name']))
  except Exception as e:
    pass

  problemStr = problemStrHeader.format(ladder['name'])

  for problem in ladder['problems']:
    problemStr += '|&#9744; Done|{}|[{}]({})|{}|{}|\n'.format(problem['id'], problem['name'], problem['url'], problem['onlineJudge'], problem['difficulty'])

  open('./ladders/{}/README.md'.format(ladder['name']), 'w', encoding = 'utf-8').write(problemStr)

open('README.md', 'w').write(s)