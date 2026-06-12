import pandas as pd

df = pd.read_csv('c:/Users/Brian/xundao/spain_2024.csv')
df['date'] = pd.to_datetime(df['date'])
df['total_goals'] = df['target__home_team__full_time_goals'] + df['target__away_team__full_time_goals']

print("=" * 80)
print("  西甲第38轮 (2026-05-24) 四场深度分析")
print("  数据: OCR赔率 + Sports-Betting历史 + Web搜索最新战绩")
print("=" * 80)

# ============================================================
# MATCH 1
# ============================================================
print("""
[第1场] 瓦伦西亚 vs 巴塞罗那  (梅斯塔利亚)
----------------------------------------
盘口 (OCR):
  亚盘: 巴萨 -0.5 (低水~1.01) / 瓦伦 +0.5
  大小: 2.5/3 (大球倾向)
  波胆最低赔: 1-1(7.2) < 0-1(8.7) < 1-2(8.5) < 0-2(11.5)

2025-26:
  巴萨:   第1 | 31W 1D 5L | GF94 GA33 (+61)
  瓦伦:   第9 | 12W 10D 15L | GF43 GA54 (-11)

H2H (近5场):
  2025-09 巴萨 6-0 瓦伦
  2025-02 瓦伦 0-5 巴萨
  2025-01 巴萨 7-1 瓦伦 (国王杯)
  2024-08 瓦伦 1-2 巴萨
  2024-04 巴萨 4-2 瓦伦
  总比分: 巴萨 24-4 瓦伦 (场均5.6球!)
  巴萨对瓦伦连续12场不败，弗里克治下4战全胜 18-1
""")

barca = df[(df['home_team']=='Barcelona') | (df['away_team']=='Barcelona')]
valencia = df[(df['home_team']=='Valencia') | (df['away_team']=='Valencia')]
barca_away_goals = barca[barca['away_team']=='Barcelona']['target__away_team__full_time_goals']
print(f"  [历史] 巴萨客场大2.5率: {(barca[barca['away_team']=='Barcelona']['total_goals']>2.5).mean():.0%}")
print(f"  [历史] 瓦伦主场小2.5率: {(valencia[valencia['home_team']=='Valencia']['total_goals']<=2.5).mean():.0%}")

# MATCH 2
print("""
[第2场] 西班牙人 vs 皇家社会  (RCDE球场)
----------------------------------------
盘口 (OCR):
  亚盘: 皇社 -0.5 (~1.03) / 西班牙人 +0.5 (~0.89)
  大小: 3/3.5 (高盘口，倾向大球!)
  波胆最低赔: 1-1(8.3) < 1-2(8.7) < 2-1(11.5) < 0-2(13.0)

2025-26:
  西班牙人: 第11 | 12W 9D 16L | GF42 GA54 (-12)
  皇社:     第10 | 11W 12D 14L | GF58 GA60 (-2)

近期状态:
  西班牙人: W W L L D (2连胜刚保级，士气↑)
  皇社:     D L D D L (7场不胜!! 4平3负)

H2H:
  2025-08 皇社 2-2 西班牙人
  2025-02 皇社 2-1 西班牙人
  2024-08 西班牙人 0-1 皇社
  近5场H2H: 皇社4胜1平统治
""")

sociedad = df[(df['home_team']=='Sociedad') | (df['away_team']=='Sociedad')]
sociedad_away_gf = sociedad[sociedad['away_team']=='Sociedad']['target__away_team__full_time_goals'].mean()
print(f"  [历史] 皇社客场场均进球: {sociedad_away_gf:.1f}")
print(f"  [历史] 皇社大2.5率: {(sociedad['total_goals']>2.5).mean():.0%}")

# MATCH 3
print("""
[第3场] 马略卡 vs 皇家奥维耶多  (Son Moix)
----------------------------------------
盘口 (OCR):
  亚盘: 马略卡 -0.5/1 (~0.94) / 奥维耶多 +0.5/1 (~0.94)
  大小: 2.5 (均衡水位)
  波胆最低赔: 1-0(6.8) < 2-0(7.8) < 1-1(7.2) < 2-1(8.2)

2025-26:
  马略卡:   第19 | 10W 9D 18L | GF44 GA57 (-13)
  奥维耶多: 第20 | 6W 11D 20L | GF26 GA57 (-31) [已降级!]

近期状态:
  马略卡:   L L D W L (主场5场不败)
  奥维耶多: L L D L L (5场进2球，无战意)

保级生死战! 马略卡差安全区3分，必须赢+看别人脸色
奥维耶多已确定降级回西乙

H2H: 2025-12 奥维耶多 0-0 马略卡
  马略卡主场对奥维耶多12场不败(自1989年)
""")

mallorca = df[(df['home_team']=='Mallorca') | (df['away_team']=='Mallorca')]
print(f"  [历史] 马略卡主场场均进球: {mallorca[mallorca['home_team']=='Mallorca']['target__home_team__full_time_goals'].mean():.1f}")
print(f"  [历史] 马略卡小2.5率: {(mallorca['total_goals']<=2.5).mean():.0%}")

# MATCH 4
print("""
[第4场] 皇家马德里 vs 毕尔巴鄂竞技  (伯纳乌)
----------------------------------------
盘口 (OCR):
  亚盘: 皇马 -1/1.5 (低水~1.05) / 毕尔巴鄂 +1/1.5 (~1.06)
  大小: 3/3.5 (高盘口，倾向大球)
  波胆最低赔: 2-1(8.2) < 2-0(8.5) < 1-0(9.6) < 3-0(11.5)

2025-26:
  皇马:     第2 | 26W 5D 6L | GF73 GA33 (+40)
  毕尔巴鄂: 第12 | 13W 6D 18L | GF41 GA54 (-13)

首循环: 2025-12 毕尔巴鄂 0-3 皇马 (姆巴佩x2, 卡马文加)
历史: 皇马100胜 毕尔巴鄂52胜 平37
""")

rm = df[(df['home_team']=='Real Madrid') | (df['away_team']=='Real Madrid')]
ath = df[(df['home_team']=='Ath Bilbao') | (df['away_team']=='Ath Bilbao')]
h2h_4 = df[((df['home_team']=='Real Madrid') & (df['away_team']=='Ath Bilbao')) |
           ((df['home_team']=='Ath Bilbao') & (df['away_team']=='Real Madrid'))]
print(f"  [历史] 皇马主场场均进球: {rm[rm['home_team']=='Real Madrid']['target__home_team__full_time_goals'].mean():.1f}")
print(f"  [历史] 皇马主场大2.5率: {(rm[rm['home_team']=='Real Madrid']['total_goals']>2.5).mean():.0%}")
print(f"  [历史] 毕尔巴鄂客场场均失球: {ath[ath['away_team']=='Ath Bilbao']['target__home_team__full_time_goals'].mean():.1f}")
if len(h2h_4) > 0:
    for _, row in h2h_4.iterrows():
        print(f"  [历史H2H] {row['date'].strftime('%Y-%m-%d')} {row['home_team']} {int(row['target__home_team__full_time_goals'])}-{int(row['target__away_team__full_time_goals'])} {row['away_team']}")

print("\n" + "=" * 80)
