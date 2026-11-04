import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Page Configuration & Custom CSS (Warm Cream & Yellow Tone)
# ---------------------------------------------------------
st.set_page_config(
    page_title="고등학교 과학 공식 모음",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #FFFDF5;
        font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
    }
    html, body, [class*="css"] {
        font-size: 1.15rem;
        color: #333333;
    }
    h1 {
        color: #B8860B !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    h2, h3, h4 {
        color: #8B6508 !important;
        font-weight: 700 !important;
    }
    div.stButton > button {
        background-color: #FFF3CD;
        color: #856404;
        border: 2px solid #FFEEBA;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1.15rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 3px 5px rgba(0,0,0,0.04);
    }
    div.stButton > button:hover {
        background-color: #FFE8A1;
        border-color: #FFE082;
        color: #533F03;
        transform: translateY(-2px);
    }
    .back-btn button {
        background-color: #F8F9FA !important;
        color: #495057 !important;
        border: 1px solid #CED4DA !important;
        width: auto !important;
        padding: 8px 18px !important;
        font-size: 1.05rem !important;
    }
    .formula-box {
        background-color: #FFFFFF;
        border-left: 6px solid #FFC107;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
</style>
""", unsafe_content_html=True)

# ---------------------------------------------------------
# 2. State Management for Navigation
# ---------------------------------------------------------
if 'grade' not in st.session_state:
    st.session_state.grade = None
if 'subject' not in st.session_state:
    st.session_state.subject = None
if 'formula' not in st.session_state:
    st.session_state.formula = None

def reset_to_grade():
    st.session_state.grade = None
    st.session_state.subject = None
    st.session_state.formula = None

def reset_to_subject():
    st.session_state.subject = None
    st.session_state.formula = None

def reset_to_formula_list():
    st.session_state.formula = None

# ---------------------------------------------------------
# 3. Helper Graph Functions
# ---------------------------------------------------------
def linear_graph(a, b, x_label, y_label, title):
    x = np.linspace(0, 10, 100)
    return x, a * x + b, x_label, y_label, title

def inverse_graph(k, x_label, y_label, title):
    x = np.linspace(0.1, 10, 100)
    return x, k / x, x_label, y_label, title

def square_graph(a, x_label, y_label, title):
    x = np.linspace(0, 10, 100)
    return x, a * (x**2), x_label, y_label, title

# ---------------------------------------------------------
# 4. Formula Database (100+ Formulas Across All Subjects)
# ---------------------------------------------------------
FORMULA_DB = {
    "1학년 (통합과학 1·2)": {
        "통합과학": [
            {"name": "1. 평균 속도", "latex": r"\bar{v} = \frac{\Delta s}{\Delta t}", "desc": "변위를 걸린 시간으로 나눈 값입니다.", "vars": {"ds": "변위 (m)", "dt": "시간 (s)"}, "calc": lambda ds, dt: ds / dt, "has_graph": True, "graph_fn": lambda ds, dt: linear_graph(ds/dt, 0, "시간 (s)", "변위 (m)", "시간-변위 그래프")},
            {"name": "2. 가속도", "latex": r"a = \frac{\Delta v}{\Delta t}", "desc": "단위 시간당 속도 변화량입니다.", "vars": {"dv": "속도 변화 (m/s)", "dt": "시간 (s)"}, "calc": lambda dv, dt: dv / dt, "has_graph": True, "graph_fn": lambda dv, dt: linear_graph(dv/dt, 0, "시간 (s)", "속도 (m/s)", "시간-속도 그래프")},
            {"name": "3. 등가속도 나중 속도", "latex": r"v = v_0 + at", "desc": "등가속도 운동에서의 나중 속도입니다.", "vars": {"v0": "초기속도 (m/s)", "a": "가속도 (m/s²)", "t": "시간 (s)"}, "calc": lambda v0, a, t: v0 + a * t, "has_graph": True, "graph_fn": lambda v0, a, t: linear_graph(a, v0, "시간 (s)", "속도 (m/s)", "시간-속도 관계")},
            {"name": "4. 등가속도 변위", "latex": r"s = v_0 t + \frac{1}{2}at^2", "desc": "등가속도 운동 시 이동 거리입니다.", "vars": {"v0": "초기속도 (m/s)", "a": "가속도 (m/s²)", "t": "시간 (s)"}, "calc": lambda v0, a, t: v0 * t + 0.5 * a * (t**2), "has_graph": True, "graph_fn": lambda v0, a, t: square_graph(0.5*a, "시간 (s)", "이동거리 (m)", "시간-거리 곡선")},
            {"name": "5. 시간 제거 속도-거리 식", "latex": r"2as = v^2 - v_0^2", "desc": "시간 t를 제외한 가속도, 거리, 속도 간 식입니다.", "vars": {"v": "나중속도 (m/s)", "v0": "초기속도 (m/s)", "a": "가속도 (m/s²)"}, "calc": lambda v, v0, a: (v**2 - v0**2) / (2 * a), "has_graph": False, "graph_fn": None},
            {"name": "6. 운동량", "latex": r"p = m v", "desc": "물체의 질량과 속도의 곱입니다.", "vars": {"m": "질량 (kg)", "v": "속도 (m/s)"}, "calc": lambda m, v: m * v, "has_graph": True, "graph_fn": lambda m, v: linear_graph(m, 0, "속도 (m/s)", "운동량 (kg·m/s)", "속도-운동량 관계")},
            {"name": "7. 충격량", "latex": r"I = F \Delta t", "desc": "힘과 힘이 작용한 시간의 곱입니다.", "vars": {"F": "힘 (N)", "dt": "시간 (s)"}, "calc": lambda F, dt: F * dt, "has_graph": True, "graph_fn": lambda F, dt: linear_graph(F, 0, "시간 (s)", "충격량 (N·s)", "시간-충격량 관계")},
            {"name": "8. 운동량 보존 법칙", "latex": r"m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'", "desc": "충돌 전후 계의 총 운동량은 일정합니다.", "vars": {"m1": "m1(kg)", "v1": "v1(m/s)", "m2": "m2(kg)", "v2": "v2(m/s)"}, "calc": lambda m1, v1, m2, v2: m1*v1 + m2*v2, "has_graph": False, "graph_fn": None},
            {"name": "9. 중력 위치 에너지", "latex": r"E_p = m g h", "desc": "기준면으로부터의 높이에 따른 위치 에너지입니다.", "vars": {"m": "질량 (kg)", "h": "높이 (m)", "g": "중력가속도 (9.8)"}, "calc": lambda m, h, g=9.8: m * g * h, "has_graph": True, "graph_fn": lambda m, h, g=9.8: linear_graph(m*g, 0, "높이 (m)", "위치에너지 (J)", "높이-위치에너지")},
            {"name": "10. 운동 에너지", "latex": r"E_k = \frac{1}{2}m v^2", "desc": "운동하는 물체가 가지는 에너지입니다.", "vars": {"m": "질량 (kg)", "v": "속도 (m/s)"}, "calc": lambda m, v: 0.5 * m * (v**2), "has_graph": True, "graph_fn": lambda m, v: square_graph(0.5*m, "속도 (m/s)", "운동에너지 (J)", "속도-운동에너지")},
            {"name": "11. 역학적 에너지 보존", "latex": r"E_{total} = E_k + E_p", "desc": "마찰이 없을 때 역학적 에너지는 일정합니다.", "vars": {"Ek": "운동에너지 (J)", "Ep": "위치에너지 (J)"}, "calc": lambda Ek, Ep: Ek + Ep, "has_graph": False, "graph_fn": None},
            {"name": "12. 질량-에너지 등가성", "latex": r"E = m c^2", "desc": "질량이 에너지로 변환되는 비율입니다.", "vars": {"m": "질량 결손 (kg)"}, "calc": lambda m: m * (3e8**2), "has_graph": True, "graph_fn": lambda m: linear_graph(3e8**2, 0, "질량 (kg)", "에너지 (J)", "질량-에너지 관계")},
            {"name": "13. 발전기 전력량", "latex": r"W = P \cdot t", "desc": "소비되거나 생산된 총 전기에너지입니다.", "vars": {"P": "전력 (W)", "t": "시간 (s)"}, "calc": lambda P, t: P * t, "has_graph": True, "graph_fn": lambda P, t: linear_graph(P, 0, "시간 (s)", "전기에너지 (J)", "시간-전기에너지")},
            {"name": "14. 열효율", "latex": r"e = \frac{W}{Q_1} = \frac{Q_1 - Q_2}{Q_1}", "desc": "흡수한 열량 대비 일로 변환된 비율입니다.", "vars": {"Q1": "고열원 열량 (J)", "Q2": "저열원 열량 (J)"}, "calc": lambda Q1, Q2: (Q1 - Q2) / Q1, "has_graph": False, "graph_fn": None},
            {"name": "15. 지구시스템 에너지 수지", "latex": r"E_{in} = E_{out}", "desc": "지구에 들어오는 복사에너지와 나가는 복사에너지는 같습니다.", "vars": {"Ein": "입수에너지"}, "calc": lambda Ein: Ein, "has_graph": False, "graph_fn": None},
            {"name": "16. 변압기 변압비", "latex": r"\frac{V_1}{V_2} = \frac{N_1}{N_2}", "desc": "1차, 2차 코일의 감은 수와 전압의 관계입니다.", "vars": {"V1": "1차전압 (V)", "N1": "1차권선수", "N2": "2차권선수"}, "calc": lambda V1, N1, N2: V1 * (N2 / N1), "has_graph": False, "graph_fn": None},
            {"name": "17. 송전 손실 전력", "latex": r"P_{loss} = I^2 R", "desc": "송전선에서 저항에 의해 손실되는 전력입니다.", "vars": {"I": "송전전류 (A)", "R": "송전선저항 (Ω)"}, "calc": lambda I, R: (I**2) * R, "has_graph": True, "graph_fn": lambda I, R: square_graph(R, "전류 (A)", "손실전력 (W)", "전류-손실전력")},
            {"name": "18. 수소 스펙트럼 에너가지", "latex": r"\Delta E = h f = \frac{hc}{\lambda}", "desc": "전자가 전이할 때 방출/흡수하는 빛의 에너지입니다.", "vars": {"f": "진동수 (Hz)"}, "calc": lambda f: (6.63e-34) * f, "has_graph": False, "graph_fn": None},
            {"name": "19. 중력의 크기", "latex": r"F = m g", "desc": "지표면 근처에서 물체가 받는 중력입니다.", "vars": {"m": "질량 (kg)", "g": "중력가속도 (9.8)"}, "calc": lambda m, g=9.8: m * g, "has_graph": True, "graph_fn": lambda m, g=9.8: linear_graph(g, 0, "질량 (kg)", "중력 (N)", "질량-중력 관계")},
            {"name": "20. 중력장 속 자유낙하 속도", "latex": r"v = g t", "desc": "자유낙하하는 물체의 시간별 속도입니다.", "vars": {"t": "시간 (s)", "g": "중력가속도 (9.8)"}, "calc": lambda t, g=9.8: g * t, "has_graph": True, "graph_fn": lambda t, g=9.8: linear_graph(g, 0, "시간 (s)", "낙하속도 (m/s)", "시간-낙하속도")}
        ]
    },
    "2,3학년 (물리학)": {
        "물리학": [
            {"name": "21. 뉴턴 제2법칙", "latex": r"F = m a", "desc": "알짜힘은 질량과 가속도의 곱입니다.", "vars": {"m": "질량 (kg)", "a": "가속도 (m/s²)"}, "calc": lambda m, a: m * a, "has_graph": True, "graph_fn": lambda m, a: linear_graph(m, 0, "가속도 (m/s²)", "알짜힘 (N)", "가속도-힘 관계")},
            {"name": "22. 만유인력 법칙", "latex": r"F = G \frac{m_1 m_2}{r^2}", "desc": "두 질량체 사이의 거리의 제곱에 반비례하는 인력입니다.", "vars": {"m1": "m1 (kg)", "m2": "m2 (kg)", "r": "거리 (m)"}, "calc": lambda m1, m2, r: (6.67e-11) * m1 * m2 / (r**2), "has_graph": True, "graph_fn": lambda m1, m2, r: inverse_graph((6.67e-11)*m1*m2, "거리 (m)", "만유인력 (N)", "거리-만유인력")},
            {"name": "23. 탄성력 (훅의 법칙)", "latex": r"F = -k x", "desc": "변형된 길이에 비례하여 되돌아가려는 복원력입니다.", "vars": {"k": "용수철상수 (N/m)", "x": "변형길이 (m)"}, "calc": lambda k, x: k * x, "has_graph": True, "graph_fn": lambda k, x: linear_graph(k, 0, "변형길이 (m)", "탄성력 (N)", "변형-탄성력")},
            {"name": "24. 탄성 위치 에너지", "latex": r"E_p = \frac{1}{2}k x^2", "desc": "변형된 용수철에 저장되는 위치 에너지입니다.", "vars": {"k": "용수철상수 (N/m)", "x": "변형길이 (m)"}, "calc": lambda k, x: 0.5 * k * (x**2), "has_graph": True, "graph_fn": lambda k, x: square_graph(0.5*k, "변형길이 (m)", "탄성위치에너지 (J)", "변형-에너지")},
            {"name": "25. 옴의 법칙", "latex": r"V = I R", "desc": "전압은 전류와 저항의 곱입니다.", "vars": {"I": "전류 (A)", "R": "저항 (Ω)"}, "calc": lambda I, R: I * R, "has_graph": True, "graph_fn": lambda I, R: linear_graph(R, 0, "전류 (A)", "전압 (V)", "전류-전압 V-I 특성")},
            {"name": "26. 저항의 직렬합성", "latex": r"R_{total} = R_1 + R_2", "desc": "직렬 연결된 저항의 총 합성 저항입니다.", "vars": {"R1": "R1 (Ω)", "R2": "R2 (Ω)"}, "calc": lambda R1, R2: R1 + R2, "has_graph": False, "graph_fn": None},
            {"name": "27. 저항의 병렬합성", "latex": r"\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2}", "desc": "병렬 연결된 저항의 역수의 합입니다.", "vars": {"R1": "R1 (Ω)", "R2": "R2 (Ω)"}, "calc": lambda R1, R2: (R1 * R2) / (R1 + R2), "has_graph": False, "graph_fn": None},
            {"name": "28. 전기저항과 비저항", "latex": r"R = \rho \frac{L}{A}", "desc": "도선의 길이 L에 비례하고 단면적 A에 반비례합니다.", "vars": {"rho": "비저항", "L": "길이 (m)", "A": "단면적 (m²)"}, "calc": lambda rho, L, A: rho * L / A, "has_graph": True, "graph_fn": lambda rho, L, A: linear_graph(rho/A, 0, "길이 (m)", "저항 (Ω)", "길이-저항 관계")},
            {"name": "29. 소비 전력", "latex": r"P = V I = I^2 R = \frac{V^2}{R}", "desc": "전기 회로에서 단위 시간당 소비되는 에너지입니다.", "vars": {"V": "전압 (V)", "I": "전류 (A)"}, "calc": lambda V, I: V * I, "has_graph": True, "graph_fn": lambda V, I: linear_graph(V, 0, "전류 (A)", "전력 (W)", "전류-전력 관계")},
            {"name": "30. 쿨롱의 법칙", "latex": r"F = k \frac{|q_1 q_2|}{r^2}", "desc": "두 전하 사이에 작용하는 정전기력입니다.", "vars": {"q1": "q1 (C)", "q2": "q2 (C)", "r": "거리 (m)"}, "calc": lambda q1, q2, r: (8.99e9) * abs(q1*q2) / (r**2), "has_graph": True, "graph_fn": lambda q1, q2, r: inverse_graph((8.99e9)*abs(q1*q2), "거리 (m)", "정전기력 (N)", "거리-정전기력")},
            {"name": "31. 파동의 속력", "latex": r"v = f \lambda", "desc": "파동의 속력은 진동수와 파장의 곱입니다.", "vars": {"f": "진동수 (Hz)", "lam": "파장 (m)"}, "calc": lambda f, lam: f * lam, "has_graph": True, "graph_fn": lambda f, lam: linear_graph(f, 0, "파장 (m)", "속력 (m/s)", "파장-속력 관계")},
            {"name": "32. 파동의 주기와 진동수", "latex": r"T = \frac{1}{f}", "desc": "주기와 진동수는 서로 역수 관계입니다.", "vars": {"f": "진동수 (Hz)"}, "calc": lambda f: 1 / f, "has_graph": True, "graph_fn": lambda f: inverse_graph(1, "진동수 (Hz)", "주기 (s)", "진동수-주기")},
            {"name": "33. 스넬의 법칙 (굴절률)", "latex": r"n_1 \sin \theta_1 = n_2 \sin \theta_2", "desc": "빛이 매질 경계면을 통과할 때의 굴절 공식입니다.", "vars": {"n1": "매질1 굴절률", "t1": "입사각(도)"}, "calc": lambda n1, t1: n1 * np.sin(np.radians(t1)), "has_graph": False, "graph_fn": None},
            {"name": "34. 임계각과 전반사", "latex": r"\sin \theta_c = \frac{n_2}{n_1}", "desc": "전반사가 일어나는 최소 입사각입니다.", "vars": {"n1": "매질1 (크다)", "n2": "매질2 (작다)"}, "calc": lambda n1, n2: np.degrees(np.arcsin(n2 / n1)), "has_graph": False, "graph_fn": None},
            {"name": "35. 광자의 에너지", "latex": r"E = h f = \frac{h c}{\lambda}", "desc": "빛의 입자인 광자 한 개가 가진 에너지입니다.", "vars": {"f": "진동수 (Hz)"}, "calc": lambda f: (6.63e-34) * f, "has_graph": True, "graph_fn": lambda f: linear_graph(6.63e-34, 0, "진동수 (Hz)", "광자에너지 (J)", "진동수-에너지")},
            {"name": "36. 광전효과 광전자 최대 운동에너지", "latex": r"E_{k, max} = h f - W", "desc": "금속판에서 튀어나오는 광전자의 최대 운동에너지입니다.", "vars": {"f": "진동수 (Hz)", "W": "일함수 (J)"}, "calc": lambda f, W: (6.63e-34) * f - W, "has_graph": False, "graph_fn": None},
            {"name": "37. 물질파 파장 (드브로이)", "latex": r"\lambda = \frac{h}{p} = \frac{h}{m v}", "desc": "운동하는 입자가 가지는 파동의 파장입니다.", "vars": {"m": "질량 (kg)", "v": "속도 (m/s)"}, "calc": lambda m, v: (6.63e-34) / (m * v), "has_graph": True, "graph_fn": lambda m, v: inverse_graph(6.63e-34/m, "속도 (m/s)", "드브로이 파장 (m)", "속도-드브로이 파장")},
            {"name": "38. 돌림힘 (토크)", "latex": r"\tau = r F \sin \theta", "desc": "물체를 회전시키려는 힘의 효과입니다.", "vars": {"r": "회전축 거리 (m)", "F": "작용 힘 (N)"}, "calc": lambda r, F: r * F, "has_graph": True, "graph_fn": lambda r, F: linear_graph(F, 0, "회전축 거리 (m)", "돌림힘 (N·m)", "거리-돌림힘")},
            {"name": "39. 유체 압력", "latex": r"P = P_0 + \rho g h", "desc": "깊이 h에서의 유체 내부 정수압입니다.", "vars": {"rho": "유체밀도 (kg/m³)", "h": "깊이 (m)"}, "calc": lambda rho, h: 101325 + rho * 9.8 * h, "has_graph": True, "graph_fn": lambda rho, h: linear_graph(rho*9.8, 101325, "깊이 (m)", "유체압력 (Pa)", "깊이-압력")},
            {"name": "40. 베르누이 방정식", "latex": r"P + \frac{1}{2}\rho v^2 + \rho g h = \text{일정}", "desc": "유체 유선상에서 압력과 속도, 높이의 에너지 보존입니다.", "vars": {"P": "압력 (Pa)", "rho": "밀도", "v": "유속 (m/s)"}, "calc": lambda P, rho, v: P + 0.5 * rho * (v**2), "has_graph": False, "graph_fn": None},
            {"name": "41. 부력 (아르키메데스 원리)", "latex": r"F_b = \rho_{fluid} V_{sub} g", "desc": "유체 속 물체가 받는 위쪽 방향의 부력입니다.", "vars": {"rho": "유체밀도 (kg/m³)", "V": "잠긴부피 (m³)"}, "calc": lambda rho, V: rho * V * 9.8, "has_graph": True, "graph_fn": lambda rho, V: linear_graph(rho*9.8, 0, "잠긴부피 (m³)", "부력 (N)", "부피-부력")},
            {"name": "42. 열역학 제1법칙", "latex": r"Q = \Delta U + W", "desc": "기체에 가한 열량은 내부에너지 변화와 일의 합입니다.", "vars": {"dU": "내부에너지 변화 (J)", "W": "기체가 한 일 (J)"}, "calc": lambda dU, W: dU + W, "has_graph": False, "graph_fn": None},
            {"name": "43. 기체가 하는 일", "latex": r"W = P \Delta V", "desc": "등압 과정에서 기체가 팽창할 때 하는 일입니다.", "vars": {"P": "압력 (Pa)", "dV": "부피변화 (m³)"}, "calc": lambda P, dV: P * dV, "has_graph": True, "graph_fn": lambda P, dV: linear_graph(P, 0, "부피변화 (m³)", "한 일 (J)", "부피-일")},
            {"name": "44. 카르노 기관 효율", "latex": r"e_{max} = 1 - \frac{T_C}{T_H}", "desc": "열기관이 가질 수 있는 이론상 최고 열효율입니다.", "vars": {"TH": "고온 절대온도 (K)", "TC": "저온 절대온도 (K)"}, "calc": lambda TH, TC: 1 - (TC / TH), "has_graph": False, "graph_fn": None},
            {"name": "45. 단진자 주기", "latex": r"T = 2\pi \sqrt{\frac{L}{g}}", "desc": "실의 길이 L인 단진자의 진동 주기입니다.", "vars": {"L": "실의 길이 (m)", "g": "중력가속도 (9.8)"}, "calc": lambda L, g=9.8: 2 * np.pi * np.sqrt(L / g), "has_graph": False, "graph_fn": None},
            {"name": "46. 용수철 단진동 주기", "latex": r"T = 2\pi \sqrt{\frac{m}{k}}", "desc": "질량 m과 용수철상수 k에 따른 진동 주기입니다.", "vars": {"m": "질량 (kg)", "k": "용수철상수 (N/m)"}, "calc": lambda m, k: 2 * np.pi * np.sqrt(m / k), "has_graph": False, "graph_fn": None},
            {"name": "47. 케플러 제3법칙 (조화 법칙)", "latex": r"T^2 = a^3", "desc": "행성의 공전 주기의 제곱은 긴반지름의 세제곱에 비례합니다.", "vars": {"a": "궤도 긴반지름 (AU)"}, "calc": lambda a: np.sqrt(a**3), "has_graph": True, "graph_fn": lambda a: (np.linspace(0.1, 10, 100), np.sqrt(np.linspace(0.1, 10, 100)**3), "긴반지름 a (AU)", "공전주기 T (년)", "케플러 제3법칙")},
            {"name": "48. 도플러 효과", "latex": r"f' = f \left( \frac{v \pm v_o}{v \mp v_s} \right)", "desc": "음원이나 관측자의 운동에 의해 변하는 진동수입니다.", "vars": {"f": "원래진동수 (Hz)", "v": "음속 (m/s)", "vs": "음원속도 (m/s)"}, "calc": lambda f, v, vs: f * (v / (v - vs)), "has_graph": False, "graph_fn": None},
            {"name": "49. 로런츠 인자 (특수상대론)", "latex": r"\gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}", "desc": "시간 팽창 및 길이 수축을 결정하는 변환 계수입니다.", "vars": {"v_ratio": "v/c 비율 (0~0.99)"}, "calc": lambda v_ratio: 1 / np.sqrt(1 - v_ratio**2), "has_graph": True, "graph_fn": lambda v_ratio: (np.linspace(0, 0.95, 100), 1/np.sqrt(1-np.linspace(0, 0.95, 100)**2), "v/c 비율", "감마 (γ) 계수", "속도에 따른 상대론적 효과")},
            {"name": "50. 시간 팽창", "latex": r"\Delta t = \gamma \Delta t_0", "desc": "운동하는 관찰자의 시간 흐름이 느려지는 현상입니다.", "vars": {"dt0": "고유시간 (s)", "gamma": "로런츠인자"}, "calc": lambda dt0, gamma: gamma * dt0, "has_graph": False, "graph_fn": None}
        ]
    },
    "2,3학년 (화학)": {
        "화학": [
            {"name": "51. 몰(Mole) 계산", "latex": r"n = \frac{w}{M}", "desc": "질량을 화학식량(분자량)으로 나눈 몰수입니다.", "vars": {"w": "질량 (g)", "M": "분자량 (g/mol)"}, "calc": lambda w, M: w / M, "has_graph": True, "graph_fn": lambda w, M: linear_graph(1/M, 0, "질량 (g)", "몰수 (mol)", "질량-몰수 관계")},
            {"name": "52. 기체 몰수와 부피 (STP)", "latex": r"n = \frac{V}{22.4 \text{ L}}", "desc": "0℃, 1기압에서 기체 부피를 몰수로 변환합니다.", "vars": {"V": "기체 부피 (L)"}, "calc": lambda V: V / 22.4, "has_graph": True, "graph_fn": lambda V: linear_graph(1/22.4, 0, "부피 (L)", "몰수 (mol)", "부피-몰수 관계")},
            {"name": "53. 아보가드로 수와 입자 수", "latex": r"N = n \times N_A", "desc": "몰수와 아보가드로 수(6.02x10^23)의 곱입니다.", "vars": {"n": "몰수 (mol)"}, "calc": lambda n: n * 6.022e23, "has_graph": False, "graph_fn": None},
            {"name": "54. 몰 농도 (Molarity)", "latex": r"M = \frac{n \text{ (mol)}}{V \text{ (L)}}", "desc": "용액 1리터에 들어있는 용질의 몰수입니다.", "vars": {"n": "용질 몰수 (mol)", "V": "용액 부피 (L)"}, "calc": lambda n, V: n / V, "has_graph": True, "graph_fn": lambda n, V: inverse_graph(n, "용액 부피 (L)", "몰 농도 (M)", "부피-몰농도 (희석)")},
            {"name": "55. 몰랄 농도 (Molality)", "latex": r"m = \frac{n \text{ (mol)}}{W \text{ (kg, 용매)}}", "desc": "용매 1kg당 녹아있는 용질의 몰수입니다.", "vars": {"n": "용질 몰수 (mol)", "W": "용매 질량 (kg)"}, "calc": lambda n, W: n / W, "has_graph": False, "graph_fn": None},
            {"name": "56. 퍼센트 농도", "latex": r"\% = \frac{\text{용질 질량 (g)}}{\text{용액 질량 (g)}} \times 100", "desc": "용액 전체 질량에 대한 용질 질량의 백분율입니다.", "vars": {"solute": "용질 질량(g)", "solution": "용액 질량(g)"}, "calc": lambda solute, solution: (solute / solution) * 100, "has_graph": False, "graph_fn": None},
            {"name": "57. 용액 희석 공식", "latex": r"M_1 V_1 = M_2 V_2", "desc": "희석 전후의 용질 몰수는 일정합니다.", "vars": {"M1": "초기농도 (M)", "V1": "초기부피 (L)", "M2": "나중농도 (M)"}, "calc": lambda M1, V1, M2: (M1 * V1) / M2, "has_graph": False, "graph_fn": None},
            {"name": "58. 이상 기체 상태 방정식", "latex": r"P V = n R T", "desc": "기체의 압력, 부피, 몰수, 절대온도의 관계입니다.", "vars": {"n": "몰수 (mol)", "T": "온도 (K)", "V": "부피 (L)"}, "calc": lambda n, T, V: (n * 0.0821 * T) / V, "has_graph": True, "graph_fn": lambda n, T, V: inverse_graph(n*0.0821*T, "부피 (L)", "압력 (atm)", "보일의 법칙 P-V 곡선")},
            {"name": "59. 기체 분자량 산출 식", "latex": r"M = \frac{w R T}{P V} = \frac{\rho R T}{P}", "desc": "기체의 밀도(ρ)나 질량을 통한 분자량 결정 공식입니다.", "vars": {"rho": "밀도 (g/L)", "T": "절대온도 (K)", "P": "압력 (atm)"}, "calc": lambda rho, T, P: (rho * 0.0821 * T) / P, "has_graph": False, "graph_fn": None},
            {"name": "60. 보일의 법칙", "latex": r"P_1 V_1 = P_2 V_2", "desc": "온도가 일정할 때 압력과 부피는 반비례합니다.", "vars": {"P1": "P1 (atm)", "V1": "V1 (L)", "P2": "P2 (atm)"}, "calc": lambda P1, V1, P2: (P1 * V1) / P2, "has_graph": True, "graph_fn": lambda P1, V1, P2: inverse_graph(P1*V1, "부피 (L)", "압력 (atm)", "보일의 법칙")},
            {"name": "61. 샤를의 법칙", "latex": r"\frac{V_1}{T_1} = \frac{V_2}{T_2}", "desc": "압력이 일정할 때 부피는 절대온도에 비례합니다.", "vars": {"V1": "V1 (L)", "T1": "T1 (K)", "T2": "T2 (K)"}, "calc": lambda V1, T1, T2: V1 * (T2 / T1), "has_graph": True, "graph_fn": lambda V1, T1, T2: linear_graph(V1/T1, 0, "온도 (K)", "부피 (L)", "샤를의 법칙 V-T")},
            {"name": "62. 달톤 분압 법칙", "latex": r"P_{total} = P_A + P_B = (n_A + n_B)\frac{RT}{V}", "desc": "혼합 기체의 총 압력은 각 성분 기체의 분압 합입니다.", "vars": {"PA": "A 분압 (atm)", "PB": "B 분압 (atm)"}, "calc": lambda PA, PB: PA + PB, "has_graph": False, "graph_fn": None},
            {"name": "63. 몰 분율", "latex": r"X_A = \frac{n_A}{n_A + n_B}", "desc": "전체 몰수에 대한 성분 A의 몰수 비율입니다.", "vars": {"nA": "A 몰수", "nB": "B 몰수"}, "calc": lambda nA, nB: nA / (nA + nB), "has_graph": False, "graph_fn": None},
            {"name": "64. 그레이엄 확산 법칙", "latex": r"\frac{v_A}{v_B} = \sqrt{\frac{M_B}{M_A}}", "desc": "기체의 확산 속도는 분자량의 제곱근에 반비례합니다.", "vars": {"MA": "A 분자량", "MB": "B 분자량"}, "calc": lambda MA, MB: np.sqrt(MB / MA), "has_graph": False, "graph_fn": None},
            {"name": "65. pH 수소 이온 농도 지수", "latex": r"\text{pH} = -\log_{10}[H^+]", "desc": "수용액 중 수소 이온 농도의 음의 로그값입니다.", "vars": {"H": "[H+] 농도 (M)"}, "calc": lambda H: -np.log10(H), "has_graph": False, "graph_fn": None},
            {"name": "66. 물의 이온화 상수", "latex": r"K_w = [H^+][OH^-] = 1.0 \times 10^{-14} \text{ (25℃)}", "desc": "25℃ 순수한 물의 자가 이온화 곱 상수입니다.", "vars": {"H": "[H+] 농도"}, "calc": lambda H: 1e-14 / H, "has_graph": False, "graph_fn": None},
            {"name": "67. 중화 적정 공식", "latex": r"n M V = n' M' V'", "desc": "산이 내놓은 H+ 몰수와 염기가 내놓은 OH- 몰수는 같습니다.", "vars": {"n": "산 가수", "M": "산 농도(M)", "V": "산 부피(L)", "n2": "염기 가수"}, "calc": lambda n, M, V, n2: (n * M * V) / n2, "has_graph": False, "graph_fn": None},
            {"name": "68. 반응 열량 계산", "latex": r"Q = C \cdot m \cdot \Delta T", "desc": "비열, 질량, 온도 변화를 통한 열량 측정입니다.", "vars": {"C": "비열 (J/g·℃)", "m": "질량 (g)", "dT": "온도변화 (℃)"}, "calc": lambda C, m, dT: C * m * dT, "has_graph": True, "graph_fn": lambda C, m, dT: linear_graph(C*m, 0, "온도변화 (℃)", "열량 (J)", "온도변화-열량")},
            {"name": "69. 헤스 법칙 (반응열 합)", "latex": r"\Delta H_{total} = \Delta H_1 + \Delta H_2", "desc": "반응 엔탈피 변화는 경로에 상관없이 일정합니다.", "vars": {"H1": "H1 (kJ)", "H2": "H2 (kJ)"}, "calc": lambda H1, H2: H1 + H2, "has_graph": False, "graph_fn": None},
            {"name": "70. 반응 속도식", "latex": r"v = k [A]^m [B]^n", "desc": "반응물 농도와 반응 속도 상수의 관계입니다.", "vars": {"k": "속도상수", "A": "농도 A (M)"}, "calc": lambda k, A: k * (A**1), "has_graph": True, "graph_fn": lambda k, A: linear_graph(k, 0, "농도 [A] (M)", "반응속도", "농도-반응속도 1차반응")},
            {"name": "71. 평형 상수", "latex": r"K = \frac{[C]^c [D]^d}{[A]^a [B]^b}", "desc": "가역 반응에서 화학 평형 시 생성물과 반응물의 농도 비입니다.", "vars": {"C": "생성물 C 농도", "A": "반응물 A 농도"}, "calc": lambda C, A: C / A, "has_graph": False, "graph_fn": None},
            {"name": "72. 삼투압 (반트호프 식)", "latex": r"\Pi = M R T", "desc": "묽은 용액의 삼투압은 몰농도와 절대온도에 비례합니다.", "vars": {"M": "몰농도 (M)", "T": "절대온도 (K)"}, "calc": lambda M, T: M * 0.0821 * T, "has_graph": True, "graph_fn": lambda M, T: linear_graph(0.0821*T, 0, "몰농도 (M)", "삼투압 (atm)", "농도-삼투압")},
            {"name": "73. 끓는점 오름", "latex": r"\Delta T_b = K_b \cdot m", "desc": "비휘발성 용질에 의한 끓는점 상승 정도입니다.", "vars": {"Kb": "몰랄 오름 상수", "m": "몰랄 농도"}, "calc": lambda Kb, m: Kb * m, "has_graph": True, "graph_fn": lambda Kb, m: linear_graph(Kb, 0, "몰랄농도 (m)", "끓는점오름 (℃)", "농도-끓는점오름")},
            {"name": "74. 어는점 내림", "latex": r"\Delta T_f = K_f \cdot m", "desc": "용액의 어는점이 강하하는 정도입니다.", "vars": {"Kf": "몰랄 내림 상수", "m": "몰랄 농도"}, "calc": lambda Kf, m: Kf * m, "has_graph": True, "graph_fn": lambda Kf, m: linear_graph(Kf, 0, "몰랄농도 (m)", "어는점내림 (℃)", "농도-어는점내림")},
            {"name": "75. 라울의 법칙 (증기압 내림)", "latex": r"P_{solution} = X_{solvent} \cdot P^\circ_{solvent}", "desc": "용액의 증기압은 용매 몰분율과 순수 증기압의 곱입니다.", "vars": {"X": "용매 몰분율", "P0": "순수 증기압"}, "calc": lambda X, P0: X * P0, "has_graph": False, "graph_fn": None}
        ]
    },
    "2,3학년 (생물과학)": {
        "생물과학": [
            {"name": "76. 하디-바인베르크 대립유전자 빈도", "latex": r"p + q = 1", "desc": "두 대립유전자 P와 Q의 빈도 총합은 1입니다.", "vars": {"p": "대립유전자 p 빈도"}, "calc": lambda p: 1 - p, "has_graph": False, "graph_fn": None},
            {"name": "77. 하디-바인베르크 유전자형 빈도", "latex": r"p^2 + 2pq + q^2 = 1", "desc": "평형 집단에서의 유전자형 조합 비율입니다.", "vars": {"p": "p 빈도 (0~1)"}, "calc": lambda p: (p**2, 2*p*(1-p), (1-p)**2), "has_graph": True, "graph_fn": lambda p: (np.linspace(0, 1, 100), np.linspace(0, 1, 100)**2, "대립유전자 p", "p^2 빈도", "유전자 빈도 그래프")},
            {"name": "78. 개체군 로지스틱 생장 모델", "latex": r"\frac{dN}{dt} = r N \left( \frac{K - N}{K} \right)", "desc": "환경 수용 능력 K를 고려한 개체수 생장율 공식입니다.", "vars": {"r": "증가율", "N": "개체수", "K": "수용능력"}, "calc": lambda r, N, K: r * N * ((K - N) / K), "has_graph": False, "graph_fn": None},
            {"name": "79. 개체군 지수 생장 모델", "latex": r"N_t = N_0 e^{rt}", "desc": "환경 저항이 없을 때 무제한 생장하는 지수 모델입니다.", "vars": {"N0": "초기 개체수", "r": "증가율", "t": "시간"}, "calc": lambda N0, r, t: N0 * np.exp(r * t), "has_graph": True, "graph_fn": lambda N0, r, t: (np.linspace(0, 10, 100), N0 * np.exp(r * np.linspace(0, 10, 100)), "시간 (t)", "개체수 N", "지수 생장 곡선")},
            {"name": "80. 에너지 효율", "latex": r"\text{효율(\%)} = \frac{\text{현 영양단계 에너지}}{\text{전 영양단계 에너지}} \times 100", "desc": "영양 단계간 에너지 이동 효율입니다.", "vars": {"E_curr": "현 단계 (kcal)", "E_prev": "전 단계 (kcal)"}, "calc": lambda E_curr, E_prev: (E_curr / E_prev) * 100, "has_graph": False, "graph_fn": None},
            {"name": "81. 포획-재포획법 개체수 추정", "latex": r"N = \frac{M \cdot C}{R}", "desc": "표지 재포획법을 이용한 전체 개체수 N 추정입니다.", "vars": {"M": "1차 표지수", "C": "2차 포획수", "R": "2차 표지확인수"}, "calc": lambda M, C, R: (M * C) / R, "has_graph": False, "graph_fn": None},
            {"name": "82. 종 다양성 지수 (시슨)", "latex": r"D = 1 - \sum (p_i^2)", "desc": "군집 내 개체들의 상대적 풍부도 지표입니다.", "vars": {"p1": "종1 비율", "p2": "종2 비율"}, "calc": lambda p1, p2: 1 - (p1**2 + p2**2), "has_graph": False, "graph_fn": None},
            {"name": "83. 호흡률 (RQ)", "latex": r"RQ = \frac{\text{방출된 CO}_2 \text{ 부피}}{\text{소모된 O}_2 \text{ 부피}}", "desc": "호흡 기질에 따른 방출 CO2와 소모 O2의 비율입니다.", "vars": {"CO2": "CO2 부피", "O2": "O2 부피"}, "calc": lambda CO2, O2: CO2 / O2, "has_graph": False, "graph_fn": None},
            {"name": "84. 광합성 순생산량", "latex": r"\text{순생산량} = \text{총생산량} - \text{호흡량}", "desc": "식물이 실제로 축적하는 유기물량입니다.", "vars": {"Gross": "총생산량", "Resp": "호흡량"}, "calc": lambda Gross, Resp: Gross - Resp, "has_graph": False, "graph_fn": None},
            {"name": "85. 개체군 밀도", "latex": r"D = \frac{N \text{ (개체수)}}{A \text{ (면적)}}", "desc": "단위 면적당 존재하는 개체수입니다.", "vars": {"N": "개체수", "A": "면적 (m²)"}, "calc": lambda N, A: N / A, "has_graph": True, "graph_fn": lambda N, A: linear_graph(1/A, 0, "개체수 N", "밀도 (개체/m²)", "개체수-밀도 관계")}
        ]
    },
    "2,3학년 (지구과학)": {
        "지구과학": [
            {"name": "86. 허블 법칙", "latex": r"v = H_0 \cdot d", "desc": "은하의 후퇴 속도는 거리에 비례합니다.", "vars": {"H0": "허블상수 (km/s/Mpc)", "d": "거리 (Mpc)"}, "calc": lambda H0, d: H0 * d, "has_graph": True, "graph_fn": lambda H0, d: linear_graph(H0, 0, "거리 d (Mpc)", "후퇴속도 v (km/s)", "허블의 법칙")},
            {"name": "87. 슈테판-볼츠만 법칙", "latex": r"E = \sigma T^4", "desc": "흑체가 방출하는 단위면적당 에너지는 절대온도의 4제곱에 비례합니다.", "vars": {"T": "절대온도 (K)"}, "calc": lambda T: (5.67e-8) * (T**4), "has_graph": True, "graph_fn": lambda T: (np.linspace(1000, 10000, 100), (5.67e-8)*(np.linspace(1000, 10000, 100)**4), "온도 (K)", "방출 에너지 E", "T^4 에너지 곡선")},
            {"name": "88. 별의 광도-반지름-온도 공식", "latex": r"L = 4\pi R^2 \sigma T^4", "desc": "별의 광도는 반지름의 제곱과 표면온도의 4제곱의 곱입니다.", "vars": {"R": "반지름 (상대값)", "T": "온도 (K)"}, "calc": lambda R, T: (R**2) * ((T/5778)**4), "has_graph": False, "graph_fn": None},
            {"name": "89. 빈의 변위 법칙", "latex": r"\lambda_{max} = \frac{A}{T}", "desc": "최대 에너지를 방출하는 파장은 표면 온도에 반비례합니다.", "vars": {"T": "표면온도 (K)"}, "calc": lambda T: 2.898e-3 / T, "has_graph": True, "graph_fn": lambda T: inverse_graph(2.898e-3, "표면온도 T (K)", "최대 파장 (m)", "빈의 변위 법칙")},
            {"name": "90. 겉보기 등급과 절대 등급 (거리지수)", "latex": r"m - M = 5 \log_{10} d - 5", "desc": "별까지의 거리를 등급 차이로 산출하는 지수입니다.", "vars": {"d": "거리 (pc)"}, "calc": lambda d: 5 * np.log10(d) - 5, "has_graph": True, "graph_fn": lambda d: (np.linspace(10, 1000, 100), 5*np.log10(np.linspace(10, 1000, 100))-5, "거리 d (pc)", "거리 지수 (m-M)", "거리-거리지수 관계")},
            {"name": "91. 파세크(pc)와 연주시차", "latex": r"d = \frac{1}{p''}", "desc": "연주시차 p초의 역수가 파세크 거리입니다.", "vars": {"p": "연주시차 (초)"}, "calc": lambda p: 1 / p, "has_graph": True, "graph_fn": lambda p: inverse_graph(1, "연주시차 p (초)", "거리 d (pc)", "시차-거리 반비례")},
            {"name": "92. 도플러 시선 속도", "latex": r"v = c \cdot \frac{\Delta \lambda}{\lambda_0}", "desc": "시선 방향 이동에 따른 파장 편이로 속도를 측정합니다.", "vars": {"d_lam": "파장변화량", "lam0": "기준파장"}, "calc": lambda d_lam, lam0: 3e5 * (d_lam / lam0), "has_graph": False, "graph_fn": None},
            {"name": "93. PS시와 진원 거리", "latex": r"d = \frac{v_P v_S}{v_P - v_S} \cdot t_{PS}", "desc": "P파, S파 도달 차이시간(PS시)으로 구하는 진원 거리입니다.", "vars": {"vP": "P파속도 (km/s)", "vS": "S파속도 (km/s)", "t": "PS시 (s)"}, "calc": lambda vP, vS, t: ((vP * vS)/(vP - vS)) * t, "has_graph": True, "graph_fn": lambda vP, vS, t: linear_graph((vP*vS)/(vP-vS), 0, "PS시 (s)", "진원거리 d (km)", "PS시-진원거리")},
            {"name": "94. 지중정력학 균형 (정역학 방정식)", "latex": r"\frac{\Delta P}{\Delta z} = -\rho g", "desc": "대기 및 해수의 연직 압력 경사력과 중력의 균형입니다.", "vars": {"rho": "밀도", "dz": "높이변화 (m)"}, "calc": lambda rho, dz: rho * 9.8 * dz, "has_graph": False, "graph_fn": None},
            {"name": "95. 지풍 (Geostrophic Wind)", "latex": r"v_g = \frac{1}{\rho f} \frac{\Delta P}{\Delta n}", "desc": "기압경사력과 코리올리 힘이 평형을 이룰 때 버는 바람입니다.", "vars": {"dP": "기압차", "rho": "밀도"}, "calc": lambda dP, rho: dP / (rho * 1e-4), "has_graph": False, "graph_fn": None},
            {"name": "96. 코리올리 힘 (전향력)", "latex": r"F = 2 m v \Omega \sin \phi", "desc": "지구 자전에 의해 자전 좌표계에서 느껴지는 가상 힘입니다.", "vars": {"m": "질량", "v": "속도 (m/s)", "lat": "위도(도)"}, "calc": lambda m, v, lat: 2 * m * v * (7.292e-5) * np.sin(np.radians(lat)), "has_graph": False, "graph_fn": None},
            {"name": "97. 천체 광도 비 (포그슨 방정식)", "latex": r"\frac{L_1}{L_2} = 100^{\frac{m_2 - m_1}{5}} \approx 2.512^{m_2 - m_1}", "desc": "5등급 차이는 광도 100배 차이에 대응합니다.", "vars": {"m1": "m1 등급", "m2": "m2 등급"}, "calc": lambda m1, m2: 2.512**(m2 - m1), "has_graph": False, "graph_fn": None},
            {"name": "98. 해수 염분 (PSU)", "latex": r"S = \frac{\text{염류 질량 (g)}}{\text{해수 1000g}} \times 1000", "desc": "해수 1kg 속에 녹아 있는 총 염류의 g수입니다.", "vars": {"salt": "염류 g", "water": "해수 g"}, "calc": lambda salt, water: (salt / water) * 1000, "has_graph": False, "graph_fn": None},
            {"name": "99. 방사성 동위원소 반감기 붕괴식", "latex": r"N(t) = N_0 \left(\frac{1}{2}\right)^{\frac{t}{T_{1/2}}}", "desc": "반감기 T를 거치면서 모원소가 감소하는 절대연령 측정식입니다.", "vars": {"N0": "초기량", "t": "경과시간", "T": "반감기"}, "calc": lambda N0, t, T: N0 * ((0.5)**(t / T)), "has_graph": True, "graph_fn": lambda N0, t, T: (np.linspace(0, 5*T, 100), N0 * ((0.5)**(np.linspace(0, 5*T, 100)/T)), "경과시간 t", "모원소 남은 양", "반감기 붕괴 곡선")},
            {"name": "100. 퇴적암 수심/수압 계산", "latex": r"P = \rho g d", "desc": "수심 d에 따른 퇴적 환경 수압 산출식입니다.", "vars": {"rho": "해수밀도(1025)", "d": "수심(m)"}, "calc": lambda rho, d: rho * 9.8 * d, "has_graph": True, "graph_fn": lambda rho, d: linear_graph(rho*9.8, 0, "수심 d (m)", "수압 (Pa)", "수심-수압 관계")},
            {"name": "101. 우주 임계 밀도", "latex": r"\rho_c = \frac{3 H_0^2}{8 \pi G}", "desc": "우주의 평탄한 구조를 결정하는 기준 임계 밀도입니다.", "vars": {"H0": "허블상수 (s^-1단위)"}, "calc": lambda H0: (3 * (H0**2)) / (8 * np.pi * 6.67e-11), "has_graph": False, "graph_fn": None}
        ]
    }
}

# ---------------------------------------------------------
# 5. Main App UI Rendering
# ---------------------------------------------------------
st.title("📚 고등학교 과학 공식 모음 (100+ 공식 포함)")
st.write("2022 개정 교육과정 고1~고3 과학 교과서 내 핵심 수식 총망라")

# Breadcrumb / Navigation Bar
nav_cols = st.columns([1, 6])
with nav_cols[0]:
    if st.session_state.grade is not None:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅️ 뒤로가기"):
            if st.session_state.formula is not None:
                reset_to_formula_list()
            elif st.session_state.subject is not None:
                reset_to_subject()
            else:
                reset_to_grade()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with nav_cols[1]:
    path = "🏠 학년 선택"
    if st.session_state.grade:
        path += f"  ➔  **{st.session_state.grade}**"
    if st.session_state.subject:
        path += f"  ➔  **{st.session_state.subject}**"
    if st.session_state.formula:
        path += f"  ➔  **{st.session_state.formula['name']}**"
    st.markdown(f"#### {path}")

st.divider()

# Step 1: Grade Selection
if st.session_state.grade is None:
    st.subheader("📌 학년을 선택해 주세요")
    grades = list(FORMULA_DB.keys())
    col1, col2 = st.columns(2)
    for idx, g in enumerate(grades):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            if st.button(f"🎓 {g}"):
                st.session_state.grade = g
                st.rerun()

# Step 2: Subject Selection
elif st.session_state.subject is None:
    st.subheader(f"📌 [{st.session_state.grade}] 과목을 선택해 주세요")
    subjects = list(FORMULA_DB[st.session_state.grade].keys())
    cols = st.columns(len(subjects) if len(subjects) > 0 else 1)
    for idx, subj in enumerate(subjects):
        with cols[idx % len(cols)]:
            if st.button(f"🔬 {subj}"):
                st.session_state.subject = subj
                st.rerun()

# Step 3: Formula List Selection
elif st.session_state.formula is None:
    st.subheader(f"📌 [{st.session_state.subject}] 전체 공식 목록 (원하는 공식을 클릭하세요)")
    formulas = FORMULA_DB[st.session_state.grade][st.session_state.subject]
    
    # 2열 레이아웃으로 공식 버튼들 나열
    col1, col2 = st.columns(2)
    for idx, f in enumerate(formulas):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            if st.button(f"📑 {f['name']}"):
                st.session_state.formula = f
                st.rerun()

# Step 4: Formula Detail View
else:
    f = st.session_state.formula
    st.header(f"💡 {f['name']}")
    
    st.markdown('<div class="formula-box">', unsafe_allow_html=True)
    st.latex(f["latex"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info(f"**설명:** {f['desc']}")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("🔢 미지수 대입 및 계산기")
        st.write("미지수에 수치를 대입하여 계산 결과를 확인하세요.")
        
        input_values = {}
        for var_key, var_desc in f["vars"].items():
            input_values[var_key] = st.number_input(
                label=f"▫️ {var_key} : ({var_desc})",
                value=2.0,
                step=0.5,
                key=f"input_{var_key}"
            )
            
        if st.button("🧮 대입 결과 계산하기"):
            try:
                result = f["calc"](**input_values)
                st.success(f"**계산 결과:** `{result}`")
            except Exception as e:
                st.error(f"계산 오류: {e}")
                
    with col_right:
        st.subheader("📈 그래프 시각화")
        if f["has_graph"] and f["graph_fn"] is not None:
            try:
                first_args = list(input_values.values())[:3]
                x_vals, y_vals, xlabel, ylabel, title = f["graph_fn"](*first_args)
                
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor('#FFFDF5')
                ax.set_facecolor('#FFFFFF')
                
                ax.plot(x_vals, y_vals, color='#FF9800', linewidth=2.5)
                ax.set_title(title, fontsize=12, fontweight='bold', color='#8B6508')
                ax.set_xlabel(xlabel, fontsize=10)
                ax.set_ylabel(ylabel, fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.5)
                
                st.pyplot(fig)
            except Exception as e:
                st.warning("이 조합에서는 그래프를 생성할 수 없습니다. 적절한 미지수 수치를 입력해 주세요.")
        else:
            st.write("ℹ️ 이 공식은 변수가 고정되어 있거나 단일 상관식 계산이므로 별도 2D 연속 그래프를 생성하지 않습니다.")
