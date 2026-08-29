"""
HobZ - Main Interface
"""

import streamlit as st
from core.causal import CausalEngine
from core.memory import UnifiedMemory
from core.agents import AgentTeam


@st.cache_resource
def init_components():
    return {
        "causal": CausalEngine(),
        "memory": UnifiedMemory(),
        "team": AgentTeam()
    }


def main():
    st.set_page_config(page_title="HobZ - نظام المحاكاة التنبؤية", layout="wide")

    st.title("🐟 HobZ")
    st.markdown("### نظام المحاكاة التنبؤية المتقدم")
    st.markdown("---")

    components = init_components()
    causal = components["causal"]
    memory = components["memory"]
    team = components["team"]

    st.sidebar.title("⚙️ الإعدادات")
    mode = st.sidebar.radio("اختر الوضع", ["🔮 محاكاة جديدة", "📚 استرجاع من الذاكرة", "📊 الإحصائيات"])

    if mode == "🔮 محاكاة جديدة":
        st.header("🔮 تشغيل محاكاة جديدة")

        scenario = st.text_area("أدخل السيناريو:", placeholder="مثال: هل سيؤدي ارتفاع أسعار النفط إلى ركود اقتصادي؟")

        st.subheader("العوامل المؤثرة")
        factors = []
        num_factors = st.number_input("عدد العوامل", min_value=1, max_value=10, value=3)

        for i in range(int(num_factors)):
            st.markdown(f"**العامل {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("الاسم", key=f"name_{i}")
            with col2:
                strength = st.slider("القوة", 0.0, 1.0, 0.5, key=f"strength_{i}")

            description = st.text_input("الوصف", key=f"desc_{i}")
            mechanism = st.text_input("آلية التأثير", key=f"mech_{i}")

            if name:
                factors.append({
                    "name": name,
                    "description": description,
                    "strength": strength,
                    "mechanism": mechanism
                })

        if st.button("🚀 تشغيل المحاكاة", type="primary"):
            if not scenario:
                st.error("الرجاء إدخال السيناريو")
            elif not factors:
                st.error("الرجاء إضافة عامل واحد على الأقل")
            else:
                with st.spinner("جاري تشغيل المحاكاة..."):
                    for factor in factors:
                        causal.add_relation(
                            factor["name"],
                            "النتيجة الرئيسية",
                            factor["strength"],
                            factor["mechanism"]
                        )

                    context = {
                        "scenario": scenario,
                        "factors": factors
                    }
                    agent_results = team.run_consultation(scenario, context)

                    prediction, confidence = causal.predict(scenario, factors)

                    memory.store(
                        content=f"السيناريو: {scenario}\nالتنبؤ: {prediction}",
                        tags=[scenario.split()[0]] if scenario else ["عام"],
                        importance=confidence
                    )

                st.success("✅ اكتملت المحاكاة!")

                st.subheader("🔮 التنبؤ")
                st.info(prediction)
                st.metric("مستوى الثقة", f"{confidence:.0%}")

                st.subheader("🤖 آراء الوكلاء")
                for result in agent_results:
                    with st.expander(f"{result['agent']} ({result['role']})"):
                        st.write(result['response'])

                st.subheader("🔍 التفسير السببي")
                explanation = causal.explain("النتيجة الرئيسية")
                st.code(explanation)

    elif mode == "📚 استرجاع من الذاكرة":
        st.header("📚 استرجاع من الذاكرة العالمية")

        query = st.text_input("ابحث بالوسوم:", placeholder="مثال: اقتصاد، نفط")

        if st.button("🔍 بحث"):
            results = memory.recall([query] if query else [])
            if results:
                for item in results:
                    st.markdown(f"**{item.id}** (الأهمية: {item.importance:.0%})")
                    st.write(item.content)
                    st.markdown("---")
            else:
                st.warning("لا توجد نتائج")

    elif mode == "📊 الإحصائيات":
        st.header("📊 إحصائيات النظام")

        mem_stats = memory.get_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("عدد الذكريات", mem_stats["total_items"])
        with col2:
            st.metric("متوسط الأهمية", f"{mem_stats['avg_importance']:.2f}")


if __name__ == "__main__":
    main()
