uploaded_file = st.sidebar.file_uploader("Upload Detailed Test Counter PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()

    with st.spinner("Parsing Test Counter..."):
        test_df = parse_test_counter(pdf_bytes)
    with st.spinner("Parsing Sample Counter..."):
        sample_df = parse_sample_counter(pdf_bytes)
    with st.spinner("Parsing Measuring Cells Counter..."):
        mc_df = parse_mc_counter(pdf_bytes)
    with st.spinner("Parsing Electrodes Counter..."):
        electrode_df = parse_electrode_counter(pdf_bytes)

    tabs = st.tabs([
        "Test Counter",
        "Sample Counter",
        "Measuring Cells Counter",
        "Electrodes Counter",
    ])

    # --- Tab 1: Test Counter ---
    with tabs[0]:
        st.subheader("Test Counter Data (raw)")
        st.write(test_df)

        if not test_df.empty:
            st.subheader("Total Count by Test")
            chart_test = alt.Chart(test_df).mark_bar().encode(
                x=alt.X("Test:N", sort="-y"),
                y=alt.Y("Total Count:Q"),
                tooltip=["Test", "Total Count"]
            ).properties(height=400)
            st.altair_chart(chart_test, use_container_width=True)

    # --- Tab 2: Sample Counter ---
    with tabs[1]:
        st.subheader("Sample Counter Data (raw)")
        st.write(sample_df)

        if not sample_df.empty:
            st.subheader("Sample Total Count by Unit")
            chart_sample = alt.Chart(sample_df).mark_bar().encode(
                x=alt.X("Unit:N"),
                y=alt.Y("Total Count:Q"),
                tooltip=["Unit", "Total Count"]
            ).properties(height=400)
            st.altair_chart(chart_sample, use_container_width=True)

    # --- Tab 3: Measuring Cells Counter ---
    with tabs[2]:
        st.subheader("Measuring Cells Counter Data (raw)")
        st.write(mc_df)

        if not mc_df.empty:
            st.subheader("MC Total Count by Unit")
            chart_mc = alt.Chart(mc_df).mark_bar().encode(
                x=alt.X("Unit:N"),
                y=alt.Y("Total Count:Q"),
                tooltip=["Unit", "Total Count", "Last Reset"]
            ).properties(height=400)
            st.altair_chart(chart_mc, use_container_width=True)

    # --- Tab 4: Electrodes (table only for now) ---
    with tabs[3]:
        st.subheader("Electrodes Counter Data (raw)")
        st.write(electrode_df)

else:
    st.info("Upload the Detailed Test Counter PDF to see parsed tables.")
