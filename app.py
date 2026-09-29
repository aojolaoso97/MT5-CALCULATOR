
import streamlit as st

st.set_page_config(
    page_title="NQ → IC Markets USTEC Hedge Calculator",
    page_icon="📊",
    layout="centered"
)

NQ_VALUE_PER_POINT = 20.0   # 1 NQ = $20 per index point
USTEC_VALUE_PER_POINT_PER_LOT = 1.0  # 1.00 USTEC lot ≈ $1 per index point

st.title("NQ → IC Markets USTEC Hedge Calculator")
st.caption("Only enter the 3 values below. The calculator gives you the USTEC lot size.")

with st.form("calculator"):
    nq_contracts = st.number_input(
        "NQ contracts",
        min_value=0.01,
        value=1.00,
        step=0.25,
        format="%.2f"
    )

    futures_risk = st.number_input(
        "Futures risk ($)",
        min_value=0.01,
        value=2000.00,
        step=100.00,
        format="%.2f"
    )

    hedge_risk = st.number_input(
        "USTEC hedge risk ($)",
        min_value=0.01,
        value=700.00,
        step=100.00,
        format="%.2f"
    )

    submitted = st.form_submit_button("Calculate lot size", use_container_width=True)

if submitted:
    nq_dollars_per_point = nq_contracts * NQ_VALUE_PER_POINT
    stop_distance_points = futures_risk / nq_dollars_per_point

    raw_lots = hedge_risk / (
        stop_distance_points * USTEC_VALUE_PER_POINT_PER_LOT
    )

    # IC Markets USTEC minimum/step commonly supports 0.1 lot increments.
    rounded_lots = round(raw_lots, 1)

    st.divider()

    st.metric("USTEC LOT SIZE", f"{rounded_lots:.1f} lots")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("NQ stop distance", f"{stop_distance_points:,.2f} pts")
    with c2:
        st.metric("Raw calculated size", f"{raw_lots:,.4f} lots")

    actual_hedge_risk = rounded_lots * stop_distance_points

    st.caption(
        f"At {rounded_lots:.1f} USTEC lots, a {stop_distance_points:,.2f}-point move "
        f"is approximately ${actual_hedge_risk:,.2f}."
    )

    st.info(
        "No live NQ/USTEC price is required for this calculation because both sides "
        "are being matched by index-point movement. 1 NQ = $20 per point, while this "
        "calculator uses $1 per point for each 1.00 USTEC lot."
    )
