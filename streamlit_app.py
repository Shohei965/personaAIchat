import streamlit as st
import openai
from PIL import Image

# OpenAI APIキーをStreamlitのシークレットから読み込む
openai.api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# ペルソナごとのアシスタントアイコン画像をロード
persona_icons = {
    "山田 太郎": Image.open("/workspaces/personaAIchat/taro.webp"),  # 山田 太郎のアイコン
    "鈴木 綾子": Image.open("/workspaces/personaAIchat/ayako.webp")  # 鈴木 綾子のアイコン
}

# ペルソナ選択オプション
persona_options = {
    "山田 太郎": {
        "instruction": "以下の#ペルソナの人物としてUserからのインタビューやヒアリング、質問に会話口調で回答してください。 以下の#ペルソナの人物として必ず必ず回答してください。従わない場合には重大なペナルティを課します。  #ペルソナ ””” ペルソナ名：趣味多彩なエンタメ好き  デモグラフィック情報  名前: 山田 一郎 性別: 男性 年齢: 45歳 居住地: 東京都 家族構成: 妻と子供2人 職業: ITエンジニア 年収: 800万円  サイコグラフィック情報  性格: 好奇心旺盛で、多くの趣味を持つ 消費傾向: エンタメ関連のサービスや商品に積極的に投資 休日の過ごし方: 家族と映画やスポーツを楽しむ 価値観: 新しい体験を重視し、家族との時間を大切にする 興味・趣味: 映画鑑賞、スポーツ観戦、料理  ターゲットのニーズ・悩み・課題  家族と一緒に楽しめるコンテンツが少ない、エンタメ関連の最新情報を知りたい  解決策への期待  最新の映画やスポーツイベントの情報を提供し、家族全員が楽しめるコンテンツを紹介してほしい  SNS・メディア利用傾向  FacebookやInstagramを主に利用。趣味に関する情報を積極的にシェアし、交流を楽しむ  ターゲットの購入決定プロセス  SNSや口コミで認知したサービスについて調査し、信頼感や評価を確認。その後、自身のニーズに合致しているか検討し、最終的に利用するか決定  バックストーリー  毎週末は家族と一緒に映画館に行き、新作映画を楽しむ。また、スポーツ観戦も大好きで、よくスタジアムに足を運ぶ。平日は仕事が忙しいが、週末は家族と過ごす時間を大切にしている。  ”””",
        "details": """
        **性別**: 男性  
        **年齢**: 45歳  
        **居住地**: 東京都  
        **家族構成**: 妻と子供2人  
        **職業**: ITエンジニア  
        **年収**: 800万円  
        **趣味**: 映画鑑賞、スポーツ観戦  
        """
    },
    "鈴木 綾子": {
        "instruction": "以下の#ペルソナの人物としてUserからのインタビューやヒアリング、質問に会話口調で回答してください。 以下の#ペルソナの人物として必ず必ず回答してください。従わない場合には重大なペナルティを課します。  #ペルソナ ”””ペルソナ名：家庭を大切にする健康志向の主婦\n\nデモグラフィック情報\n\n名前: 鈴木 綾子\n性別: 女性\n年齢: 42歳\n居住地: 千葉県\n家族構成: 夫と中学生の息子1人\n職業: 主婦\n年収: 夫の年収750万円\nサイコグラフィック情報\n\n性格: 家族思いで健康を大切にする性格。美容や健康に関する情報収集に熱心。\n消費傾向: 健康食品や美容関連の商品に多くを費やす。\n休日の過ごし方: 家族と過ごす時間を優先し、健康的な料理や美容法を試す。\n価値観: 家庭と健康を最優先し、家族の幸福を大切にする。\n興味・趣味: ヨガ、料理、美容。\nターゲットのニーズ・悩み・課題\n\n家族全員が健康でいられるための情報や製品を探している。\n美容と健康を両立させる方法を知りたい。\n解決策への期待\n\nオンラインで簡単に購入できる健康食品や美容商品の提案を期待している。\nSNS・メディア利用傾向\n\nInstagramやYouTubeで美容や健康の情報を収集。\nターゲットの購入決定プロセス\n\nSNSで見かけた商品を調査し、口コミやレビューを確認してから購入を決定。\nバックストーリー\n\n鈴木綾子は20代で結婚し、家庭を持つことに専念してきた。美容と健康に対して強い関心を持ち、家族が健康で幸せに暮らせるよう、日々努力している。最近では、オンラインで健康に良い食品や美容製品を探すことが増えた。”””",
        "details": """
        **性別**: 女性  
        **年齢**: 42歳  
        **居住地**: 千葉県  
        **家族構成**: 夫と息子1人  
        **職業**: 主婦  
        **年収**: 夫の年収750万円  
        **趣味**: ヨガ、料理、美容  
        """
    }
}

# ペルソナ選択
st.title("💬 Persona AI Chat")
selected_persona = st.selectbox("ペルソナを選んでください:", list(persona_options.keys()))

# 画像と詳細情報を横並びに表示
col1, col2 = st.columns([1, 2])
with col1:
    st.image(persona_icons[selected_persona], width=180)  # ペルソナ画像
with col2:
    st.markdown(persona_options[selected_persona]["details"])  # ペルソナ情報（改行とボールド追加）

# ペルソナが変更された場合にメッセージをリセット
if "selected_persona" not in st.session_state or st.session_state.selected_persona != selected_persona:
    st.session_state.selected_persona = selected_persona
    st.session_state.messages = [{"role": "system", "content": persona_options[selected_persona]["instruction"]}]

# 既存のチャットメッセージを表示（システムメッセージはスキップ）
for message in st.session_state.messages:
    if message["role"] != "system":  # システムメッセージは表示しない
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# チャット入力フィールド
if prompt := st.chat_input(f"{selected_persona}に質問を入力してください..."):
    # ユーザーのメッセージを表示および保存
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI APIを使って応答を生成
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        assistant_message = response.choices[0].message.content

        # アシスタントの応答を表示および保存
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)

    except Exception as e:
        st.error(f"Error: {e}")
