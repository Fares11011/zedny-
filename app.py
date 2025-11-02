# app.py
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="التقييم القيادي المتقدم",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق CSS مخصص
def load_css():
    st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-right: 5px solid #4361ee;
    }
    .option {
        background: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e9ecef;
    }
    .option:hover {
        background: #e9ecef;
        border-color: #4361ee;
        transform: translateX(-5px);
    }
    .selected {
        background: linear-gradient(135deg, #4361ee, #3a0ca3) !important;
        color: white !important;
        border-color: #4361ee !important;
    }
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #4361ee, #3a0ca3);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

class LeadershipAssessment:
    def __init__(self):
        self.questions = self.load_questions()
        self.current_question = 0
        self.answers = {}
        self.scores = {
            'SL': 0, 'EI': 0, 'IN': 0, 
            'PM': 0, 'CO': 0, 'ET': 0
        }
        
    def load_questions(self):
        # بيانات الأسئلة مدمجة مباشرة
        return [
            {
                "id": 1,
                "text": "عند تطوير استراتيجيات طويلة المدى، كيف توازن بين الابتكار والاستقرار التشغيلي؟",
                "options": [
                    "إعطاء الأولوية للابتكار للميزة التنافسية",
                    "الحفاظ على الاستقرار مع إجراء تحسينات تدريجية",
                    "إنشاء فرق منفصلة للابتكار والعمليات",
                    "دمج الابتكار ضمن الأطر التشغيلية المستقرة"
                ],
                "dimensions": {"SL": 0.40, "IN": 0.30, "PM": 0.20, "CO": 0.10}
            },
            {
                "id": 2, 
                "text": "كم توافق على العبارة: 'أحلل اتجاهات الصناعة بانتظام لتوقع التحديات المستقبلية'؟",
                "options": ["غير موافق بشدة", "غير موافق", "محايد", "موافق", "موافق بشدة"],
                "dimensions": {"SL": 0.45, "IN": 0.25, "PM": 0.20, "EI": 0.10}
            }
            # يمكن إضافة المزيد من الأسئلة هنا
        ]
    
    def display_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            
            st.markdown(f"""
            <div class="question-card">
                <h3>السؤال {question['id']}</h3>
                <p>{question['text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # عرض الخيارات
            cols = st.columns(2)
            for i, option in enumerate(question['options']):
                with cols[i % 2]:
                    if st.button(
                        option, 
                        key=f"q{self.current_question}_opt{i}",
                        use_container_width=True,
                        type="secondary" if str(self.answers.get(self.current_question)) != str(i) else "primary"
                    ):
                        self.answers[self.current_question] = i
                        self.calculate_score(question, i)
                        
            # شريط التقدم
            progress = (self.current_question + 1) / len(self.questions)
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress * 100}%"></div>
            </div>
            <p style="text-align: center;">التقدم: {self.current_question + 1} / {len(self.questions)}</p>
            """, unsafe_allow_html=True)
            
            # أزرار التنقل
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("السابق", disabled=self.current_question == 0):
                    self.current_question -= 1
                    st.rerun()
            with col3:
                if st.button("التالي", type="primary"):
                    if self.current_question < len(self.questions) - 1:
                        self.current_question += 1
                        st.rerun()
                    else:
                        self.show_results()
        else:
            self.show_results()
    
    def calculate_score(self, question, answer_index):
        for dimension, weight in question['dimensions'].items():
            self.scores[dimension] += answer_index * weight
    
    def show_results(self):
        st.balloons()
        st.success("🎉 تهانينا! لقد أكملت التقييم")
        
        # عرض النتائج
        st.subheader("📊 نتائج تقييمك القيادي")
        
        dimension_names = {
            'SL': 'القيادة الاستراتيجية',
            'EI': 'الذكاء العاطفي', 
            'IN': 'الابتكار',
            'PM': 'إدارة الأداء',
            'CO': 'التواصل',
            'ET': 'الأخلاقيات'
        }
        
        # إنشاء مخطط النتائج
        dimensions = list(dimension_names.values())
        scores = [self.scores[dim] * 20 for dim in dimension_names.keys()]  # تحويل إلى نسبة مئوية
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=dimensions,
            fill='toself',
            name='القدرات القيادية'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="الملف القيادي الشخصي"
        )
        
        st.plotly_chart(fig)
        
        # عرض النتائج التفصيلية
        st.subheader("📈 التحليل التفصيلي")
        
        for dim_code, dim_name in dimension_names.items():
            score = self.scores[dim_code] * 20
            st.write(f"**{dim_name}**: {score:.1f}%")
            st.progress(score / 100)
            
        # التوصيات
        st.subheader("💡 توصيات التطوير")
        self.show_recommendations()
    
    def show_recommendations(self):
        recommendations = {
            'SL': "• حضور ورش عمل في التخطيط الاستراتيجي\n• قراءة كتب عن القيادة الاستراتيجية",
            'EI': "• ممارسة التأمل والوعي الذاتي\n• تدريب على الاستماع النشط",
            'IN': "• المشاركة في جلسات العصف الذهني\n• دراسة حالات نجاح الابتكار",
            'PM': "• تعلم منهجيات إدارة المشاريع\n• تطوير مهارات المتابعة والتقييم",
            'CO': "• دورات في التواصل الفعال\n• التدرب على العروض التقديمية", 
            'ET': "• دراسة الأخلاقيات المهنية\n• تحليل حالات دراسية أخلاقية"
        }
        
        for dim, rec in recommendations.items():
            with st.expander(f"توصيات {list(self.get_dimension_names().values())[list(self.get_dimension_names().keys()).index(dim)]}"):
                st.write(rec)
    
    def get_dimension_names(self):
        return {
            'SL': 'القيادة الاستراتيجية',
            'EI': 'الذكاء العاطفي',
            'IN': 'الابتكار', 
            'PM': 'إدارة الأداء',
            'CO': 'التواصل',
            'ET': 'الأخلاقيات'
        }

def main():
    load_css()
    
    st.title("🎯 التقييم القيادي المتقدم")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4361ee, #3a0ca3); padding: 2rem; border-radius: 15px; color: white;'>
        <h2 style='color: white; margin: 0;'>اكتشف إمكاناتك القيادية</h2>
        <p style='color: white; margin: 0;'>اختبار شامل يقيس 6 أبعاد قيادية رئيسية</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تهيئة حالة الجلسة
    if 'assessment' not in st.session_state:
        st.session_state.assessment = LeadershipAssessment()
    
    assessment = st.session_state.assessment
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("الإعدادات")
        if st.button("بدء اختبار جديد"):
            st.session_state.assessment = LeadershipAssessment()
            st.rerun()
        
        st.markdown("---")
        st.subheader("معلومات التقييم")
        st.write("""
        - 6 أبعاد قيادية
        - تقييم شامل
        - نتائج فورية
        - توصيات مخصصة
        """)
    
    # عرض السؤال الحالي
    assessment.display_question()

if __name__ == "__main__":
    main()
