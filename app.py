from flask import Flask, jsonify, request
from flask_api import status
from pymongo import MongoClient
import math

app = Flask(__name__)
client = MongoClient('localhost', 27017, connect=True)
db = client['test']
project = db['project']


def to_dict(obj):
    d = dict(obj)
    d['_id'] = str(d['_id'])
    return d


# @app.route('/project/<id>', methods=['PUT'])
# def update(id):
#     # [Project Phase Actual Start Date, Total Phase Actual Spending Amount]
#     return 'WIP'
    

@app.route('/search/project')
def search():
    args = request.args.to_dict()

    # search by school name or description
    projectSchoolName = args.get('projectSchoolName')
    projectDescription = args.get('projectDescription')
    if projectDescription is None and projectSchoolName is None:
        return jsonify([])

    query = {}
    if projectSchoolName is not None:
        query['Project School Name'] = projectSchoolName
    elif projectDescription is not None:
        query['Project Description'] = projectDescription
    
    # filter by amount [Project Budget Amount]
    budgetAmount = args.get('budgetAmount')
    if budgetAmount is not None:
        query['Project Budget Amount'] = budgetAmount

    # filter by final estimate [Final Estimate of Actual Costs Through End of Phase Amount]
    finalEstimate = args.get('finalEstimate')
    if finalEstimate is not None:
        query['Final Estimate of Actual Costs Through End of Phase Amount'] = int(finalEstimate)

    # filter by total amount [Total Phase Actual Spending Amount]
    totalAmount = args.get('totalAmount')
    if totalAmount is not None:
        query['Total Phase Actual Spending Amount'] = int(totalAmount)

    # filter by date [Project Phase Actual Start Date, Project Phase Planned End Date, Project Phase Actual End Date]
    actualStartDate = args.get('actualStartDate')
    if actualStartDate is not None:
        query['Project Phase Actual Start Date'] = actualStartDate

    plannedEndDate = args.get('plannedEndDate')
    if plannedEndDate is not None:
        query['Project Phase Planned End Date'] = plannedEndDate

    actualEndDate = args.get('actualEndDate')
    if actualEndDate is not None:
        query['Project Phase Actual End Date'] = actualEndDate

    projects = project.find(query)
    
    # pagination WIP
    pageIndex = args.get('pageIndex', 0)
    pageLimit = args.get('pageLimit', 10)
    pageIndex = int(pageIndex)
    pageLimit = int(pageLimit)
    totalEntries = projects.count()
    totalPages = math.ceil(totalEntries / pageLimit)
    skip = pageIndex*pageLimit
    print('skip', skip)

    projects = project.find(query).skip(skip).limit(pageLimit)

    # pdb.set_trace()

    projects_list = list(projects)
    data = [to_dict(p) for p in projects_list]
    return {
        'currentPage': pageIndex,
        'pageLimit': pageLimit,
        'totalPages': totalPages,
        'data': data,
        'totalEntries': totalEntries
    }

app.run(debug=True)