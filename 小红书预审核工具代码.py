# 安装 Streamlit（如果没装的话先运行：pip install streamlit）
import re
import streamlit as st

# 敏感词库（根据小红书官方规则，持续可扩展）
sensitive_words = [
    "返佣", "变现渠道", "保本收益", "稳赚", "秒到账",
    "震惊", "必看", "薅羊毛", "外挂", "刷单", "引流",
    "赌博", "色情", "代孕", "虚拟货币", "炒币", "合约交易",
    "内部消息", "精准割韭菜", "爆仓", "一夜暴富"
]

# 敏感表达模式
sensitive_patterns = [
    r"(?i)零成本.*高回报",
    r"(?i)稳赚不赔",
    r"(?i)轻松赚钱",
    r"(?i)代写代发",
    r"(?i)限时.*福利",
    r"(?i)一单一结",
    r"(?i)返现.*奖励",
]

# 自动改写建议
rewrite_suggestions = {
    "震惊": "用‘意外’或‘出乎意料’替代",
    "必看": "用‘干货分享’替代",
    "稳赚": "用‘风险自担，合理预期收益’替代",
    "秒到账": "用‘到账速度快’替代",
    "返佣": "改为‘推广奖励’（注意避免金钱承诺）",
    "刷单": "避免出现，可用‘活动参与’描述"
}

# 审核函数
def audit_content(text):
    issues = []
    suggestions = []

    # 敏感词检查
    for word in sensitive_words:
        if word in text:
            issues.append(f"【敏感词】{word}")
            if word in rewrite_suggestions:
                suggestions.append(f"将【{word}】修改为：{rewrite_suggestions[word]}")

    # 敏感表达检查
    for pattern in sensitive_patterns:
        if re.search(pattern, text):
            issues.append("【敏感表达】存在引导式或夸大宣传用语")
            suggestions.append("请避免使用夸大收益、轻松赚钱等承诺词")

    # 诱导行为检查
    if any(x in text for x in ["评论领取", "转发抽奖", "关注送礼"]):
        issues.append("【诱导行为】诱导关注/评论/转发")
        suggestions.append("改为‘欢迎交流/欢迎参与讨论’等自然引导")

    # 评估风险等级
    if len(issues) == 0:
        risk_level = "🟢 低风险（建议发布）"
    elif len(issues) <= 2:
        risk_level = "🟡 中风险（需修改）"
    else:
        risk_level = "🔴 高风险（高危，容易被限流或封号）"

    return issues, suggestions, risk_level

# Streamlit界面
st.set_page_config(page_title="小红书内容预审核工具", page_icon="📋")

st.title("📋 小红书帖子内容预审核工具（高级版）")
st.markdown("根据小红书社区公约和风控规则，帮助你在发布前自检内容，减少违规风险。")

user_input = st.text_area("✍️ 请粘贴你的小红书帖子内容：", height=300)

if st.button("🔎 开始审核"):
    if user_input.strip() == "":
        st.warning("请先输入内容！")
    else:
        issues, suggestions, risk_level = audit_content(user_input)

        st.subheader("审核结果：")
        if issues:
            for issue in issues:
                st.error(issue)
        else:
            st.success("未发现明显问题！")

        st.subheader("修改建议：")
        if suggestions:
            for suggestion in suggestions:
                st.info(suggestion)
        else:
            st.info("内容符合规范，无需修改。")

        st.subheader("综合风险等级：")
        st.write(f"### {risk_level}")

st.markdown("---")
st.caption("工具规则参考：小红书社区公约 · 规范内容发布 · 保护账号安全 🚀")
