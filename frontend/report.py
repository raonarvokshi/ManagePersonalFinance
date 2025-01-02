import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

BASE_URL = "http://127.0.0.1:8000"


def view_report():
    st.subheader("Financial Report")

    with st.sidebar:
        st.header("Filters")
        filters = ["Date", "Category"]
        select_filters = st.multiselect(
            "Select Filters you want to use", options=filters)

        if "Date" in select_filters:
            start_date = st.date_input("Start Date*")
            end_date = st.date_input("End Date*")

        if "Category" in select_filters:
            category_filter = st.text_input(
                "Category (optional)", placeholder="Category (optional)", max_chars=50)

        apply_filters = st.button("Apply Filters") if select_filters else None
        # Butoni për shkarkim PDF
        download_pdf = st.button("Download PDF Report")

    expenses_response = requests.get(
        f"{BASE_URL}/expenses/", params={"user_id": st.session_state.user_id})
    incomes_response = requests.get(
        f"{BASE_URL}/incomes/", params={"user_id": st.session_state.user_id})

    if expenses_response.status_code == 200 and incomes_response.status_code == 200:
        expenses = expenses_response.json()
        incomes = incomes_response.json()

        expenses_df = pd.DataFrame(expenses)
        incomes_df = pd.DataFrame(incomes)

        if apply_filters:
            expenses_df["date"] = pd.to_datetime(
                expenses_df["date"], format="mixed", errors="coerce")
            incomes_df["date"] = pd.to_datetime(
                incomes_df["date"], format="mixed", errors="coerce")

            if "Date" in select_filters:
                if not expenses_df.empty:
                    expenses_df = expenses_df[
                        (expenses_df["date"] >= pd.to_datetime(start_date)) &
                        (expenses_df["date"] <= pd.to_datetime(end_date))
                    ]
                if not incomes_df.empty:
                    incomes_df = incomes_df[
                        (incomes_df["date"] >= pd.to_datetime(start_date)) &
                        (incomes_df["date"] <= pd.to_datetime(end_date))
                    ]

            if "Category" in select_filters and category_filter:
                if not expenses_df.empty:
                    expenses_df = expenses_df[
                        expenses_df["category"].str.contains(
                            category_filter, case=False, na=False)
                    ]

        total_expenses = expenses_df["amount"].sum(
        ) if not expenses_df.empty else 0
        total_incomes = incomes_df["amount"].sum(
        ) if not incomes_df.empty else 0
        balance = total_incomes - total_expenses

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incomes:", value=f"${total_incomes:.2f}")
        with col2:
            st.metric("Total Expenses:", value=f"${total_expenses:.2f}")
        with col3:
            st.metric("Balance:", value=f"${balance:.2f}")

        st.markdown("---")

        if not expenses_df.empty or not incomes_df.empty:
            st.header("Incomes and Expenses Charts 📊")

            charts = {}
            temp_files = []
            if not expenses_df.empty and "category" in expenses_df:
                st.write("### Expenses by Category")
                category_chart = expenses_df.groupby("category")[
                    "amount"].sum()
                st.bar_chart(category_chart)

                plt.figure()
                category_chart.plot(kind="bar")
                plt.title("Expenses by Category")
                plt.ylabel("Amount")
                temp_file = "category_chart.png"
                plt.savefig(temp_file)
                charts["category_chart"] = temp_file
                temp_files.append(temp_file)

            if not expenses_df.empty and "date" in expenses_df:
                st.write("### Expenses Over Time")
                expense_chart_df = pd.DataFrame(expenses)
                expense_chart_df["date"] = pd.to_datetime(
                    expense_chart_df["date"], format="mixed")

                time_chart = expense_chart_df.groupby("date")["amount"].sum()
                st.line_chart(time_chart)

                plt.figure()
                time_chart.plot()
                plt.title("Expenses Over Time")
                plt.ylabel("Amount")
                temp_file = "expense_time_chart.png"
                plt.savefig(temp_file)
                charts["expense_time_chart"] = temp_file
                temp_files.append(temp_file)

            if not incomes_df.empty and "date" in incomes_df:
                st.write("### Incomes Over Time")
                incomes_df["date"] = pd.to_datetime(
                    incomes_df["date"], format="mixed")
                income_chart = incomes_df.groupby("date")["amount"].sum()
                st.line_chart(income_chart)

                plt.figure()
                income_chart.plot()
                plt.title("Incomes Over Time")
                plt.ylabel("Amount")
                temp_file = "income_time_chart.png"
                plt.savefig(temp_file)
                charts["income_time_chart"] = temp_file
                temp_files.append(temp_file)

            if download_pdf:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                pdf.cell(200, 10, txt="Financial Report", ln=True, align="C")
                pdf.ln(10)

                pdf.cell(200, 10, txt=f"Total Incomes: ${
                    total_incomes:.2f}", ln=True)
                pdf.cell(200, 10, txt=f"Total Expenses: ${
                    total_expenses:.2f}", ln=True)
                pdf.cell(200, 10, txt=f"Balance: ${balance:.2f}", ln=True)
                pdf.ln(10)

                for title, chart_path in charts.items():
                    pdf.add_page()
                    pdf.cell(200, 10, txt=title.replace(
                        "_", " ").title(), ln=True)
                    pdf.ln(10)
                    pdf.image(chart_path, x=10, y=30, w=190)

                pdf_output = BytesIO()
                pdf_output.write(pdf.output(dest="S").encode(
                    "latin1"))  # Kalon përmbajtjen si bytes
                pdf_output.seek(0)

                st.download_button(
                    label="Download PDF",
                    data=pdf_output,
                    file_name="financial_report.pdf",
                    mime="application/pdf"
                )

                # Fshij skedarët e përkohshëm pas përdorimit
                for temp_file in temp_files:
                    os.remove(temp_file)

        else:
            st.warning("No data available to generate the charts!")
            st.info("Please add new incomes or expenses.")

    else:
        if expenses_response.status_code != 200:
            st.error(f"Failed to retrieve expenses data! {
                     expenses_response.text}")
        if incomes_response.status_code != 200:
            st.error(f"Failed to retrieve incomes data! {
                     incomes_response.text}")
