class HitPath:
    api_key = '7e02580f43d0645302757bccb8184b46'
    url = 'http://reporting.eadvtracker.com/api.php'
    type = ('clicks', 'sales', 'test')
    start_date = '2011-02-01'
    end_date = '2011-02-01'
    format = ('csv','tsv','xml','excel','sql')
    nozip = 1
    result_dict = {'campaign_id'}
    
    def get_todays_stats(self):
        pass
