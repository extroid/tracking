'''show stats by:

ADSOURCE
ADSOURCE|CAMPAIGN
SITE
OFFERSET
SITE|OFFERSET
CAMPAIGN
CAMPAIGN|ADID

Allow the person to pick checkboxes in order
then create a group by statement with these fields
also pick a date range and time range
also allow to pick days and time slots individually

WHERE DAY IN LIST[1,8,15]
AND HOUR IN LIST[1,2,3,4,5]

SHOW these stats:
clicks, sales, cost, revenue, revenue/click, profit/click

SHOW charts:
hour by hour trend
day by day trend

compare the last X days for this hour range
compare the last X fridays
compare time between 2 snapshots

A snapshot stores the visitor id and all table values outside the visitor
any changes to any table now is updated in a history table
a 2nd snapshot then can be taken to compare the timeframe to analyze the income

=-=-=
LEFT TO DO:
save visitor query
templating with safe view and redirect
exit page tracking
view coupon codes and prices
force domain offersets
stats page
time page load-> offer click time, exit page time, exitoffer click time
grab stats from networks
create a function here that will return the bid price to bid on based on moving average
of todays stats + historical stats




def get_todays_stats(request):
    api_key = '7e02580f43d0645302757bccb8184b46'
    url = 'http://reporting.eadvtracker.com/api.php?'
    type = ('clicks', 'sales', 'test')
    start_date = '2011-02-01'
    end_date = '2011-02-01'
    format = ('csv','tsv','xml','excel','sql')
    nozip = 1
    d = {'key':str(api_key),'type':'test', 'format':'sql','nozip':str(1)}
    query_param = ''
    for p,v in d.items():
        query_param += str(p)+'='+str(v)+'&'
    full_url = str(url)+'?'+str(query_param)
    params = urllib.urlencode(d)
    f = urllib.urlopen(full_url)
    returned_data = f.read()
    x = len(returned_data)
    something = 'nothing'
    return render_to_response('hitpath.html',locals())


class urllibtest:
    api_key = '7e02580f43d0645302757bccb8184b46'
    url = 'http://reporting.eadvtracker.com/api.php'
    type = ('clicks', 'sales', 'test')
    start_date = '2011-02-01'
    end_date = '2011-02-01'
    format = ('csv','tsv','xml','excel','sql')
    nozip = 1
    d = {'key':api_key,'type':'test', 'format':'xml','nozip':1}
    query_param = ''
    for p,v in d.items():
        query_param += str(p)+'='+str(v)+'&'
    full_url = str(url)+'?'+str(query_param)






'''





