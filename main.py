import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Page Configuration & Custom CSS (대형 글자, 꽉 찬 레이아웃)
# ---------------------------------------------------------
st.set_page_config(
    page_title="고등학교 과학 공식 모음",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    :root {
      --bg-cream: #FFFDF5;
      --card-cream: #FFF9E6;
      --primary-yellow: #F6D061;
      --primary-hover: #E3B83B;
      --accent-warm: #E27B58;
      --accent-soft: #FFE385;
      --text-dark: #2C241B;
      --text-muted: #5C5042;
      --border-warm: #E3D1A5;
      --shadow-soft: 0 10px 30px rgba(165, 130, 70, 0.12);
      --font-main: 'Pretendard', 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background-color: var(--bg-cream);
        font-family: var(--font-main);
        color: var(--text-dark);
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 95% !important;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        color: var(--text-dark) !important;
    }
    h2 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: var(--text-dark) !important;
        margin-bottom: 12px !important;
    }
    h3 {
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: var(--text-dark) !important;
    }
    p, label, span {
        font-size: 1.25rem !important;
    }

    /* 카드형 대형 버튼 (빈공간 최소화 및 폰트 확대) */
    div.stButton > button {
        background-color: var(--card-cream) !important;
        color: var(--text-dark) !important;
        border: 3px solid var(--border-warm) !important;
        border-radius: 22px !important;
        padding: 30px 22px !important;
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        width: 100% !important;
        min-height: 110px !important;
        box-shadow: var(--shadow-soft) !important;
        transition: all 0.25s ease !important;
        margin-bottom: 12px !important;
        white-space: pre-wrap !important;
    }

    div.stButton > button:hover {
        background-color: var(--accent-soft) !important;
        border-color: var(--primary-hover) !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(165, 130, 70, 0.2) !important;
    }

    .back-btn button {
        background-color: #FFFFFF !important;
        color: var(--text-dark) !important;
        border: 2px solid var(--border-warm) !important;
        border-radius: 14px !important;
        padding: 10px 22px !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        min-height: unset !important;
        box-shadow: none !important;
    }
    .back-btn button:hover {
        background-color: var(--primary-yellow) !important;
        border-color: var(--primary-hover) !important;
        transform: translateX(-3px) !important;
    }

    .badge-curr {
      background-color: var(--accent-warm);
      color: #FFF;
      font-size: 1.1rem;
      font-weight: 800;
      padding: 6px 16px;
      border-radius: 25px;
      display: inline-block;
      margin-bottom: 10px;
    }

    .math-display {
      background: #FFFFFF;
      border: 3px solid var(--border-warm);
      border-radius: 20px;
      padding: 30px;
      text-align: center;
      margin: 20px 0 25px 0;
      box-shadow: inset 0 3px 8px rgba(0,0,0,0.03);
    }

    .desc-card {
      background-color: var(--card-cream);
      border: 3px solid var(--border-warm);
      border-radius: 20px;
      padding: 24px;
      margin-bottom: 22px;
      font-size: 1.3rem !important;
      line-height: 1.6;
    }

    .stTextInput input {
        font-size: 1.3rem !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: 2px solid var(--border-warm) !important;
    }
    .search-hint {
      font-size: 1.15rem;
      color: var(--text-muted);
      background: #FFFFFF;
      padding: 12px 18px;
      border-radius: 15px;
      border: 2px solid var(--border-warm);
      margin-top: 8px;
      margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

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
# 4. Helper Database Generator (200+ High School Science Formulas)
# ---------------------------------------------------------

def build_database():
    db = {
        "1학년 (통합과학 1·2)": {"통합과학": []},
        "2학년 (고등학교 2학년)": {"물리학Ⅰ": [], "화학Ⅰ": [], "생명과학Ⅰ": [], "지구과학Ⅰ": []},
        "3학년 (고등학교 3학년)": {"물리학Ⅱ": [], "화학Ⅱ": [], "생명과학Ⅱ": [], "지구과학Ⅱ": []}
    }
    
    count = 1
    
    def add_f(grade, subject, name, latex, desc, vars_dict, calc_fn, has_graph=False, graph_fn=None):
        nonlocal count
        db[grade][subject].append({
            "id": f"f_{count}",
            "grade": grade,
            "subject": subject,
            "name": f"{count}. {name}",
            "latex": latex,
            "desc": desc,
            "vars": vars_dict,
            "calc": calc_fn,
            "has_graph": has_graph,
            "graph_fn": graph_fn
        })
        count += 1

    # ==================== [1학년 통합과학 1·2 : 1~30] ====================
    add_f("1학년 (통합과학 1·2)", "통합과학", "평균 속도", r"\bar{v} = \frac{\Delta s}{\Delta t}", "변위를 걸린 시간으로 나눈 값입니다.", {"ds": "변위 Δs (m)", "dt": "시간 Δt (s)"}, lambda ds, dt: ds / (dt if dt!=0 else 1e-9), True, lambda ds, dt: linear_graph(ds/(dt if dt!=0 else 1e-9), 0, "시간(s)", "변위(m)", "시간-변위"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "가속도", r"a = \frac{\Delta v}{\Delta t}", "단위 시간당 속도 변화량입니다.", {"dv": "속도변화량 Δv (m/s)", "dt": "시간 Δt (s)"}, lambda dv, dt: dv / (dt if dt!=0 else 1e-9), True, lambda dv, dt: linear_graph(dv/(dt if dt!=0 else 1e-9), 0, "시간(s)", "속도(m/s)", "시간-속도"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "등가속도 나중 속도", r"v = v_0 + at", "등가속도 운동에서 시간 t 후의 속도입니다.", {"v0": "초기속도 v0 (m/s)", "a": "가속도 a (m/s²)", "t": "시간 t (s)"}, lambda v0, a, t: v0 + a*t, True, lambda v0, a, t=0: linear_graph(a, v0, "시간(s)", "속도(m/s)", "시간-속도"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "등가속도 이동 거리", r"s = v_0 t + \frac{1}{2}at^2", "등가속도 운동 시 이동 거리입니다.", {"v0": "초기속도 v0 (m/s)", "a": "가속도 a (m/s²)", "t": "시간 t (s)"}, lambda v0, a, t: v0*t + 0.5*a*(t**2), True, lambda v0, a, t=0: square_graph(0.5*a if a!=0 else 0.1, "시간(s)", "거리(m)", "시간-거리"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "시간 제거 등가속도 식", r"2as = v^2 - v_0^2", "시간 t를 제외한 가속도, 거리, 속도 관계식입니다.", {"v": "나중속도 v (m/s)", "v0": "초기속도 v0 (m/s)", "a": "가속도 a (m/s²)"}, lambda v, v0, a: (v**2 - v0**2) / (2*a if a!=0 else 1e-9))
    add_f("1학년 (통합과학 1·2)", "통합과학", "운동량", r"p = m v", "질량과 속도의 곱으로 정의되는 운동 효과입니다.", {"m": "질량 m (kg)", "v": "속도 v (m/s)"}, lambda m, v: m * v, True, lambda m, v: linear_graph(m, 0, "속도(m/s)", "운동량(kg·m/s)", "속도-운동량"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "충격량", r"I = F \Delta t", "힘과 힘이 작용한 시간의 곱입니다.", {"F": "힘 F (N)", "dt": "시간 Δt (s)"}, lambda F, dt: F * dt, True, lambda F, dt: linear_graph(F, 0, "시간(s)", "충격량(N·s)", "시간-충격량"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "충격량과 운동량 변화량", r"I = \Delta p = m v_f - m v_i", "충격량은 물체의 운동량 변화량과 같습니다.", {"m": "질량 m (kg)", "vf": "나중속도 vf (m/s)", "vi": "초기속도 vi (m/s)"}, lambda m, vf, vi: m * (vf - vi))
    add_f("1학년 (통합과학 1·2)", "통합과학", "중력 위치 에너지", r"E_p = m g h", "기준면으로부터의 높이에 따른 중력 위치 에너지입니다.", {"m": "질량 m (kg)", "h": "높이 h (m)", "g": "중력가속도 g (9.8)"}, lambda m, h, g=9.8: m * g * h, True, lambda m, h, g=9.8: linear_graph(m*g, 0, "높이(m)", "위치에너지(J)", "높이-위치에너지"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "운동 에너지", r"E_k = \frac{1}{2}m v^2", "운동하는 물체가 가지는 에너지입니다.", {"m": "질량 m (kg)", "v": "속도 v (m/s)"}, lambda m, v: 0.5 * m * (v**2), True, lambda m, v: square_graph(0.5*m, "속도(m/s)", "운동에너지(J)", "속도-운동에너지"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "역학적 에너지 보존", r"E_{total} = E_k + E_p", "마찰과 공기저항이 없을 때 역학적 에너지는 보존됩니다.", {"Ek": "운동에너지 Ek (J)", "Ep": "위치에너지 Ep (J)"}, lambda Ek, Ep: Ek + Ep)
    add_f("1학년 (통합과학 1·2)", "통합과학", "질량-에너지 등가성", r"E = m c^2", "질량이 에너지로 변환되는 관계식입니다.", {"m": "질량 결손 m (kg)"}, lambda m: m * (3e8**2), True, lambda m: linear_graph(3e8**2, 0, "질량(kg)", "에너지(J)", "질량-에너지"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "소비 전력", r"P = V I", "단위 시간당 소비되는 전기 에너지입니다.", {"V": "전압 V (V)", "I": "전류 I (A)"}, lambda V, I: V * I, True, lambda V, I: linear_graph(V, 0, "전류(A)", "전력(W)", "전류-전력"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "전력량", r"W = P \cdot t", "일정 시간 동안 소비한 총 전기에너지입니다.", {"P": "전력 P (W)", "t": "시간 t (h)"}, lambda P, t: P * t, True, lambda P, t: linear_graph(P, 0, "시간(h)", "전력량(Wh)", "시간-전력량"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "열효율", r"e = \frac{W}{Q_1} = \frac{Q_1 - Q_2}{Q_1}", "흡수한 열량 대비 일로 변환된 열기관의 효율입니다.", {"Q1": "고열원 공급열 Q1 (J)", "Q2": "저열원 방출열 Q2 (J)"}, lambda Q1, Q2: (Q1 - Q2) / (Q1 if Q1!=0 else 1e-9))
    add_f("1학년 (통합과학 1·2)", "통합과학", "변압기 변압비", r"\frac{V_1}{V_2} = \frac{N_1}{N_2}", "1차, 2차 코일 감은 수와 전압의 관계입니다.", {"V1": "1차전압 V1 (V)", "N1": "1차 권선수 N1", "N2": "2차 권선수 N2"}, lambda V1, N1, N2: V1 * (N2 / (N1 if N1!=0 else 1)))
    add_f("1학년 (통합과학 1·2)", "통합과학", "변압기 전력 보존", r"V_1 I_1 = V_2 I_2", "이상적인 변압기에서 1차와 2차 전력은 같습니다.", {"V1": "V1 (V)", "I1": "I1 (A)", "V2": "V2 (V)"}, lambda V1, I1, V2: (V1 * I1) / (V2 if V2!=0 else 1e-9))
    add_f("1학년 (통합과학 1·2)", "통합과학", "송전 손실 전력", r"P_{loss} = I^2 R", "송전선 저항에 의해 손실되는 전력입니다.", {"I": "송전전류 I (A)", "R": "저항 R (Ω)"}, lambda I, R: (I**2) * R, True, lambda I, R: square_graph(R, "전류(A)", "손실전력(W)", "전류-손실전력"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "수소 스펙트럼 에너지", r"\Delta E = h f", "전자가 전이할 때 방출 또는 흡수하는 빛의 에너지입니다.", {"f": "진동수 f (Hz)"}, lambda f: (6.63e-34) * f)
    add_f("1학년 (통합과학 1·2)", "통합과학", "중력의 크기", r"F = m g", "지표면 근처에서 물체가 받는 중력입니다.", {"m": "질량 m (kg)", "g": "중력가속도 g (9.8)"}, lambda m, g=9.8: m * g, True, lambda m, g=9.8: linear_graph(g, 0, "질량(kg)", "중력(N)", "질량-중력"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "자유낙하 속도", r"v = g t", "자유낙하 시 시간 t에서의 속도입니다.", {"t": "시간 t (s)", "g": "중력가속도 g (9.8)"}, lambda t, g=9.8: g * t, True, lambda t, g=9.8: linear_graph(g, 0, "시간(s)", "속도(m/s)", "시간-속도"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "자유낙하 낙하 거리", r"h = \frac{1}{2}g t^2", "자유낙하 시 시간 t 동안 낙하한 거리입니다.", {"t": "시간 t (s)", "g": "중력가속도 g (9.8)"}, lambda t, g=9.8: 0.5 * g * (t**2), True, lambda t, g=9.8: square_graph(0.5*g, "시간(s)", "낙하거리(m)", "시간-낙하거리"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "지구 시스템 복사 평형", r"E_{in} = E_{out}", "지구가 흡수하는 태양 복사 에너지와 방출하는 지구 복사 에너지는 같습니다.", {"Ein": "흡수 에너지 (상대값)"}, lambda Ein: Ein)
    add_f("1학년 (통합과학 1·2)", "통합과학", "밀도", r"\rho = \frac{m}{V}", "단위 부피당 질량입니다.", {"m": "질량 m (g)", "V": "부피 V (mL)"}, lambda m, V: m / (V if V!=0 else 1e-9), True, lambda m, V=1: linear_graph(1/(V if V!=0 else 1e-9), 0, "질량(g)", "밀도", "질량-밀도"))
    add_f("1학년 (통합과학 1·2)", "통합과학", "용해도 및 퍼센트 농도", r"\% = \frac{\text{용질 질량}}{\text{용액 질량}} \times 100", "용액 전체 질량에 대한 용질 질량의 백분율입니다.", {"solute": "용질 (g)", "solution": "용액 (g)"}, lambda solute, solution: (solute / (solution if solution!=0 else 1e-9)) * 100)
    add_f("1학년 (통합과학 1·2)", "통합과학", "지각 구성 요소 존재 비율", r"\text{비율} = \frac{\text{원소 질량}}{\text{총 질량}} \times 100", "지각이나 생명체를 구성하는 주요 원소의 질량 비율입니다.", {"elem": "원소 질량", "total": "총 질량"}, lambda elem, total: (elem / (total if total!=0 else 1e-9)) * 100)
    add_f("1학년 (통합과학 1·2)", "통합과학", "산화-환원 전자 이동수", r"N_{e, lost} = N_{e, gained}", "산화 환원 반응에서 잃은 전자 수와 얻은 전자 수는 같습니다.", {"lost": "잃은 전자 몰수"}, lambda lost: lost)
    add_f("1학년 (통합과학 1·2)", "통합과학", "중화 반응 생성 수량", r"H^+ + OH^- \rightarrow H_2O", "수소 이온과 수산화 이온이 1:1 몰비로 반응하여 물을 생성합니다.", {"H": "H+ 몰수 (mol)", "OH": "OH- 몰수 (mol)"}, lambda H, OH: min(H, OH))
    add_f("1학년 (통합과학 1·2)", "통합과학", "생태계 에너지 전달 효율", r"\text{효율} = \frac{\text{현 단계 에너지}}{\text{전 단계 에너지}} \times 100", "상위 영양 단계로 전달되는 에너지 비율입니다.", {"curr": "현 단계 에너지", "prev": "전 단계 에너지"}, lambda curr, prev: (curr / (prev if prev!=0 else 1e-9)) * 100)
    add_f("1학년 (통합과학 1·2)", "통합과학", "엘니뇨 다윈-타히티 남방진동 지수", r"SOI = P_{Tahiti} - P_{Darwin}", "해수면 기압 차를 이용한 남방진동 지수입니다.", {"t": "타히티 기압", "d": "다윈 기압"}, lambda t, d: t - d)

    # ==================== [2학년 물리학Ⅰ: 31~55] ====================
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "뉴턴 제1법칙 (관성)", r"\sum F = 0 \Rightarrow a = 0", "알짜힘이 0이면 정지 물체는 정지, 운동 물체는 등속 직선 운동합니다.", {"F": "알짜힘 (N)"}, lambda F: 0 if F==0 else F)
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "뉴턴 제2법칙", r"F = m a", "알짜힘은 질량과 가속도의 곱입니다.", {"m": "질량 m (kg)", "a": "가속도 a (m/s²)"}, lambda m, a: m * a, True, lambda m, a: linear_graph(m, 0, "가속도(m/s²)", "알짜힘(N)", "가속도-힘"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "뉴턴 제3법칙 (작용 반작용)", r"F_{A \rightarrow B} = -F_{B \rightarrow A}", "두 물체 사이 작용하는 힘은 크기가 같고 방향이 반대입니다.", {"F": "작용 힘 (N)"}, lambda F: -F)
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "만유인력 법칙", r"F = G \frac{m_1 m_2}{r^2}", "두 질량체 사이의 거리의 제곱에 반비례하는 인력입니다.", {"m1": "m1 (kg)", "m2": "m2 (kg)", "r": "거리 r (m)"}, lambda m1, m2, r: (6.67e-11) * m1 * m2 / ((r**2) if r!=0 else 1e-9), True, lambda m1, m2, r=1: inverse_graph((6.67e-11)*m1*m2, "거리(m)", "만유인력(N)", "거리-만유인력"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "탄성력 (훅의 법칙)", r"F = -k x", "변형된 길이에 비례하여 되돌아가려는 복원력입니다.", {"k": "용수철상수 k (N/m)", "x": "변형길이 x (m)"}, lambda k, x: k * x, True, lambda k, x: linear_graph(k, 0, "변형길이(m)", "탄성력(N)", "변형-탄성력"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "탄성 위치 에너지", r"E_p = \frac{1}{2}k x^2", "변형된 용수철에 저장되는 위치 에너지입니다.", {"k": "용수철상수 k (N/m)", "x": "변형길이 x (m)"}, lambda k, x: 0.5 * k * (x**2), True, lambda k, x: square_graph(0.5*k, "변형길이(m)", "에너지(J)", "변형-에너지"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "옴의 법칙", r"V = I R", "전압은 전류와 저항의 곱입니다.", {"I": "전류 I (A)", "R": "저항 R (Ω)"}, lambda I, R: I * R, True, lambda I, R: linear_graph(R, 0, "전류(A)", "전압(V)", "전류-전압"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "저항 직렬합성", r"R_{total} = R_1 + R_2", "직렬 연결된 저항의 총합입니다.", {"R1": "R1 (Ω)", "R2": "R2 (Ω)"}, lambda R1, R2: R1 + R2)
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "저항 병렬합성", r"\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2}", "병렬 연결된 저항의 역수의 합입니다.", {"R1": "R1 (Ω)", "R2": "R2 (Ω)"}, lambda R1, R2: (R1 * R2) / ((R1 + R2) if (R1+R2)!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "전기저항과 비저항", r"R = \rho \frac{L}{A}", "길이 L에 비례하고 단면적 A에 반비례합니다.", {"rho": "비저항", "L": "길이 (m)", "A": "단면적 (m²)"}, lambda rho, L, A: rho * L / (A if A!=0 else 1e-9), True, lambda rho, L, A=1: linear_graph(rho/(A if A!=0 else 1), 0, "길이(m)", "저항(Ω)", "길이-저항"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "쿨롱의 법칙", r"F = k \frac{|q_1 q_2|}{r^2}", "두 전하 사이의 정전기력입니다.", {"q1": "q1 (C)", "q2": "q2 (C)", "r": "거리 r (m)"}, lambda q1, q2, r: (8.99e9) * abs(q1*q2) / ((r**2) if r!=0 else 1e-9), True, lambda q1, q2, r=1: inverse_graph((8.99e9)*abs(q1*q2), "거리(m)", "정전기력(N)", "거리-정전기력"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "파동의 속력", r"v = f \lambda", "파동의 속력은 진동수와 파장의 곱입니다.", {"f": "진동수 f (Hz)", "lam": "파장 λ (m)"}, lambda f, lam: f * lam, True, lambda f, lam: linear_graph(f, 0, "파장(m)", "속력(m/s)", "파장-속력"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "주기와 진동수", r"T = \frac{1}{f}", "주기와 진동수는 역수 관계입니다.", {"f": "진동수 f (Hz)"}, lambda f: 1 / (f if f!=0 else 1e-9), True, lambda f: inverse_graph(1, "진동수(Hz)", "주기(s)", "진동수-주기"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "굴절률 정의", r"n = \frac{c}{v}", "진공에서의 빛의 속도 c와 매질 속 속도 v의 비입니다.", {"v": "매질 속 속도 v (m/s)"}, lambda v: 3e8 / (v if v!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "스넬의 법칙", r"n_1 \sin \theta_1 = n_2 \sin \theta_2", "빛이 매질 경계면을 통과할 때의 굴절 관계식입니다.", {"n1": "굴절률 n1", "t1": "입사각 t1 (도)"}, lambda n1, t1: n1 * np.sin(np.radians(t1)))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "임계각과 전반사", r"\sin \theta_c = \frac{n_2}{n_1}", "전반사가 일어나는 최소 입사각 조건입니다.", {"n1": "매질1 n1", "n2": "매질2 n2"}, lambda n1, n2: np.degrees(np.arcsin(min(1.0, max(-1.0, n2 / (n1 if n1!=0 else 1e-9))))))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "광자 에너지", r"E = h f = \frac{h c}{\lambda}", "빛의 단일 광자 에너지입니다.", {"f": "진동수 f (Hz)"}, lambda f: (6.63e-34) * f, True, lambda f: linear_graph(6.63e-34, 0, "진동수(Hz)", "에너지(J)", "진동수-에너지"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "광전효과 최대 운동에너지", r"E_{k, max} = h f - W", "금속판에서 방출되는 광전자의 최대 운동에너지입니다.", {"f": "진동수 f (Hz)", "W": "일함수 W (J)"}, lambda f, W: (6.63e-34) * f - W)
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "드브로이 물질파 파장", r"\lambda = \frac{h}{p} = \frac{h}{m v}", "운동하는 입자가 가지는 물질파 파장입니다.", {"m": "질량 m (kg)", "v": "속도 v (m/s)"}, lambda m, v: (6.63e-34) / ((m*v) if (m*v)!=0 else 1e-9), True, lambda m, v: inverse_graph(6.63e-34/(m if m!=0 else 1e-9), "속도(m/s)", "파장(m)", "속도-물질파파장"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "열역학 제1법칙", r"Q = \Delta U + W", "기체에 공급한 열량은 내부에너지 변화와 일의 합입니다.", {"dU": "내부에너지 변화 dU (J)", "W": "한 일 W (J)"}, lambda dU, W: dU + W)
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "등압 과정 기체가 한 일", r"W = P \Delta V", "일정한 압력 아래 기체가 팽창할 때 하는 일입니다.", {"P": "압력 P (Pa)", "dV": "부피변화 dV (m³)"}, lambda P, dV: P * dV, True, lambda P, dV: linear_graph(P, 0, "부피변화(m³)", "일(J)", "부피변화-일"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "솔레노이드 자기장", r"B = \mu_0 n I", "솔레노이드 내부 중앙에서의 자기장 세기입니다.", {"n": "단위길이당 권선수 n", "I": "전류 I (A)"}, lambda n, I: (4 * np.pi * 1e-7) * n * I, True, lambda n, I: linear_graph((4*np.pi*1e-7)*n, 0, "전류(A)", "자기장(T)", "전류-자기장"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "직선 도선 자기장", r"B = k \frac{I}{r}", "무한히 긴 직선 도선 주변의 자기장 세기입니다.", {"I": "전류 I (A)", "r": "거리 r (m)"}, lambda I, r: (2e-7) * I / (r if r!=0 else 1e-9), True, lambda I, r=1: inverse_graph((2e-7)*I, "거리(m)", "자기장(T)", "거리-자기장"))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "패러데이 전자기 유도 법칙", r"V = -N \frac{\Delta \Phi}{\Delta t}", "유도 기전력은 자기 선속 변화율과 코일 권선수에 비례합니다.", {"N": "권선수 N", "dPhi": "자속변화량 dPhi (Wb)", "dt": "시간 dt (s)"}, lambda N, dPhi, dt: -N * dPhi / (dt if dt!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "물리학Ⅰ", "자기 선속 (자속)", r"\Phi = B \cdot A", "자기장 B와 면적 A의 곱으로 구하는 자기선속입니다.", {"B": "자기장 B (T)", "A": "면적 A (m²)"}, lambda B, A: B * A)

    # ==================== [2학년 화학Ⅰ: 56~80] ====================
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "몰(Mole) 질량 관계", r"n = \frac{w}{M}", "질량을 화학식량(분자량)으로 나눈 몰수입니다.", {"w": "질량 w (g)", "M": "분자량 M (g/mol)"}, lambda w, M: w / (M if M!=0 else 1e-9), True, lambda w, M=1: linear_graph(1/(M if M!=0 else 1e-9), 0, "질량(g)", "몰수(mol)", "질량-몰수"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "기체 몰수 부피 관계 (STP)", r"n = \frac{V}{22.4}", "0℃, 1기압에서 기체 부피를 몰수로 환산하는 식입니다.", {"V": "기체 부피 V (L)"}, lambda V: V / 22.4, True, lambda V: linear_graph(1/22.4, 0, "부피(L)", "몰수(mol)", "부피-몰수"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "입자 수와 몰수", r"N = n \times N_A", "몰수와 아보가드로 수(6.02x10²³)의 곱입니다.", {"n": "몰수 n (mol)"}, lambda n: n * 6.022e23)
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "몰농도 (Molarity)", r"M = \frac{n}{V}", "용액 1L 속에 녹아 있는 용질의 몰수입니다.", {"n": "용질 몰수 n (mol)", "V": "용액 부피 V (L)"}, lambda n, V: n / (V if V!=0 else 1e-9), True, lambda n, V=1: inverse_graph(n, "부피(L)", "몰농도(M)", "부피-몰농도"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "용액 희석 공식", r"M_1 V_1 = M_2 V_2", "용액을 희석해도 녹아 있는 용질의 몰수는 일정합니다.", {"M1": "초기농도 M1 (M)", "V1": "초기부피 V1 (L)", "M2": "나중농도 M2 (M)"}, lambda M1, V1, M2: (M1 * V1) / (M2 if M2!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "이상기체 상태 방정식", r"P V = n R T", "기체의 압력, 부피, 몰수, 절대온도 관계식입니다.", {"P": "압력 P (atm)", "n": "몰수 n (mol)", "T": "절대온도 T (K)"}, lambda P, n, T: (n * 0.0821 * T) / (P if P!=0 else 1e-9), True, lambda P, n, T: inverse_graph(n*0.0821*T, "부피(L)", "압력(atm)", "보일의법칙"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "기체 밀도와 분자량", r"M = \frac{\rho R T}{P}", "기체 밀도(ρ)를 통해 분자량을 산출하는 식입니다.", {"rho": "밀도 rho (g/L)", "T": "온도 T (K)", "P": "압력 P (atm)"}, lambda rho, T, P: (rho * 0.0821 * T) / (P if P!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "보일의 법칙", r"P_1 V_1 = P_2 V_2", "온도가 일정할 때 압력과 부피는 반비례합니다.", {"P1": "P1 (atm)", "V1": "V1 (L)", "P2": "P2 (atm)"}, lambda P1, V1, P2: (P1 * V1) / (P2 if P2!=0 else 1e-9), True, lambda P1, V1, P2=1: inverse_graph(P1*V1, "부피(L)", "압력(atm)", "보일의법칙"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "샤를의 법칙", r"\frac{V_1}{T_1} = \frac{V_2}{T_2}", "압력이 일정할 때 부피는 절대온도에 비례합니다.", {"V1": "V1 (L)", "T1": "T1 (K)", "T2": "T2 (K)"}, lambda V1, T1, T2: V1 * (T2 / (T1 if T1!=0 else 1e-9)), True, lambda V1, T1, T2=1: linear_graph(V1/(T1 if T1!=0 else 1e-9), 0, "온도(K)", "부피(L)", "샤를의법칙"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "달톤 분압 법칙", r"P_{total} = P_A + P_B", "혼합 기체의 총 압력은 각 성분 기체의 분압의 합입니다.", {"PA": "A 분압 (atm)", "PB": "B 분압 (atm)"}, lambda PA, PB: PA + PB)
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "몰분율", r"X_A = \frac{n_A}{n_A + n_B}", "전체 기체 몰수 중 성분 A 기체의 몰수 비율입니다.", {"nA": "nA (mol)", "nB": "nB (mol)"}, lambda nA, nB: nA / ((nA + nB) if (nA+nB)!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "pH 수소이온농도지수", r"\text{pH} = -\log_{10}[H^+]", "수용액 내 수소 이온 농도의 음의 로그값입니다.", {"H": "[H+] 농도 (M)"}, lambda H: -np.log10(max(1e-14, H)))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "pOH 수산화이온농도지수", r"\text{pOH} = -\log_{10}[OH^-]", "수용액 내 수산화 이온 농도의 음의 로그값입니다.", {"OH": "[OH-] 농도 (M)"}, lambda OH: -np.log10(max(1e-14, OH)))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "물의 이온화 상수", r"K_w = [H^+][OH^-] = 1.0 \times 10^{-14}", "25℃ 순수한 물의 자가 이온화 곱 상수입니다.", {"H": "[H+] 농도 (M)"}, lambda H: 1e-14 / (H if H!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "pH와 pOH의 관계", r"\text{pH} + \text{pOH} = 14", "25℃ 수용액에서 pH와 pOH의 합은 항상 14입니다.", {"pH": "pH 값"}, lambda pH: 14 - pH)
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "중화 적정 수식", r"n M V = n' M' V'", "산이 내놓은 H+ 몰수와 염기가 내놓은 OH- 몰수는 같습니다.", {"n": "산 가수 n", "M": "산 농도 M (M)", "V": "산 부피 V (L)", "n2": "염기 가수 n'"}, lambda n, M, V, n2: (n * M * V) / (n2 if n2!=0 else 1))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "반응 열량 계산식", r"Q = C \cdot m \cdot \Delta T", "비열, 질량, 온도변화를 통한 반응 열량 측정식입니다.", {"C": "비열 (J/g·℃)", "m": "질량 m (g)", "dT": "온도변화 dT (℃)"}, lambda C, m, dT: C * m * dT, True, lambda C, m, dT: linear_graph(C*m, 0, "온도변화(℃)", "열량(J)", "온도변화-열량"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "열용량과 열량", r"Q = C_{total} \cdot \Delta T", "열용량과 온도 변화를 이용한 방출/흡수 열량 공식입니다.", {"C": "열용량 (J/℃)", "dT": "온도변화 dT (℃)"}, lambda C, dT: C * dT, True, lambda C, dT: linear_graph(C, 0, "온도변화(℃)", "열량(J)", "온도변화-열량"))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "수소 원자 오비탈 에너지 level", r"E_n = -\frac{2.18 \times 10^{-18}}{n^2} \text{ J}", "보어 수소 원자 모형에서의 주양자수 n에 따른 에너지입니다.", {"n": "주양자수 n (1, 2, 3...)"}, lambda n: -2.18e-18 / ((n**2) if n!=0 else 1))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "유효 핵전하 공식", r"Z^* = Z - S", "원자핵 전하(Z)에서 가막이 효과(S)를 뺀 유효 핵전하입니다.", {"Z": "원자번호 Z", "S": "가림상수 S"}, lambda Z, S: Z - S)
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "결합 극성과 쌍극자 모멘트", r"\mu = q \cdot r", "전하량 q와 전하 사이 거리 r의 곱으로 표현되는 크기입니다.", {"q": "전하량 q (C)", "r": "거리 r (m)"}, lambda q, r: q * r)
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "평형 상수 K", r"K = \frac{[C]^c [D]^d}{[A]^a [B]^b}", "화학 평형 시 생성물과 반응물의 농도비입니다.", {"prod": "생성물 농도곱", "react": "반응물 농도곱"}, lambda prod, react: prod / (react if react!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "산 이온화 상수 Ka", r"K_a = \frac{[H^+][A^-]}{[HA]}", "약산 HA의 수용액 내 이온화 평형상수입니다.", {"H": "[H+]", "A": "[A-]", "HA": "[HA]"}, lambda H, A, HA: (H * A) / (HA if HA!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "염기 이온화 상수 Kb", r"K_b = \frac{[BH^+][OH^-]}{[B]}", "약염기 B의 수용액 내 이온화 평형상수입니다.", {"BH": "[BH+]", "OH": "[OH-]", "B": "[B]"}, lambda BH, OH, B: (BH * OH) / (B if B!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "화학Ⅰ", "Ka와 Kb의 관계", r"K_a \cdot K_b = K_w = 1.0 \times 10^{-14}", "짝산-짝염기 쌍의 이온화 상수의 곱은 Kw와 같습니다.", {"Ka": "Ka 값"}, lambda Ka: 1e-14 / (Ka if Ka!=0 else 1e-9))

    # ==================== [2학년 생명과학Ⅰ: 81~105] ====================
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "하디-바인베르크 대립유전자 빈도", r"p + q = 1", "우성(p)과 열성(q) 대립유전자 빈도의 합은 1입니다.", {"p": "p 빈도 (0~1)"}, lambda p: 1 - p)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "하디-바인베르크 유전자형 빈도", r"p^2 + 2pq + q^2 = 1", "멘델 집단에서의 유전자형 빈도 관계식입니다.", {"p": "p 빈도 (0~1)"}, lambda p: (p**2, 2*p*(1-p), (1-p)**2), True, lambda p: (np.linspace(0, 1, 100), np.linspace(0, 1, 100)**2, "p", "p² 빈도", "유전자빈도"))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "개체군 밀도", r"D = \frac{N}{A}", "단위 면적당 존재하는 개체수입니다.", {"N": "개체수 N", "A": "면적 A (m²)"}, lambda N, A: N / (A if A!=0 else 1e-9), True, lambda N, A=1: linear_graph(1/(A if A!=0 else 1e-9), 0, "개체수 N", "밀도", "개체수-밀도"))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "포획-재포획법 개체수 추정", r"N = \frac{M \cdot C}{R}", "표지 재포획법을 이용한 전체 개체수 N 추정 공식입니다.", {"M": "1차 표지 개체수 M", "C": "2차 포획 개체수 C", "R": "2차 중 표지 개체수 R"}, lambda M, C, R: (M * C) / (R if R!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "개체군 지수 생장 모델", r"N_t = N_0 e^{rt}", "환경 저항이 없을 때 무제한 생장하는 지수 모델입니다.", {"N0": "초기 개체수 N0", "r": "증가율 r", "t": "시간 t"}, lambda N0, r, t: N0 * np.exp(min(100, r * t)), True, lambda N0, r, t=0: (np.linspace(0, 10, 100), N0 * np.exp(r * np.linspace(0, 10, 100)), "시간(t)", "개체수 N", "지수생장곡선"))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "로지스틱 생장 모델", r"\frac{dN}{dt} = r N \left(\frac{K - N}{K}\right)", "환경 수용 능력 K를 고려한 개체수 생장 속도 공식입니다.", {"r": "증가율 r", "N": "개체수 N", "K": "수용능력 K"}, lambda r, N, K: r * N * ((K - N) / (K if K!=0 else 1e-9)))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "에너지 효율", r"\text{효율} = \frac{\text{현 영양단계 에너지}}{\text{전 영양단계 에너지}} \times 100", "영양 단계 간 에너지 이동 효율입니다.", {"curr": "현 단계 에너지", "prev": "전 단계 에너지"}, lambda curr, prev: (curr / (prev if prev!=0 else 1e-9)) * 100)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "호흡률 (RQ)", r"RQ = \frac{\text{방출 CO}_2}{\text{소모 O}_2}", "호흡 기질 종류에 따른 방출 CO2와 소모 O2의 부피비입니다.", {"CO2": "CO2 부피", "O2": "O2 부피"}, lambda CO2, O2: CO2 / (O2 if O2!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "광합성 순생산량", r"\text{순생산량} = \text{총생산량} - \text{호흡량}", "식물이 실제로 축적하는 유기물량 공식입니다.", {"Gross": "총생산량", "Resp": "호흡량"}, lambda Gross, Resp: Gross - Resp)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "군집 상대 밀도", r"\text{상대밀도} = \frac{\text{특정 종 개체수}}{\text{전체 개체수}} \times 100", "군집 전체 개체수에 대한 특정 종 개체수 백분율입니다.", {"spec": "특정 종 개체수", "total": "전체 개체수"}, lambda spec, total: (spec / (total if total!=0 else 1e-9)) * 100)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "군집 상대 빈도", r"\text{상대빈도} = \frac{\text{특정 종 출현 방사구 수}}{\text{전체 방사구 수 합}} \times 100", "방사구 조사법에서의 특정 종 상대 빈도입니다.", {"spec": "특정 종 빈도", "total": "전체 빈도합"}, lambda spec, total: (spec / (total if total!=0 else 1e-9)) * 100)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "군집 상대 피도", r"\text{상대피도} = \frac{\text{특정 종 점유 면적}}{\text{전체 점유 면적}} \times 100", "방사구 조사법에서의 특정 종 상대 피도입니다.", {"spec": "특정 종 면적", "total": "전체 면적"}, lambda spec, total: (spec / (total if total!=0 else 1e-9)) * 100)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "중요도 (우점도 지수)", r"\text{중요도} = \text{상대밀도} + \text{상대빈도} + \text{상대피도}", "우점종을 결정하기 위한 상대 수치들의 합입니다.", {"rd": "상대밀도", "rf": "상대빈도", "rc": "상대피도"}, lambda rd, rf, rc: rd + rf + rc)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "심장 박출량 (CO)", r"CO = HR \times SV", "1분 동안 심장이 분출하는 혈액 총량입니다.", {"HR": "심박수 (회/분)", "SV": "1회 박출량 (mL)"}, lambda HR, SV: HR * SV, True, lambda HR, SV: linear_graph(SV, 0, "심박수", "심박출량(mL/min)", "심박수-박출량"))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "여과율 (신장 기능)", r"\text{여과율} = \text{사구체 여과액 부피} / \text{시간}", "단위 시간당 콩팥 사구체에서 여과되는 원뇨의 양입니다.", {"vol": "여과액 부피 (mL)", "t": "시간 t (min)"}, lambda vol, t: vol / (t if t!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "ATP 합성과 분해 열량", r"ATP + H_2O \rightarrow ADP + P_i + 7.3 \text{ kcal/mol}", "ATP 1몰이 분해될 때 방출되는 에너지 공식입니다.", {"n": "ATP 몰수 (mol)"}, lambda n: n * 7.3)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "1일 필요 에너지 양", r"E_{total} = \text{기초대사량} + \text{활동대사량} + \text{소화대사량}", "하루에 필요한 전체 에너지 소비량입니다.", {"bmr": "기초대사량", "amr": "활동대사량", "dmr": "소화대사량"}, lambda bmr, amr, dmr: bmr + amr + dmr)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "체질량 지수 (BMI)", r"BMI = \frac{\text{체중 (kg)}}{\text{키 (m)}^2}", "비만도를 산출하는 체질량 지수 공식입니다.", {"w": "체중 w (kg)", "h": "신장 h (m)"}, lambda w, h: w / ((h**2) if h!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "뉴런 휴지 전위와 나트륨 칼륨 펌프", r"V_m = -70 \text{ mV}", "뉴런 분극 상태에서의 기본 휴지 전위 값입니다.", {"v": "전위차 (mV)"}, lambda v: v)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "흥분 전도 속도", r"v = \frac{d}{t}", "축삭 돌기를 따라 흥분이 전도되는 속도입니다.", {"d": "거리 d (cm)", "t": "시간 t (ms)"}, lambda d, t: d / (t if t!=0 else 1e-9), True, lambda d, t: linear_graph(1/(t if t!=0 else 1e-9), 0, "거리(cm)", "속도(cm/ms)", "거리-속도"))
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "근육 원섬유 마디 길이 변화", r"L_{H-zone} = L_{I-band} = \Delta x", "근수축 시 H대 및 I대의 길이 변화 공식입니다.", {"x": "수축 변화량 dx (um)"}, lambda x: x)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "혈당량 조절 인슐린 농도", r"\Delta G = -k [Insulin]", "인슐린 농도 증가에 따른 혈당 감소 비율입니다.", {"k": "상수 k", "ins": "인슐린 농도"}, lambda k, ins: -k * ins)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "체온 조절 열방출량", r"Q_{loss} \propto A \cdot (T_{body} - T_{env})", "체온과 환경 온도 차이에 따른 열방출 비례식입니다.", {"Tb": "체온 (℃)", "Te": "환경온도 (℃)"}, lambda Tb, Te: Tb - Te)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "혈장 삼투압 조절 (ADH)", r"[ADH] \propto \text{혈장 삼투압}", "혈장 삼투압 증가 시 항디뇨 호르몬 분비 비례 관계입니다.", {"osm": "삼투압 (mOsm/L)"}, lambda osm: osm * 0.1)
    add_f("2학년 (고등학교 2학년)", "생명과학Ⅰ", "다인자 유전자형 조합 수", r"N = 2^n", "n쌍의 대립유전자가 독립일 때 생식세포 조합 수입니다.", {"n": "유전자 쌍 수 n"}, lambda n: 2**n)

    # ==================== [2학년 지구과학Ⅰ: 106~130] ====================
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "허블의 법칙", r"v = H_0 \cdot d", "외부 은하 후퇴 속도와 거리의 비례 공식입니다.", {"H0": "허블상수 H0 (km/s/Mpc)", "d": "거리 d (Mpc)"}, lambda H0, d: H0 * d, True, lambda H0, d: linear_graph(H0, 0, "거리(Mpc)", "후퇴속도(km/s)", "허블의법칙"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "슈테판-볼츠만 법칙", r"E = \sigma T^4", "흑체 단위 면적당 방출 에너지는 절대온도의 4제곱에 비례합니다.", {"T": "절대온도 T (K)"}, lambda T: (5.67e-8) * (T**4), True, lambda T: (np.linspace(1000, 10000, 100), (5.67e-8)*(np.linspace(1000, 10000, 100)**4), "온도(K)", "방출에너지", "온도-에너지"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "별의 광도 공식", r"L = 4\pi R^2 \sigma T^4", "별의 광도는 반지름의 제곱과 표면온도 4제곱의 곱에 비례합니다.", {"R": "반지름 R (상대값)", "T": "표면온도 T (K)"}, lambda R, T: (R**2) * ((T/5778)**4))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "빈의 변위 법칙", r"\lambda_{max} = \frac{A}{T}", "최대 에너지를 방출하는 파장은 표면 온도에 반비례합니다.", {"T": "표면온도 T (K)"}, lambda T: 2.898e-3 / (T if T!=0 else 1e-9), True, lambda T: inverse_graph(2.898e-3, "온도(K)", "최대파장(m)", "빈의변위"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "거리지수 공식", r"m - M = 5 \log_{10} d - 5", "겉보기 등급(m)과 절대 등급(M)의 차이로 거리를 산출합니다.", {"d": "거리 d (pc)"}, lambda d: 5 * np.log10(max(1e-9, d)) - 5, True, lambda d: (np.linspace(10, 1000, 100), 5*np.log10(np.linspace(10, 1000, 100))-5, "거리(pc)", "거리지수", "거리-거리지수"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "연주시차와 거리", r"d = \frac{1}{p}", "연주시차 p초의 역수가 파세크(pc) 거리입니다.", {"p": "연주시차 p (초)"}, lambda p: 1 / (p if p!=0 else 1e-9), True, lambda p: inverse_graph(1, "시차(초)", "거리(pc)", "시차-거리"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "도플러 시선 속도", r"v = c \cdot \frac{\Delta \lambda}{\lambda_0}", "스펙트럼 파장 편이량을 이용한 천체의 시선 속도 산출식입니다.", {"dlam": "파장변화량 dlam", "lam0": "기준파장 lam0"}, lambda dlam, lam0: 3e5 * (dlam / (lam0 if lam0!=0 else 1e-9)))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "PS시 진원 거리", r"d = \frac{v_P v_S}{v_P - v_S} \cdot t_{PS}", "P파와 S파 도달 차이시간(PS시)으로 구하는 진원 거리입니다.", {"vP": "P파속도 (km/s)", "vS": "S파속도 (km/s)", "t": "PS시 (s)"}, lambda vP, vS, t: ((vP * vS)/((vP - vS) if (vP-vS)!=0 else 1e-9)) * t, True, lambda vP, vS, t=1: linear_graph((vP*vS)/((vP-vS) if (vP-vS)!=0 else 1e-9), 0, "PS시(s)", "거리(km)", "PS시-진원거리"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "포그슨 방정식 (등급 광도비)", r"\frac{L_1}{L_2} = 2.512^{m_2 - m_1}", "별의 등급 차이에 따른 광도 비 공식입니다 (5등급 차 = 100배).", {"m1": "m1 등급", "m2": "m2 등급"}, lambda m1, m2: 2.512**(m2 - m1))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "해수 염분 (PSU)", r"S = \frac{\text{염류 질량 (g)}}{\text{해수 1000g}} \times 1000", "해수 1kg 속에 녹아 있는 총 염류의 g수입니다.", {"salt": "염류 g", "water": "해수 g"}, lambda salt, water: (salt / (water if water!=0 else 1e-9)) * 1000)
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "방사성 동위원소 반감기", r"N(t) = N_0 \left(\frac{1}{2}\right)^{\frac{t}{T}}", "반감기 T를 통해 남아있는 모원소 양을 산출하는 반감기 식입니다.", {"N0": "초기량 N0", "t": "경과시간 t", "T": "반감기 T"}, lambda N0, t, T: N0 * ((0.5)**(t / (T if T!=0 else 1e-9))), True, lambda N0, t, T=1: (np.linspace(0, 5*(T if T!=0 else 1), 100), N0 * ((0.5)**(np.linspace(0, 5*(T if T!=0 else 1), 100)/(T if T!=0 else 1))), "시간", "모원소양", "반감기붕괴"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "퇴적암 수심 수압 관계", r"P = \rho g d", "퇴적 환경에서 수심 d에 따른 수압 계산식입니다.", {"rho": "해수밀도 (kg/m³)", "d": "수심 d (m)"}, lambda rho, d: rho * 9.8 * d, True, lambda rho, d: linear_graph(rho*9.8, 0, "수심(m)", "수압(Pa)", "수심-수압"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "지진 규모와 에너지 관계", r"\log_{10} E = 11.8 + 1.5 M", "지진 규모 M과 방출 에너지 E 사이의 리히터 로그 관계식입니다.", {"M": "지진 규모 M"}, lambda M: 10**(11.8 + 1.5*M))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "상대 습도 계산식", r"\text{상대습도} = \frac{\text{현재 수증기량}}{\text{포화 수증기량}} \times 100", "현재 공기 중 수증기량과 포화 수증기량의 백분율입니다.", {"curr": "현재 수증기량", "sat": "포화 수증기량"}, lambda curr, sat: (curr / (sat if sat!=0 else 1e-9)) * 100)
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "이슬점과 단열 감율", r"T_d = T_0 - 0.2 h", "공기 덩어리 상승 시 높이 h(m)에 따른 이슬점 변화입니다.", {"T0": "지표 이슬점 (℃)", "h": "높이 h (m)"}, lambda T0, h: T0 - 0.002 * h, True, lambda T0, h: linear_graph(-0.002, T0, "높이(m)", "이슬점(℃)", "높이-이슬점"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "건조 단열 감율", r"T = T_0 - 1.0 \times \frac{h}{100}", "불포화 공기 덩어리 상승 시 100m당 1℃ 하강하는 감율입니다.", {"T0": "지표 온도 (℃)", "h": "높이 h (m)"}, lambda T0, h: T0 - 0.01 * h, True, lambda T0, h: linear_graph(-0.01, T0, "높이(m)", "온도(℃)", "높이-건조단열"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "습윤 단열 감율", r"T = T_0 - 0.5 \times \frac{h}{100}", "포화 공기 덩어리 상승 시 100m당 0.5℃ 하강하는 감율입니다.", {"T0": "응결 고도 온도 (℃)", "h": "상승 높이 h (m)"}, lambda T0, h: T0 - 0.005 * h, True, lambda T0, h: linear_graph(-0.005, T0, "높이(m)", "온도(℃)", "높이-습윤단열"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "푄 현상 (높새바람) 온도", r"T_{after} = T_{init} - 1.0 h_1 + 0.5 h_1 + 1.0 h_2", "산맥을 넘어 내리는 공기의 단열 변화 온도 산출식입니다.", {"Ti": "초기온도", "h1": "산높이 (km)"}, lambda Ti, h1: Ti - 10*h1 + 5*h1 + 10*h1)
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "우주 적색 편이량", r"z = \frac{\Delta \lambda}{\lambda_0}", "빛의 파장 증가량을 통한 우주 적색편이 지수 z입니다.", {"dlam": "파장변화량", "lam0": "기준파장"}, lambda dlam, lam0: dlam / (lam0 if lam0!=0 else 1e-9))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "우주 팽창 인자 a(t)", r"1 + z = \frac{a(t_0)}{a(t)}", "적색 편이 z와 우주 척도 인자 a(t)의 관계식입니다.", {"z": "적색편이 z"}, lambda z: 1 + z)
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "해일파 전파 속도", r"v = \sqrt{g d}", "수심 d인 얕은 바다에서 지진해일(쓰나미) 전파 속도입니다.", {"d": "수심 d (m)", "g": "중력가속도 (9.8)"}, lambda d, g=9.8: np.sqrt(max(0.0, g * d)), True, lambda d, g=9.8: (np.linspace(1, 4000, 100), np.sqrt(g * np.linspace(1, 4000, 100)), "수심(m)", "속도(m/s)", "수심-해일속도"))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "해석 파동 파장 속도 관계", r"c = \frac{g T}{2\pi}", "심해파에서의 파동 속도 c와 주기 T의 관계입니다.", {"T": "주기 T (s)"}, lambda T: (9.8 * T) / (2 * np.pi))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "지구 자전 속도 (위도별)", r"v = v_{eq} \cos \phi", "위도 φ에 따른 지구 자전 선속도 계산식입니다.", {"veq": "적도속도 (465 m/s)", "lat": "위도 (도)"}, lambda veq, lat: veq * np.cos(np.radians(lat)))
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "태양 상수 수지", r"S_0 = 1361 \text{ W/m}^2", "지구 대기 상단 단위 면적에 수직 입사하는 태양 복사에너지입니다.", {"s0": "태양상수"}, lambda s0: s0)
    add_f("2학년 (고등학교 2학년)", "지구과학Ⅰ", "알베도 (반사율)", r"A = \frac{\text{반사 에너지}}{\text{입사 에너지}} \times 100", "지표면이나 구름이 입사 에너지를 반사하는 비율입니다.", {"ref": "반사에너지", "inc": "입사에너지"}, lambda ref, inc: (ref / (inc if inc!=0 else 1e-9)) * 100)

    # ==================== [3학년 물리학Ⅱ: 131~155] ====================
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "돌림힘 (토크)", r"\tau = r F \sin \theta", "회전축으로부터 거리 r과 작용한 힘 F의 회전 효과입니다.", {"r": "거리 r (m)", "F": "힘 F (N)"}, lambda r, F: r * F, True, lambda r, F: linear_graph(F, 0, "거리(m)", "토크(N·m)", "거리-토크"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "포탄 운동 최고 높이", r"h = \frac{(v_0 \sin \theta)^2}{2g}", "비스듬히 쏘아올린 포탄의 최고 도달 높이입니다.", {"v0": "초속 v0 (m/s)", "deg": "각도 (도)"}, lambda v0, deg: ((v0 * np.sin(np.radians(deg)))**2) / (2 * 9.8))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "포탄 운동 수평 도달 거리", r"R = \frac{v_0^2 \sin 2\theta}{g}", "비스듬히 쏘아올린 포탄의 수평 도달 거리입니다.", {"v0": "초속 v0 (m/s)", "deg": "각도 (도)"}, lambda v0, deg: ((v0**2) * np.sin(np.radians(2*deg))) / 9.8)
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "구심 가속도", r"a_c = \frac{v^2}{r} = r \omega^2", "등속 원운동하는 물체의 구심 가속도 공식입니다.", {"v": "선속도 v (m/s)", "r": "반지름 r (m)"}, lambda v, r: (v**2) / (r if r!=0 else 1e-9), True, lambda v, r=1: square_graph(1/(r if r!=0 else 1e-9), "속도(m/s)", "구심가속도", "속도-구심가속도"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "구심력", r"F_c = m \frac{v^2}{r} = m r \omega^2", "등속 원운동을 유지시키는 원중심 방향의 힘입니다.", {"m": "질량 m (kg)", "v": "속도 v (m/s)", "r": "반지름 r (m)"}, lambda m, v, r: m * (v**2) / (r if r!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "각속도와 주기 관계", r"\omega = \frac{2\pi}{T} = 2\pi f", "각속도 ω와 공전/회전 주기 T의 관계식입니다.", {"T": "주기 T (s)"}, lambda T: (2 * np.pi) / (T if T!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "단진자 주기", r"T = 2\pi \sqrt{\frac{L}{g}}", "실의 길이 L인 단진자의 소각도 진동 주기 공식입니다.", {"L": "길이 L (m)"}, lambda L: 2 * np.pi * np.sqrt(max(0.0, L / 9.8)), True, lambda L: (np.linspace(0.1, 10, 100), 2*np.pi*np.sqrt(np.linspace(0.1, 10, 100)/9.8), "길이(m)", "주기(s)", "길이-주기"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "용수철 단진동 주기", r"T = 2\pi \sqrt{\frac{m}{k}}", "질량 m과 용수철상수 k의 단진동 주기입니다.", {"m": "질량 m (kg)", "k": "용수철상수 k (N/m)"}, lambda m, k: 2 * np.pi * np.sqrt(max(0.0, m / (k if k!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "케플러 제1법칙 타원 방정식", r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1", "행성의 궤도 타원 방정식입니다.", {"a": "장반경 a", "b": "단반경 b"}, lambda a, b: a * b)
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "케플러 제2법칙 (면적속도 보존)", r"\frac{dA}{dt} = \frac{1}{2} r v \sin \theta = \text{일정}", "행성과 태양을 잇는 선분이 단위 시간당 훑고 지나가는 면적은 일정합니다.", {"r": "거리 r", "v": "속도 v"}, lambda r, v: 0.5 * r * v)
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "케플러 제3법칙 (조화 법칙)", r"T^2 = k a^3", "공전 주기 T의 제곱은 긴반지름 a의 세제곱에 비례합니다.", {"a": "긴반지름 a (AU)"}, lambda a: np.sqrt(max(0.0, a**3)), True, lambda a: (np.linspace(0.1, 10, 100), np.sqrt(np.linspace(0.1, 10, 100)**3), "긴반지름(AU)", "주기(년)", "케플러3법칙"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "탈출 속도 (제2 우주 속도)", r"v_{esc} = \sqrt{\frac{2 G M}{R}}", "행성의 중력권을 탈출하기 위한 최소 초속도 공식입니다.", {"M": "행성질량 M (kg)", "R": "행성반지름 R (m)"}, lambda M, R: np.sqrt(max(0.0, 2 * (6.67e-11) * M / (R if R!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "인공위성 궤도 속도 (제1 우주 속도)", r"v = \sqrt{\frac{G M}{R}}", "행성 주위를 원궤도로 공전하기 위한 속도 공식입니다.", {"M": "행성질량 M (kg)", "R": "궤도반지름 R (m)"}, lambda M, R: np.sqrt(max(0.0, (6.67e-11) * M / (R if R!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "전위차와 전기장", r"V = E \cdot d", "균일한 전기장 E 내에서 거리 d만큼 떨어진 두 점 사이의 전위차입니다.", {"E": "전기장 E (V/m)", "d": "거리 d (m)"}, lambda E, d: E * d, True, lambda E, d: linear_graph(E, 0, "거리(m)", "전위차(V)", "거리-전위차"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "점전하에 의한 전기장", r"E = k \frac{|q|}{r^2}", "점전하 q가 거리 r 떨어진 곳에 만드는 전기장 세기입니다.", {"q": "전하 q (C)", "r": "거리 r (m)"}, lambda q, r: (8.99e9) * abs(q) / ((r**2) if r!=0 else 1e-9), True, lambda q, r=1: inverse_graph((8.99e9)*abs(q), "거리(m)", "전기장(V/m)", "거리-전기장"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "축전기 전기용량", r"C = \epsilon \frac{A}{d}", "평행판 축전기의 극판 면적 A와 거리 d에 따른 전기용량입니다.", {"A": "면적 A (m²)", "d": "간격 d (m)"}, lambda A, d: (8.85e-12) * A / (d if d!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "축전기 저장 에너지", r"U = \frac{1}{2} C V^2 = \frac{1}{2} Q V", "전압 V로 충전된 축전기에 저장되는 전기 에너지입니다.", {"C": "전기용량 C (F)", "V": "전압 V (V)"}, lambda C, V: 0.5 * C * (V**2), True, lambda C, V: square_graph(0.5*C, "전압(V)", "에너지(J)", "전압-저장에너지"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "로런츠 힘 (자기력)", r"F = q v B \sin \theta", "자기장 B 속에서 속도 v로 이동하는 전하 q가 받는 힘입니다.", {"q": "전하 q (C)", "v": "속도 v (m/s)", "B": "자기장 B (T)"}, lambda q, v, B: q * v * B)
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "원운동하는 전하의 궤도 반지름", r"r = \frac{m v}{q B}", "자기장 내 수직 입사한 전하의 원운동 반지름 공식입니다.", {"m": "질량 m", "v": "속도 v", "q": "전하 q", "B": "자기장 B"}, lambda m, v, q, B: (m * v) / ((q * B) if (q*B)!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "RLC 회로 임피던스", r"Z = \sqrt{R^2 + (X_L - X_C)^2}", "교류 RLC 회로 전체의 합성 저항(임피던스) 공식입니다.", {"R": "저항 R (Ω)", "XL": "유도리액턴스 XL", "XC": "용량리액턴스 XC"}, lambda R, XL, XC: np.sqrt(R**2 + (XL - XC)**2))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "RLC 회로 공진 진동수", r"f_0 = \frac{1}{2\pi \sqrt{L C}}", "유도리액턴스와 용량리액턴스가 같아지는 공진 진동수입니다.", {"L": "인덕턴스 L (H)", "C": "전기용량 C (F)"}, lambda L, C: 1 / (2 * np.pi * np.sqrt(max(1e-18, L * C))))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "볼츠만 평균 운동 에너지", r"E_k = \frac{3}{2} k_B T", "단원자 이상기체 분자 1개의 평균 기체 운동 에너지입니다.", {"T": "절대온도 T (K)"}, lambda T: 1.5 * (1.38e-23) * T, True, lambda T: linear_graph(1.5*1.38e-23, 0, "온도(K)", "평균에너지(J)", "온도-평균에너지"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "기체 분자 제곱평균제곱근 속도", r"v_{rms} = \sqrt{\frac{3 R T}{M}}", "기체 분자들의 평균 열운동 속도 식입니다.", {"T": "온도 T (K)", "M": "몰질량 M (kg/mol)"}, lambda T, M: np.sqrt(max(0.0, 3 * 8.314 * T / (M if M!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "로런츠 인자 (상대론)", r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}", "속도 v에 따른 특수상대론 계수 γ입니다.", {"v_ratio": "v/c 비율 (0~0.99)"}, lambda v_ratio: 1 / np.sqrt(max(1e-9, 1 - min(0.99, v_ratio)**2)), True, lambda v_ratio: (np.linspace(0, 0.95, 100), 1/np.sqrt(1-np.linspace(0, 0.95, 100)**2), "v/c", "gamma", "속도-로런츠인자"))
    add_f("3학년 (고등학교 3학년)", "물리학Ⅱ", "상대론적 운동량", r"p = \gamma m v", "상대론적 효과가 고려된 물체의 운동량입니다.", {"gamma": "로런츠인자 gamma", "m": "질량 m", "v": "속도 v"}, lambda gamma, m, v: gamma * m * v)

    # ==================== [3학년 화학Ⅱ: 156~180] ====================
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "몰랄농도 (Molality)", r"m = \frac{\text{용질 몰수 (mol)}}{\text{용매 질량 (kg)}}", "용매 1kg 속에 녹아 있는 용질의 몰수입니다.", {"n": "용질 몰수 n (mol)", "W": "용매 질량 W (kg)"}, lambda n, W: n / (W if W!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "라울의 법칙 (증기압 내림)", r"P_{sol} = X_{solvent} \cdot P^\circ_{solvent}", "용액의 증기압은 용매 몰분율과 순수 증기압의 곱입니다.", {"X": "용매 몰분율 X", "P0": "순수 증기압 P0"}, lambda X, P0: X * P0)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "끓는점 오름 공식", r"\Delta T_b = K_b \cdot m", "비휘발성 용질에 의한 끓는점 상승 온도 변화량입니다.", {"Kb": "몰랄오름상수 Kb", "m": "몰랄농도 m"}, lambda Kb, m: Kb * m, True, lambda Kb, m: linear_graph(Kb, 0, "몰랄농도", "끓는점오름(℃)", "농도-끓는점오름"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "어는점 내림 공식", r"\Delta T_f = K_f \cdot m", "비휘발성 용질에 의한 어는점 강하 온도 변화량입니다.", {"Kf": "몰랄내림상수 Kf", "m": "몰랄농도 m"}, lambda Kf, m: Kf * m, True, lambda Kf, m: linear_graph(Kf, 0, "몰랄농도", "어는점내림(℃)", "농도-어는점내림"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "삼투압 반트호프 식", r"\Pi = M R T", "묽은 용액의 삼투압은 몰농도 M과 절대온도 T에 비례합니다.", {"M": "몰농도 M (M)", "T": "절대온도 T (K)"}, lambda M, T: M * 0.0821 * T, True, lambda M, T: linear_graph(0.0821*T, 0, "몰농도(M)", "삼투압(atm)", "농도-삼투압"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "그레이엄 기체 확산 법칙", r"\frac{v_A}{v_B} = \sqrt{\frac{M_B}{M_A}}", "기체 확산 속도는 분자량의 제곱근에 반비례합니다.", {"MA": "A 분자량", "MB": "B 분자량"}, lambda MA, MB: np.sqrt(max(0.0, MB / (MA if MA!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "반응 엔탈피 변화", r"\Delta H = H_{prod} - H_{react}", "생성물 엔탈피 총합에서 반응물 엔탈피 총합을 뺀 값입니다.", {"Hp": "생성물 엔탈피", "Hr": "반응물 엔탈피"}, lambda Hp, Hr: Hp - Hr)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "헤스 법칙 (엔탈피 합)", r"\Delta H = \Delta H_1 + \Delta H_2", "총 반응 엔탈피는 반응 경로에 관계없이 일정합니다.", {"H1": "H1 (kJ)", "H2": "H2 (kJ)"}, lambda H1, H2: H1 + H2)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "1차 반응 속도식", r"v = k [A]", "반응 속도가 반응물 A 농도에 1차 비례하는 식입니다.", {"k": "속도상수 k", "A": "농도 [A] (M)"}, lambda k, A: k * A, True, lambda k, A: linear_graph(k, 0, "농도(M)", "속도", "농도-반응속도"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "1차 반응 반감기", r"t_{1/2} = \frac{\ln 2}{k} \approx \frac{0.693}{k}", "1차 반응에서 반응물 농도가 절반으로 줄어드는 시간입니다.", {"k": "속도상수 k"}, lambda k: 0.693 / (k if k!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "2차 반응 속도식", r"v = k [A]^2", "반응 속도가 반응물 농도의 제곱에 비례하는 반응식입니다.", {"k": "속도상수 k", "A": "농도 [A] (M)"}, lambda k, A: k * (A**2), True, lambda k, A: square_graph(k, "농도(M)", "속도", "농도-2차속도"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "아레니우스 속도상수 온도 식", r"k = A e^{-\frac{E_a}{R T}}", "온도 T와 활성화 에너지 Ea에 따른 반응 속도 상수 k 공식입니다.", {"Ea": "Ea (J/mol)", "T": "온도 T (K)"}, lambda Ea, T: np.exp(-Ea / (8.314 * (T if T!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "아레니우스 두 온도 반응상수 비", r"\ln\frac{k_2}{k_1} = \frac{E_a}{R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)", "두 온도 T1, T2에서의 속도상수 변화 관계식입니다.", {"Ea": "Ea (J/mol)", "T1": "T1 (K)", "T2": "T2 (K)"}, lambda Ea, T1, T2: (Ea / 8.314) * (1/(T1 if T1!=0 else 1e-9) - 1/(T2 if T2!=0 else 1e-9)))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "압력 평형 상수 Kp", r"K_p = K_c (R T)^{\Delta n}", "농도 평형상수 Kc와 압력 평형상수 Kp의 관계식입니다.", {"Kc": "Kc", "T": "온도 T (K)", "dn": "몰수변화 dn"}, lambda Kc, T, dn: Kc * ((0.0821 * T)**dn))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "르샤틀리에 평형 이동 지수 Q", r"Q < K \Rightarrow \text{정반응 진행}", "반응商 Q와 평형상수 K 비교를 통한 진행 방향 예측입니다.", {"Q": "반응상 Q", "K": "평형상수 K"}, lambda Q, K: Q - K)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "핸더슨-하셀바흐 완충용액 식", r"\text{pH} = pK_a + \log_{10}\frac{[A^-]}{[HA]}", "완충 용액의 pH를 산 이온화 상수와 농도비로 계산하는 식입니다.", {"pKa": "pKa", "A": "[A-]", "HA": "[HA]"}, lambda pKa, A, HA: pKa + np.log10(max(1e-9, A / (HA if HA!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "기브스 자유 에너지", r"\Delta G = \Delta H - T \Delta S", "자발적 반응 여부를 결정하는 기브스 자유 에너지 공식입니다.", {"dH": "dH (kJ)", "T": "온도 T (K)", "dS": "dS (kJ/K)"}, lambda dH, T, dS: dH - T * dS, True, lambda dH, T, dS: linear_graph(-dS, dH, "온도(K)", "자유에너지(kJ)", "온도-자유에너지"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "표준 전지 전위", r"E^\circ_{cell} = E^\circ_{cathode} - E^\circ_{anode}", "환원 전위차를 이용한 화학 전지의 표준 전압 계산식입니다.", {"Ec": "환원극 전위", "Ea": "산화극 전위"}, lambda Ec, Ea: Ec - Ea)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "네른스트 방정식 (비표준 전지 전위)", r"E = E^\circ - \frac{0.0592}{n} \log_{10} Q", "반응물 농도 조건 Q에 따른 전지 전위 E 변화식입니다.", {"E0": "표준전위 E0", "n": "전자수 n", "Q": "반응상 Q"}, lambda E0, n, Q: E0 - (0.0592 / (n if n!=0 else 1)) * np.log10(max(1e-9, Q)))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "패러데이 전기분해 석출량", r"w = \frac{M \cdot I \cdot t}{n \cdot F}", "전기분해 시 석출되는 물질의 질량 w 공식입니다.", {"M": "분자량 M", "I": "전류 I (A)", "t": "시간 t (s)", "n": "전하수 n"}, lambda M, I, t, n: (M * I * t) / ((n * 96500) if n!=0 else 1e-9), True, lambda M, I, t=1, n=1: linear_graph(M*t/(n*96500), 0, "전류(A)", "석출질량(g)", "전류-석출량"))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "결정 격자 밀도 계산식", r"\rho = \frac{n \cdot M}{N_A \cdot a^3}", "단위 세포 길이에 따른 결정의 밀도 계산 공식입니다.", {"n": "입자수 n", "M": "원자량 M", "a": "세포길이 a (cm)"}, lambda n, M, a: (n * M) / ((6.022e23 * (a**3)) if a!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "증기압 내림율", r"\frac{\Delta P}{P^\circ} = X_{solute}", "순수한 용매 증기압에 대한 내림 비율은 용질 몰분율과 같습니다.", {"X": "용질 몰분율"}, lambda X: X)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "용해도 적 상수 Ksp", r"K_{sp} = [M^{m+}]^n [A^{n-}]^m", "난용성 염의 침전 이온화 평형 상수입니다.", {"c1": "이온1 농도", "c2": "이온2 농도"}, lambda c1, c2: c1 * c2)
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "엔트로피 변화량", r"\Delta S = \frac{Q_{rev}}{T}", "가역 과정에서 일어나는 엔트로피 변화 계산식입니다.", {"Q": "가역열량 Q (J)", "T": "온도 T (K)"}, lambda Q, T: Q / (T if T!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "화학Ⅱ", "자유 에너지와 평형 상수", r"\Delta G^\circ = -R T \ln K", "표준 기브스 자유 에너지와 화학 평형 상수 K의 관계식입니다.", {"T": "온도 T (K)", "K": "평형상수 K"}, lambda T, K: -8.314 * T * np.log(max(1e-9, K)))

    # ==================== [3학년 생명과학Ⅱ: 181~195] ====================
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "미카엘리스-멘텐 효소 속도식", r"v = \frac{V_{max} [S]}{K_m + [S]}", "기질 농도 [S]에 따른 효소 반응 속도 산출 공식입니다.", {"Vmax": "Vmax", "Km": "Km", "S": "[S] 농도"}, lambda Vmax, Km, S: (Vmax * S) / ((Km + S) if (Km+S)!=0 else 1e-9), True, lambda Vmax, Km, S=1: (np.linspace(0, 50, 100), (Vmax*np.linspace(0, 50, 100))/(Km+np.linspace(0, 50, 100)), "기질농도", "속도", "미카엘리스멘텐"))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "라인위버-버크 이중 역수 식", r"\frac{1}{v} = \frac{K_m}{V_{max}}\frac{1}{[S]} + \frac{1}{V_{max}}", "미카엘리스-멘텐 식을 직선 형태로 변환한 역수 방정식입니다.", {"Km": "Km", "Vmax": "Vmax", "S": "[S]"}, lambda Km, Vmax, S: (Km / (Vmax if Vmax!=0 else 1e-9)) * (1/(S if S!=0 else 1e-9)) + (1/(Vmax if Vmax!=0 else 1e-9)))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "세포 호흡 총 ATP 생산량", r"C_6H_{12}O_6 + 6O_2 \rightarrow 6CO_2 + 6H_2O + 30 \sim 32 \text{ ATP}", "포도당 1분자가 완전 산화될 때 생성되는 ATP 수량입니다.", {"n": "포도당 몰수"}, lambda n: n * 32)
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "포도당 발효 이산화탄소 생성", r"C_6H_{12}O_6 \rightarrow 2C_2H_5OH + 2CO_2 + 2 \text{ ATP}", "알코올 발효 시 포도당 1분자당 생성되는 CO2 및 ATP 수입니다.", {"n": "포도당 몰수"}, lambda n: n * 2)
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "힐(Hill) 계수 (효소 협동성)", r"\theta = \frac{[L]^n}{K_d + [L]^n}", "결합 리간드 농도 [L]과 올리고머 단백질 결합 비의 관계입니다.", {"L": "리간드 농도", "n": "힐 계수 n"}, lambda L, n: (L**n) / (1 + (L**n)))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "DNA 샤가프 법칙", r"A = T, \quad G = C, \quad \frac{A+G}{T+C} = 1", "이중 가닥 DNA에서 아데닌과 티민, 구아닌과 시토신 비율은 같습니다.", {"A": "A 비율 (%)"}, lambda A: (A, A, 50-A, 50-A))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "세포 분열 염색체 수와 DNA 양", r"2n, 4c \rightarrow n, 2c \rightarrow n, 1c", "감수 분열 단계에 따른 염색체 수와 상대적 DNA 양 변화입니다.", {"c": "상대 DNA 양 c"}, lambda c: c / 2)
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "유전자 재조합 빈도 (교차율)", r"\text{교차율(\%)} = \frac{\text{재조합 개체수}}{\text{전체 자손수}} \times 100", "두 유전자 사이의 교차율로 유전자 지도를 작성하는 공식입니다.", {"rec": "재조합 개체수", "total": "전체 자손수"}, lambda rec, total: (rec / (total if total!=0 else 1e-9)) * 100)
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "엽록체 광합성 명반응 ATP/NADPH 생성비", r"3 \text{ ATP} : 2 \text{ NADPH}", "비순환적 전자 전달계에서의 ATP 및 NADPH 생성 비율입니다.", {"nadph": "NADPH 분자수"}, lambda nadph: nadph * (1.5))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "루비스코(Rubisco) CO2 고정 효율", r"\text{고정율} \propto \frac{[CO_2]}{[O_2]}", "CO2 농도와 O2 농도 비에 따른 루비스코 탄소 고정 비례식입니다.", {"co2": "CO2 농도", "o2": "O2 농도"}, lambda co2, o2: co2 / (o2 if o2!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "PCR 유전자 증폭 수량", r"N_t = N_0 \times 2^n", "n회 회차 중합효소 연쇄 반응(PCR) 후 증폭된 DNA 가닥 수입니다.", {"N0": "초기 가닥수 N0", "n": "사이클 수 n"}, lambda N0, n: N0 * (2**n), True, lambda N0, n=1: (np.linspace(1, 30, 30), N0 * (2**np.linspace(1, 30, 30)), "사이클(n)", "DNA수", "PCR증폭"))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "制限酵素 절단 조각 수", r"N_{fragments} = N_{sites} + 1", "선형 DNA 단편에서 제한효소 인식 부위 수에 따른 조각 수 공식입니다.", {"sites": "인식 절단 부위 수"}, lambda sites: sites + 1)
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "원심분리 침강 계수 (Svedberg)", r"s = \frac{v}{\omega^2 r}", "초원심분리기에서의 입자 침도 s(Svedberg 단위) 산출 공식입니다.", {"v": "침강속도 v", "w": "각속도 w", "r": "반지름 r"}, lambda v, w, r: v / (( (w**2)*r ) if (w**2*r)!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "세균 이분법 개체 증식", r"N(t) = N_0 \cdot 2^{t / g}", "세대 시간 g에 따른 세균 개체수 증가 지수 공식입니다.", {"N0": "초기 세균수", "t": "경과시간 t", "g": "세대시간 g"}, lambda N0, t, g: N0 * (2**(t / (g if g!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "생명과학Ⅱ", "흡수도 (빛 흡광도 Lambert-Beer)", r"A = \epsilon \cdot c \cdot l", "분광광도계에서 용액 농도 c와 빛 통과 길이 l에 따른 흡광도 식입니다.", {"eps": "흡광계수 eps", "c": "농도 c (M)", "l": "길이 l (cm)"}, lambda eps, c, l: eps * c * l, True, lambda eps, c, l=1: linear_graph(eps*l, 0, "농도(M)", "흡광도(A)", "농도-흡광도"))

    # ==================== [3학년 지구과학Ⅱ: 196~210] ====================
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "정역학 방정식 (대기/해수)", r"\frac{\Delta P}{\Delta z} = -\rho g", "연직 방향 기압 및 수압 경사력과 중력의 균형 방정식입니다.", {"rho": "밀도 rho (kg/m³)", "dz": "높이변화 dz (m)"}, lambda rho, dz: rho * 9.8 * dz, True, lambda rho, dz: linear_graph(rho*9.8, 0, "높이(m)", "압력변화(Pa)", "높이-압력"))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "전향력 (코리올리 힘)", r"F = 2 m v \Omega \sin \phi", "지구 자전에 의해 회전 좌표계에서 발생하는 전향력 공식입니다.", {"m": "질량 m", "v": "속도 v (m/s)", "lat": "위도 (도)"}, lambda m, v, lat: 2 * m * v * (7.292e-5) * np.sin(np.radians(lat)))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지풍 (Geostrophic Wind) 속도", r"v_g = \frac{1}{\rho f} \frac{\Delta P}{\Delta n}", "기압경도력과 전향력이 평형을 이룰 때 부는 바람 속도입니다.", {"dP": "기압차 dP (Pa)", "rho": "밀도 rho"}, lambda dP, rho: dP / ((rho * 1e-4) if rho!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "경풍 (Gradient Wind) 방정식", r"\frac{v^2}{R} + f v = \frac{1}{\rho}\frac{\Delta P}{\Delta n}", "곡선 등압선에서 구심력, 전향력, 기압경도력의 평형 방정식입니다.", {"f": "코리올리파라미터 f", "dP": "기압경도 dP"}, lambda f, dP: dP / (f if f!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "경도풍 지경풍 비율", r"v_{grad} = v_g \left(1 \pm \frac{v}{f R}\right)", "고기압과 저기압 주변에서의 경도풍 속도 수정 공식입니다.", {"vg": "지풍속도 vg", "v": "속도 v"}, lambda vg, v: vg * (1 + 0.1*v))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지상풍 풍향 마찰각", r"\tan \alpha = \frac{F_k}{f v}", "마찰력 Fk에 의해 등압선을 横切는 지상풍 마찰각 α 산출 공식입니다.", {"Fk": "마찰력 Fk", "fv": "전향력 fv"}, lambda Fk, fv: np.degrees(np.arctan(Fk / (fv if fv!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지형류 (Geostrophic Current)", r"v = \frac{g}{f} \tan \theta", "수면 경사에 의한 수압경도력과 전향력 평형의 해류 속도입니다.", {"deg": "수면경사각 (도)", "lat": "위도 (도)"}, lambda deg, lat: (9.8 / (2*(7.292e-5)*np.sin(np.radians(lat)) if lat!=0 else 1e-9)) * np.tan(np.radians(deg)))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "에크만 수송 (Ekman Transport)", r"V_E = \frac{\tau}{\rho f}", "바람의 응력 τ에 의해 북반구에서 오른쪽 90도로 수송되는 물의 양입니다.", {"tau": "바람응력 tau", "rho": "해수밀도 rho"}, lambda tau, rho: tau / ((rho * 1e-4) if rho!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "우주 임계 밀도", r"\rho_c = \frac{3 H_0^2}{8 \pi G}", "우주의 평탄한 팽창 구조를 결정하는 임계 밀도 공식입니다.", {"H0": "허블상수 H0 (s^-1)"}, lambda H0: (3 * (H0**2)) / (8 * np.pi * 6.67e-11))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "우주 밀도 파라미터 \Omega", r"\Omega = \frac{\rho}{\rho_c}", "우주 물질 밀도와 임계 밀도의 비입니다 (\Omega=1 이면 평탄 우주).", {"rho": "현재밀도 rho", "rhoc": "임계밀도 rhoc"}, lambda rho, rhoc: rho / (rhoc if rhoc!=0 else 1e-9))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "우주 감속 파라미터 q0", r"q_0 = -\frac{\ddot{a} a}{\dot{a}^2}", "우주 팽창 속도가 시간에 따라 변화하는 척도 지수입니다.", {"q": "감속지수 q"}, lambda q: q)
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지진파 P파 파동 속도", r"v_P = \sqrt{\frac{K + \frac{4}{3}\mu}{\rho}}", "매질의 체적 탄성률 K와 강성률 μ, 밀도 ρ에 따른 P파 속도입니다.", {"K": "체적탄성률 K", "mu": "강성률 mu", "rho": "밀도 rho"}, lambda K, mu, rho: np.sqrt(max(0.0, (K + (4/3)*mu) / (rho if rho!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지진파 S파 파동 속도", r"v_S = \sqrt{\frac{\mu}{\rho}}", "매질의 강성률 μ와 밀도 ρ에 따른 S파 (횡파) 속도 공식입니다.", {"mu": "강성률 mu", "rho": "밀도 rho"}, lambda mu, rho: np.sqrt(max(0.0, mu / (rho if rho!=0 else 1e-9))))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "지자기 감도 및 伏角 관계", r"\tan I = 2 \tan \phi", "지구 자북 위도 φ와 해당 지점에서의 복각 I 사이의 상관 공식입니다.", {"lat": "자북위도 (도)"}, lambda lat: np.degrees(np.arctan(2 * np.tan(np.radians(lat)))))
    add_f("3학년 (고등학교 3학년)", "지구과학Ⅱ", "천체 위치 구면삼각형 좌표", r"\sin a = \sin \phi \sin \delta + \cos \phi \cos \delta \cos h", "구면천문학에서 고도 a, 적위 δ, 시간각 h 변환 공식입니다.", {"lat": "위도 (도)", "dec": "적위 (도)", "h": "시간각 (도)"}, lambda lat, dec, h: np.degrees(np.arcsin(min(1.0, max(-1.0, np.sin(np.radians(lat))*np.sin(np.radians(dec)) + np.cos(np.radians(lat))*np.cos(np.radians(dec))*np.cos(np.radians(h)))))))

    return db

FORMULA_DB = build_database()

# 전체 공식 1차원 리스트 생성 (첫 화면 실시간 검색용)
ALL_FORMULAS = []
for grade_data in FORMULA_DB.values():
    for subj_formulas in grade_data.values():
        ALL_FORMULAS.extend(subj_formulas)

# ---------------------------------------------------------
# 5. Header Component & Navigation Bar
# ---------------------------------------------------------
nav_col1, nav_col2 = st.columns([1, 5])

with nav_col1:
    if st.session_state.grade is not None or st.session_state.formula is not None:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← 뒤로"):
            if st.session_state.formula is not None:
                reset_to_formula_list()
            elif st.session_state.subject is not None:
                reset_to_subject()
            else:
                reset_to_grade()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with nav_col2:
    st.markdown('<span class="badge-curr">2022 개정 교육과정 총 210개 핵심 공식 수록</span>', unsafe_allow_html=True)
    st.title("고등학교 과학 공식 모음")

st.divider()

# ---------------------------------------------------------
# 6. Global Search Input (첫 화면 및 모든 위치에서 즉시 검색 가능)
# ---------------------------------------------------------
search_query = st.text_input(
    "🔍 전 과목 통합 공식 검색 (200+ 공식 대상)", 
    placeholder="공식 이름, 설명 또는 미지수 기호(v, m, F, t, P, pH, λ 등) 입력...",
    key="global_search_input"
)
st.markdown(
    '<div class="search-hint">💡 <b>검색 팁:</b> \'v\', \'m\', \'속도\', \'질량\', \'전압\', \'pH\'처럼 기호나 키워드를 입력하면 해당하는 모든 공식이 즉시 검색됩니다.</div>', 
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# 7. Main Dynamic Router & View Renderer
# ---------------------------------------------------------
query = search_query.strip().lower()

# [상황 A] 글로벌 검색어가 입력되었을 경우 (카테고리 무관 즉시 목록 표시)
if query:
    st.markdown(f"### 🔍 '{search_query}' 검색 결과")
    
    filtered = []
    for f in ALL_FORMULAS:
        match_name = query in f["name"].lower()
        match_desc = query in f["desc"].lower()
        match_vars = any(query in k.lower() or query in v.lower() for k, v in f["vars"].items())
        match_subj = query in f["subject"].lower()
        if match_name or match_desc or match_vars or match_subj:
            filtered.append(f)
            
    if not filtered:
        st.info("검색어와 일치하는 미지수나 공식이 없습니다.")
    else:
        cols = st.columns(2)
        for idx, f in enumerate(filtered):
            var_list_str = ", ".join(f["vars"].keys())
            with cols[idx % 2]:
                btn_label = f"📑 {f['name']} [{f['subject']}]\n📌 미지수: {var_list_str}"
                if st.button(btn_label, key=f"search_f_{f['id']}"):
                    st.session_state.grade = f["grade"]
                    st.session_state.subject = f["subject"]
                    st.session_state.formula = f
                    st.rerun()

# [상황 B] 공식 상세 정보 화면 (Step 4)
elif st.session_state.formula is not None:
    f = st.session_state.formula
    st.markdown(f"## 💡 {f['name']}")
    st.markdown(f"<p style='color:var(--text-muted);'>{f['subject']} · {f['grade']}</p>", unsafe_allow_html=True)
    
    # LaTeX 수식 대형 박스
    st.markdown('<div class="math-display">', unsafe_allow_html=True)
    st.latex(f["latex"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 공식 설명 카드
    st.markdown(f"""
    <div class="desc-card">
        <h3 style="margin-bottom:12px;">📖 공식 설명</h3>
        <p style="color:#2C241B; margin:0;">{f['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    # 좌측: 미지수 입력 및 실시간 대입 계산기
    with col_left:
        st.markdown("### 🔢 기호/미지수 설명 및 실시간 대입 계산기")
        
        input_values = {}
        for var_key, var_desc in f["vars"].items():
            input_values[var_key] = st.number_input(
                label=f"▫️ {var_desc}",
                value=2.0,
                step=0.5,
                key=f"calc_in_{f['id']}_{var_key}"
            )
            
        if st.button("🧮 값 계산하기", key="run_calc"):
            try:
                res = f["calc"](**input_values)
                st.success(f"**계산 결과:** `{res}`")
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")

    # 우측: 실시간 그래프 시각화
    with col_right:
        st.markdown("### 📈 실시간 그래프 변화")
        if f["has_graph"] and f["graph_fn"] is not None:
            try:
                vals = list(input_values.values())
                try:
                    graph_res = f["graph_fn"](*vals)
                except TypeError:
                    graph_res = f["graph_fn"](*vals[:2])
                    
                x_vals, y_vals, xlabel, ylabel, title = graph_res
                
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor('#FFFDF5')
                ax.set_facecolor('#FFFFFF')
                
                ax.plot(x_vals, y_vals, color='#E27B58', linewidth=2.5)
                ax.set_title(title, fontsize=12, fontweight='bold', color='#332C23')
                ax.set_xlabel(xlabel, fontsize=10)
                ax.set_ylabel(ylabel, fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.5)
                
                st.pyplot(fig)
            except Exception as e:
                st.warning("이 대입값에서는 그래프를 표시할 수 없습니다. 적절한 수치를 입력해 주세요.")
        else:
            st.info("ℹ️ 이 공식은 고정 비율 또는 단일 상관식이므로 2D 연속 그래프를 제공하지 않습니다.")

# [상황 C] Step 3: 과목 내 공식 목록 화면
elif st.session_state.subject is not None:
    formulas = FORMULA_DB[st.session_state.grade][st.session_state.subject]
    st.markdown(f"## [{st.session_state.subject}] 공식 목록 (총 {len(formulas)}개)")
    
    cols = st.columns(2)
    for idx, f in enumerate(formulas):
        var_list_str = ", ".join(f["vars"].keys())
        with cols[idx % 2]:
            if st.button(f"📑 {f['name']}\n📌 미지수: {var_list_str}", key=f"form_{idx}"):
                st.session_state.formula = f
                st.rerun()

# [상황 D] Step 2: 학년 선택 후 과목 선택 화면
elif st.session_state.grade is not None:
    st.markdown(f"## [{st.session_state.grade}] 과목을 선택하세요")
    st.markdown("<p style='color: var(--text-muted); font-size: 1.3rem;'>공식을 확인하고 싶은 과목을 누르세요.</p>", unsafe_allow_html=True)
    
    subjects = list(FORMULA_DB[st.session_state.grade].keys())
    cols = st.columns(min(len(subjects), 4))
    for idx, subj in enumerate(subjects):
        count_f = len(FORMULA_DB[st.session_state.grade][subj])
        with cols[idx % len(cols)]:
            if st.button(f"📚 {subj}\n\n({count_f}개 공식)", key=f"subj_{idx}"):
                st.session_state.subject = subj
                st.rerun()

# [상황 E] Step 1: 첫 화면 (학년 선택 화면)
else:
    st.markdown("## 학년을 선택하세요")
    st.markdown("<p style='color: var(--text-muted); font-size: 1.3rem;'>배우고자 하는 고등학교 학년을 클릭하거나, 상단 검색창에서 바로 공식을 찾아보세요.</p>", unsafe_allow_html=True)
    
    grades = [
        {"key": "1학년 (통합과학 1·2)", "title": "🌱 고등학교 1학년", "desc": "통합과학 1 · 통합과학 2 (30개 공식)"},
        {"key": "2학년 (고등학교 2학년)", "title": "🌿 고등학교 2학년", "desc": "물리학Ⅰ, 화학Ⅰ, 생명과학Ⅰ, 지구과학Ⅰ (100개 공식)"},
        {"key": "3학년 (고등학교 3학년)", "title": "🌳 고등학교 3학년", "desc": "물리학Ⅱ, 화학Ⅱ, 생명과학Ⅱ, 지구과학Ⅱ (80개 공식)"}
    ]
    
    cols = st.columns(3)
    for idx, g in enumerate(grades):
        with cols[idx]:
            if st.button(f"{g['title']}\n\n{g['desc']}", key=f"grade_{idx}"):
                st.session_state.grade = g["key"]
                st.rerun()
