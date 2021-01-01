import json, os
import urllib.parse

ladders = json.loads(open('ladders.json').read())

handle = 'FanTDung20Nam'

s = ''

s += '''# A2OJ-Ladder

### Codeforces handle: {}

| Checkbox | ID  | Name | Problems Count |
|:---:|:---:|:---:|:---:|
'''.format(handle)

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
    checkBox = '&#9744'

    if (problem['onlineJudge'] == 'Codeforces'):
      checkBox = '<img src="https://a2oj.thao.pw/?handle={}&url={}" width="13px"/>'.format(urllib.parse.quote(handle), urllib.parse.quote(problem['url']))

    problemStr += '|{} Done|{}|[{}]({})|{}|{}|\n'.format(checkBox, problem['id'], problem['name'], problem['url'], problem['onlineJudge'], problem['difficulty'])

  open('./ladders/{}/README.md'.format(ladder['name']), 'w', encoding = 'utf-8').write(problemStr)

open('README.md', 'w').write(s)