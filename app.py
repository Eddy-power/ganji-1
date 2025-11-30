from flask import Flask, render_template, request, jsonify
from korean_lunar_calendar import KoreanLunarCalendar

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

HEAVENLY_STEMS_KR = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
HEAVENLY_STEMS_CN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
EARTHLY_BRANCHES_KR = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
EARTHLY_BRANCHES_CN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

TIME_NAMES_KR = ['자시', '축시', '인시', '묘시', '진시', '사시', '오시', '미시', '신시', '유시', '술시', '해시']
TIME_NAMES_CN = ['子時', '丑時', '寅時', '卯時', '辰時', '巳時', '午時', '未時', '申時', '酉時', '戌時', '亥時']
TIME_RANGES = ['23:00-01:00', '01:00-03:00', '03:00-05:00', '05:00-07:00', '07:00-09:00', '09:00-11:00',
               '11:00-13:00', '13:00-15:00', '15:00-17:00', '17:00-19:00', '19:00-21:00', '21:00-23:00']

START_STEM_MAP = {
    0: 0, 5: 0,
    1: 2, 6: 2,
    2: 4, 7: 4,
    3: 6, 8: 6,
    4: 8, 9: 8
}

def get_hour_index(hour):
    if hour == 23 or hour == 0:
        return 0
    return ((hour + 1) // 2) % 12

def get_day_stem_index(gapja_string):
    for i, stem in enumerate(HEAVENLY_STEMS_KR):
        if stem + EARTHLY_BRANCHES_KR[0] in gapja_string or any(stem + branch + '일' in gapja_string for branch in EARTHLY_BRANCHES_KR):
            day_part = gapja_string.split()[-1] if gapja_string else ''
            if day_part and len(day_part) >= 2:
                day_stem = day_part[0]
                if day_stem in HEAVENLY_STEMS_KR:
                    return HEAVENLY_STEMS_KR.index(day_stem)
    return 0

def get_day_stem_from_gapja(gapja_string):
    parts = gapja_string.split()
    if len(parts) >= 3:
        day_part = parts[2]
        if len(day_part) >= 1:
            day_stem = day_part[0]
            if day_stem in HEAVENLY_STEMS_KR:
                return HEAVENLY_STEMS_KR.index(day_stem)
    return 0

def calculate_time_gapja(day_stem_index, hour):
    hour_index = get_hour_index(hour)
    start_stem = START_STEM_MAP[day_stem_index]
    time_stem_index = (start_stem + hour_index) % 10
    time_branch_index = hour_index
    
    korean_gapja = HEAVENLY_STEMS_KR[time_stem_index] + EARTHLY_BRANCHES_KR[time_branch_index] + '시'
    chinese_gapja = HEAVENLY_STEMS_CN[time_stem_index] + EARTHLY_BRANCHES_CN[time_branch_index] + '時'
    time_name_kr = TIME_NAMES_KR[hour_index]
    time_name_cn = TIME_NAMES_CN[hour_index]
    time_range = TIME_RANGES[hour_index]
    
    return {
        'korean_gapja': korean_gapja,
        'chinese_gapja': chinese_gapja,
        'time_name_kr': time_name_kr,
        'time_name_cn': time_name_cn,
        'time_range': time_range,
        'hour_index': hour_index
    }

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    year = int(data.get('year'))
    month = int(data.get('month'))
    day = int(data.get('day'))
    hour = int(data.get('hour', 12))
    minute = int(data.get('minute', 0))
    calendar_type = data.get('calendar_type')
    is_intercalation = data.get('is_intercalation', False)
    
    calendar = KoreanLunarCalendar()
    result = {}
    
    try:
        if year < 1880 or year > 2050:
            return jsonify({
                'success': False,
                'error': f'지원 가능한 연도 범위는 1880년~2050년입니다. 입력하신 {year}년은 변환할 수 없습니다.'
            })
        
        if calendar_type == 'solar':
            calendar.setSolarDate(year, month, day)
        else:
            calendar.setLunarDate(year, month, day, is_intercalation)
        
        korean_gapja = calendar.getGapJaString()
        chinese_gapja = calendar.getChineseGapJaString()
        
        day_stem_index = get_day_stem_from_gapja(korean_gapja)
        time_gapja = calculate_time_gapja(day_stem_index, hour)
        
        result = {
            'success': True,
            'input_type': '양력' if calendar_type == 'solar' else ('음력 (윤달)' if is_intercalation else '음력'),
            'input_date': f'{year}년 {month}월 {day}일',
            'input_time': f'{hour:02d}시 {minute:02d}분',
            'solar_date': calendar.SolarIsoFormat(),
            'lunar_date': calendar.LunarIsoFormat(),
            'korean_gapja': korean_gapja,
            'chinese_gapja': chinese_gapja,
            'time_gapja_kr': time_gapja['korean_gapja'],
            'time_gapja_cn': time_gapja['chinese_gapja'],
            'time_name_kr': time_gapja['time_name_kr'],
            'time_name_cn': time_gapja['time_name_cn'],
            'time_range': time_gapja['time_range'],
            'is_intercalation': 'Intercalation' in calendar.LunarIsoFormat() if calendar_type == 'solar' else is_intercalation
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
