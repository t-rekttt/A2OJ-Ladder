import requests, json
from bs4 import BeautifulSoup

class A2OJ:
  def login(self, username, password):
    r = self.s.post('{}/signincode'.format(self.BASE_API), data = {
      'url': '/ladders',
      'Username': username,
      'Password': password
    }, allow_redirects = False)

    assert(r.status_code == 302 and r.headers['Location'] == '/ladders')

  def getLadders(self):
    html = self.s.get('{}/ladders'.format(self.BASE_API)).text

    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table', class_ = 'tablesorter')

    ladders = []

    for table in tables:
      body = table.find('tbody')

      rows = body.find_all('tr')

      for row in rows:
        cols = row.find_all('td')

        colsText = map(lambda item: item.text, cols)

        [_id, name, owner, problemsCount, usersCount, dependsOn] = colsText

        ladders.append({
          'id': _id,
          'name': name,
          'problemsCount': problemsCount
        })

    ladders.sort(key=lambda item: int(item['id']))

    return ladders

  def getProblems(self, ladderId):
    html = self.s.get('{}/ladder'.format(self.BASE_API), params = { 'ID': ladderId }).text

    soup = BeautifulSoup(html)

    table = soup.find('table', class_ = 'tablesorter')

    problems = []

    body = table.find('tbody')

    rows = body.find_all('tr')

    for row in rows:
      cols = row.find_all('td')

      colsText = map(lambda item: item.text, cols)

      assert(len(cols) == 5 or len(cols) == 6)

      if len(cols) == 6:
        [_id, name, onlineJudge, contest, difficulty, dependsOn] = colsText

        problems.append({
          'id': _id,
          'name': name,
          'onlineJudge': onlineJudge,
          'contest': contest,
          'difficulty': difficulty,
          'url': cols[1].find('a')['href']
        })
      else:
        [_id, name, onlineJudge, difficulty, dependsOn] = colsText

        problems.append({
          'id': _id,
          'name': name,
          'onlineJudge': onlineJudge,
          'difficulty': difficulty,
          'url': cols[1].find('a')['href']
        })

    problems.sort(key=lambda item: int(item['id']))

    return problems

  def formatLadderForWindows(self, ladders):
    for i in range(len(ladders)):
      ladders[i]['name'] = ladders[i]['name'] \
        .replace('<= Codeforces Rating <=', 'to') \
        .replace('<', 'before') \
        .replace('>=', 'after') \
        .replace('>', 'after')

    return ladders

  def getAll(self):
    ladders = self.formatLadderForWindows(self.getLadders())

    data = []

    for ladder in ladders:
      problems = self.getProblems(ladder['id'])

      ladder['problems'] = problems

      data.append(ladder)

    return data

  def __init__(self, username, password):
    self.s = requests.session()
    self.s.proxies = { 'http': 'http://localhost:8888', 'https': 'http://localhost:8888' }
    self.s.verify = False
    self.BASE_API = 'https://a2oj.com'

    self.login(username, password)

### To be filled
username = ''
password = ''
###

a2oj = A2OJ(username, password)
open('ladders.json', 'w', encoding='utf-8').write(json.dumps(a2oj.getAll()))