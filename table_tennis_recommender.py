import random
import streamlit as st


st.set_page_config(
    page_title="맞춤형 탁구채 추천!",
    page_icon="🏓",
    layout="centered",
)

# ---------------------------------------------------------
# 실제 판매되는 목판·러버 또는 완제품을 사용한 추천 데이터
# 저가: 100,000원 이하 / 고가: 100,000원 이상
# 가벼움: 180g 이하 / 무거움: 180g 초과
# 조립형 무게는 목판과 커팅 러버의 무게를 이용한 예상치이며
# 제조사에서 완성 라켓 무게를 보증한 값은 아닙니다.
# 가격은 조사 시점의 참고가이며 배송비·부착비가 별도일 수 있습니다.
# ---------------------------------------------------------

BUDGET_LOW = "저가 (10만 원 이하)"
BUDGET_HIGH = "고가 (10만 원 이상)"
WEIGHT_LIGHT = "가벼움 (180g 이하)"
WEIGHT_HEAVY = "무거움 (180g 초과)"

PRODUCTS = [
    # 공격적 / 저가 / 가벼움
    {
        "id": "attack_low_light",
        "name": "엑시옴 M 6.0 P 완제품",
        "style": "공격적",
        "price": 65000,
        "weight_g": 150,
        "weight_text": "약 150g (판매처 표기)",
        "weight_basis": "완제품 라켓의 판매처 표기 무게",
        "components": "엑시옴 M 6.0 P 완제품 라켓",
        "description": "공격형 펜홀더 완제품입니다. 가벼운 라켓을 선호하는 공격형 입문자가 참고할 수 있습니다.",
        "price_note": "참고 판매가 65,000원",
        "links": [
            ("제품 및 무게 정보", "https://www.ssg.com/item/itemView.ssg?itemId=1000458556110"),
            ("엑시옴 공식 스토어", "https://xiom.store/product/m-60-p-%EC%99%84%EC%A0%9C%ED%92%88-%EB%9D%BC%EC%BC%93/78/"),
        ],
    },
    # 공격적 / 저가 / 무거움
    {
        "id": "attack_low_heavy",
        "name": "엑시옴 오펜시브 S + DHS PF4 양면 조합",
        "style": "공격적",
        "price": 90747,
        "weight_g": 194,
        "weight_text": "약 194g (부품 기준 예상)",
        "weight_basis": "목판 86g + PF4 커팅 러버 약 54g × 2장으로 계산한 예상치",
        "components": "목판: 엑시옴 오펜시브 S (86g) / 앞면·뒷면 러버: DHS PF4 각 1장",
        "description": "공격용으로 분류되는 오펜시브 S 목판과 빠른 공격·드라이브에 활용되는 DHS PF4를 양면에 붙이는 조합입니다.",
        "price_note": "목판 63,147원 + PF4 13,800원 × 2장 기준",
        "links": [
            ("엑시옴 오펜시브 S 목판 가격·무게", "https://price.enuri.com/catalog/101558984"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
            ("PF4 시트 무게 참고", "https://tabletennis-reviews.com/reference/rubber-sheet-mass-size-database/"),
        ],
    },
    # 공격적 / 고가 / 가벼움
    {
        "id": "attack_high_light",
        "name": "닛타쿠 어쿠스틱 C + 버터플라이 로제나 조합",
        "style": "공격적",
        "price": 230000,
        "weight_g": 134,
        "weight_text": "약 134g (단면 펜홀더 예상)",
        "weight_basis": "어쿠스틱 C 펜홀더 목판 84g + 로제나 커팅 러버 약 50g 예상",
        "components": "목판: 닛타쿠 어쿠스틱 C 중국식 펜홀더 (84g) / 앞면 러버: 버터플라이 로제나 1장",
        "description": "고급 목판에 공격과 회전에 활용되는 로제나를 한 면에 부착하는 중국식 펜홀더 조합입니다. 한 면만 러버를 붙이는 구성이라 전체 무게를 낮추기 쉽습니다.",
        "price_note": "목판 약 198,000원 + 로제나 32,000원 기준",
        "links": [
            ("닛타쿠 어쿠스틱 C 목판 가격·무게", "https://www.nishohi.com/kr/nittaku-acoustic-c-table-tennis-blade"),
            ("버터플라이 로제나 러버 가격", "https://tabletennis24.co.kr/product/detail.html?cate_no=0&display_group=0&product_no=20"),
        ],
    },
    # 공격적 / 고가 / 무거움
    {
        "id": "attack_high_heavy",
        "name": "버터플라이 코르벨 + 로제나 양면 조합",
        "style": "공격적",
        "price": 124000,
        "weight_g": 190,
        "weight_text": "185~195g (판매처 표기)",
        "weight_basis": "판매처의 완성 라켓 중량 표기",
        "components": "목판: 버터플라이 코르벨 / 앞면·뒷면 러버: 버터플라이 로제나 2장",
        "description": "5겹 합판 코르벨에 로제나를 양면 부착한 공격형 조합입니다. 드라이브와 회전을 활용하는 플레이어가 고려할 수 있습니다.",
        "price_note": "조합 세트 판매가 124,000원",
        "links": [
            ("조합 가격·무게 정보", "https://m.thesportsshop.co.kr/product/detail.html?cate_no=723&display_group=1&product_no=4863"),
        ],
    },

    # 수비적 / 저가 / 가벼움
    {
        "id": "defense_low_light",
        "name": "버터플라이 다이오드 V + DHS C8 OX + DHS PF4 조합",
        "style": "수비적",
        "price": 91510,
        "weight_g": 170,
        "weight_text": "약 170g (부품 기준 예상)",
        "weight_basis": "다이오드 V 목판 96g + C8 OX 커팅분 약 20g + PF4 커팅분 약 54g 예상",
        "components": "목판: 버터플라이 다이오드 V (96g) / 한 면: DHS C8 OX 롱핌플 / 반대 면: DHS PF4",
        "description": "수비형 목판 다이오드 V에 가벼운 OX 롱핌플과 컨트롤용 평면 러버를 조합한 구성입니다.",
        "price_note": "다이오드 V 71,790원 + DHS C8 약 5,920원 + PF4 13,800원 기준",
        "links": [
            ("다이오드 V 목판 가격·무게", "https://price.enuri.com/catalog/33253762"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
        ],
    },
    # 수비적 / 저가 / 무거움
    {
        "id": "defense_low_heavy",
        "name": "버터플라이 다이오드 V + DHS C8 스펀지 + DHS PF4 조합",
        "style": "수비적",
        "price": 91510,
        "weight_g": 227,
        "weight_text": "약 227g (부품 기준 예상)",
        "weight_basis": "다이오드 V 목판 96g + 스펀지형 C8 커팅분 약 77g + PF4 커팅분 약 54g 예상",
        "components": "목판: 버터플라이 다이오드 V (96g) / 한 면: DHS C8 스펀지형 롱핌플 / 반대 면: DHS PF4",
        "description": "수비형 다이오드 V에 스펀지형 롱핌플을 붙여 커트 수비와 변화를 노리는 조합입니다. 러버 스펀지 두께에 따라 무게가 달라질 수 있습니다.",
        "price_note": "다이오드 V 71,790원 + DHS C8 약 5,920원 + PF4 13,800원 기준",
        "links": [
            ("다이오드 V 목판 가격·무게", "https://price.enuri.com/catalog/33253762"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
        ],
    },
    # 수비적 / 고가 / 가벼움
    {
        "id": "defense_high_light",
        "name": "빅타스 코지 마츠시타 + DHS C8 OX + DHS PF4 조합",
        "style": "수비적",
        "price": 153532,
        "weight_g": 161,
        "weight_text": "약 161g (부품 기준 예상)",
        "weight_basis": "코지 마츠시타 DEF 목판 87g + C8 OX 약 20g + PF4 커팅분 약 54g 예상",
        "components": "목판: 빅타스 코지 마츠시타 DEF (약 87g) / 한 면: DHS C8 OX 롱핌플 / 반대 면: DHS PF4",
        "description": "수비 전용 성향의 5겹 목판에 롱핌플과 평면 러버를 조합한 구성입니다. 가벼운 수비형 라켓을 원하는 경우의 참고 조합입니다.",
        "price_note": "코지 마츠시타 약 133,812원 + C8 5,920원 + PF4 13,800원 기준",
        "links": [
            ("코지 마츠시타 목판 가격·무게", "https://www.nishohi.com/kr/victas-koji-matsushita-table-tennis-blade"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
        ],
    },
    # 수비적 / 고가 / 무거움
    {
        "id": "defense_high_heavy",
        "name": "빅타스 코지 마츠시타 + DHS C8 스펀지 + DHS PF4 조합",
        "style": "수비적",
        "price": 162612,
        "weight_g": 218,
        "weight_text": "약 218g (부품 기준 예상)",
        "weight_basis": "코지 마츠시타 DEF 목판 87g + 스펀지형 C8 약 77g + PF4 커팅분 약 54g 예상",
        "components": "목판: 빅타스 코지 마츠시타 DEF (약 87g) / 한 면: DHS C8 스펀지형 롱핌플 / 반대 면: DHS PF4",
        "description": "수비 전용 목판과 스펀지형 롱핌플을 활용하는 수비 조합입니다. 커트와 변화구 중심의 플레이를 생각하는 사용자에게 적합한 방향입니다.",
        "price_note": "코지 마츠시타 약 133,812원 + C8 15,000원 + PF4 13,800원 기준",
        "links": [
            ("코지 마츠시타 목판 가격·무게", "https://www.nishohi.com/kr/victas-koji-matsushita-table-tennis-blade"),
            ("DHS C8 롱핌플 러버", "https://www.smashingsports.co.kr/shop/shopdetail.html?GfDT=bWt3UA%3D%3D&branduid=637522&current_category=027004007&mcode=004&scode=007&search=&sort=viewcnt&type=Y&xcode=027"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
        ],
    },

    # 핌플 / 저가 / 가벼움
    {
        "id": "pimple_low_light",
        "name": "버터플라이 다이오드 V + DHS C8 OX + 729 RITC799 조합",
        "style": "핌플",
        "price": 96940,
        "weight_g": 161,
        "weight_text": "약 161g (부품 기준 예상)",
        "weight_basis": "다이오드 V 목판 96g + C8 OX 약 20g + 729 RITC799 커팅분 약 45g 예상",
        "components": "목판: 버터플라이 다이오드 V (96g) / 한 면: DHS C8 OX 롱핌플 / 반대 면: 729 RITC799 숏핌플",
        "description": "롱핌플과 숏핌플을 각각 한 면씩 사용하는 핌플 조합입니다. 가벼운 라켓을 원하는 핌플 사용자용 참고 구성입니다.",
        "price_note": "다이오드 V 71,790원 + C8 5,920원 + 729 RITC799 19,230원 기준",
        "links": [
            ("다이오드 V 목판 가격·무게", "https://price.enuri.com/catalog/33253762"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("729 RITC799 숏핌플 가격", "https://www.auction.co.kr/n/search?keyword=729%20RITC799"),
        ],
    },
    # 핌플 / 저가 / 무거움
    {
        "id": "pimple_low_heavy",
        "name": "버터플라이 다이오드 V + DHS C8 스펀지 + 729 RITC799 조합",
        "style": "핌플",
        "price": 96940,
        "weight_g": 218,
        "weight_text": "약 218g (부품 기준 예상)",
        "weight_basis": "다이오드 V 목판 96g + 스펀지형 C8 약 77g + 729 RITC799 커팅분 약 45g 예상",
        "components": "목판: 버터플라이 다이오드 V (96g) / 한 면: DHS C8 스펀지형 롱핌플 / 반대 면: 729 RITC799 숏핌플",
        "description": "롱핌플과 숏핌플을 함께 사용하는 조합입니다. 스펀지형 롱핌플을 선택해 무게감 있는 핌플 라켓을 구성하는 예시입니다.",
        "price_note": "다이오드 V 71,790원 + C8 5,920원 + 729 RITC799 19,230원 기준",
        "links": [
            ("다이오드 V 목판 가격·무게", "https://price.enuri.com/catalog/33253762"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("729 RITC799 숏핌플 가격", "https://www.auction.co.kr/n/search?keyword=729%20RITC799"),
        ],
    },
    # 핌플 / 고가 / 가벼움
    {
        "id": "pimple_high_light",
        "name": "빅타스 코지 마츠시타 + DHS C8 OX + 닛타쿠 모리스토 SP 조합",
        "style": "핌플",
        "price": 192232,
        "weight_g": 157,
        "weight_text": "약 157g (부품 기준 예상)",
        "weight_basis": "코지 마츠시타 목판 87g + C8 OX 약 20g + 모리스토 SP 커팅분 약 50g 예상",
        "components": "목판: 빅타스 코지 마츠시타 (약 87g) / 한 면: DHS C8 OX 롱핌플 / 반대 면: 닛타쿠 모리스토 SP 숏핌플",
        "description": "수비형 목판에 롱핌플과 숏핌플을 조합한 고급 핌플 세팅입니다. 숏핌플과 롱핌플의 서로 다른 구질을 활용할 수 있습니다.",
        "price_note": "코지 마츠시타 약 133,812원 + C8 5,920원 + 모리스토 SP 52,500원 기준",
        "links": [
            ("코지 마츠시타 목판 가격·무게", "https://www.nishohi.com/kr/victas-koji-matsushita-table-tennis-blade"),
            ("DHS C8 롱핌플 러버 가격", "https://price.enuri.com/catalog/35817318"),
            ("닛타쿠 모리스토 SP 가격", "https://tabletennis24.co.kr/product/detail.html?cate_no=0&display_group=0&product_no=203"),
        ],
    },
    # 핌플 / 고가 / 무거움
    {
        "id": "pimple_high_heavy",
        "name": "닛타쿠 어쿠스틱 카본 + 모리스토 SP + DHS PF4 조합",
        "style": "핌플",
        "price": 284364,
        "weight_g": 193,
        "weight_text": "약 193g (부품 기준 예상)",
        "weight_basis": "어쿠스틱 카본 목판 88.7g + 모리스토 SP 커팅분 약 50g + PF4 커팅분 약 54g 예상",
        "components": "목판: 닛타쿠 어쿠스틱 카본 (약 88.7g) / 한 면: 닛타쿠 모리스토 SP 숏핌플 / 반대 면: DHS PF4",
        "description": "카본 목판에 숏핌플과 평면 러버를 조합한 고급 핌플 세팅입니다. 숏핌플을 활용한 빠른 공격과 반대 면의 회전 플레이를 함께 고려한 구성입니다.",
        "price_note": "어쿠스틱 카본 약 218,064원 + 모리스토 SP 52,500원 + PF4 13,800원 기준",
        "links": [
            ("닛타쿠 어쿠스틱 카본 목판 가격·무게", "https://www.nishohi.com/kr/nittaku-acoustic-carbon-table-tennis-blade"),
            ("닛타쿠 모리스토 SP 가격", "https://tabletennis24.co.kr/product/detail.html?cate_no=0&display_group=0&product_no=203"),
            ("DHS PF4 러버 가격", "https://www.ssg.com/item/itemView.ssg?itemId=1000044902499"),
        ],
    },
]

# 프로그램에 넣은 일반 탁구채 예시 사진입니다.
# 개별 추천 제품의 실제 상품 사진은 아닐 수 있습니다.
RACKET_IMAGE_URL = (
    "https://joola.fr/cdn/shop/files/"
    "54207_JOOLA_InfinityCarbon_04_web_b8ed6cb3-c55b-4f6f-9c9c-c49122362a32.jpg"
    "?v=1753177664&width=1200"
)


def classify_budget(price):
    """가격을 예산 구간으로 분류합니다. 10만 원은 두 구간 모두에 포함됩니다."""
    budget_groups = []
    if price <= 100000:
        budget_groups.append(BUDGET_LOW)
    if price >= 100000:
        budget_groups.append(BUDGET_HIGH)
    return budget_groups


def classify_weight(weight_g):
    """완성 라켓의 예상 무게를 가벼움 또는 무거움으로 분류합니다."""
    if weight_g <= 180:
        return WEIGHT_LIGHT
    else:
        return WEIGHT_HEAVY


def get_matching_rackets(style, budget, weight):
    """세 가지 선택 조건이 모두 일치하는 라켓만 반환합니다."""
    matches = []

    # 반복문으로 모든 제품을 하나씩 확인합니다.
    for racket in PRODUCTS:
        # 조건문으로 가격과 무게 구간을 제품 데이터에서 다시 계산합니다.
        product_budgets = classify_budget(racket["price"])
        product_weight = classify_weight(racket["weight_g"])

        # 플레이 스타일, 예산, 무게가 모두 일치해야 추천 목록에 넣습니다.
        if (
            racket["style"] == style
            and budget in product_budgets
            and product_weight == weight
        ):
            matches.append(racket)

    return matches


def show_selected_conditions(style, budget, weight):
    """선택한 조건을 리스트로 화면에 표시합니다."""
    conditions = [
        ("플레이 스타일", style),
        ("예산", budget),
        ("무게", weight),
    ]

    # 반복문으로 조건을 하나씩 출력합니다.
    for condition_name, condition_value in conditions:
        st.markdown(f"- **{condition_name}:** {condition_value}")


def show_product_links(links):
    """목판·러버 및 가격 정보를 확인할 수 있는 링크를 표시합니다."""
    st.markdown("**제품 정보 확인**")
    for link_name, link_url in links:
        st.markdown(f"- [{link_name}]({link_url})")


def show_recommendation(racket, style, budget, weight):
    """추천 문구, 선택 조건, 사진, 가격과 제품 구성을 순서대로 출력합니다."""
    st.success(f"당신의 맞춤형 탁구채는 **{racket['name']}**입니다")

    st.subheader("선택한 조건")
    show_selected_conditions(style, budget, weight)

    # 요청한 대로 가격보다 사진을 먼저 보여줍니다.
    st.image(
        RACKET_IMAGE_URL,
        caption="탁구채 예시 사진입니다. 추천 조합의 실제 사진과 다를 수 있습니다.",
        use_container_width=True,
    )

    st.subheader("가격")
    st.markdown(f"### {racket['price']:,}원")
    st.caption(racket["price_note"])

    st.subheader("목판과 러버 구성")
    st.write(racket["components"])
    st.write(racket["description"])

    st.subheader("무게")
    st.write(racket["weight_text"])
    st.caption("무게 산정: " + racket["weight_basis"])

    show_product_links(racket["links"])


# -------------------- 화면 --------------------
st.title("🏓 맞춤형 탁구채 추천!")
st.write("플레이 스타일, 예산, 무게를 버튼으로 선택한 뒤 **찾아보기**를 눌러 주세요.")

st.subheader("1. 플레이 스타일")
play_style = st.segmented_control(
    "플레이 스타일",
    options=["공격적", "수비적", "핌플"],
    default="공격적",
    label_visibility="collapsed",
    key="play_style",
)

st.subheader("2. 예산")
budget = st.segmented_control(
    "예산",
    options=[BUDGET_LOW, BUDGET_HIGH],
    default=BUDGET_LOW,
    label_visibility="collapsed",
    key="budget",
)

st.subheader("3. 무게")
weight = st.segmented_control(
    "무게",
    options=[WEIGHT_LIGHT, WEIGHT_HEAVY],
    default=WEIGHT_LIGHT,
    label_visibility="collapsed",
    key="weight",
)

st.caption(
    "분류 기준: 저가는 10만 원 이하, 고가는 10만 원 이상입니다. "
    "가벼움은 180g 이하, 무거움은 180g 초과입니다."
)
st.info(
    "조립형 라켓은 목판과 러버의 개체·스펀지 두께·커팅 크기에 따라 실제 무게가 달라집니다. "
    "예상 무게로 분류한 조합은 제품을 실제 조립한 뒤 무게를 확인해 주세요. 가격도 판매처와 시점에 따라 바뀔 수 있습니다."
)

if st.button("찾아보기", type="primary", use_container_width=True):
    if play_style is None or budget is None or weight is None:
        st.warning("플레이 스타일, 예산, 무게를 모두 선택해 주세요.")
    else:
        matching_rackets = get_matching_rackets(play_style, budget, weight)
        st.divider()
        st.subheader("추천 결과")

        if matching_rackets:
            # 선택 조건이 모두 일치하는 제품 중 하나를 선택합니다.
            selected_racket = random.choice(matching_rackets)
            show_recommendation(selected_racket, play_style, budget, weight)
        else:
            st.warning("선택한 세 가지 조건을 모두 만족하는 제품 조합을 찾지 못했습니다.")

# 데이터가 각 조건 조합에 모두 들어 있는지 코드에서 확인할 수 있도록 구성했습니다.
with st.expander("추천 데이터에 들어 있는 12가지 조건 조합 확인"):
    styles = ["공격적", "수비적", "핌플"]
    budgets = [BUDGET_LOW, BUDGET_HIGH]
    weights = [WEIGHT_LIGHT, WEIGHT_HEAVY]
    for style in styles:
        for budget_option in budgets:
            for weight_option in weights:
                found = get_matching_rackets(style, budget_option, weight_option)
                status = "등록 완료" if found else "조합 없음"
                st.write(f"- {style} / {budget_option} / {weight_option}: {status}")

st.divider()
st.caption(
    "제품은 실제 판매되는 목판·러버 또는 완제품 모델을 사용했습니다. "
    "단, 조립형 조합은 동일 조합의 완제품 판매가가 아니라 구성품 가격의 합계이며, "
    "무게는 공개된 목판·러버 사양을 참고한 예상치입니다."
)
