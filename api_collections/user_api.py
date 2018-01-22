# from api_configurations.config import *
from api_client.client import *
from api_modules.module import *


def avatar(db):
    name = request.args.get("login")
    query = {'login': name}
    projection = {'_id': 0, 'collection_name': 0}
    query_result = query_find_to_dictionary(db, 'Dev', query, projection)
    if not query_result:
        return json.dumps([{'response': 404}])
    query_result[0]['db_last_updated'] = last_updated_at(query_result[0]['db_last_updated'])
    query_result[0]['response'] = 200
    return json.dumps(query_result)


def user_commit(db):
    name = request.args.get("name")
    start_date = start_day_string_time()
    end_date = end_date_string_time()
    query = [{'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lt': end_date}}},
             {'$group': {
                 '_id': {
                     'year': {'$year': "$committedDate"},
                     'month': {'$month': "$committedDate"},
                     'day': {'$dayOfMonth': "$committedDate"},
                 },
                 'count': {'$sum': 1}
             }},
             {'$project': {'_id': 0, "year": "$_id.year", "month": "$_id.month", "day": "$_id.day", 'count': 1}}
             ]
    delta = end_date - start_date
    commits_count_list = db.Commit.aggregate(query)
    commits_count_list = [dict(i) for i in commits_count_list]
    for commit_count in commits_count_list:
        commit_count['date'] = dt.datetime(commit_count['year'], commit_count['month'], commit_count['day'], 0, 0)
    days = [start_date + dt.timedelta(days=i) for i in range(delta.days + 1)]
    lst = [fill_all_dates(day, commits_count_list) for day in days]
    return json.dumps(lst)


def user_contributed_repo(db):
    name = request.args.get("name")
    start_date = start_day_string_time()
    end_date = end_date_string_time()
    query = [
        {'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group':
                {
                    '_id': {'repoName': "$repoName",
                            'org':  "$org",

                            }
                }
        },
        {'$project': {'_id': 0, "org": "$_id.org", 'repoName': '$_id.repoName'}}
    ]
    # projection = {'_id': 0, 'repoName': 1, 'org': 1}
    query_result = query_aggregate_to_dictionary(db, 'Commit', query)
    # query_result = query_find(db, 'Commit', query, projection).distinct("repoName")
    print(query_result)
    return json.dumps(query_result)


def user_stats(db):
    name = request.args.get("name")
    start_date = start_day_string_time()
    end_date = end_date_string_time()
    delta = end_date - start_date
    query_addttions = [
        {'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group':
                {
                    '_id': {'author': "$author",
                            'year': {'$year': "$committedDate"},
                            'month': {'$month': "$committedDate"},
                            'day': {'$dayOfMonth': "$committedDate"},
                            },
                    'totalAmount': {'$sum': '$additions'}
                }
        },
        {'$project': {'_id': 0, "year": "$_id.year", "month": "$_id.month", "day": "$_id.day", 'author': '$_id.author',
                      'count': '$totalAmount'}}
    ]
    query_deletions = [
        {'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group':
                {
                    '_id': {'author': "$author",
                            'year': {'$year': "$committedDate"},
                            'month': {'$month': "$committedDate"},
                            'day': {'$dayOfMonth': "$committedDate"},
                            },
                    'totalAmount': {'$sum': '$deletions'}
                }
        },
        {'$project': {'_id': 0, "year": "$_id.year", "month": "$_id.month", "day": "$_id.day", 'author': '$_id.author',
                      'count': '$totalAmount'}}
    ]
    additions_list = process_data(db, 'Commit', query_addttions, delta, start_date)
    deletions_list = process_data(db, 'Commit', query_deletions, delta, start_date)
    response = [additions_list, deletions_list]
    return json.dumps(response)


def user_team(db):
    name = request.args.get("name")
    query = [{'$lookup': {
        'from': 'Teams', 'localField': 'to', 'foreignField': '_id', 'as': 'Team'}}
        , {'$lookup': {
            'from': 'Dev', 'localField': 'from', 'foreignField': '_id', 'as': 'Dev'}},
        {
            '$match':
                {"Dev.0.login": name, 'type': 'dev_to_team', 'data.db_last_updated':
                    {'$gte': utc_time_datetime_format(-1)}}
        },
        {'$sort': {'Team.teamName': 1}},
        {'$project': {'_id': 0, "Team.teamName": 1, 'Team.org': 1, 'Team.slug': 1}}
    ]
    result = query_aggregate_to_dictionary(db, 'edges', query)
    result = [x['Team'][0] for x in result]
    return json.dumps(result)


def user_login(db):
    return name_regex_search(db, 'Dev', 'login')


def new_work(db):
    name = request.args.get("name")
    start_date = start_day_string_time()
    end_date = end_date_string_time()
    query = [{'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lt': end_date}}},
             {'$group': {
                 '_id': {'author': "$author"
                         },
                 'additions': {'$sum': '$additions'},
                 'deletions': {'$sum': '$deletions'},
                 'commits': {'$sum': 1},
             }},
             {'$project': {'_id': 0, 'author': '$_id.author',
                           'additions': '$additions', 'deletions': '$deletions', 'commits': '$commits'}}
             ]
    query2 = [{'$match': {'author': name, 'committedDate': {'$gte': start_date, '$lt': end_date}}},
              {'$group': {
                  '_id': {
                      'year': {'$year': "$committedDate"},
                      'month': {'$month': "$committedDate"},
                      'day': {'$dayOfMonth': "$committedDate"},
                  }
              }}
              ]

    commits_count_list = query_aggregate_to_dictionary(db, 'Commit', query)
    total_days_count = len(query_aggregate_to_dictionary(db, 'Commit', query2))
    all_days = [start_date + dt.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    working_days = sum(1 for d in all_days if d.weekday() < 5)
    if not commits_count_list:
        return json.dumps([[{'author': name, 'commits': 0, 'additions': 0, 'deletions': 0}, {'x': -100, 'y': 0}]])
    commits_ratio = int((total_days_count / working_days - 0.5) * 2 * 100)
    value_result = commits_count_list[0]['additions'] - commits_count_list[0]['deletions']
    if value_result >= 0:
        addittions_deletions_ratio = int((value_result / commits_count_list[0]['additions'] - 0.5) * 200)
    else:
        addittions_deletions_ratio = -100
    return json.dumps([[{'author': name, 'commits': commits_count_list[0]['commits'],
                         'additions': commits_count_list[0]['additions'], 'deletions':
                             commits_count_list[0]['deletions']}, {'x': commits_ratio,
                                                                   'y': addittions_deletions_ratio}]])
