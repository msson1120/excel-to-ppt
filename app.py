import os
import streamlit as st
import base64

APP_TITLE = "(주)건화 관리카드 자동작성 프로그램"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

MANUAL_PDF = os.path.join(ASSETS_DIR, "manual.pdf")
MACRO_PACK = os.path.join(ASSETS_DIR, "ppt_macro_pack.zip")   # 필요시 파일명 변경
EXCEL_TEMPLATE = os.path.join(ASSETS_DIR, "merge_template.xlsx")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📄",
    layout="centered"
)

st.title(APP_TITLE)
st.caption("부서 내부 배포용 · PPT 템플릿 기반 자동작성 도구")

# ----------------------------
# 유틸: 다운로드 버튼
# ----------------------------
def download_button(label: str, file_path: str, mime: str):
    if not os.path.exists(file_path):
        st.error(f"파일이 없습니다: {os.path.basename(file_path)}")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    st.download_button(
        label=label,
        data=data,
        file_name=os.path.basename(file_path),
        mime=mime,
        use_container_width=True
    )

# ----------------------------
# PDF 매뉴얼 토글
# ----------------------------
with st.expander("PDF 매뉴얼 보기", expanded=False):
    if os.path.exists(MANUAL_PDF):
        with open(MANUAL_PDF, "rb") as f:
            pdf_bytes = f.read()

        # 브라우저 내 PDF 뷰어(간단/안정)
        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_viewer = f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="750"
            style="border:none;">
        </iframe>
        """
        st.components.v1.html(pdf_viewer, height=780, scrolling=True)
    else:
        st.warning("manual.pdf가 assets 폴더에 없습니다.")

st.divider()

# ----------------------------
# 서비스 이용 안내
# ----------------------------
st.subheader("서비스 이용 안내")
st.markdown(
    """
1. 아래에서 **PPT 매크로 패키지**와 **결합용 엑셀 양식**을 다운로드합니다.  
2. PPT 매크로 패키지의 안내대로 설치/실행합니다. (PPT에서 버튼 눌러 실행)  
3. 엑셀 양식에 데이터를 입력하고, 이미지 폴더/파일 규칙을 맞춘 뒤 병합 실행합니다.  

주의:
- 설치/실행 중 PowerPoint는 모두 종료한 상태에서 진행하세요.
- 결과 품질은 템플릿 버전/폰트 설치 여부에 영향을 받습니다.
"""
)

st.divider()

# ----------------------------
# 다운로드 섹션
# ----------------------------
st.subheader("다운로드")
col1, col2 = st.columns(2)

with col1:
    st.markdown("PPT 매크로")
    download_button(
        label="PPT 매크로 다운로드",
        file_path=MACRO_PACK,
        mime="application/zip"
    )

with col2:
    st.markdown("결합용 엑셀 양식")
    download_button(
        label="엑셀 양식 다운로드",
        file_path=EXCEL_TEMPLATE,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("배포 파일 교체는 assets 폴더의 파일만 바꾸면 됩니다.")
