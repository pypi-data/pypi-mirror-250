import asyncio
from multiprocessing import freeze_support, Process
import threading
import glob
from argparse import ArgumentParser
import datetime
import ssl
import numpy as np
import json
import pandas
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# place subfolders below this section:
import py.custom_reasons as cr
from py.functions import topFailedTC, format_df, hyperlink, prepare_failed_table, prepare_tags_table, topFailedReasons, prepare_module_graph, flatten_json, create_summary_pie, create_pie, get_report_details, df_formatter, prepare_device_coverage, get_resources, prepare_custom_failure_graph, generateExcel
from py.html import prepare_html
from py.analytics import generate_advanced_analytics
pandas.options.mode.copy_on_write = True

# Variables
reportTag = ""


def customReporter(client_logo, tags_to_remove, automation_owners, reportTag, loadCsv, analytics_html, analytics):
    truncated = True
    page = 1
    i = 0
    daysOlder = 0
    resources = []
    failurecategorytable, topfailedtc_table, tags_df_table, tags_base64 = "", "", "", ""

    if loadCsv == "":
        resources = get_resources(
            truncated, reportTag, page, daysOlder, resources, jobName, jobNumber, startDate, endDate)

        if len(resources) > 0:
            # update tags - Pools no use
            rem_list = ['uxDuration', 'parameters', 'customFields',
                        'executionEngine', 'selectionCriteriaV2', 'artifacts']
            vid_list = ['startTime', 'endTime', 'format', 'screen']
            platform_list = ['deviceId', 'triggerType',
                             'selectionCriteria', 'selectionCriteriaV2', 'customFields']
            for x in range(len(resources)):
                resources[x]['tags'] = [ele.replace("@", "") for ele in resources[x]["tags"] if not re.compile(
                    r"([0-9a-zA-Z-]){34}|"+tags_to_remove).match(ele)]
                resources[x] = {key: resources[x][key]
                                for key in resources[x] if key not in rem_list}
                if len(resources[x]['videos']) > 0:
                    for v in range(len(resources[x]['videos'][0])):
                        resources[x]['videos'][0] = {key: resources[x]['videos'][0][key]
                                                     for key in resources[x]['videos'][0] if key not in vid_list}
                if len(resources[x]['platforms']) > 0:
                    for v in range(len(resources[x]['platforms'][0])):
                        resources[x]['platforms'][0] = {key: resources[x]['platforms'][0][key]
                                                        for key in resources[x]['platforms'][0] if key not in platform_list}

            jsonDump = json.dumps(resources)
            resources = json.loads(jsonDump)
            print("Total executions: " + str(len(resources)))
            df = pandas.DataFrame([flatten_json(x)
                                  for x in resources])  # no use of pool
            df = format_df(df, jobName, jobNumber, automation_owners)
            # export df to csv
            xl_thread = threading.Thread(target=generateExcel, name="Downloader", args=[
                df])
            xl_thread.start()
        else:
            print("0 test executions")
            exit(0)

    else:
        df = pandas.read_csv(loadCsv, low_memory=False)

    total = df.shape[0]

    # replace failed in cleanException
    if not 'cleanException' in df.columns:
        failure_items, custom_failure_items, failedTable = "", "", ""
    else:
        # don't put the below two methods below hyperlink
        async def do_multiple_tasks():
            return await asyncio.gather(cr.get_failure_reason_category_table(df, total),
                                        topFailedTC(total, df[(df["Status"] == "FAILED")]))
        failurecategorytable, topfailedtc_table = asyncio.run(
            do_multiple_tasks())

        # clean error message
        df = df.reset_index()
        df["cleanException"] = df["cleanException"].fillna("")
        df['cleanException'] = df['cleanException'].str.replace(
            r'\s+failed$|^Step\:And\s+|^Step\:Then\s+|^Step\:Given\s+|^Step\:When\s+', '', regex=True).astype('str')
        df["message"] = df["message"].fillna("")
        df['message'] = df['message'].astype(
            'string').str.replace(r'Step.*\n|.*Error\:|.*Exception\:|\n.*|<[^>]+>|\.\.\.|.*\.xpath\:|.*\.cssSelector\:|.*intercepted\:(\s)+|(\s)+Other element.*|.*locate(\s)+element\:|.*reference\:|.*seconds\:|\: Timed out receiving message.*|\(\d*\.?\d.*seconds\)\.', '', regex=True)

    report_filename = "PerfectReports.html"

    # TODO: make it async - prepares analytics report.
    if (analytics.lower() == "true"):
        # matplotlib.pyplot.switch_backend('Agg')
        profile_thread = Process(target=generate_advanced_analytics, args=(df, client_logo, report_filename, os.path.dirname(
            os.path.abspath(__file__)), analytics_html))
        profile_thread.start()
    else:
        profile_thread = Process()
    if startDate != "":
        # based on descending end time, skiping if latest tests have passed
        trend_df = df.sort_values(by="endTime", ascending=False)
        latest = trend_df.groupby('name').first()
        remove_names = latest.drop(
            latest[latest["Status"] != "PASSED"].index)
        # Remove from trend_df the rows that matches the most recent passed tests names.
        trend_df = trend_df[~trend_df['name'].isin(
            remove_names.index.tolist())]
        # gets latest test name which has above 80% failure rate
        mostfailedNames = []
        for name in trend_df['name'].unique():
            trends = (trend_df[trend_df["name"] == name]['Status'].value_counts(
                normalize=True) * 100).round(2)
            if ('FAILED' in trends.index):
                if trends.get(key='FAILED') > 80:
                    mostfailedNames.append(name)
        lst = [trend_df]
        del trend_df
        del lst
        # get the latest df based on tests names that has above 80% failure rate
        latest = latest[latest.index.isin(mostfailedNames)]
        latest['name'] = latest.index
        latest = latest.drop_duplicates('name', keep='first')
        # fetch AMT to seperate column: #TODO parameterize regex for identifying jira test id
        df['AMT'] = df['name'].str.extract('^([^\s]+)')
        # todo: what do do with these data, add hyperlinks, and then display it?
        print(latest[['Custom Failure Reasons', 'message']])
        # latest[latest['Custom Failure Reasons'] == 'Application Issue'] # -> Raise POTENTIAL BUG

    # hyperlinking name with report link
    df = hyperlink(df, "Result",
                    "reportURL", "name", "", False)

    passed = df[(df["Status"] == "PASSED")].shape[0]
    blocked = df[(df["Status"] == "BLOCKED")].shape[0]
    unknown = df[(df["Status"] == "UNKNOWN")].shape[0]
    failed_df = df[(df["Status"] == "FAILED")]
    failed = failed_df.shape[0]
    failed_blocked = df[(df["Status"] == "FAILED") |
                        (df["Status"] == "BLOCKED")]
    failed_blocked = failed_blocked[~failed_blocked['name'].str.contains(
        "Interactive session")]
    failed_df = failed_df[~failed_df['name'].str.contains(
        "Interactive session")]

    execution_summary = {}
    df.replace(np.nan, '', regex=True)  # important to display all modules
    # prepare Device coverage: don't async
    df, version_items = prepare_device_coverage(df)
    failed_df["Custom Failure Reasons"] = failed_df["Custom Failure Reasons"].fillna(
        'Uncategorized')

    async def do_for_graphs():
        return await asyncio.gather(create_summary_pie(df, "", "Status", "count"),
                                    prepare_custom_failure_graph(
                                        failed_blocked),
                                    prepare_module_graph(df))
    execution_summary, custom_failure_items, tags_base64 = asyncio.run(
        do_for_graphs())
    lst = [failed_blocked]
    del failed_blocked
    del lst
    lst = [df]
    del df
    del lst
    if 'cleanException' in failed_df.columns:
        failed_df = failed_df.rename(
            columns={
                "cleanException": "Failed Steps",
                "message": "Failure Message",
            }
        )

        failed_df['Failed Steps'] = failed_df['Failed Steps'].astype(
            'string').str.replace(r'<[^>]+>|\.\.\.', '', regex=True)

        # create table for failures, pivot tags, prepare failed table
        async def do_if_failures():
            return await asyncio.gather(topFailedReasons(total, failed_df),
                                        prepare_tags_table(
                                            total, failed_df),
                                        prepare_failed_table(failed_df))
        failure_items, tags_df_table, failedTable = asyncio.run(
            do_if_failures())
    lst = [failed_df]
    del failed_df
    del lst
    strTable = prepare_html(client_logo, criteria, total, passed, failed, unknown, blocked, execution_summary,
                            tags_base64, failure_items, custom_failure_items, version_items, tags_df_table, failedTable, topfailedtc_table, analytics_html, failurecategorytable)
    strTable = strTable.replace("<thead>", "<thead class='stuckHead'>")
    if profile_thread.is_alive():
        profile_thread.join()
    with open(report_filename, 'w') as f:
        f.write(strTable)
    print(
        "Report: file://"
        + os.path.join(os.getcwd(), report_filename)
    )
    if xl_thread.is_alive():
        xl_thread.join()


