import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.data_fetcher import DataFetcher
from utils.portfolio_manager import PortfolioManager
from utils.turkish_locale import TurkishLocale
from utils.auth import AuthManager
from utils.database import DatabaseManager

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Altair Finance",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize utilities
locale = TurkishLocale()
data_fetcher = DataFetcher()
portfolio_manager = PortfolioManager()
auth_manager = AuthManager()
db_manager = DatabaseManager()

def main():
    # Check authentication
    if not auth_manager.is_authenticated():
        auth_manager.show_login_page()
        return
    
    # Load user portfolio from database
    user_id = auth_manager.get_user_id()
    if user_id:
        portfolio_df = db_manager.get_user_portfolio(user_id)
        if not portfolio_df.empty:
            # Convert DataFrame to session state format
            st.session_state.portfolio = {}
            for _, row in portfolio_df.iterrows():
                st.session_state.portfolio[row['symbol']] = {
                    'quantity': row['quantity'],
                    'avg_cost': row['avg_cost'],
                    'target_quantity': row['target_quantity'],
                    'date_added': row['date_added']
                }
    
    st.title("🏦 Altair Finance")
    st.markdown("---")
    
    # Sidebar with user menu and settings
    with st.sidebar:
        auth_manager.show_user_menu()
        
        st.header("⚙️ Ayarlar")
        
        # Load user preferences
        user_prefs = db_manager.get_user_preferences(user_id)
        
        theme_toggle = st.toggle("🌙 Karanlık Tema", value=(user_prefs.get('theme', 'light') == 'dark'))
        if theme_toggle != (user_prefs.get('theme', 'light') == 'dark'):
            new_theme = 'dark' if theme_toggle else 'light'
            db_manager.update_user_preferences(user_id, theme=new_theme)
            st.session_state.theme = new_theme
            st.rerun()
        
        st.markdown("---")
        st.info("📱 **Navigasyon**\n\nSol menüden farklı sayfalara geçiş yapabilirsiniz:\n- 📊 Portfolio: Portföy yönetimi\n- 📈 Analiz: Teknik analiz\n- 💰 Temettü: Temettü takibi")
    
    # Ana dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Piyasa Özeti")
        
        # BIST 100 overview
        try:
            bist_data = data_fetcher.get_stock_data("XU100.IS", period="1d")
            if not bist_data.empty:
                current_price = bist_data['Close'].iloc[-1]
                prev_close = bist_data['Open'].iloc[-1]
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(
                        "BIST 100",
                        f"{current_price:,.2f}",
                        f"{change:+.2f} ({change_pct:+.2f}%)"
                    )
            else:
                st.warning("BIST 100 verisi alınamadı")
        except Exception as e:
            st.error(f"BIST 100 verisi alınırken hata: {str(e)}")
        
        # S&P 500 overview
        try:
            sp500_data = data_fetcher.get_stock_data("^GSPC", period="1d")
            if not sp500_data.empty:
                current_price = sp500_data['Close'].iloc[-1]
                prev_close = sp500_data['Open'].iloc[-1]
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                with metric_col2:
                    st.metric(
                        "S&P 500",
                        f"{current_price:,.2f}",
                        f"{change:+.2f} ({change_pct:+.2f}%)"
                    )
            else:
                st.warning("S&P 500 verisi alınamadı")
        except Exception as e:
            st.error(f"S&P 500 verisi alınırken hata: {str(e)}")
    
    with col2:
        st.subheader("🔍 Hızlı Hisse Arama")
        
        # Stock search
        search_symbol = st.text_input("Hisse/ETF Sembolü", placeholder="Örn: THYAO.IS, SPY")
        
        if search_symbol:
            try:
                stock_data = data_fetcher.get_stock_data(search_symbol, period="5d")
                if not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    prev_price = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else stock_data['Close'].iloc[-1]
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                    
                    st.metric(
                        search_symbol.upper(),
                        f"{current_price:.2f}",
                        f"{change:+.2f} ({change_pct:+.2f}%)"
                    )
                    
                    # Mini chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=stock_data.index,
                        y=stock_data['Close'],
                        mode='lines',
                        name='Kapanış',
                        line=dict(color='#1f77b4')
                    ))
                    fig.update_layout(
                        height=300,
                        showlegend=False,
                        margin=dict(l=0, r=0, t=20, b=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Veri bulunamadı")
            except Exception as e:
                st.error(f"Hisse verisi alınırken hata: {str(e)}")
    
    # Portfolio summary
    st.markdown("---")
    st.subheader("💼 Portföy Özeti")
    
    if 'portfolio' in st.session_state and st.session_state.portfolio:
        portfolio_summary = portfolio_manager.get_portfolio_summary()
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Toplam Değer", f"₺{portfolio_summary['total_value']:,.2f}")
        
        with summary_col2:
            st.metric("Toplam Maliyet", f"₺{portfolio_summary['total_cost']:,.2f}")
        
        with summary_col3:
            profit_loss = portfolio_summary['total_value'] - portfolio_summary['total_cost']
            profit_loss_pct = (profit_loss / portfolio_summary['total_cost']) * 100 if portfolio_summary['total_cost'] > 0 else 0
            st.metric(
                "Kar/Zarar",
                f"₺{profit_loss:,.2f}",
                f"{profit_loss_pct:+.2f}%"
            )
        
        with summary_col4:
            st.metric("Hisse Sayısı", str(len(st.session_state.portfolio)))
    else:
        st.info("Henüz portföy eklenmemiş. Portföy sayfasından hisse ekleyebilirsiniz.")
    
    # Recent market news section (placeholder)
    st.markdown("---")
    st.subheader("📰 Piyasa Haberleri")
    st.info("Piyasa haberleri entegrasyonu için harici API gerekiyor. Bu özellik ileride eklenebilir.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>💡 Bu platform eğitim amaçlıdır. Yatırım kararlarınızı alırken profesyonel danışmanlık alınız.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
