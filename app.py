import streamlit as st

st.set_page_config(
    page_title="Futures → IC Markets Hedge Calculator",
    page_icon="📊",
    layout="centered"
)

MARKETS = {
    "NQ → IC Markets USTEC": {
        "future": "NQ",
        "hedge": "USTEC",
        "future_value_per_point": 20.0,
        "cfd_value_per_point_per_lot": 1.0,
        "lot_step": 0.1,
    },
    "ES → IC Markets US500": {
        "future": "ES",
        "hedge": "US500",
        "future_value_per_point": 50.0,
        "cfd_value_per_point_per_lot": 1.0,
        "lot_step": 0.1,
    },
    "GC → IC Markets XAUUSD": {
        "future": "GC",
        "hedge": "XAUUSD",
        "future_value_per_point": 100.0,
        "cfd_value_per_point_per_lot": 100.0,
        "lot_step": 0.01,
    },
}

def round_to_step(value, step):
    return round(value / step) * step

def decimals_for_step(step):
    s = f"{step:.10f}".rstrip("0")
    return len(s.split(".")[1]) if "." in s else 0

st.title("Futures → IC Markets Hedge Calculator")
st.caption(
    "Choose NQ/USTEC, ES/US500, or GC/XAUUSD, then enter only "
    "the futures contracts, futures risk, and hedge risk."
)

market = st.selectbox("Market", list(MARKETS.keys()))
cfg = MARKETS[market]

with st.form("calculator"):
    contracts = st.number_input(
        f"{cfg['future']} contracts",
        min_value=0.01,
        value=1.0,
        step=0.25,
        format="%.2f",
    )

    futures_risk = st.number_input(
        "Futures risk ($)",
        min_value=0.01,
        value=2000.0,
        step=100.0,
        format="%.2f",
    )

    hedge_risk = st.number_input(
        f"{cfg['hedge']} hedge risk ($)",
        min_value=0.01,
        value=700.0,
        step=100.0,
        format="%.2f",
    )

    submitted = st.form_submit_button("Calculate lot size", use_container_width=True)

if submitted:
    futures_dollars_per_point = contracts * cfg["future_value_per_point"]
    stop_distance_points = futures_risk / futures_dollars_per_point

    raw_lots = hedge_risk / (
        stop_distance_points * cfg["cfd_value_per_point_per_lot"]
    )

    rounded_lots = round_to_step(raw_lots, cfg["lot_step"])
    actual_hedge_risk = (
        rounded_lots
        * stop_distance_points
        * cfg["cfd_value_per_point_per_lot"]
    )

    lot_decimals = decimals_for_step(cfg["lot_step"])

    st.divider()
    st.metric(
        f"{cfg['hedge']} LOT SIZE",
        f"{rounded_lots:.{lot_decimals}f} lots"
    )

    c1, c2 = st.columns(2)
    with c1:
        stop_label = "$ gold move" if cfg["future"] == "GC" else "pts"
        st.metric(
            f"{cfg['future']} stop distance",
            f"{stop_distance_points:,.2f} {stop_label}"
        )
    with c2:
        st.metric(
            "Raw calculated size",
            f"{raw_lots:,.4f} lots"
        )

    if cfg["future"] == "GC":
        st.caption(
            f"At {rounded_lots:.{lot_decimals}f} XAUUSD lots, a "
            f"${stop_distance_points:,.2f} gold move is approximately "
            f"${actual_hedge_risk:,.2f}."
        )
        st.info(
            "GC = $100 P/L for each $1.00 move per contract. "
            "1.00 XAUUSD lot = 100 oz, so it also changes by about "
            "$100 for each $1.00 move in gold."
        )
    else:
        st.caption(
            f"At {rounded_lots:.{lot_decimals}f} {cfg['hedge']} lots, a "
            f"{stop_distance_points:,.2f}-point move is approximately "
            f"${actual_hedge_risk:,.2f}."
        )

st.divider()
st.caption(
    "Check your IC Markets MT5 symbol specification before live trading, "
    "as contract size and volume step can vary by entity/account."
)