def main():
    tags_to_remove = ""
    automation_owners = ""

    try:
        #     """fix Python SSL CERTIFICATE_VERIFY_FAILED"""
        if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
            ssl, "_create_unverified_context", None
        ):
            ssl._create_default_https_context = ssl._create_unverified_context
        parser = ArgumentParser(
            description="Perfecto Actions Reporter")
        parser.add_argument(
            "-c",
            "--cloud_name",
            metavar="cloud_name",
            help="Perfecto cloud name. (E.g. demo) or add it as a cloudName environment variable",
            nargs="?",
        )
        parser.add_argument(
            "-s",
            "--security_token",
            metavar="security_token",
            type=str,
            help="Perfecto Security Token/ Pass your Perfecto's username and password in user:password format  or add it as a securityToken environment variable",
            nargs="?",
        )
        parser.add_argument(
            "-r",
            "--report",
            type=str,
            metavar="prepares custom report",
            help="creates a custom report.",
            nargs="?",
        )
        parser.add_argument(
            "-l",
            "--logo",
            type=str,
            metavar="customer logo link",
            help="Customer logo link",
            nargs="?",
        )
        parser.add_argument(
            "-remove-tags",
            "--tags_to_remove",
            type=str,
            metavar="Remove Tags",
            help="Tags that needs to be removed from the results",
            nargs="?",
        )
        parser.add_argument(
            "-automation-owners",
            "--automation_owners",
            type=str,
            metavar="Automation Owners",
            help="JSON format of Automation Owners and modules",
            nargs="?",
        )

        args = vars(parser.parse_args())
        try:
            if not args["cloud_name"]:
                print("Loading cloudName: " +
                      os.environ["cloudName"] + " from environment variable.")
            else:
                os.environ["cloudName"] = args["cloud_name"]
        except Exception:
            if not args["cloud_name"]:
                parser.error(
                    "cloud_name parameter is empty. Either Pass the argument -c followed by cloud_name"
                )
                exit
            os.environ["cloudName"] = args["cloud_name"]
        try:
            if not args["security_token"]:
                print("Loading securityToken: " +
                      os.environ["securityToken"] + " from environment variable.")
            else:
                os.environ["securityToken"] = args["security_token"]
        except Exception:
            if not args["security_token"]:
                parser.error(
                    "security_token parameter is empty. Pass the argument -c followed by cloud_name"
                )
            os.environ["securityToken"] = args["security_token"]
        if args["logo"]:
            if str("www.").lower() not in str(args["logo"]).lower():
                raise Exception(
                    "Kindly provide valid client website url. Sample format: www.perfecto.io"
                )
            client_logo = args["logo"]
        else:
            client_logo = "https://www.perforce.com/sites/default/themes/custom/perforce/logo.svg"

        if args["tags_to_remove"]:
            tags_to_remove = args["tags_to_remove"]

        if args["automation_owners"]:
            automation_owners = args["automation_owners"]

        try:
            global criteria
            global jobNumber
            global jobName
            global startDate
            global endDate
            loadCsv = ""
            jobName = ""
            jobNumber = ""
            startDate = ""
            endDate = ""
            temp = ""
            criteria = ""
            reportTag = ""
            analytics_html = "Analytics.html"
            analytics = "true"
            report = args["report"]
            report_array = report.split("|")
            for item in report_array:
                if "report" in item:
                    report, criteria = get_report_details(
                        item, temp, "report", criteria
                    )
                if "jobName" in item:
                    jobName, criteria = get_report_details(
                        item, temp, "jobName", criteria
                    )
                if "jobNumber" in item:
                    jobNumber, criteria = get_report_details(
                        item, temp, "jobNumber", criteria
                    )
                if "startDate" in item:
                    startDate, criteria = get_report_details(
                        item, temp, "startDate", criteria
                    )
                if "endDate" in item:
                    endDate, criteria = get_report_details(
                        item, temp, "endDate", criteria
                    )
                if "reportTag" in item:
                    reportTag, criteria = get_report_details(
                        item, temp, "reportTag", criteria
                    )
                if "loadCsv" in item:
                    loadCsv, criteria = get_report_details(
                        item, temp, "loadCsv", criteria
                    )
                if "analytics" in item:
                    analytics, criteria = get_report_details(
                        item, temp, "analytics", criteria
                    )
        except Exception as e:
            raise Exception(
                "Verify parameters of report, split them by | seperator. Exception: " +
                str(e)
            )
            sys.exit(-1)
        filelist = glob.glob(os.path.join("*.html"))
        for f in filelist:
            os.remove(f)
        if jobName:
            criteria += "JOB: " + jobName.replace(";", "; ").upper() + ", "
        if jobNumber != "":
            criteria += "JOB#: " + \
                jobNumber.replace(";", "; ") + " "
        if reportTag != "":
            criteria += "TAG:" + str(reportTag).upper() + ", "
        if startDate != "":
            if "-" not in startDate:
                criteria += "START: " + str(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(int(int(startDate) / 1000))), "%Y-%m-%d %H:%M:%S")) + \
                    ", END: " + \
                    str(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(
                        int(int(endDate) / 1000))), "%Y-%m-%d %H:%M:%S"))
            else:
                criteria += "START: " + startDate + ", END: " + endDate
        customReporter(client_logo, tags_to_remove, automation_owners,
                       reportTag, loadCsv, analytics_html, analytics)

    except Exception as e:
        raise Exception("Oops!", e)


if __name__ == "__main__":
    freeze_support()
    start_time = datetime.datetime.now().replace(microsecond=0)
    main()
    end = datetime.datetime.now().replace(microsecond=0)
    print("Total Time taken:" + str(end - start_time))
    sys.exit()
