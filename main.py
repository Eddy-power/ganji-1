from korean_lunar_calendar import KoreanLunarCalendar

calendar = KoreanLunarCalendar()

calendar.setSolarDate(2021, 9, 8) 
print("양력 21년 2월 23일은 음력으로", calendar .LunarIsoFormat(), "입니다")
print(calendar .getGapJaString())
print(calendar.getChineseGapJaString())


# 양력을 음력변환 
#https://pypi.org/project/korean-lunar-calendar/

calendar = KoreanLunarCalendar()
# params : year(년), month(월), day(일)
calendar.setSolarDate(2017, 6, 24)
# Lunar Date (ISO Format)
print(calendar.LunarIsoFormat())
# Korean GapJa String
print(calendar.getGapJaString())
# Chinese GapJa String
print(calendar.getChineseGapJaString())



# 음력을 양력변환 

# params : year(년), month(월), day(일), intercalation(윤달여부)
calendar.setLunarDate(1956, 1, 21, False)
# Solar Date (ISO Format)
print(calendar.SolarIsoFormat())
# Korean GapJa String
print(calendar.getGapJaString())
# Chinese GapJa String
print(calendar.getChineseGapJaString())


calendar = KoreanLunarCalendar()
# params : year(년), month(월), day(일)
calendar.setSolarDate(2019, 9, 22)
# Lunar Date (ISO Format)
print("양력>음력",calendar.LunarIsoFormat(),"입니다.")
# Korean GapJa String
print(calendar.getGapJaString())
# Chinese GapJa String
print(calendar.getChineseGapJaString())
 
# params : year(년), month(월), day(일), intercalation(윤달여부)
calendar.setLunarDate(2019, 9, 22, False)
# Solar Date (ISO Format)
print("음력>양력",calendar.SolarIsoFormat(),"입니다.")
# Korean GapJa String
print(calendar.getGapJaString())
# Chinese GapJa String
print(calendar.getChineseGapJaString())


