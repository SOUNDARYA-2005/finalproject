import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Log Monitoring Dashboard", layout="wide")

st.title("🚀 Real-Time Log Monitoring Dashboard")

refresh_interval = 5000
st.caption("Auto-refresh every 5 seconds")

# Auto refresh
st_autorefresh(interval=refresh_interval, key="datarefresh")

# -------------------------------------------------
# TOP NAVIGATION TABS
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🚨 Anomalies", "📄 Logs"])

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
try:

    df = pd.read_csv("processed_logs/output.csv")

    # -------------------------------------------------
    # COLUMN VALIDATION
    # -------------------------------------------------
    required_columns = ["level", "service", "message", "anomaly"]

    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            st.stop()

    # -------------------------------------------------
    # SIDEBAR FILTERS
    # -------------------------------------------------
    st.sidebar.header("🔍 Filters")

    level_filter = st.sidebar.multiselect(
        "Select Log Level",
        options=df["level"].unique(),
        default=df["level"].unique()
    )

    service_filter = st.sidebar.multiselect(
        "Select Service",
        options=df["service"].unique(),
        default=df["service"].unique()
    )

    search = st.sidebar.text_input("🔎 Search logs")

    filtered_df = df[
        (df["level"].isin(level_filter)) &
        (df["service"].isin(service_filter))
    ]

    if search:
        filtered_df = filtered_df[
            filtered_df["message"].str.contains(search, case=False, na=False)
        ]

    anomalies = filtered_df[filtered_df["anomaly"] == 1]

    # =================================================
    # DASHBOARD TAB
    # =================================================
    with tab1:

        st.subheader("📊 System Health Overview")

        col1, col2, col3, col4 = st.columns(4)

        total_logs = len(filtered_df)
        error_logs = len(filtered_df[filtered_df["level"] == "ERROR"])
        anomaly_count = int(filtered_df["anomaly"].sum())

        col1.metric("Total Logs", total_logs)
        col2.metric("Errors", error_logs)
        col3.metric("Anomalies", anomaly_count)

        if anomaly_count > 5:
            status = "CRITICAL ⚠️"
        elif anomaly_count > 0:
            status = "WARNING ⚠️"
        else:
            status = "HEALTHY ✅"

        col4.metric("System Status", status)

        # ALERT SECTION
        if anomaly_count > 0:
            st.error(f"🚨 {anomaly_count} anomalies detected!")
            st.toast("🚨 Anomaly detected in logs!")
        else:
            st.success("✅ System running normally")

        st.divider()

        # -------------------------------------------------
        # CHARTS
        # -------------------------------------------------
        colA, colB = st.columns(2)

        # LOG LEVEL CHART
        with colA:

            st.subheader("📊 Log Level Distribution")

            if not filtered_df.empty:

                level_counts = filtered_df["level"].value_counts()

                fig = px.bar(
                    x=level_counts.index,
                    y=level_counts.values,
                    labels={"x": "Log Level", "y": "Count"},
                    title="Log Level Distribution"
                )

                st.plotly_chart(fig, use_container_width=True)

                # PIE CHART
                fig_pie = px.pie(
                    values=level_counts.values,
                    names=level_counts.index,
                    title="Log Level Breakdown"
                )

                st.plotly_chart(fig_pie, use_container_width=True)

            else:
                st.info("No data available")

        # SERVICE CHART
        with colB:

            st.subheader("🧩 Service Distribution")

            if not filtered_df.empty:

                service_counts = filtered_df["service"].value_counts()

                fig2 = px.bar(
                    x=service_counts.index,
                    y=service_counts.values,
                    labels={"x": "Service", "y": "Count"},
                    title="Service Distribution"
                )

                st.plotly_chart(fig2, use_container_width=True)

            else:
                st.info("No data available")

        st.divider()

        # -------------------------------------------------
        # LOG ACTIVITY OVER TIME
        # -------------------------------------------------
        st.subheader("📈 Logs Over Time")

        if not filtered_df.empty and "@timestamp" in filtered_df.columns:

            df_time = filtered_df.copy()
            df_time["@timestamp"] = pd.to_datetime(df_time["@timestamp"])
            df_time = df_time.sort_values("@timestamp")

            fig3 = px.line(
                df_time,
                x="@timestamp",
                title="Log Activity Over Time"
            )

            st.plotly_chart(fig3, use_container_width=True)

        # -------------------------------------------------
        # ANOMALY TREND
        # -------------------------------------------------
        st.subheader("🚨 Anomaly Trend")

        if not anomalies.empty and "@timestamp" in anomalies.columns:

            anomaly_time = anomalies.copy()
            anomaly_time["@timestamp"] = pd.to_datetime(anomaly_time["@timestamp"])
            anomaly_time = anomaly_time.sort_values("@timestamp")

            fig_anomaly = px.line(
                anomaly_time,
                x="@timestamp",
                title="Anomalies Over Time"
            )

            st.plotly_chart(fig_anomaly, use_container_width=True)

        else:
            st.info("No anomaly trend data available")

        st.divider()

        # -------------------------------------------------
        # TOP ERROR MESSAGES
        # -------------------------------------------------
        st.subheader("⚠️ Top Error Messages")

        error_df = filtered_df[filtered_df["level"] == "ERROR"]

        if not error_df.empty:

            top_errors = error_df["message"].value_counts().head(5)

            fig_errors = px.bar(
                x=top_errors.values,
                y=top_errors.index,
                orientation="h",
                labels={"x": "Count", "y": "Error Message"},
                title="Most Frequent Errors"
            )

            st.plotly_chart(fig_errors, use_container_width=True)

        else:
            st.info("No error messages detected")

        # -------------------------------------------------
        # SERVICE SUMMARY
        # -------------------------------------------------
        st.subheader("📊 Log Count Per Service")

        service_summary = filtered_df.groupby("service").size().reset_index(name="log_count")

        st.dataframe(service_summary, use_container_width=True)

        # -------------------------------------------------
        # LATEST ANOMALY
        # -------------------------------------------------
        if not anomalies.empty:

            st.subheader("⚠️ Latest Anomaly")

            latest_anomaly = anomalies.tail(1)

            st.dataframe(latest_anomaly, use_container_width=True)

    # =================================================
    # ANOMALIES TAB
    # =================================================
    with tab2:

        st.subheader("🚨 Detected Anomalies")

        if not anomalies.empty:

            st.dataframe(anomalies, use_container_width=True)

            st.download_button(
                "⬇ Download Anomalies CSV",
                anomalies.to_csv(index=False),
                file_name="anomalies.csv"
            )

        else:
            st.success("No anomalies detected")

    # =================================================
    # LOGS TAB
    # =================================================
    with tab3:

        st.subheader("📄 Log Explorer")

        if filtered_df.empty:
            st.warning("No logs found for selected filters")
        else:
            st.dataframe(filtered_df, use_container_width=True)

        st.download_button(
            "⬇ Download Logs CSV",
            filtered_df.to_csv(index=False),
            file_name="logs.csv"
        )

# -------------------------------------------------
# ERROR HANDLING
# -------------------------------------------------
except Exception as e:

    st.warning("Waiting for pipeline data...")
    st.text(e)