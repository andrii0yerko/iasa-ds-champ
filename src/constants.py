TARGET_COL = ['target_sub_ltv_day30', 'target_iap_ltv_day30', 'target_ad_ltv_day30', 'target_full_ltv_day30']
CATEGORY_COL = ['media_source', 'country_code', 'platform']
DATE_COL = ['install_date']

TS_COLS = {
    'sub': ['app_sub_ltv_day0', 'app_sub_ltv_day1', 'app_sub_ltv_day3'],
    'iap': ['app_iap_ltv_day0', 'app_iap_ltv_day1', 'app_iap_ltv_day3'],
    'ad': ['ad_ltv_day0', 'ad_ltv_day1', 'ad_ltv_day3']
}
TS_TARGET = {
    'sub': 'target_sub_ltv_day30',
    'iap': 'target_iap_ltv_day30',
    'ad': 'target_ad_ltv_day30'
}

daily_cols = ['total_sessions_day', 'chapters_finished_day', 'chapters_opened_day', 'chapters_closed_day', 
               'diamonds_received_day', 'diamonds_spent_day', 'tickets_spent_day']
ret_cols  = ['retained_day']
sessions_cols =  ['chapters_finished_session', 'chapters_opened_session',
                          'chapters_closed_session', 'diamonds_spent_session', 'tickets_spent_session']
trg_daily_cols = ['app_sub_ltv_day', 'app_iap_ltv_day', 'app_iap_ltv_day', 'ad_ltv_day']
daily_days, ret_days, sessions_days, trg_daily_days = [0,1,3,7], [1,3,7], [1,3,9], [0,1,3]