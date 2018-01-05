from flask import Flask
from flask_cors import CORS
from api_collections import *
from api_configurations.config import *


app = Flask(__name__, static_url_path='/static')
CORS(app)

with open("static/assets/js/configs.js", "w") as config_js:
    config_js.write('let address = "'+os.getenv("API_URL")+'"')

# Repos #####


@app.route('/get_languages_repo')
def get_languages_repo():
    return repo_languages(db)


@app.route('/get_commits_repo')
def get_commits_repo():
    return repo_commits(db)


@app.route('/get_members_repo')
def get_members_repo():
    return repo_members(db)


@app.route('/get_best_practices_repo')
def get_best_practices_repo():
    return repo_best_practices(db)


@app.route('/get_issues_repo')
def get_issues_repo():
    return repo_issues(db)


@app.route('/get_repo_name')
def get_repo_name():
    return repo_name(db)

# Orgs ############


@app.route('/get_org_names')
def get_org_names():
    return org_names(db)


@app.route('/get_org_info')
def get_org_info():
    return org_info(db)


@app.route('/get_languages_org')
def get_languages_org():
    return org_languages(db)


@app.route('/get_open_source_org')
def get_open_source_org():
    return org_open_source(db)


@app.route('/get_commits_org')
def get_commits_org():
    return org_commits(db)


@app.route('/get_readme_org')
def get_readme_org():
    return org_readme(db)


@app.route('/get_open_source_readme_org')
def get_open_source_readme_org():
    return open_source_readme_org(db)


@app.route('/get_license_type_org')
def get_license_type_org():
    return org_license(db)


@app.route('/get_issues_org')
def get_issues_org():
    return org_issues(db)


# Teams ###
@app.route('/team_check_with_exist')
def team_check_with_exist():
    return check_with_exist(db)


@app.route('/get_languages_team')
def get_languages_team():
    return team_languages(db)


@app.route('/get_open_source_team')
def get_open_source_team():
    return team_open_source(db)


@app.route('/get_commits_team')
def get_commits_team():
    return team_commits(db)


@app.route('/get_readme_team')
def get_readme_team():
    return team_readme(db)


@app.route('/get_license_type_team')
def get_license_type_team():
    return team_license(db)


@app.route('/get_repo_members_team')
def get_repo_members_team():
    return team_repo_members(db)


@app.route('/get_issues_team')
def get_issues_team():
    return issues_team(db)


@app.route('/get_team_name')
def get_team_name():
    return team_name(db)
# Users #########################


@app.route('/get_avatar')
def get_avatar():
    return avatar(db)


@app.route('/get_user_commit')
def get_user_commit():
    return user_commit(db)


@app.route('/get_user_contributed_repo')
def get_user_contributed_repo():
    return user_contributed_repo(db)


@app.route('/get_user_stats')
def get_user_stats():
    return user_stats(db)


@app.route('/get_user_team')
def get_user_team():
    return user_team(db)


@app.route('/get_user_login')
def get_user_login():
    return user_login(db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT"))

