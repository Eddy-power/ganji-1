from flask import Flask, render_template, request, jsonify
from korean_lunar_calendar import KoreanLunarCalendar

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
    calendar_type = data.get('calendar_type')
    is_intercalation = data.get('is_intercalation', False)
    
    calendar = KoreanLunarCalendar()
    result = {}
    
    try:
        if calendar_type == 'solar':
            calendar.setSolarDate(year, month, day)
            result = {
                'success': True,
                'input_type': '양력',
                'input_date': f'{year}년 {month}월 {day}일',
                'solar_date': calendar.SolarIsoFormat(),
                'lunar_date': calendar.LunarIsoFormat(),
                'korean_gapja': calendar.getGapJaString(),
                'chinese_gapja': calendar.getChineseGapJaString(),
                'is_intercalation': 'Intercalation' in calendar.LunarIsoFormat()
            }
        else:
            calendar.setLunarDate(year, month, day, is_intercalation)
            result = {
                'success': True,
                'input_type': '음력' + (' (윤달)' if is_intercalation else ''),
                'input_date': f'{year}년 {month}월 {day}일',
                'solar_date': calendar.SolarIsoFormat(),
                'lunar_date': calendar.LunarIsoFormat(),
                'korean_gapja': calendar.getGapJaString(),
                'chinese_gapja': calendar.getChineseGapJaString(),
                'is_intercalation': is_intercalation
            }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
